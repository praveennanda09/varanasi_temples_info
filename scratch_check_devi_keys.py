import sys
import json
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

with open('devis_extracted.json', 'r', encoding='utf-8') as f:
    devis = json.load(f)

print(f"Total devis: {len(devis)}")
for i, d in enumerate(devis):
    orig = d['orig_title']
    slug = d['slug']
    # Check if key exists in mtc.COORDINATES_DB
    found_key = None
    if slug in mtc.COORDINATES_DB:
        found_key = slug
    else:
        for k in mtc.COORDINATES_DB:
            k_norm = k.replace('-', '').replace('_', '').lower()
            slug_norm = slug.replace('-', '').replace('_', '').lower()
            if k_norm in slug_norm or slug_norm in k_norm:
                found_key = k
                break
    
    if found_key:
        entry = mtc.COORDINATES_DB[found_key]
        print(f"#{i+1}: {orig} (slug: {slug}) -> Found: {found_key} | {entry['hindi']} ({entry['lat']}, {entry['lon']})")
    else:
        print(f"#{i+1}: {orig} (slug: {slug}) -> NOT FOUND in DB!")
