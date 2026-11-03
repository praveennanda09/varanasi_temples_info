# inspect_adityas.py
import os
import sys
import re
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

expected_adityas = [
    ("Arun Aditya", "https://varanasitemples.in/category/aditya-temples/arun-aditya/"),
    ("Draupad Aditya", "https://varanasitemples.in/category/aditya-temples/draupad-aditya/"),
    ("Ganga Aditya", "https://varanasitemples.in/category/aditya-temples/ganga-aditya/"),
    ("Keshava Aditya", "https://varanasitemples.in/category/aditya-temples/keshava-aditya/"),
    ("Khakholkh Aditya", "https://varanasitemples.in/category/aditya-temples/khakholkh-aditya/"),
    ("Lolark Aditya", "https://varanasitemples.in/category/aditya-temples/lolark-aditya/"),
    ("Mayukh Aditya", "https://varanasitemples.in/category/aditya-temples/mayukh-aditya/"),
    ("Saamba Aditya", "https://varanasitemples.in/category/aditya-temples/saamba-aditya/"),
    ("Uttarark Aditya", "https://varanasitemples.in/category/aditya-temples/uttarark-aditya/"),
    ("Vimal Aditya", "https://varanasitemples.in/category/aditya-temples/vimal-aditya/"),
    ("Vriddh Aditya", "https://varanasitemples.in/category/aditya-temples/vriddh-aditya/"),
    ("Yama Aditya", "https://varanasitemples.in/category/aditya-temples/yama-aditya/"),
]

for name, url in expected_adityas:
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    fpath = os.path.join(CACHE_DIR, f"{h}.html")
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Post content
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        content = ""
        for p in posts:
            if len(p) > len(content):
                content = p
        
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+uploads[^\'"]+)[\'"]', content, re.I)
        
        # Extract location section
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
