# extract_all_shiva_mirror_data.py
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("EXTRACTING ALL MAIN SHIVA TEMPLES, JYOTIRLINGAS & OTHER SHIVA INVENTORY")
print("=" * 70)

BASE_DIR = 'Kashi_Exact_Offline_Website'

# Master temple details if needed for fallback
master_by_slug = {}
if os.path.exists('temples_master.json'):
    with open('temples_master.json', 'r', encoding='utf-8') as f:
        for t in json.load(f):
            slug = t.get('local_mirror_url', '').replace('/index.html', '').split('/')[-1]
            if slug:
                master_by_slug[slug] = t

def parse_temple_page(rel_path, category_label, designation):
    full_path = os.path.join(BASE_DIR, rel_path, 'index.html')
    if not os.path.exists(full_path):
        print(f"  [MISSING] {full_path}")
        return None

    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Title extraction
    t_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    raw_title = t_m.group(1).strip() if t_m else os.path.basename(rel_path).replace('-', ' ').title()
    title = re.sub(r'\s*-\s*Varanasi Temples.*', '', raw_title, flags=re.IGNORECASE).strip()

    # Post content extraction: between art-PostContent and art-sidebar1
    s_idx = html.find('class="art-PostContent"')
    if s_idx == -1:
        s_idx = html.find('class="art-article"')
    if s_idx == -1:
        s_idx = 0

    e_idx = html.find('class="art-sidebar1"', s_idx)
    if e_idx == -1:
        e_idx = html.find('class="art-Footer"', s_idx)
    if e_idx == -1:
        e_idx = len(html)

    post_html = html[s_idx:e_idx]

    # Extract all images inside post
    raw_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', post_html)
    valid_imgs = []
    seen_img = set()
    for src in raw_imgs:
        if any(skip in src.lower() for skip in ['hit-counter', 'gravatar', 'wp-includes', 'pixel', 'logo', 'button', 'banner', 'ad-']):
            continue
        if src.lower().endswith('.gif'):
            continue
        
        clean_src = src.split('?')[0]
        basename = os.path.basename(clean_src)
        if basename in seen_img:
            continue
        seen_img.add(basename)

        # Check local paths
        cand1 = os.path.join('assets', 'images', basename)
        cand2 = os.path.join(BASE_DIR, 'assets', 'images', basename)
        
        local_path = None
        if os.path.exists(cand1):
            local_path = cand1.replace('\\', '/')
        elif os.path.exists(cand2):
            local_path = cand2.replace('\\', '/')
        else:
            local_path = f"assets/images/{basename}"

        # Try to find caption or alt
        alt_m = re.search(r'<img[^>]+src=[\'"]' + re.escape(src) + r'[\'"][^>]+alt=[\'"]([^\'"]*)[\'"]', post_html)
        alt = alt_m.group(1).strip() if alt_m else basename

        valid_imgs.append({
            'original_src': src,
            'basename': basename,
            'local_path': local_path,
            'caption': alt or title
        })

    # Sanskrit verses in Devanagari script
    devanagari_blocks = []
    # Match contiguous Devanagari blocks
    for block in re.findall(r'[\u0900-\u097F\s\.,;:!\?\-\|॥।\(\)\']{12,}', post_html):
        clean_v = block.strip()
        # Count actual Devanagari characters
        dev_chars = len(re.findall(r'[\u0900-\u097F]', clean_v))
        if dev_chars >= 12:
            # check not already included
            if clean_v not in devanagari_blocks:
                devanagari_blocks.append(clean_v)

    # YouTube links
    yt_links = re.findall(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)', post_html)
    yt_urls = list(dict.fromkeys([f"https://www.youtube.com/watch?v={vid}" for vid in yt_links]))

    # Google Maps links
    maps_links = list(dict.fromkeys(re.findall(r'https?://(?:maps\.google\.com|goo\.gl/maps|maps\.app\.goo\.gl)/[^\s"\'<>]+', post_html)))

    # Location text
    location_text = ""
    loc_m = re.search(r'<strong>\s*(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF SHIVALING|LOCATION OF LINGA|LOCATION|WHERE TO FIND)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
    if loc_m:
        location_text = re.sub(r'<[^>]+>', ' ', loc_m.group(1)).strip()
        location_text = re.sub(r'\s+', ' ', location_text)
    else:
        # plain text search
        clean_all = re.sub(r'<[^>]+>', '\n', post_html)
        s_loc = re.search(r'(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF SHIVALING|LOCATION OF LINGA|LOCATION).*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|TIMINGS|POOJA|$)', clean_all, re.DOTALL | re.IGNORECASE)
        if s_loc:
            location_text = s_loc.group(1).strip()
            location_text = re.sub(r'\s+', ' ', location_text)

    # Darshan & Pooja Timings text
    timings_text = ""
    t_m = re.search(r'<strong>\s*(?:TYPES OF POOJA|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|POOJA|TIMINGS)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
    if t_m:
        timings_text = re.sub(r'<[^>]+>', ' ', t_m.group(1)).strip()
        timings_text = re.sub(r'\s+', ' ', timings_text)
    else:
        clean_all = re.sub(r'<[^>]+>', '\n', post_html)
        s_tim = re.search(r'(?:TYPES OF POOJA|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|TIMINGS).*?\n(.*?)(?:\n\s*\n|$)', clean_all, re.DOTALL | re.IGNORECASE)
        if s_tim:
            timings_text = s_tim.group(1).strip()
            timings_text = re.sub(r'\s+', ' ', timings_text)

    # Clean body paragraphs (preserve complete article text)
    raw_paras = re.split(r'</p>|<br\s*/?>\s*<br\s*/?>', post_html, flags=re.IGNORECASE)
    paragraphs = []
    for p in raw_paras:
        clean_p = re.sub(r'<[^>]+>', ' ', p).strip()
        clean_p = re.sub(r'&nbsp;', ' ', clean_p)
        clean_p = re.sub(r'&amp;', '&', clean_p)
        clean_p = re.sub(r'\s+', ' ', clean_p)
        if len(clean_p) > 10 and not clean_p.startswith('&#128740;') and not 'Varanasi Temples &raquo;' in clean_p and not 'COPY PROTECTED' in clean_p:
            paragraphs.append(clean_p)

    return {
        'id': os.path.basename(rel_path).replace('-', '_'),
        'slug': os.path.basename(rel_path),
        'title': title,
        'category_label': category_label,
        'designation': designation,
        'rel_path': rel_path,
        'original_url': f"https://varanasitemples.in/{rel_path}/",
        'images': valid_imgs,
        'sanskrit_verses': devanagari_blocks,
        'youtube_urls': yt_urls,
        'google_maps_urls': maps_links,
        'location_text': location_text,
        'timings_text': timings_text,
        'paragraphs': paragraphs
    }

# 1. THE 9 CANONICAL MAIN SHIVA TEMPLES
main_shiva_specs = [
    ('category/shiva-temples/main-shiva-temples/visweshwar-vishwanath', 'Main Shiva Temple', 'Supreme Sovereign of Kashi & Jyotirlinga #7 (Golden Temple)'),
    ('category/shiva-temples/main-shiva-temples/mrityunjay-mahadev', 'Main Shiva Temple', 'The Conqueror of Death (Amrit Kupa Well Sanctum)'),
    ('category/shiva-temples/main-shiva-temples/omkareshwar', 'Main Shiva Temple', 'Primordial Pranava Linga & Omkareshwar Jyotirlinga Counterpart'),
    ('category/shiva-temples/main-shiva-temples/krithi-vaseshwar', 'Main Shiva Temple', 'Slayer of Demon Gajasura (Avimukta Maha-Linga)'),
    ('category/shiva-temples/main-shiva-temples/kedareshwar', 'Main Shiva Temple', 'Sovereign of Kedar Khanda & Kedarnath Jyotirlinga Counterpart'),
    ('category/shiva-temples/main-shiva-temples/dharmeshwar', 'Main Shiva Temple', 'Sanctum Established by Dharmaraja Yama (Mirzapur Ghat)'),
    ('category/shiva-temples/main-shiva-temples/vridha-kalelshwar', 'Main Shiva Temple', 'Vriddha Kaleshwar — Conqueror of Aging and Time'),
    ('category/shiva-temples/main-shiva-temples/atma-veereshwar', 'Main Shiva Temple', 'Sanctum Established by Maharishi Vishwamitra'),
    ('category/shiva-temples/main-shiva-temples/gabhasteeshwar', 'Main Shiva Temple', 'Sanctum Established by Surya Bhagwan (Mayukh Aditya)')
]

# 2. PAN-INDIA JYOTIRLINGA COUNTERPARTS IN KASHI
jyotirlinga_specs = [
    ('category/shiva-temples/other-shiva-temples-s-y/someshwar', 'Kashi Jyotirlinga Counterpart', 'Somnath Jyotirlinga Counterpart (Man Mandir Ghat)'),
    ('category/shiva-temples/other-shiva-temples-s-y/tripurantakeshwar', 'Kashi Jyotirlinga Counterpart', 'Mallikarjuna & Grishneshwar Counterpart (Sigra / Kamakhya)'),
    ('category/shiva-temples/other-shiva-temples-l-r/mahakaleshwar', 'Kashi Jyotirlinga Counterpart', 'Mahakaleshwar Ujjain Counterpart (Daranagar)'),
    ('category/shiva-temples/other-shiva-temples-a-d/bheemeshwar', 'Kashi Jyotirlinga Counterpart', 'Bhimashankar Counterpart (Kashi Karvat Temple)'),
    ('category/shiva-temples/other-shiva-temples-e-k/ganeshwar-rameshwar', 'Kashi Jyotirlinga Counterpart', 'Rameshwaram Counterpart (Man Mandir Ghat)'),
    ('category/shiva-temples/other-shiva-temples-l-r/nageshwar', 'Kashi Jyotirlinga Counterpart', 'Nageshwar Jyotirlinga Counterpart (Bhonsla Ghat)'),
    ('category/shiva-temples/other-shiva-temples-e-k/karkotak-nageshwar', 'Kashi Jyotirlinga Counterpart', 'Karkotak Nageshwar (Naga King Karkotak Sanctum)'),
    ('category/shiva-temples/other-shiva-temples-s-y/triambakeshwar', 'Kashi Jyotirlinga Counterpart', 'Trimbakeshwar Nashik Counterpart (Godowlia)')
]

# 3. HIGH CELEBRITY / SCRIPTURAL LANDMARK SHIVA SHRINES
landmark_specs = [
    ('category/shiva-temples/other-shiva-temples-s-y/trilochan', 'Celebrated Shiva Sanctum', 'The Three-Eyed Lord Mahadev (Trilochan Ghat)'),
    ('category/shiva-temples/other-shiva-temples-a-d/aadi-mahadev', 'Celebrated Shiva Sanctum', 'Primordial Linga of Kashi Kshetra (Trilochan Locality)'),
    ('category/shiva-temples/other-shiva-temples-e-k/kardhameshwar', 'Celebrated Shiva Sanctum', 'First Station of the Sacred Panchkroshi Pilgrimage (Kandwa)'),
    ('category/shiva-temples/other-shiva-temples-l-r/markandeyshwar', 'Celebrated Shiva Sanctum', 'Shrine Where Markandeya Rishi Conquered Death'),
    ('category/shiva-temples/other-shiva-temples-l-r/ratneshwar', 'Celebrated Shiva Sanctum', 'The Iconic Leaning Temple of Manikarnika Ghat'),
    ('category/shiva-temples/other-shiva-temples-l-r/pasupateshwar', 'Celebrated Shiva Sanctum', 'Pashupatinath of Nepal Counterpart in Kashi')
]

print("1. Extracting 9 Main Shiva Temples...")
main_temples = []
for p, cat, des in main_shiva_specs:
    res = parse_temple_page(p, cat, des)
    if res:
        main_temples.append(res)
        print(f"   [+] {res['title']} -> {len(res['images'])} imgs, {len(res['paragraphs'])} paras, {len(res['sanskrit_verses'])} verses")

print(f"\n2. Extracting {len(jyotirlinga_specs)} Jyotirlinga Counterparts...")
jyotirlingas = []
for p, cat, des in jyotirlinga_specs:
    res = parse_temple_page(p, cat, des)
    if res:
        jyotirlingas.append(res)
        print(f"   [+] {res['title']} -> {len(res['images'])} imgs, {len(res['paragraphs'])} paras, {len(res['sanskrit_verses'])} verses")

print(f"\n3. Extracting {len(landmark_specs)} Celebrated Landmark Shiva Shrines...")
landmarks = []
for p, cat, des in landmark_specs:
    res = parse_temple_page(p, cat, des)
    if res:
        landmarks.append(res)
        print(f"   [+] {res['title']} -> {len(res['images'])} imgs, {len(res['paragraphs'])} paras, {len(res['sanskrit_verses'])} verses")

# 4. EXTRACT ALL OTHER SHIVA TEMPLES INTO DEDICATED SEPARATE DIRECTORY / INVENTORY
print("\n4. Extracting Complete Directory of All Other Shiva Temples...")
already_featured = set([t['slug'] for t in main_temples + jyotirlingas + landmarks])

other_groups = [
    ('other-shiva-temples-a-d', 'A to D'),
    ('other-shiva-temples-e-k', 'E to K'),
    ('other-shiva-temples-l-r', 'L to R'),
    ('other-shiva-temples-s-y', 'S to Y')
]

other_directory = []
for grp, section_label in other_groups:
    grp_dir = os.path.join(BASE_DIR, 'category', 'shiva-temples', grp)
    if not os.path.exists(grp_dir):
        continue
    for sub in sorted(os.listdir(grp_dir)):
        if sub in ['feed', 'page'] or sub in already_featured:
            continue
        sub_path = os.path.join(grp_dir, sub)
        if not os.path.isdir(sub_path):
            continue
        page_file = os.path.join(sub_path, 'index.html')
        if not os.path.exists(page_file):
            continue
        
        with open(page_file, 'r', encoding='utf-8', errors='ignore') as pf:
            p_html = pf.read()
        
        # Title
        t_m = re.search(r'<title>(.*?)</title>', p_html, re.IGNORECASE)
        raw_t = t_m.group(1).strip() if t_m else sub.replace('-', ' ').title()
        title = re.sub(r'\s*-\s*Varanasi Temples.*', '', raw_t, flags=re.IGNORECASE).strip()
        
        # Location
        loc = "Refer to shrine article"
        loc_m = re.search(r'<strong>\s*(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION|WHERE TO FIND)[^<]*</strong>(.*?)(?:<strong>|$)', p_html, re.DOTALL | re.IGNORECASE)
        if loc_m:
            loc = re.sub(r'<[^>]+>', ' ', loc_m.group(1)).strip()
        else:
            clean_t = re.sub(r'<[^>]+>', '\n', p_html)
            s_loc = re.search(r'(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF SHIVALING|LOCATION).*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|POOJA|TIMINGS|$)', clean_t, re.IGNORECASE)
            if s_loc:
                loc = s_loc.group(1).strip()
        loc = re.sub(r'\s+', ' ', loc)[:220]
        
        # YouTube
        yt_m = re.findall(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)', p_html)
        yt_url = f"https://www.youtube.com/watch?v={yt_m[0]}" if yt_m else ""
        
        # Has local image
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', p_html)
        valid_i = [i for i in imgs if not i.endswith('.gif') and not 'hit-counter' in i and 'uploads' in i]
        
        other_directory.append({
            'slug': sub,
            'title': title,
            'section': section_label,
            'location': loc,
            'has_photo': len(valid_i) > 0,
            'photo_file': os.path.basename(valid_i[0]) if valid_i else '',
            'youtube_url': yt_url,
            'mirror_path': f"category/shiva-temples/{grp}/{sub}/index.html",
            'original_url': f"https://varanasitemples.in/category/shiva-temples/{grp}/{sub}/"
        })

print(f"Total other Shiva temples cataloged in Directory: {len(other_directory)}")

# Save to shiva_temples_extracted.json
full_payload = {
    'summary': {
        'main_shiva_count': len(main_temples),
        'jyotirlinga_count': len(jyotirlingas),
        'landmarks_count': len(landmarks),
        'other_directory_count': len(other_directory),
        'total_shiva_shrines': len(main_temples) + len(jyotirlingas) + len(landmarks) + len(other_directory)
    },
    'main_shiva_temples': main_temples,
    'jyotirlinga_counterparts': jyotirlingas,
    'celebrated_landmarks': landmarks,
    'other_shiva_directory': other_directory
}

with open('shiva_temples_extracted.json', 'w', encoding='utf-8') as out_f:
    json.dump(full_payload, out_f, indent=2, ensure_ascii=False)

print("\nSuccessfully written 'shiva_temples_extracted.json'!")
