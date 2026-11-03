import sys
import json
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("INSPECTING DATASETS AND MAPPING TO COORDINATES_DB")
print("=" * 60)

db = mtc.COORDINATES_DB

def match_key(title, category=""):
    title_clean = title.lower().replace('-', ' ').replace('_', ' ')
    # Try direct match
    for k in db:
        k_clean = k.lower().replace('-', ' ').replace('_', ' ')
        if k_clean in title_clean or all(w in title_clean for w in k_clean.split()):
            return k
    # Partial word matching
    for k in db:
        words = [w for w in k.lower().split('-') if len(w) > 3]
        if words and all(w in title_clean for w in words):
            return k
    return None

# 1. Adityas
with open('adityas_extracted.json', 'r', encoding='utf-8') as f:
    adityas = json.load(f)
print(f"\n1. DWADASA ADITYAS ({len(adityas)} items):")
for item in adityas:
    aid = item.get('id', '')
    title = item.get('title', '')
    k = match_key(aid) or match_key(title)
    coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
    print(f"  [{aid}] -> Key: {k} {coords}")

# 2. Bhairavs
with open('bhairavs_extracted.json', 'r', encoding='utf-8') as f:
    bhairavs = json.load(f)
print(f"\n2. BHAIRAVS ({len(bhairavs)} items):")
for item in bhairavs:
    bid = item.get('id', '')
    title = item.get('title', '')
    k = match_key(bid) or match_key(title)
    coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
    print(f"  [{bid}] {title} -> Key: {k} {coords}")

# 3. Devis
with open('devis_extracted.json', 'r', encoding='utf-8') as f:
    devis = json.load(f)
print(f"\n3. DEVIS ({len(devis)} items):")
for i, item in enumerate(devis):
    title = item.get('title', '')
    cat = item.get('category', '')
    k = match_key(title, cat)
    coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
    print(f"  #{i+1} {title} ({cat}) -> Key: {k} {coords}")

# 4. Shiva
with open('shiva_temples_extracted.json', 'r', encoding='utf-8') as f:
    sdata = json.load(f)
print(f"\n4. SHIVA TEMPLES:")
for cat_name in ['main_shiva_temples', 'jyotirlinga_counterparts', 'celebrated_landmarks']:
    print(f"  -- {cat_name} ({len(sdata[cat_name])}):")
    for t in sdata[cat_name]:
        title = t.get('name', t.get('title', ''))
        k = match_key(title)
        coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
        print(f"     {title} -> Key: {k} {coords}")

# 5. Ganesh
with open('ganesh_temples_extracted.json', 'r', encoding='utf-8') as f:
    gdata = json.load(f)
print(f"\n5. GANESH TEMPLES ({len(gdata['main_10_ganesh_temples'])}):")
for t in gdata['main_10_ganesh_temples']:
    title = t.get('name', t.get('title', ''))
    k = match_key(title)
    coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
    print(f"     {title} -> Key: {k} {coords}")

# 6. Vishnu
with open('vishnu_temples_extracted.json', 'r', encoding='utf-8') as f:
    vdata = json.load(f)
print(f"\n6. VISHNU TEMPLES (18 Main + 12 Additional):")
for cat_name in ['main_18_vishnu_temples', 'additional_vishnu_temples']:
    print(f"  -- {cat_name} ({len(vdata[cat_name])}):")
    for t in vdata[cat_name]:
        title = t.get('name', t.get('title', ''))
        k = match_key(title)
        coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
        print(f"     {title} -> Key: {k} {coords}")

# 7. Ganga & Teerths
with open('ganga_teerths_extracted.json', 'r', encoding='utf-8') as f:
    gngdata = json.load(f)
print(f"\n7. GANGA & TEERTHS ({len(gngdata)}):")
for sec in gngdata:
    title = sec.get('title', sec.get('section_title', ''))
    k = match_key(title)
    coords = f"({db[k]['lat']}, {db[k]['lon']})" if k and k in db else "MISSING"
    print(f"     {title} -> Key: {k} {coords}")
