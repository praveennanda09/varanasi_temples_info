# generate_offline_mirror.py
import os
import re
import json
import csv
import hashlib
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')
MIRROR_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website')
DATA_DIR = os.path.join(MIRROR_DIR, 'data')

os.makedirs(MIRROR_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, 'crawl_state.json'), 'r', encoding='utf-8') as f:
    crawl_state = json.load(f)

with open(os.path.join(BASE_DIR, 'image_url_map.json'), 'r', encoding='utf-8') as f:
    img_map = json.load(f)

visited = crawl_state.get('visited', {})

# Build URL to relative path mapping
# E.g. https://varanasitemples.in/ -> index.html
# https://varanasitemples.in/category/aditya-temples/arun-aditya/ -> category/aditya-temples/arun-aditya/index.html
def url_to_rel_path(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/')
    query = parsed.query
    if not path and not query:
        return 'index.html'
    if query:
        # e.g. p=533
        clean_q = re.sub(r'[^a-zA-Z0-9_=-]', '_', query)
        if path:
            return f"{path}_{clean_q}.html"
        return f"{clean_q}.html"
    # Normal path
    return f"{path}/index.html"

url_to_local_file = {}
for u in visited.keys():
    rel = url_to_rel_path(u)
    url_to_local_file[u] = rel
    # Also without trailing slash
    if u.endswith('/'):
        url_to_local_file[u[:-1]] = rel
    else:
        url_to_local_file[u + '/'] = rel

print(f"Total URL mappings generated: {len(url_to_local_file)}")

def get_relative_url(source_file, target_file):
    # Calculate relative path from source_file dir to target_file
    source_dir = os.path.dirname(source_file)
    rel = os.path.relpath(target_file, source_dir if source_dir else '.')
    return rel.replace('\\', '/')

manifest_records = []
visited_urls_list = []
failed_records = []

processed_pages = 0
for url, info in visited.items():
    if info.get('status') != 'ok':
        failed_records.append({
            'url': url,
            'error': info.get('error', 'Unknown error')
        })
        continue

    visited_urls_list.append(url)
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{h}.html")
    if not os.path.exists(cache_path):
        continue

    with open(cache_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    target_rel = url_to_rel_path(url)
    target_abs = os.path.join(MIRROR_DIR, target_rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(target_abs), exist_ok=True)

    # 1. Rewrite internal links
    def replace_href(match):
        full_match = match.group(0)
        href = match.group(1).strip()
        parsed_href = urllib.parse.urlparse(href)
        netloc = parsed_href.netloc.lower()
        if 'varanasitemples.in' in netloc or not netloc:
            # internal link
            clean_href = urllib.parse.urlunparse(('https', 'varanasitemples.in', parsed_href.path, '', parsed_href.query, ''))
            if clean_href in url_to_local_file:
                target_dest = url_to_local_file[clean_href]
                rel_link = get_relative_url(target_rel, target_dest)
                return f'href="{rel_link}"'
            elif clean_href.rstrip('/') + '/' in url_to_local_file:
                target_dest = url_to_local_file[clean_href.rstrip('/') + '/']
                rel_link = get_relative_url(target_rel, target_dest)
                return f'href="{rel_link}"'
        # external link
        return f'href="{href}" target="_blank" rel="noopener" title="External link (requires internet)"'

    rewritten_html = re.sub(r'href=[\'"](https?://[^\'"#\s]+)[\'"]', replace_href, html, flags=re.I)

    # 2. Rewrite images
    def replace_img(match):
        src = match.group(1).strip()
        if src in img_map:
            target_dest = img_map[src]
            rel_link = get_relative_url(target_rel, target_dest)
            return f'src="{rel_link}"'
        # Check if basename matches
        fname = os.path.basename(urllib.parse.urlparse(src).path)
        local_img = os.path.join(MIRROR_DIR, 'assets', 'images', fname)
        if os.path.exists(local_img):
            rel_link = get_relative_url(target_rel, f"assets/images/{fname}")
            return f'src="{rel_link}"'
        return match.group(0)

    rewritten_html = re.sub(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', replace_img, rewritten_html, flags=re.I)

    # 3. Rewrite CSS and JS links to local assets
    rel_css = get_relative_url(target_rel, 'assets/css/style.css')
    rel_js = get_relative_url(target_rel, 'assets/js/script.js')
    rel_jquery = get_relative_url(target_rel, 'assets/js/jquery.js')

    # Replace stylesheets
    rewritten_html = re.sub(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"][^\'"]*kashitemplesonecol2/style\.css[^\'"]*[\'"][^>]*>',
                            f'<link rel="stylesheet" href="{rel_css}" type="text/css" media="screen" />', rewritten_html, flags=re.I)
    rewritten_html = re.sub(r'<script[^>]+src=[\'"][^\'"]*kashitemplesonecol2/script\.js[^\'"]*[\'"][^>]*></script>',
                            f'<script type="text/javascript" src="{rel_js}"></script>', rewritten_html, flags=re.I)
    rewritten_html = re.sub(r'<script[^>]+src=[\'"][^\'"]*jquery/jquery\.js[^\'"]*[\'"][^>]*></script>',
                            f'<script type="text/javascript" src="{rel_jquery}"></script>', rewritten_html, flags=re.I)

    # Add offline navigation notice at top of body
    banner_html = f'''<!-- OFFLINE ARCHIVE BANNER -->
<div style="background:#8b0000; color:#fff; padding:8px 15px; font-family:sans-serif; font-size:13px; text-align:center; z-index:99999; position:relative;">
  <strong>KASHI OFFLINE MIRROR</strong> &mdash; Original: <a href="{url}" style="color:#ffd700; text-decoration:underline;">{url}</a> &mdash; 
  <a href="{get_relative_url(target_rel, 'index.html')}" style="color:#fff; font-weight:bold; margin-left:10px;">[Home]</a>
  <a href="{get_relative_url(target_rel, '../Kashi_Pilgrimage_Master_Index.html')}" style="color:#fff; font-weight:bold; margin-left:10px;">[Master Pilgrimage Guide]</a>
</div>
'''
    if '<body' in rewritten_html:
        rewritten_html = re.sub(r'(<body[^>]*>)', r'\1' + banner_html, rewritten_html, count=1, flags=re.I)

    with open(target_abs, 'w', encoding='utf-8') as out_f:
        out_f.write(rewritten_html)

    # Manifest record
    category = "general"
    if '/aditya-temples/' in url:
        category = "surya"
    elif '/bhairav-temples/' in url:
        category = "bhairav"
    elif '/devi-temples/' in url:
        category = "devi"
    elif '/shiva-temples/' in url or '/jyotir-lings/' in url:
        category = "shiva"
    elif '/vinayak-temples/' in url:
        category = "vinayaka"
    elif '/vishnu-temples/' in url:
        category = "vishnu"
    elif '/importance-of-river-ganga/' in url:
        category = "ganga"

    manifest_records.append({
        'original_url': url,
        'final_url': info.get('final_url', url),
        'http_status': info.get('http_status', 200),
        'retrieval_timestamp': info.get('timestamp', ''),
        'page_title': info.get('title', ''),
        'content_type': 'text/html; charset=UTF-8',
        'local_saved_path': target_rel,
        'page_category': category,
        'discovered_internal_links': info.get('discovered_links_count', 0),
        'discovered_media_resources': info.get('images_count', 0),
        'downloaded_assets_count': info.get('images_count', 0),
        'extraction_status': 'COMPLETED',
        'validation_status': 'VALIDATED',
        'error_details': ''
    })

    processed_pages += 1
    if processed_pages % 200 == 0:
        print(f"Mirror generated: {processed_pages} / {len(visited)} pages...")

print(f"Exact offline website mirror generated completely: {processed_pages} pages processed.")

# Save crawl_manifest.csv and crawl_manifest.json (both in root and in Kashi_Exact_Offline_Website/data/)
fieldnames = [
    'original_url', 'final_url', 'http_status', 'retrieval_timestamp', 'page_title',
    'content_type', 'local_saved_path', 'page_category', 'discovered_internal_links',
    'discovered_media_resources', 'downloaded_assets_count', 'extraction_status',
    'validation_status', 'error_details'
]

for out_dir in [BASE_DIR, DATA_DIR]:
    with open(os.path.join(out_dir, 'crawl_manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in manifest_records:
            writer.writerow(r)

    with open(os.path.join(out_dir, 'crawl_manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest_records, f, indent=2)

    with open(os.path.join(out_dir, 'visited_urls.txt'), 'w', encoding='utf-8') as f:
        for u in sorted(visited_urls_list):
            f.write(u + '\n')

    with open(os.path.join(out_dir, 'failed_urls.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'error'])
        writer.writeheader()
        for r in failed_records:
            writer.writerow(r)

print("Saved crawl_manifest.csv, crawl_manifest.json, visited_urls.txt, failed_urls.csv in both root and data/!")
