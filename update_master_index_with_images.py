# update_master_index_with_images.py
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Updating Kashi_Pilgrimage_Master_Index.html with Image column...")

with open('temples_master.json', 'r', encoding='utf-8') as f:
    temples = json.load(f)

temples_sorted = sorted(temples, key=lambda x: x['canonical_name'])

with open('Kashi_Pilgrimage_Master_Index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update masterTable <thead> to include <th>Image</th>
old_thead = r'<thead>\s*<tr>\s*<th>Temple Name</th>'
new_thead = '<thead>\n        <tr>\n          <th style="width:65px; text-align:center;">Image</th>\n          <th>Temple Name</th>'

html = re.sub(old_thead, new_thead, html)

# 2. Rebuild the tbody rows
rows_html = []
for t in temples_sorted:
    cname = t['canonical_name']
    cname_clean = cname.replace('\'', '&apos;')
    cat = t['deity_category']
    zone = t['geographic_zone']
    zone_clean = zone.split('—')[0].split('-')[0].strip() if '—' in zone else zone.split('-')[0].strip()
    zone_class = "other"
    if "North" in zone: zone_class = "north"
    elif "South" in zone: zone_class = "south"
    elif "East" in zone: zone_class = "east"
    elif "West" in zone: zone_class = "west"

    guide_file = {
        'Surya': '01_Surya_Dwadasa_Aditya.html',
        'Bhairav': '02_Bhairav_Temples.html',
        'Devi': '03_Devi_and_Dashamaha_Vidya.html',
        'Shiva': '04_Shiva_and_Kashi_Jyotirlingas.html',
        'Vinayaka': '05_Vinayaka_Temples.html',
        'Vishnu': '06_Vishnu_Temples.html'
    }.get(cat, '01_Surya_Dwadasa_Aditya.html')

    photo_path = t.get('local_photo_path', '')
    if not photo_path or photo_path == 'None':
        photo_path = 'assets/images/0.gif'

    img_html = f'''<td style="text-align:center; vertical-align:middle; width:65px; padding:6px;">
            <img src="Kashi_Exact_Offline_Website/{photo_path}" 
                 alt="{cname_clean}" 
                 style="width:52px; height:52px; object-fit:cover; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.15); display:block; margin:0 auto;" 
                 loading="eager"
                 onerror="if(!this.dataset.retried){{this.dataset.retried=1; this.src='{photo_path}';}}">
          </td>'''

    row = f'''        <tr data-zone="{zone}">
          {img_html}
          <td><strong>{cname}</strong><br><span style="font-size:0.75rem; color:#6b7280;">{t['associated_form']}</span></td>
          <td><span class="badge" style="background:#fee2e2; color:#991b1b;">{cat}</span></td>
          <td><span class="badge badge-zone-{zone_class}">{zone_clean}</span></td>
          <td style="font-size:0.82rem;">{t['address'][:80]}</td>
          <td><a class="btn-link btn-live" href="{guide_file}">View Guide &#8594;</a></td>
          <td><a class="btn-link btn-mirror" href="{t['local_mirror_url']}">Mirror &#8599;</a></td>
        </tr>'''
    rows_html.append(row)

# Replace tbody contents in masterTable
tbody_pattern = re.compile(r'(<table class="itinerary-table" id="masterTable">[\s\S]*?<tbody>)[\s\S]*?(</tbody>)', re.I)
replacement = r'\1\n' + '\n'.join(rows_html) + r'\n      \2'

html = tbody_pattern.sub(replacement, html)

with open('Kashi_Pilgrimage_Master_Index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"SUCCESS: Kashi_Pilgrimage_Master_Index.html updated with {len(rows_html)} image-populated rows!")
