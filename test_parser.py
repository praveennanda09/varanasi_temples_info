# test_parser.py
import os
import sys
import re
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

jyoti_url = 'https://varanasitemples.in/category/jyotir-lings/'
h = hashlib.md5(jyoti_url.encode('utf-8')).hexdigest()
fpath = os.path.join(CACHE_DIR, f"{h}.html")
if os.path.exists(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
    for p in posts:
        clean = re.sub(r'<[^>]+>', '\n', p)
        lines = [l.strip() for l in clean.split('\n') if l.strip()]
        if len(lines) > 10:
            print("Lines in Jyotirlinga Hub:")
            for l in lines[:40]:
                print("  ", l)
