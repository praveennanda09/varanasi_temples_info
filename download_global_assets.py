# download_global_assets.py
import os
import urllib.request
import re
from urllib.parse import urljoin, urlparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

with open('homepage_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all CSS
css_links = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I)
# Find all JS
js_links = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)

print("Found CSS links:", len(css_links))
print("Found JS links:", len(js_links))

os.makedirs('Kashi_Exact_Offline_Website/assets/css', exist_ok=True)
os.makedirs('Kashi_Exact_Offline_Website/assets/js', exist_ok=True)
os.makedirs('Kashi_Exact_Offline_Website/assets/images', exist_ok=True)

for c in css_links:
    c_clean = c.split('?')[0]
    fname = os.path.basename(urlparse(c_clean).path)
    if not fname:
        fname = "style.css"
    dest = os.path.join('Kashi_Exact_Offline_Website/assets/css', fname)
    print(f"Downloading CSS: {c} -> {dest}")
    try:
        req = urllib.request.Request(c, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(dest, 'wb') as out:
            out.write(data)
    except Exception as e:
        print(f"Failed CSS {c}: {e}")

for j in js_links:
    j_clean = j.split('?')[0]
    fname = os.path.basename(urlparse(j_clean).path)
    if not fname:
        fname = "script.js"
    dest = os.path.join('Kashi_Exact_Offline_Website/assets/js', fname)
    print(f"Downloading JS: {j} -> {dest}")
    try:
        req = urllib.request.Request(j, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(dest, 'wb') as out:
            out.write(data)
    except Exception as e:
        print(f"Failed JS {j}: {e}")

print("Global assets download step complete.")
