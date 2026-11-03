# generate_all_7_maps.py
# Generates 7 ultra-high-resolution vector SVG pilgrimage maps matching the user's reference screenshot
# Features: River Ganga curve, Varanasi road grid, ॐ pin badges, Hindi/English labels, and collision avoidance

import os
import sys
import json
import math
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 65)
print("GENERATING 7 HIGH-RESOLUTION VECTOR PILGRIMAGE MAPS (SVG)")
print("=" * 65)

# Map Geographic Boundaries (Varanasi Pilgrimage Zone)
MIN_LON = 82.9500
MAX_LON = 83.0450
MIN_LAT = 25.2650
MAX_LAT = 25.3420

WIDTH = 1200
HEIGHT = 800
PAD_X = 60
PAD_Y = 60

def project(lat, lon):
    """Projects GPS coordinates into SVG canvas (x, y)"""
    x = PAD_X + ((lon - MIN_LON) / (MAX_LON - MIN_LON)) * (WIDTH - 2 * PAD_X)
    # Lat increases going North, so Y inverts
    y = PAD_Y + ((MAX_LAT - lat) / (MAX_LAT - MIN_LAT)) * (HEIGHT - 2 * PAD_Y)
    return round(x, 1), round(y, 1)

def build_base_map_svg():
    """Generates the background map features: River Ganga curve, highways, railway, city labels"""
    # River Ganga polyline through Varanasi (from Assi in south to Varuna Sangam in north)
    # Assi (25.290, 83.006) -> Kedar (25.300, 83.009) -> Dashashwamedh (25.307, 83.011) ->
    # Manikarnika (25.311, 83.014) -> Panchganga (25.317, 83.018) -> Trilochan (25.321, 83.022) ->
    # Rajghat / Varuna Sangam (25.329, 83.037) -> North East exit (25.342, 83.045)
    river_points = [
        (25.2650, 83.0020),
        (25.2750, 83.0035),
        (25.2850, 83.0050),
        (25.2905, 83.0065), # Assi Ghat
        (25.2996, 83.0092), # Kedar Ghat
        (25.3068, 83.0108), # Dashashwamedh Ghat
        (25.3108, 83.0140), # Manikarnika Ghat
        (25.3168, 83.0177), # Panchganga Ghat
        (25.3210, 83.0225), # Trilochan Ghat
        (25.3289, 83.0372), # Varuna Sangam
        (25.3350, 83.0420),
        (25.3420, 83.0450)
    ]
    
    # Project river left bank
    left_bank = [project(lat, lon) for lat, lon in river_points]
    
    # Create river polygon extending to the eastern boundary
    river_path_d = f"M {left_bank[0][0]},{left_bank[0][1]} "
    for pt in left_bank[1:]:
        river_path_d += f"L {pt[0]},{pt[1]} "
    river_path_d += f"L {WIDTH},{left_bank[-1][1]} L {WIDTH},{HEIGHT} L {left_bank[0][0]},{HEIGHT} Z"

    # Roads
    # NH 731B running across west
    r731_start = project(25.3150, 82.9500)
    r731_mid = project(25.3200, 82.9800)
    r731_end = project(25.3350, 83.0150)
    
    # DLW Road from south-west
    dlw_start = project(25.2700, 82.9650)
    dlw_mid = project(25.2950, 82.9750)
    dlw_end = project(25.3150, 82.9900)

    # Cantt Railway Station
    cantt_pt = project(25.3280, 82.9850)
    manduadih_pt = project(25.2950, 82.9700)
    city_station_pt = project(25.3350, 83.0120)

    svg_base = f"""
  <!-- Background Landmass -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#f8fafc" />
  
  <!-- Subtle Urban Grids -->
  <pattern id="urbanGrid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e2e8f0" stroke-width="0.75" opacity="0.6"/>
  </pattern>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#urbanGrid)" />

  <!-- Major Roadways -->
  <!-- NH 731B -->
  <path d="M {r731_start[0]},{r731_start[1]} Q {r731_mid[0]},{r731_mid[1]} {r731_end[0]},{r731_end[1]}" fill="none" stroke="#93c5fd" stroke-width="6" stroke-linecap="round" />
  <path d="M {r731_start[0]},{r731_start[1]} Q {r731_mid[0]},{r731_mid[1]} {r731_end[0]},{r731_end[1]}" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" />

  <!-- DLW Road -->
  <path d="M {dlw_start[0]},{dlw_start[1]} L {dlw_mid[0]},{dlw_mid[1]} L {dlw_end[0]},{dlw_end[1]}" fill="none" stroke="#cbd5e1" stroke-width="5" stroke-linecap="round" />
  <path d="M {dlw_start[0]},{dlw_start[1]} L {dlw_mid[0]},{dlw_mid[1]} L {dlw_end[0]},{dlw_end[1]}" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />

  <!-- Railway Line (Dashed) -->
  <path d="M {manduadih_pt[0]},{manduadih_pt[1]} L {cantt_pt[0]},{cantt_pt[1]} L {city_station_pt[0]},{city_station_pt[1]} L {project(25.3300, 83.0350)[0]},{project(25.3300, 83.0350)[1]}" fill="none" stroke="#64748b" stroke-width="3" stroke-dasharray="6,4" />

  <!-- River Ganga (Ganges) Waterbody -->
  <path d="{river_path_d}" fill="#bae6fd" stroke="#7dd3fc" stroke-width="2" />

  <!-- River Flow Label -->
  <g transform="translate({project(25.3000, 83.0250)[0]}, {project(25.3000, 83.0250)[1]}) rotate(-45)">
    <text fill="#0369a1" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" opacity="0.65" letter-spacing="4">RIVER GANGES • पवित्र गंगा</text>
  </g>

  <!-- Highway Badge 731B -->
  <g transform="translate({project(25.3210, 82.9720)[0]}, {project(25.3210, 82.9720)[1]})">
    <rect x="-18" y="-10" width="36" height="20" rx="4" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5" />
    <text x="0" y="4" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="800" fill="#713f12">731B</text>
  </g>

  <!-- DLW Rd Label -->
  <text x="{dlw_mid[0] + 12}" y="{dlw_mid[1]}" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748b" transform="rotate(75, {dlw_mid[0]}, {dlw_mid[1]})">DLW Rd</text>

  <!-- Varanasi City Landmark Label -->
  <g transform="translate({project(25.3230, 82.9800)[0]}, {project(25.3230, 82.9800)[1]})">
    <text x="0" y="0" font-family="'Segoe UI', 'Cinzel', serif" font-size="24" font-weight="800" fill="#0f172a">Varanasi</text>
    <text x="0" y="22" font-family="'Segoe UI', 'Nirmala UI', sans-serif" font-size="20" font-weight="700" fill="#334155">वाराणसी</text>
  </g>

  <!-- Railway Station Icons -->
  <g transform="translate({cantt_pt[0]}, {cantt_pt[1]})">
    <circle r="9" fill="#0284c7" />
    <text x="0" y="3.5" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="10" fill="#ffffff">&#128646;</text>
    <text x="12" y="3" font-family="'Segoe UI', sans-serif" font-size="9" font-weight="700" fill="#0369a1">Cantt Jn</text>
  </g>
  <g transform="translate({manduadih_pt[0]}, {manduadih_pt[1]})">
    <circle r="8" fill="#0284c7" />
    <text x="0" y="3" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="9" fill="#ffffff">&#128646;</text>
    <text x="12" y="3" font-family="'Segoe UI', sans-serif" font-size="8.5" font-weight="600" fill="#0369a1">Banaras Stn</text>
  </g>

  <!-- Map Scale & Copyright Bar (Matching Reference Screenshot) -->
  <g transform="translate({WIDTH - 280}, {HEIGHT - 25})">
    <rect x="-10" y="-16" width="280" height="32" rx="4" fill="#ffffff" opacity="0.9" stroke="#cbd5e1" stroke-width="1" />
    <text x="0" y="4" font-family="'Segoe UI', sans-serif" font-size="9.5" fill="#475569">Map data &#169;2026 Terms</text>
    <!-- 1 km Scale Bar -->
    <text x="175" y="4" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="700" fill="#1e293b">1 km</text>
    <line x1="205" y1="2" x2="255" y2="2" stroke="#1e293b" stroke-width="2.5" />
    <line x1="205" y1="-3" x2="205" y2="7" stroke="#1e293b" stroke-width="1.5" />
    <line x1="255" y1="-3" x2="255" y2="7" stroke="#1e293b" stroke-width="1.5" />
  </g>
"""
    return svg_base

def render_temple_pins_and_labels(temple_list, theme_color="#dc2626"):
    """
    Renders pins and 3-line callout cards matching the user's uploaded reference screenshot:
    - Teardrop circular pin with ॐ symbol
    - 3 lines of text: English Title, Devanagari Hindi, and Role Subtitle
    - Smart positioning to avoid overlapping in dense central Kashi
    """
    svg_elements = []
    
    # Sort temples by latitude descending (North to South)
    sorted_temples = sorted(temple_list, key=lambda t: t['lat'], reverse=True)
    
    # We will compute label anchors with alternating placement
    placed_boxes = []

    for idx, t in enumerate(sorted_temples):
        px, py = project(t['lat'], t['lon'])
        
        # Determine pin color (cycle through red, blue, purple, amber, emerald)
        pin_colors = [
            ("#dc2626", "#ef4444"), # Red
            ("#2563eb", "#3b82f6"), # Blue
            ("#7c3aed", "#8b5cf6"), # Purple
            ("#d97706", "#f59e0b"), # Amber
            ("#059669", "#10b981")  # Emerald
        ]
        dark_col, light_col = pin_colors[idx % len(pin_colors)]

        # Determine label offset to prevent collisions
        # In Varanasi, Ganga is to the East (right), so dense central shrines can branch right over the river
        # or left into the city
        is_even = (idx % 2 == 0)
        
        # Label card dimensions
        card_w = 215
        card_h = 44
        
        # Staggered offsets
        if px > 750: # Near Rajghat / River
            lx = px - card_w - 22
            ly = py - 18
        elif px < 400: # West Kashi (Manduadih, Pisachmochan)
            lx = px + 22
            ly = py - 18
        else: # Central Kashi (Vishwanath / Chowk / Ghats)
            # Alternate left and right, with vertical jitter
            v_jitter = ((idx % 3) - 1) * 14
            if is_even:
                lx = px + 24
                ly = py - 20 + v_jitter
            else:
                lx = px - card_w - 24
                ly = py - 20 + v_jitter

        # Clamp label inside canvas bounds
        lx = max(15, min(lx, WIDTH - card_w - 15))
        ly = max(20, min(ly, HEIGHT - card_h - 35))

        # Leader line from pin to label card
        leader_line = f"""
    <!-- Leader Line -->
    <path d="M {px},{py} Q {(px + lx + card_w/2)/2},{(py + ly + card_h/2)/2} {lx + (card_w/2 if px > lx and px < lx + card_w else (0 if px < lx else card_w))},{ly + card_h/2}" fill="none" stroke="{dark_col}" stroke-width="1.2" stroke-dasharray="3,2" opacity="0.75" />
"""

        # Map Pin Marker (Teardrop shape + Circular Om Badge)
        pin_marker = f"""
    <!-- Pin at ({px}, {py}) -->
    <g transform="translate({px}, {py})">
      <!-- Shadow -->
      <ellipse cx="0" cy="3" rx="7" ry="3" fill="#0f172a" opacity="0.25" />
      
      <!-- Teardrop Body -->
      <path d="M 0,0 C -8,-9 -11,-15 -11,-22 A 11,11 0 1,1 11,-22 C 11,-15 8,-9 0,0 Z" fill="{dark_col}" stroke="#ffffff" stroke-width="1.5" />
      
      <!-- Inner Circle for ॐ -->
      <circle cx="0" cy="-22" r="8" fill="#ffffff" />
      <text x="0" y="-18" text-anchor="middle" font-family="'Segoe UI', 'Nirmala UI', sans-serif" font-size="11" font-weight="800" fill="{dark_col}">&#2384;</text>
    </g>
"""

        # Truncate strings cleanly if necessary
        title_en = t['title']
        if len(title_en) > 28:
            title_en = title_en[:26] + "..."
            
        title_hi = t['hindi']
        if len(title_hi) > 32:
            title_hi = title_hi[:30] + "..."
            
        subtitle = t['subtitle']
        if len(subtitle) > 34:
            subtitle = subtitle[:32] + "..."

        # Callout Text Box (3 lines matching user screenshot)
        label_card = f"""
    <!-- Callout Card -->
    <g transform="translate({lx}, {ly})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="5" fill="#ffffff" opacity="0.94" stroke="{light_col}" stroke-width="1.2" filter="drop-shadow(0px 2px 4px rgba(0,0,0,0.15))" />
      <!-- Left Accent Line -->
      <rect x="0" y="0" width="4" height="{card_h}" rx="2" fill="{dark_col}" />
      <!-- Line 1: English Title -->
      <text x="10" y="13" font-family="'Segoe UI', Arial, sans-serif" font-size="9.5" font-weight="700" fill="#0f172a">{title_en}</text>
      <!-- Line 2: Devanagari Hindi -->
      <text x="10" y="26" font-family="'Segoe UI', 'Nirmala UI', sans-serif" font-size="8.5" font-weight="600" fill="#334155">{title_hi}</text>
      <!-- Line 3: Subtitle / Role -->
      <text x="10" y="38" font-family="'Segoe UI', Arial, sans-serif" font-size="8" font-style="italic" fill="#0284c7">{subtitle}</text>
    </g>
"""
        svg_elements.append(leader_line + pin_marker + label_card)

    return "\n".join(svg_elements)

def generate_svg_map(guide_title, guide_subtitle, temples, output_filename, theme_color="#dc2626"):
    """Compiles complete standalone SVG map"""
    base_svg = build_base_map_svg()
    pins_svg = render_temple_pins_and_labels(temples, theme_color)
    
    full_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="auto">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.2"/>
    </filter>
  </defs>

  {base_svg}

  <!-- Map Header Banner -->
  <g transform="translate(40, 35)">
    <rect x="-10" y="-16" width="420" height="48" rx="6" fill="#ffffff" opacity="0.95" stroke="#cbd5e1" stroke-width="1.2" filter="url(#shadow)" />
    <rect x="-10" y="-16" width="6" height="48" rx="3" fill="{theme_color}" />
    <text x="8" y="4" font-family="'Segoe UI', 'Cinzel', serif" font-size="14" font-weight="800" fill="#0f172a">{guide_title}</text>
    <text x="8" y="21" font-family="'Segoe UI', sans-serif" font-size="9.5" font-weight="600" fill="#64748b">{guide_subtitle} ({len(temples)} Verified Sanctums)</text>
  </g>

  <!-- Temple Pins & Callout Cards -->
  {pins_svg}

</svg>"""

    # Ensure output directories exist
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('Kashi_Exact_Offline_Website/assets/images', exist_ok=True)
    
    # Write to root assets
    root_path = os.path.join('assets/images', output_filename)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(full_svg)
        
    # Write to website assets
    web_path = os.path.join('Kashi_Exact_Offline_Website/assets/images', output_filename)
    with open(web_path, 'w', encoding='utf-8') as f:
        f.write(full_svg)
        
    print(f"  [+] Created: {root_path} & {web_path}")

# =========================================================================
# BUILD 7 MAPS
# =========================================================================

# 1. Dwadasa Adityas (12)
with open('adityas_extracted.json', 'r', encoding='utf-8') as f:
    adityas_data = json.load(f)
aditya_temples = []
for a in adityas_data:
    if a['id'] == 'hub': continue
    meta = mtc.get_coords_and_meta(a['id'])
    aditya_temples.append({
        'title': a['title'].split('.')[1].strip() if '.' in a['title'] else a['title'],
        'hindi': meta['hindi'],
        'subtitle': meta['subtitle'],
        'lat': meta['lat'],
        'lon': meta['lon']
    })
generate_svg_map(
    "KASHI DWADASHA ADITYAS MAP",
    "Twelve Sacred Solar Sanctums of Varanasi",
    aditya_temples,
    "Map_Dwadasa_Adityas.svg",
    "#dc2626"
)

# 2. Bhairav Temples (11)
with open('bhairavs_extracted.json', 'r', encoding='utf-8') as f:
    bhairavs_data = json.load(f)
bhairav_temples = []
for b in bhairavs_data:
    if b['id'] == 'hub': continue
    meta = mtc.get_coords_and_meta(b['id'])
    bhairav_temples.append({
        'title': b['title'],
        'hindi': meta['hindi'],
        'subtitle': meta['subtitle'],
        'lat': meta['lat'],
        'lon': meta['lon']
    })
# Add Bal Bhairav
meta_bal = mtc.get_coords_and_meta('bal-bhairav')
bhairav_temples.append({
    'title': 'Bal Bhairav Temple',
    'hindi': meta_bal['hindi'],
    'subtitle': meta_bal['subtitle'],
    'lat': meta_bal['lat'],
    'lon': meta_bal['lon']
})
generate_svg_map(
    "KASHI BHAIRAV TEMPLES MAP",
    "Ashta Bhairavas, Kaal Bhairav & Protective Sanctums",
    bhairav_temples,
    "Map_Bhairav_Temples.svg",
    "#7c3aed"
)

# 3. Devi Temples (32)
with open('devis_extracted.json', 'r', encoding='utf-8') as f:
    devis_data = json.load(f)
devi_temples = []
for d in devis_data:
    meta = mtc.get_coords_and_meta(d['slug'])
    devi_temples.append({
        'title': d['orig_title'],
        'hindi': meta['hindi'],
        'subtitle': meta['subtitle'],
        'lat': meta['lat'],
        'lon': meta['lon']
    })
generate_svg_map(
    "KASHI DEVI TEMPLES & DASGAMAHA VIDYA MAP",
    "Navadurgas, Navagauris, Shaktipeeths & Tantric Sanctums",
    devi_temples,
    "Map_Devi_Temples.svg",
    "#be123c"
)

# 4. Main Shiva Temples & Jyotirlingas (23)
with open('shiva_temples_extracted.json', 'r', encoding='utf-8') as f:
    shiva_data = json.load(f)
shiva_temples = []
for group in ['main_shiva_temples', 'jyotirlinga_counterparts', 'celebrated_landmarks']:
    for s in shiva_data[group]:
        t_title = s.get('title', s.get('canonical_name', ''))
        meta = mtc.get_coords_and_meta(t_title)
        shiva_temples.append({
            'title': t_title,
            'hindi': meta['hindi'],
            'subtitle': meta['subtitle'],
            'lat': meta['lat'],
            'lon': meta['lon']
        })
generate_svg_map(
    "KASHI MAIN SHIVA TEMPLES & JYOTIRLINGAS MAP",
    "Supreme Avimukta Mahalingas & Kashi Jyotirlinga Counterparts",
    shiva_temples,
    "Map_Main_Shiva_Temples.svg",
    "#1e40af"
)

# 5. Main Ganesh Temples (10)
with open('ganesh_temples_extracted.json', 'r', encoding='utf-8') as f:
    ganesh_data = json.load(f)
ganesh_temples = []
for g in ganesh_data['main_10_ganesh_temples']:
    t_title = g.get('title', g.get('canonical_name', ''))
    meta = mtc.get_coords_and_meta(t_title)
    ganesh_temples.append({
        'title': t_title,
        'hindi': meta['hindi'],
        'subtitle': meta['subtitle'],
        'lat': meta['lat'],
        'lon': meta['lon']
    })
generate_svg_map(
    "KASHI MAIN GANESH TEMPLES MAP",
    "The Ten Essential Vinayaka Sanctums of Kashi",
    ganesh_temples,
    "Map_Main_Ganesh_Temples.svg",
    "#d97706"
)

# 6. Main Vishnu Temples (30)
with open('vishnu_temples_extracted.json', 'r', encoding='utf-8') as f:
    vishnu_data = json.load(f)
vishnu_temples = []
for group in ['main_18_vishnu_temples', 'additional_vishnu_temples']:
    for v in vishnu_data[group]:
        t_title = v.get('title', v.get('canonical_name', ''))
        meta = mtc.get_coords_and_meta(t_title)
        vishnu_temples.append({
            'title': t_title,
            'hindi': meta['hindi'],
            'subtitle': meta['subtitle'],
            'lat': meta['lat'],
            'lon': meta['lon']
        })
generate_svg_map(
    "KASHI MAIN VISHNU TEMPLES MAP",
    "Eighteen Main Vishnu Manifestations & Additional Keshava Sanctums",
    vishnu_temples,
    "Map_Main_Vishnu_Temples.svg",
    "#0d9488"
)

# 7. Ganga & Sacred Teerths (14)
with open('ganga_teerths_extracted.json', 'r', encoding='utf-8') as f:
    ganga_data = json.load(f)
ganga_temples = []
for sec in ganga_data:
    meta = mtc.get_coords_and_meta(sec['title'])
    ganga_temples.append({
        'title': sec['title'],
        'hindi': meta['hindi'],
        'subtitle': meta['subtitle'],
        'lat': meta['lat'],
        'lon': meta['lon']
    })
generate_svg_map(
    "KASHI GANGA & SACRED TEERTHS MAP",
    "Holy River Ganga, Confluences, Sacred Kunds & Pushkarinis",
    ganga_temples,
    "Map_Ganga_and_Teerths.svg",
    "#0284c7"
)

print("\nALL 7 PILGRIMAGE MAPS GENERATED SUCCESSFULLY!")
