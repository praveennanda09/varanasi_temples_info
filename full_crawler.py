# full_crawler.py
import os
import sys
import re
import json
import csv
import time
import hashlib
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Set up directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')
IMAGES_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website', 'assets', 'images')
DATA_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website', 'data')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

STATE_FILE = os.path.join(BASE_DIR, 'crawl_state.json')

def get_url_hash(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def normalize_url(url):
    url = url.split('#')[0].strip()
    if not url:
        return ""
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        return ""
    # normalize scheme
    scheme = 'https'
    netloc = parsed.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    if netloc != 'varanasitemples.in':
        return ""
    path = parsed.path
    if not path.endswith('/') and not '.' in path.split('/')[-1]:
        path = path + '/'
    query = parsed.query
    # filter out harmless analytics query params
    if query:
        q_params = [q for q in query.split('&') if not q.startswith('utm_') and not q.startswith('ver=')]
        query = '&'.join(q_params)
    norm = urllib.parse.urlunparse((scheme, 'varanasitemples.in', path, '', query, ''))
    return norm

def fetch_url(url, retries=3):
    h = get_url_hash(url)
    cache_path = os.path.join(CACHE_DIR, f"{h}.html")
    meta_path = os.path.join(CACHE_DIR, f"{h}.json")
    
    if os.path.exists(cache_path) and os.path.exists(meta_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                html = f.read()
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            return html, meta, None
        except Exception:
            pass

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=20) as resp:
                status = resp.status
                final_url = resp.geturl()
                content_type = resp.headers.get('Content-Type', '')
                raw_bytes = resp.read()
                html = raw_bytes.decode('utf-8', errors='ignore')
                meta = {
                    'original_url': url,
                    'final_url': final_url,
                    'status': status,
                    'content_type': content_type,
                    'bytes': len(raw_bytes),
                    'timestamp': datetime.now().isoformat(),
                    'duration_sec': round(time.time() - t0, 3)
                }
                with open(cache_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                with open(meta_path, 'w', encoding='utf-8') as f:
                    json.dump(meta, f, indent=2)
                return html, meta, None
        except Exception as e:
            time.sleep(1 + attempt * 2)
            if attempt == retries - 1:
                return None, None, str(e)
    return None, None, "Max retries exceeded"

def main():
    print("=== STARTING AUTONOMOUS CRAWLER ===")
    
    # Load initial seed list
    seeds = set()
    if os.path.exists('discovered_seeds.txt'):
        with open('discovered_seeds.txt', 'r', encoding='utf-8') as f:
            for line in f:
                u = normalize_url(line.strip())
                if u:
                    seeds.add(u)
    
    # Explicit primary hubs
    seeds.add('https://varanasitemples.in/')
    seeds.add('https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/')
    seeds.add('https://varanasitemples.in/category/jyotir-lings/')

    # Load persistent state
    state = {'visited': {}, 'queue': list(sorted(seeds)), 'discovered': list(sorted(seeds))}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                loaded_state = json.load(f)
                state['visited'] = loaded_state.get('visited', {})
                existing_q = set(loaded_state.get('queue', []))
                existing_q.update(seeds)
                state['queue'] = list(sorted(existing_q - set(state['visited'].keys())))
                state['discovered'] = loaded_state.get('discovered', list(seeds))
        except Exception as e:
            print(f"Error loading state file: {e}")

    print(f"Queue size: {len(state['queue'])}, Already visited: {len(state['visited'])}")

    max_workers = 5
    batch_size = 25
    iteration = 0

    while state['queue']:
        iteration += 1
        batch = state['queue'][:batch_size]
        state['queue'] = state['queue'][batch_size:]
        print(f"\n--- Batch {iteration} ({len(batch)} URLs) | Remaining in queue: {len(state['queue'])} ---")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(fetch_url, u): u for u in batch}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    html, meta, err = future.result()
                    if err:
                        print(f"[-] FAILED: {url} -> {err}")
                        state['visited'][url] = {'status': 'failed', 'error': err}
                    else:
                        print(f"[+] OK ({meta['status']}): {url} ({meta['bytes']} bytes)")
                        # Extract title
                        m_title = re.findall(r'<title>(.*?)</title>', html, re.I | re.DOTALL)
                        title = m_title[0].strip() if m_title else ""
                        
                        # Extract all internal links
                        links = re.findall(r'href=[\'"](https?://[^\'"#\s]+)[\'"]', html, re.I)
                        new_links = set()
                        for l in links:
                            nl = normalize_url(l)
                            if nl and nl not in state['visited'] and nl not in state['queue']:
                                # Only queue in-scope URLs (categories, posts, pages)
                                if any(x in nl for x in ['/category/', '/aditya-temples/', '/bhairav-temples/', '/devi-temples/', '/shiva-temples/', '/vinayak-temples/', '/vishnu-temples/', '/importance-of-river-ganga/']) or nl.count('/') <= 4:
                                    if not any(nl.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.css', '.js', '.xml', '.php']):
                                        new_links.add(nl)
                        
                        # Add newly discovered links
                        for nl in new_links:
                            if nl not in state['discovered']:
                                state['discovered'].append(nl)
                                state['queue'].append(nl)

                        # Extract images
                        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
                        
                        state['visited'][url] = {
                            'status': 'ok',
                            'title': title,
                            'final_url': meta['final_url'],
                            'http_status': meta['status'],
                            'bytes': meta['bytes'],
                            'discovered_links_count': len(new_links),
                            'images_count': len(imgs),
                            'images': imgs,
                            'timestamp': meta['timestamp'],
                        }
                except Exception as e:
                    print(f"[-] EXCEPTION: {url} -> {e}")
                    state['visited'][url] = {'status': 'failed', 'error': str(e)}

        # Checkpoint state
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        print(f"Checkpoint saved. Total visited: {len(state['visited'])}, Total queue: {len(state['queue'])}")

    print("\n=== ALL HTML CRAWLING COMPLETED ===")
    print(f"Total pages successfully visited: {len([u for u, d in state['visited'].items() if d.get('status') == 'ok'])}")
    print(f"Total pages failed: {len([u for u, d in state['visited'].items() if d.get('status') == 'failed'])}")

if __name__ == '__main__':
    main()
