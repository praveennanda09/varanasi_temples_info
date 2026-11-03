# inspect_devi.py
import os
import sys
import re
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')

with open('crawl_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

visited = state.get('visited', {})
devi_urls = [u for u in visited if '/category/devi-temples/' in u and not '/feed/' in u and not u.endswith('/devi-temples/')]
print(f"Total Devi URLs in categories: {len(devi_urls)}")

# The 10 Mahavidyas in standard Shakta tradition:
# 1. Kali
# 2. Tara
# 3. Tripurasundari / Shodashi / Lalitha
# 4. Bhuvaneshwari
# 5. Bhairavi / Tripura Bhairavi
# 6. Chhinnamasta
# 7. Dhumavati
# 8. Bagalamukhi
# 9. Matangi
# 10. Kamalatmika / Kamala / Lakshmi

mahavidya_keywords = ['KALI', 'TARA', 'TRIPURA', 'SUNDARI', 'LALITHA', 'BHUVANESHWARI', 'BHAIRAVI', 'CHHINNA', 'DHUMAVATI', 'BAGALAMUKHI', 'MATANGI', 'KAMALA', 'LAKSHMI', 'MAHALAKSHMI', 'SIDDHA LAKSHMI']

devi_temples_data = []

for u in sorted(devi_urls):
    h = hashlib.md5(u.encode('utf-8')).hexdigest()
    fpath = os.path.join(CACHE_DIR, f"{h}.html")
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        content = max(posts, key=len) if posts else ""
        clean = re.sub(r'<[^>]+>', '\n', content)
        lines = [l.strip() for l in clean.split('\n') if l.strip()]
        
        # Name from URL
        slug = u.strip('/').split('/')[-1]
        name = slug.replace('-', ' ').title()
        
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+uploads[^\'"]+)[\'"]', content, re.I)
        
        devi_temples_data.append({
            'name': name,
            'url': u,
            'slug': slug,
            'lines_count': len(lines),
            'first_lines': lines[:3],
            'photo': imgs[0] if imgs else None,
            'full_text': ' '.join(lines)
        })

print(f"Extracted data for {len(devi_temples_data)} Devi temples.")
for dt in devi_temples_data:
    photo_str = "YES" if dt['photo'] else "NO"
    # check Mahavidya relevance
    rel_m = [k for k in mahavidya_keywords if k in dt['name'].upper() or k in dt['full_text'][:300].upper()]
    print(f"- {dt['name']} | Photo: {photo_str} | Mahavidya keywords: {rel_m}")
