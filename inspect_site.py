# inspect_site.py
import urllib.request
import re
from urllib.parse import urljoin, urlparse

url = 'https://varanasitemples.in/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

with open('homepage_raw.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved homepage_raw.html (bytes: %d)" % len(html))

# Find all links
all_links = set(re.findall(r'href=[\'"](https?://varanasitemples\.in[^\'"#\s]*)[\'"]', html))
print(f"Total varanasitemples.in links on homepage: {len(all_links)}")

# Breakdown of links
cats = [u for u in all_links if '/category/' in u]
posts = [u for u in all_links if not '/category/' in u and not '/tag/' in u and not '/page/' in u and u != 'https://varanasitemples.in/']

print(f"Categories on homepage: {len(cats)}")
print(f"Other pages/posts on homepage: {len(posts)}")

# Look for assets
css = set(re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I))
js = set(re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))
imgs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

print(f"CSS files: {len(css)}")
print(f"JS files: {len(js)}")
print(f"Images: {len(imgs)}")
