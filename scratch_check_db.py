import sys
import json
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

print("Total temples in coordinates DB:", len(mtc.COORDINATES_DB))

# Let's inspect the keys in the 7 extracted JSON files or builders:
# 1. adityas_extracted.json (12 + 1 hub)
# 2. bhairavs_extracted.json (11)
# 3. devis_extracted.json (32)
# 4. shiva_temples_extracted.json (23)
# 5. extract_10_ganesh_mirror_data.py -> ganeshs_extracted.json / 10 main ganesh
# 6. vishnu_temples_extracted.json (18 main + 12 additional = 30)
# 7. build_ganga_pdf.py (14 Ganga & Teerths)

categories = {
    'Adityas': [k for k in mtc.COORDINATES_DB if 'aditya' in k],
    'Bhairavs': [k for k in mtc.COORDINATES_DB if 'bhairav' in k],
    'Devis': [],
    'Shiva': [],
    'Ganesh': [k for k in mtc.COORDINATES_DB if 'vinayak' in k or 'ganesh' in k],
    'Vishnu': [],
    'Ganga/Teerths': []
}

for k, v in mtc.COORDINATES_DB.items():
    print(f"KEY: {k} -> {v['hindi']} ({v['lat']}, {v['lon']})")
