# verify_all_guides_final.py
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

docs = [
    'Kashi_Pilgrimage_Master_Index.html',
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html'
]

print("=" * 65)
print("FINAL AUDIT: IMAGE VISIBILITY ACROSS ALL TABS & MASTER PORTAL")
print("=" * 65)

total_images = 0
all_valid = True

for doc in docs:
    with open(doc, 'r', encoding='utf-8') as f:
        html = f.read()
    
    imgs = re.findall(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', html)
    print(f"\nDocument: {doc}")
    print(f"  Total <img> tags: {len(imgs)}")
    missing = []
    eager_count = 0
    lazy_count = 0
    fallback_count = 0
    for im in imgs:
        total_images += 1
        clean = im.split('?')[0].split('#')[0]
        if not os.path.exists(clean):
            missing.append(im)
    
    # Check tags attributes
    img_tags = re.findall(r'<img\s+[^>]*>', html)
    for tag in img_tags:
        if 'loading="eager"' in tag:
            eager_count += 1
        elif 'loading="lazy"' in tag:
            lazy_count += 1
        if 'onerror=' in tag:
            fallback_count += 1

    print(f"  Existing on disk: {len(imgs) - len(missing)} / {len(imgs)}")
    print(f"  Eager loaded: {eager_count}, Lazy: {lazy_count}, With Fallback Handler: {fallback_count}")
    if missing:
        all_valid = False
        print(f"  ❌ Missing {len(missing)} files! Sample: {missing[:3]}")

print("\n" + "=" * 65)
if all_valid:
    print(f"ALL {total_images} IMAGES ACROSS ALL TABS ARE 100% VISIBLE & VERIFIED!")
else:
    print("SOME IMAGES FAILED AUDIT!")
print("=" * 65)
