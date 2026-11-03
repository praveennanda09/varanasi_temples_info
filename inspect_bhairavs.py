# inspect_bhairavs.py
import os
import sys
import re
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

expected_bhairavs = [
    ("Kaal Bhairav", "https://varanasitemples.in/category/bhairav-temples/kaal-bhairav/"),
    ("Asitang Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/asitang-bhairav/"),
    ("Bheeshan Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/bheeshan-bhairav/"),
    ("Chand Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/chand-bhairav/"),
    ("Kapal Bhairav (Laat Bhairav)", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/kapal-bhairav-laat-bhairav/"),
    ("Krodhan Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/krodhan-bhairav/"),
    ("Ruru Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/ruru-bhairav/"),
    ("Samhar Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/samhar-bhairav/"),
    ("Unmat Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/unmat-bhairav/"),
]

for name, url in expected_bhairavs:
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    fpath = os.path.join(CACHE_DIR, f"{h}.html")
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        content = ""
        for p in posts:
            if len(p) > len(content):
                content = p
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+uploads[^\'"]+)[\'"]', content, re.I)
        loc_match = re.search(r'(LOCATION OF [^<]+)(.*?)(TYPES OF POOJA|POOJA|TIMINGS|COMMENTS|$)', content, re.DOTALL | re.I)
        loc_text = ""
        if loc_match:
            loc_text = re.sub(r'<[^>]+>', ' ', loc_match.group(2)).strip()
            loc_text = ' '.join(loc_text.split())
        print(f"[{name}]")
        print(f"  Photo: {imgs[0] if imgs else 'NONE'}")
        print(f"  Location Excerpt: {loc_text[:200] if loc_text else 'NOT DETECTED'}")
    else:
        print(f"[{name}] NOT FOUND IN CACHE!")
