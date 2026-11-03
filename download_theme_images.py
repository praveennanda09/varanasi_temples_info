# download_theme_images.py
import os
import re
import urllib.request
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
}

css_path = 'Kashi_Exact_Offline_Website/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
    css_content = f.read()

# Artisteer style.css references url('images/...') relative to the css file
img_urls = re.findall(r'url\s*\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', css_content)
print(f"Total url() references in style.css: {len(img_urls)}")

base_url = 'https://varanasitemples.in/wp-content/themes/kashitemplesonecol2/'

# Store images in assets/css/images/ so relative url('images/...') works automatically!
os.makedirs('Kashi_Exact_Offline_Website/assets/css/images', exist_ok=True)

downloaded = 0
for ref in set(img_urls):
    if ref.startswith('data:'):
        continue
    # If ref is like 'images/header.jpg'
    full_url = urljoin(base_url, ref)
    dest_path = os.path.join('Kashi_Exact_Offline_Website/assets/css', ref.replace('/', os.sep))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        continue
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
        with open(dest_path, 'wb') as out:
            out.write(data)
        downloaded += 1
    except Exception as e:
        print(f"Failed theme img {ref}: {e}")

print(f"Downloaded {downloaded} theme background images.")
