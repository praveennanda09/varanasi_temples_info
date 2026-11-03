import sys
import json
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

print("TESTING FULL 7-GUIDE COVERAGE IN COORDINATES DB")

# 1. Adityas
with open('adityas_extracted.json', 'r', encoding='utf-8') as f:
    adityas = json.load(f)
aditya_slugs = [x['id'] for x in adityas if x['id'] != 'hub']

# 2. Bhairavs
with open('bhairavs_extracted.json', 'r', encoding='utf-8') as f:
    bhairavs = json.load(f)
bhairav_slugs = [x['id'] for x in bhairavs if x['id'] != 'hub']

# 3. Devis
with open('devis_extracted.json', 'r', encoding='utf-8') as f:
    devis = json.load(f)
devi_slugs = [x['slug'] for x in devis]

# 4. Shiva
with open('shiva_temples_extracted.json', 'r', encoding='utf-8') as f:
    shiva_data = json.load(f)
shiva_items = shiva_data['main_shiva_temples'] + shiva_data['jyotirlinga_counterparts'] + shiva_data['celebrated_landmarks']

# 5. Ganesh
with open('ganesh_temples_extracted.json', 'r', encoding='utf-8') as f:
    ganesh_data = json.load(f)
ganesh_items = ganesh_data['main_10_ganesh_temples']

# 6. Vishnu
with open('vishnu_temples_extracted.json', 'r', encoding='utf-8') as f:
    vishnu_data = json.load(f)
vishnu_items = vishnu_data['main_18_vishnu_temples'] + vishnu_data['additional_vishnu_temples']

# 7. Ganga & Teerths
with open('ganga_teerths_extracted.json', 'r', encoding='utf-8') as f:
    ganga_items = json.load(f)

print(f"Target counts: Adityas={len(aditya_slugs)}, Bhairavs={len(bhairav_slugs)}, Devis={len(devi_slugs)}, Shiva={len(shiva_items)}, Ganesh={len(ganesh_items)}, Vishnu={len(vishnu_items)}, Ganga={len(ganga_items)}")
print(f"Total target temples: {len(aditya_slugs) + len(bhairav_slugs) + len(devi_slugs) + len(shiva_items) + len(ganesh_items) + len(vishnu_items) + len(ganga_items)}")
