# analyze_images.py
import os
import re
import json
from urllib.parse import urlparse, urljoin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

all_images = set()
upload_images = set()
plugin_images = set()
external_images = set()

for fname in os.listdir(CACHE_DIR):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(CACHE_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Extract src
    srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
    for s in srcs:
        s = s.strip()
        if not s or s.startswith('data:'):
            continue
        all_images.add(s)
        parsed = urlparse(s)
        netloc = parsed.netloc.lower()
        if 'varanasitemples.in' in netloc or not netloc:
            if 'wp-content/uploads' in s:
                upload_images.add(s)
            else:
                plugin_images.add(s)
        else:
            external_images.add(s)

print(f"Total unique images found across all pages: {len(all_images)}")
print(f"Temple/Upload photos (wp-content/uploads): {len(upload_images)}")
print(f"Theme/Plugin/Widget images: {len(plugin_images)}")
print(f"External images: {len(external_images)}")

print("\nSample upload photos:")
for u in sorted(upload_images)[:10]:
    print(" ", u)

print("\nExternal hosts:")
ext_hosts = set(urlparse(u).netloc for u in external_images)
for h in ext_hosts:
    print(" ", h)

# Save lists
with open('upload_photos.txt', 'w', encoding='utf-8') as f:
    for u in sorted(upload_images):
        f.write(u + '\n')
