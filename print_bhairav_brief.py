# print_bhairav_brief.py
import os
import sys
import re
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

url = "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/a-brief-about-bhairav-temples/"
h = hashlib.md5(url.encode('utf-8')).hexdigest()
fpath = os.path.join("raw_html_cache", f"{h}.html")
if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()
    posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
    content = max(posts, key=len)
    clean = re.sub(r'<[^>]+>', '\n', content)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    print("=== A BRIEF ABOUT BHAIRAV TEMPLES ===")
    for l in lines:
        print("  ", l)
