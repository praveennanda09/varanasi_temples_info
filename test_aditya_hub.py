# test_aditya_hub.py
import os
import sys
import re
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

url = 'https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/'
h = hashlib.md5(url.encode('utf-8')).hexdigest()
fpath = os.path.join(CACHE_DIR, f"{h}.html")
if os.path.exists(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
    for p in posts:
        clean = re.sub(r'<[^>]+>', '\n', p)
        lines = [l.strip() for l in clean.split('\n') if l.strip()]
        if len(lines) > 10:
            print("Aditya Hub Excerpt:")
            for l in lines[:50]:
                print("  ", l)
