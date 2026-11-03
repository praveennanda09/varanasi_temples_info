# check_cat_vs_post.py
import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

cat_url = 'https://varanasitemples.in/category/aditya-temples/arun-aditya/'
req = urllib.request.Request(cat_url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    cat_html = r.read().decode('utf-8', errors='ignore')

with open('arun_cat.html', 'w', encoding='utf-8') as f:
    f.write(cat_html)

print("Cat HTML size:", len(cat_html))
posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', cat_html, re.DOTALL)
print(f"Cat art-PostContent blocks: {len(posts)}")
for i, p in enumerate(posts):
    print(f"Block {i} len: {len(p)}")
