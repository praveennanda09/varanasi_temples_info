# download_all_images.py
import os
import re
import json
import csv
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')
IMAGES_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website', 'assets', 'images')
DATA_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website', 'data')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://varanasitemples.in/',
}

# Collect all image URLs from cached HTML files
all_img_urls = set()
for fname in os.listdir(CACHE_DIR):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(CACHE_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    found = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
    for u in found:
        u = u.strip()
        if u and not u.startswith('data:'):
            all_img_urls.add(u)

print(f"Total raw image URLs collected: {len(all_img_urls)}")

# Function to clean and standardize URL to filename
def get_image_filename(url):
    parsed = urllib.parse.urlparse(url)
    basename = os.path.basename(parsed.path)
    if not basename:
        basename = "image_" + hashlib.md5(url.encode('utf-8')).hexdigest()[:8] + ".jpg"
    # Ensure extension
    if not '.' in basename:
        basename += ".jpg"
    return basename

url_to_local = {}
failed_images = []
downloaded_images = []
external_hosts = set()

# Normalize URLs to fetch
fetch_queue = []
for u in sorted(all_img_urls):
    parsed = urllib.parse.urlparse(u)
    netloc = parsed.netloc.lower()
    
    # Target URL on varanasitemples.in
    target_url = u
    if 'varanasi-temples.com' in netloc:
        external_hosts.add(netloc)
        target_url = urllib.parse.urlunparse(('https', 'varanasitemples.in', parsed.path, '', parsed.query, ''))
    elif netloc.startswith('www.'):
        target_url = urllib.parse.urlunparse(('https', 'varanasitemples.in', parsed.path, '', parsed.query, ''))
    elif not netloc:
        target_url = urllib.parse.urljoin('https://varanasitemples.in/', u)
    elif 'varanasitemples.in' in netloc:
        target_url = urllib.parse.urlunparse(('https', 'varanasitemples.in', parsed.path, '', parsed.query, ''))
    else:
        external_hosts.add(netloc)

    fname = get_image_filename(target_url)
    local_path = os.path.join(IMAGES_DIR, fname)
    url_to_local[u] = f"assets/images/{fname}"
    url_to_local[target_url] = f"assets/images/{fname}"
    
    fetch_queue.append((u, target_url, local_path, fname))

def download_one(item):
    orig_url, target_url, local_path, fname = item
    if os.path.exists(local_path) and os.path.getsize(local_path) > 100:
        return orig_url, target_url, local_path, True, "Already exists", os.path.getsize(local_path)
    
    # Try downloading target_url
    for attempt in range(2):
        try:
            req = urllib.request.Request(target_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) > 0:
                    with open(local_path, 'wb') as f:
                        f.write(data)
                    return orig_url, target_url, local_path, True, "Downloaded", len(data)
        except Exception as e:
            time.sleep(0.5)
            # If target_url failed and orig_url was different, try orig_url
            if attempt == 1 and orig_url != target_url:
                try:
                    req = urllib.request.Request(orig_url, headers=HEADERS)
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = resp.read()
                        if len(data) > 0:
                            with open(local_path, 'wb') as f:
                                f.write(data)
                            return orig_url, target_url, local_path, True, "Downloaded from orig", len(data)
                except Exception as e2:
                    return orig_url, target_url, local_path, False, str(e2), 0
    return orig_url, target_url, local_path, False, "Failed after retries", 0

print(f"Starting download of {len(fetch_queue)} unique images...")

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(download_one, item) for item in fetch_queue]
    for f in as_completed(futures):
        orig_url, target_url, local_path, success, msg, size = f.result()
        if success:
            downloaded_images.append({
                'original_url': orig_url,
                'target_url': target_url,
                'local_path': local_path,
                'bytes': size,
                'status': msg
            })
        else:
            failed_images.append({
                'original_url': orig_url,
                'target_url': target_url,
                'local_path': local_path,
                'error': msg
            })

print(f"\nImage Download Results:")
print(f"Successfully downloaded: {len(downloaded_images)}")
print(f"Failed images: {len(failed_images)}")

# Save mapping
with open('image_url_map.json', 'w', encoding='utf-8') as f:
    json.dump(url_to_local, f, indent=2)

# Save missing_assets.csv
with open(os.path.join(DATA_DIR, 'missing_assets.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['original_url', 'target_url', 'local_path', 'error'])
    writer.writeheader()
    for row in failed_images:
        writer.writerow(row)

# Also write to root directory
with open('missing_assets.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['original_url', 'target_url', 'local_path', 'error'])
    writer.writeheader()
    for row in failed_images:
        writer.writerow(row)

# Save external_asset_hosts.csv
with open(os.path.join(DATA_DIR, 'external_asset_hosts.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['hostname'])
    for h in sorted(external_hosts):
        writer.writerow([h])

with open('external_asset_hosts.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['hostname'])
    for h in sorted(external_hosts):
        writer.writerow([h])

print("Saved image_url_map.json, missing_assets.csv, external_asset_hosts.csv")
