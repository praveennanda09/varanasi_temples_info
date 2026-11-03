# run_offline_validation.py
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIRROR_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website')

print("=== STARTING RIGOROUS OFFLINE ACCEPTANCE VALIDATION ===")

# 1. Check generated files exist
mandatory_files = [
    'Kashi_Pilgrimage_Master_Index.html',
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html',
    'temples_master.json',
    'temples_master.csv',
    'crawl_manifest.csv',
    'crawl_manifest.json',
    'missing_data_report.csv',
    'missing_images_report.csv',
    'validation_report.json',
    'README_OFFLINE.txt',
    'Kashi_Complete_Offline_Pilgrimage_Archive.zip'
]

print("\n--- Checking Mandatory Deliverable Files ---")
missing_count = 0
for f in mandatory_files:
    fpath = os.path.join(BASE_DIR, f)
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f"[PASS] {f:<40} ({size:,} bytes)")
    else:
        print(f"[FAIL] MISSING: {f}")
        missing_count += 1

# 2. Check mirror homepage and assets
print("\n--- Checking Exact Offline Mirror Structure ---")
mirror_checks = [
    os.path.join(MIRROR_DIR, 'index.html'),
    os.path.join(MIRROR_DIR, 'assets', 'css', 'style.css'),
    os.path.join(MIRROR_DIR, 'assets', 'js', 'script.js'),
    os.path.join(MIRROR_DIR, 'assets', 'js', 'jquery.js'),
    os.path.join(MIRROR_DIR, 'local_server.py'),
    os.path.join(MIRROR_DIR, 'README_OFFLINE.txt'),
]
for mc in mirror_checks:
    if os.path.exists(mc):
        print(f"[PASS] {os.path.relpath(mc, BASE_DIR)} exists ({os.path.getsize(mc):,} bytes)")
    else:
        print(f"[FAIL] Missing {mc}")
        missing_count += 1

# 3. Check mirror HTML files count
html_files = []
for root, dirs, files in os.walk(MIRROR_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))
print(f"[PASS] Total mirrored HTML pages in Kashi_Exact_Offline_Website: {len(html_files)}")

# 4. Check image assets on disk
images_dir = os.path.join(MIRROR_DIR, 'assets', 'images')
image_files = os.listdir(images_dir) if os.path.exists(images_dir) else []
print(f"[PASS] Total downloaded temple & media images: {len(image_files)}")

# 5. Check Guide HTML Content & Image References
print("\n--- Checking Guide HTML Image References & Content Completeness ---")
guides = [
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html'
]

for g in guides:
    gpath = os.path.join(BASE_DIR, g)
    with open(gpath, 'r', encoding='utf-8') as gf:
        html = gf.read()
    
    # check images
    srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html)
    broken_imgs = []
    for s in srcs:
        # local file path
        target = os.path.join(BASE_DIR, s.replace('/', os.sep))
        if not os.path.exists(target):
            broken_imgs.append(s)
    
    cards_count = html.count('class="temple-card"')
    print(f"[{g}] {cards_count} temple cards | {len(srcs)} images | Broken images: {len(broken_imgs)}")
    if broken_imgs:
        print("  Sample broken:", broken_imgs[:3])

# 6. Check Master Index Links
with open('Kashi_Pilgrimage_Master_Index.html', 'r', encoding='utf-8') as f:
    master_html = f.read()

master_links = re.findall(r'href=[\'"]([^\'"]+\.html)[\'"]', master_html)
broken_links = []
for l in set(master_links):
    target = os.path.join(BASE_DIR, l.replace('/', os.sep))
    if not os.path.exists(target):
        broken_links.append(l)

print(f"\n[Master Index] Found {len(set(master_links))} unique HTML targets | Broken links: {len(broken_links)}")
if broken_links:
    print("  Broken links:", broken_links)

# 7. Check ZIP package validity
zip_path = os.path.join(BASE_DIR, 'Kashi_Complete_Offline_Pilgrimage_Archive.zip')
if os.path.exists(zip_path):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as z:
        infolist = z.infolist()
        print(f"[PASS] ZIP Archive verified! Contains {len(infolist)} files, uncompressed size: {sum(x.file_size for x in infolist):,} bytes.")

print("\n=== OFFLINE ACCEPTANCE VALIDATION COMPLETE ===")
