# print_bhairav_full.py
import os
import sys
import re
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

for name, slug in [
    ("Bheeshan Bhairav", "bheeshan-bhairav"),
    ("Chand Bhairav", "chand-bhairav"),
    ("Kapal Bhairav", "kapal-bhairav-laat-bhairav"),
    ("Ruru Bhairav", "ruru-bhairav")
]:
    url = f"https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/{slug}/"
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    fpath = os.path.join("raw_html_cache", f"{h}.html")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        content = max(posts, key=len)
        clean = re.sub(r'<[^>]+>', '\n', content)
        lines = [l.strip() for l in clean.split('\n') if l.strip()]
        print(f"\n==================== {name} ====================")
        for l in lines:
            print("  ", l)
