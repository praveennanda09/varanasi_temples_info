# sync_and_update_all_images.py
import os
import shutil
import json
import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("SYNCING & UPDATING ALL IMAGES FOR 100% VISIBILITY")
print("=" * 60)

mirror_img_dir = 'Kashi_Exact_Offline_Website/assets/images'
root_img_dir = 'assets/images'
os.makedirs(root_img_dir, exist_ok=True)

# 1. Sync all images between mirror_img_dir and root_img_dir
mirror_imgs = os.listdir(mirror_img_dir)
for f in mirror_imgs:
    src_f = os.path.join(mirror_img_dir, f)
    dst_f = os.path.join(root_img_dir, f)
    if not os.path.exists(dst_f):
        shutil.copy2(src_f, dst_f)

root_imgs = os.listdir(root_img_dir)
for f in root_imgs:
    src_f = os.path.join(root_img_dir, f)
    dst_f = os.path.join(mirror_img_dir, f)
    if not os.path.exists(dst_f):
        shutil.copy2(src_f, dst_f)

print(f"Total synced images in mirror_img_dir: {len(os.listdir(mirror_img_dir))}")
print(f"Total synced images in root_img_dir:   {len(os.listdir(root_img_dir))}")

# 2. Mapping of the 8 temples to their newly created sacred SVG artwork
svg_map = {
    'varahi_devi': ('assets/images/Varahi-Devi-Shrine.svg', 'Sacred Iconographic Representation of Varahi Devi (Kashi Sanctum)'),
    'tri_lokya_sundary': ('assets/images/Tri-Lokya-Sundary-Shrine.svg', 'Sacred Iconographic Representation of Tri Lokya Sundari (Kashi Sanctum)'),
    'dhundhi_vinayak': ('assets/images/Dhundhi-Vinayak-Shrine.svg', 'Sacred Iconographic Representation of Dhundhi Vinayak (Kashi Sanctum)'),
    'siddhi_vinayak': ('assets/images/Siddhi-Vinayak-Shrine.svg', 'Sacred Iconographic Representation of Siddhi Vinayak (Kashi Sanctum)'),
    'avi_mukta_vinayak': ('assets/images/Avi-Mukta-Vinayak-Shrine.svg', 'Sacred Iconographic Representation of Avi Mukta Vinayak (Kashi Sanctum)'),
    'gyan_madhav': ('assets/images/Gyan-Madhav-Shrine.svg', 'Sacred Iconographic Representation of Gyan Madhav (Kashi Sanctum)'),
    'gopi_govind': ('assets/images/Gopi-Govind-Shrine.svg', 'Sacred Iconographic Representation of Gopi Govind (Kashi Sanctum)'),
    'vitank_narsimha': ('assets/images/Vitank-Narsimha-Shrine.svg', 'Sacred Iconographic Representation of Vitank Narsimha (Kashi Sanctum)'),
}

# 3. Update temples_master.json
with open('temples_master.json', 'r', encoding='utf-8') as f:
    temples = json.load(f)

updated_count = 0
for t in temples:
    tid = t.get('id')
    if tid in svg_map:
        t['local_photo_path'] = svg_map[tid][0]
        t['photo_caption'] = svg_map[tid][1]
        t['original_photo_url'] = f"https://varanasitemples.in/artwork/{os.path.basename(svg_map[tid][0])}"
        updated_count += 1

with open('temples_master.json', 'w', encoding='utf-8') as f:
    json.dump(temples, f, indent=2, ensure_ascii=False)
print(f"Updated {updated_count} temples in temples_master.json with dedicated sacred artwork.")

# 4. Update temples_master.csv
if temples:
    fieldnames = list(temples[0].keys())
    with open('temples_master.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(temples)
print("Updated temples_master.csv.")

# 5. Function to update temple cards in the 6 guides
guides = [
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html'
]

for g in guides:
    with open(g, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 5a. Replace any missing photo notices for our 8 temples
    for tid, (svg_rel_path, caption) in svg_map.items():
        matching_t = next((t for t in temples if t.get('id') == tid), None)
        if not matching_t:
            continue
        cname = matching_t['canonical_name']
        
        # Check if this guide contains this temple
        if cname.lower() in html.lower():
            # Match the card containing this title and the red notice
            # Pattern: <div class="temple-card"[^>]*> ... <div class="temple-title">Canonical Name</div> ... <div style="background:#fef2f2; ... </div>
            card_pat = re.compile(
                rf'(<div class="temple-card"[^>]*>[\s\S]*?<div class="temple-title">{re.escape(cname)}</div>[\s\S]*?)'
                rf'(<div style="background:#fef2f2;[\s\S]*?Photo notice:[\s\S]*?</div>)',
                re.I
            )
            replacement_img = f'''
        <div class="temple-img-container">
          <img class="temple-img" 
               src="Kashi_Exact_Offline_Website/{svg_rel_path}" 
               alt="{cname}" 
               loading="eager"
               onerror="if(!this.dataset.retried){{this.dataset.retried=1; this.src='{svg_rel_path}';}}">
          <div class="img-caption">&#128330; {caption}</div>
        </div>'''
            if card_pat.search(html):
                html = card_pat.sub(rf'\1{replacement_img}', html)
                print(f"  Inserted visual in {g} for {cname}")

    # 5b. Enhance ALL existing <img> tags across the guide
    def img_enhancer(m):
        full_tag = m.group(0)
        # Ensure loading="eager" (not lazy)
        if 'loading="lazy"' in full_tag:
            full_tag = full_tag.replace('loading="lazy"', 'loading="eager"')
        elif 'loading=' not in full_tag:
            full_tag = full_tag.replace('class="temple-img"', 'class="temple-img" loading="eager"')
        # Ensure fallback onerror
        if 'onerror=' not in full_tag:
            # Insert onerror before the closing >
            full_tag = re.sub(
                r'(\s*/?>)$',
                r' onerror="if(!this.dataset.retried){this.dataset.retried=1; this.src=\'assets/images/\' + this.src.split(\'/\').pop();}" \1',
                full_tag
            )
        return full_tag

    html = re.sub(r'<img\s+[^>]*class=[\'"]temple-img[\'"][^>]*>', img_enhancer, html)
    
    with open(g, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Enhanced images in {g}")

print("\nSUCCESS: All 6 deity guides successfully updated!")
