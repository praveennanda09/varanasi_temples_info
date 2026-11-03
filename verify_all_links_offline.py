# verify_all_links_offline.py
import os
import re

print("=" * 60)
print("VERIFYING OFFLINE LINKS ACROSS ENTIRE ARCHIVE")
print("=" * 60)

# 1. Check Master Index and 6 Deity Guides
root_htmls = [
    'Kashi_Pilgrimage_Master_Index.html',
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html',
]

for doc in root_htmls:
    if not os.path.exists(doc):
        print(f"Missing: {doc}")
        continue
    with open(doc, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for live varanasitemples.in links
    live_links = re.findall(r'href=[\'"](https?://(?:www\.)?varanasitemples\.in[^\'"]*)[\'"]', content)
    # Check for relative local links
    local_links = re.findall(r'href=[\'"](Kashi_Exact_Offline_Website/[^\'"]*|[0-9a-zA-Z_]+\.html[^\'"]*)[\'"]', content)
    print(f"{doc}: {len(live_links)} live links, {len(local_links)} local relative links")

# 2. Check Exact Offline Website Mirror
mirror_index = 'Kashi_Exact_Offline_Website/index.html'
with open(mirror_index, 'r', encoding='utf-8') as f:
    m_content = f.read()

# Check navigation links
nav_live = re.findall(r'<a\s+[^>]*href=[\'"](https?://(?:www\.)?varanasitemples\.in[^\'"]*)[\'"]', m_content)
nav_relative = re.findall(r'<a\s+[^>]*href=[\'"](category/[^\'"]*|assets/[^\'"]*|index\.html[^\'"]*)[\'"]', m_content)
print(f"\nMirror index.html navigation: {len(nav_live)} live <a href>, {len(nav_relative)} local <a href>")

# Check collapsItems dynamic JS array in mirror index.html
js_live = re.findall(r'collapsItems\[.*?\]\s*=\s*[\'"][^\'"]*varanasitemples\.in', m_content)
print(f"Mirror index.html collapsItems pointing to live: {len(js_live)}")

# 3. Check sample deep pages
deep_samples = [
    'Kashi_Exact_Offline_Website/category/aditya-temples/arun-aditya/index.html',
    'Kashi_Exact_Offline_Website/category/bhairav-temples/kaal-bhairav/index.html',
    'Kashi_Exact_Offline_Website/category/devi-temples/annapurna/index.html',
    'Kashi_Exact_Offline_Website/category/jyotir-lings/kashi-visweshwar/index.html',
]

print("\nDeep Page Audits:")
for dp in deep_samples:
    if os.path.exists(dp):
        with open(dp, 'r', encoding='utf-8') as f:
            txt = f.read()
        dp_live_a = re.findall(r'<a\s+[^>]*href=[\'"](https?://(?:www\.)?varanasitemples\.in[^\'"]*)[\'"]', txt)
        dp_live_js = re.findall(r'collapsItems\[.*?\]\s*=\s*[\'"][^\'"]*varanasitemples\.in', txt)
        dp_imgs = re.findall(r'<img\s+[^>]*src=[\'"](\.\./\.\./\.\./assets/images/[^\'"]+)[\'"]', txt)
        print(f" {os.path.basename(os.path.dirname(dp))}: {len(dp_live_a)} live <a href>, {len(dp_live_js)} live JS links, {len(dp_imgs)} local relative images")

print("=" * 60)
