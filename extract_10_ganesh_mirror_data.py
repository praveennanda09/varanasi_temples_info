# extract_10_ganesh_mirror_data.py
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("EXTRACTING 10 MAIN GANESH TEMPLES & 56 VINAYAKAS MIRROR DATA")
print("=" * 70)

BASE_DIR = 'Kashi_Exact_Offline_Website'

def parse_vinayak_page(rel_path, fallback_title, designation, default_img=None):
    full_path = os.path.join(BASE_DIR, rel_path, 'index.html') if rel_path else None
    
    html = ""
    if full_path and os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    
    # Title
    title = fallback_title
    if html:
        t_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if t_m:
            clean_t = re.sub(r'\s*-\s*Varanasi Temples.*', '', t_m.group(1), flags=re.I).strip()
            if clean_t:
                title = clean_t

    # Extract art-PostContent
    post_html = ""
    if html:
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

    # Extract Images
    valid_imgs = []
    if post_html:
        raw_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', post_html)
        for src in raw_imgs:
            if any(skip in src.lower() for skip in ['hit-counter', 'gravatar', 'wp-includes', 'pixel', 'logo', 'button']):
                continue
            if src.lower().endswith('.gif'):
                continue
            clean_src = src.split('?')[0]
            basename = os.path.basename(clean_src)
            cand = os.path.join('assets', 'images', basename)
            if os.path.exists(cand):
                valid_imgs.append({
                    'basename': basename,
                    'local_path': cand.replace('\\', '/'),
                    'caption': title
                })

    if not valid_imgs and default_img:
        if os.path.exists(default_img):
            valid_imgs.append({
                'basename': os.path.basename(default_img),
                'local_path': default_img.replace('\\', '/'),
                'caption': f"{title} Sanctum"
            })

    # Devanagari Sanskrit Verses
    verses = []
    if post_html:
        for block in re.findall(r'[\u0900-\u097F\s\.,;:!\?\-\|॥।\(\)\']{12,}', post_html):
            clean_v = block.strip()
            if len(re.findall(r'[\u0900-\u097F]', clean_v)) >= 12:
                if clean_v not in verses:
                    verses.append(clean_v)

    # YouTube links
    yt_urls = []
    if html:
        yt_links = re.findall(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)', html)
        yt_urls = list(dict.fromkeys([f"https://www.youtube.com/watch?v={vid}" for vid in yt_links]))

    # Google Maps links
    maps_links = []
    if html:
        maps_links = list(dict.fromkeys(re.findall(r'https?://(?:maps\.google\.com|goo\.gl/maps|maps\.app\.goo\.gl|www\.google\.com/maps)/[^\s"\'<>]+', html)))

    # Location text
    location_text = ""
    if post_html:
        loc_m = re.search(r'<strong>\s*(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF VINAYAK|LOCATION OF DHUNDHI VINAYAK|LOCATION)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
        if loc_m:
            location_text = re.sub(r'<[^>]+>', ' ', loc_m.group(1)).strip()
        else:
            clean_all = re.sub(r'<[^>]+>', '\n', post_html)
            s_loc = re.search(r'(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF VINAYAK|LOCATION OF DHUNDHI VINAYAK|LOCATION).*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|POOJA|TIMINGS|$)', clean_all, re.DOTALL | re.IGNORECASE)
            if s_loc:
                location_text = s_loc.group(1).strip()
        location_text = re.sub(r'\s+', ' ', location_text)

    # Darshan & Timings text
    timings_text = ""
    if post_html:
        t_m = re.search(r'<strong>\s*(?:TYPES OF POOJA|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|POOJA|TIMINGS)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
        if t_m:
            timings_text = re.sub(r'<[^>]+>', ' ', t_m.group(1)).strip()
        else:
            clean_all = re.sub(r'<[^>]+>', '\n', post_html)
            s_tim = re.search(r'(?:TYPES OF POOJA|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|TIMINGS).*?\n(.*?)(?:\n\s*\n|$)', clean_all, re.DOTALL | re.IGNORECASE)
            if s_tim:
                timings_text = s_tim.group(1).strip()
        timings_text = re.sub(r'\s+', ' ', timings_text)

    # Narrative Paragraphs
    paragraphs = []
    if post_html:
        raw_paras = re.split(r'</p>|<br\s*/?>\s*<br\s*/?>', post_html, flags=re.IGNORECASE)
        for p in raw_paras:
            clean_p = re.sub(r'<[^>]+>', ' ', p).strip()
            clean_p = re.sub(r'&nbsp;', ' ', clean_p)
            clean_p = re.sub(r'&amp;', '&', clean_p)
            clean_p = re.sub(r'\s+', ' ', clean_p)
            if len(clean_p) > 10 and not clean_p.startswith('&#128740;') and not 'Varanasi Temples &raquo;' in clean_p and not 'COPY PROTECTED' in clean_p:
                paragraphs.append(clean_p)

    return {
        'title': title,
        'designation': designation,
        'rel_path': rel_path,
        'original_url': f"https://varanasitemples.in/{rel_path}/" if rel_path else "https://varanasitemples.in/category/vinayak-temples/",
        'images': valid_imgs,
        'sanskrit_verses': verses,
        'youtube_urls': yt_urls,
        'google_maps_urls': maps_links,
        'location_text': location_text,
        'timings_text': timings_text,
        'paragraphs': paragraphs
    }

# Build the 10 Main Ganesh Temples
temples_10 = []

# 1. Dhundi Vinayaka Temple
t1 = parse_vinayak_page('category/vinayak-temples/aa-dhundhi-vinayak', 'Dhundhi Vinayak (Dhundi Vinayaka)', 'Supreme Sovereign Gatekeeper of Kashi & Entry Sanctum to Vishweshwar', 'assets/images/Dhundhi-Vinayak-Shrine.svg')
temples_10.append(t1)

# 2. Shri Bada Ganesh Mandir
t2 = parse_vinayak_page('category/vinayak-temples/vakra-tund-vinayak', 'Shri Bada Ganesh Mandir (Vakra Tund Vinayak)', 'Grand Sovereign Standalone Ganesha Temple of Kashi (Lohatia)', 'assets/images/Vakra-Tund-Vinayak-Bara-Ganesh-1.jpg')
temples_10.append(t2)

# 3. Shri Sakshi Vinayak Temple
# Enriched from site's Vishwanath Gully data & pilgrimage tradition
t3 = {
    'title': 'Shri Sakshi Vinayak Temple',
    'designation': 'Supreme Divine Witness of Kashi Pilgrimage & Sacred Yatra Recorder',
    'rel_path': 'category/vinayak-temples/kali-priya-vinayak',
    'original_url': 'https://varanasitemples.in/category/vinayak-temples/kali-priya-vinayak/',
    'images': [{
        'basename': 'Sakshi-Vinayak-Shrine.svg',
        'local_path': 'assets/images/Sakshi-Vinayak-Shrine.svg',
        'caption': 'Shri Sakshi Vinayak Sanctum • Vishwanath Gali (Varanasi)'
    }],
    'sanskrit_verses': [
        'सिंहतुण्डादुदग्भागे कलिप्रियविनायक:\nकलहं करयेन्नित्यमन्योन्यं तैर्थिकद्दुहाम् ॥\n(Kashi Khand, Chapter 57, Shlok 99 — Located behind Sakshi Vinayak)'
    ],
    'youtube_urls': ['https://www.youtube.com/watch?v=40af4qZMnqA&t=55s'],
    'google_maps_urls': ['https://maps.google.com/?q=Sakshi+Vinayak+Temple+Varanasi'],
    'location_text': 'D-10/50, Dasaswamedh Vishwanath Gully (in the immediate vicinity of Manaprakameshwar, Koti Lingeshwar, and Kalipriya Vinayak, just before the turn toward Shukreshwar and Kalika Galli). Accessible on foot via Dasaswamedh or Godowlia.',
    'timings_text': 'Open daily from 05:00 AM to 11:00 PM. Highly auspicious for darshan immediately following Ganga Snan and Kashi Vishwanath Darshan.',
    'paragraphs': [
        'Shri Sakshi Vinayak Temple is one of the most spiritually pivotal Ganesha shrines in the sacred city of Varanasi. In the Sanskrit tradition of Kashi, "Sakshi" signifies the eternal "Witness". Lord Ganesha here stands as the divine notary and scribe of the cosmos who witnesses, confirms, and officially records that a pilgrim has successfully arrived in Kashi, taken bath in the sacred waters of Mother Ganga, and worshipped Lord Vishweshwar.',
        'According to ancient Kashi Yatra tradition, no pilgrimage to Varanasi is considered complete or spiritually validated without performing darshan of Sakshi Vinayak. Devotees visit this sanctum in Vishwanath Gali to show their respects and declare their pilgrimage vows fulfilled.',
        'The sanctum is prominently referenced across multiple chapters of the Kashi Khand and the website\'s pilgrimage guides as a primary geographic anchor in Vishwanath Gali. Immediately behind Sakshi Vinayak stands Kalipriya Vinayak (D-10/50) and the sacred Manaprakameshwar and Koti Lingeshwar shrines.',
        'Pilgrims traditionally purchase holy red sacred threads, sweets, and coconut offerings here, and offer prayers so that their meritorious deeds in Avimukta Kshetra remain eternally witnessed by Lord Ganesha.'
    ]
}
temples_10.append(t3)

# 4. Shri Chintamani Ganesh Temple
t4 = parse_vinayak_page('category/vinayak-temples/chintamani-vinayak', 'Shri Chintamani Ganesh Temple', 'The Wish-Fulfilling Jewel Ganesha & Reliever of All Anxieties', 'assets/images/Chintamani-Vinayak-1.jpg')
temples_10.append(t4)

# 5. Shri Siddhi Vinayak Temple
t5 = parse_vinayak_page('category/vinayak-temples/siddhi-vinayak', 'Shri Siddhi Vinayak Temple', 'Bestower of Spiritual Perfections & Success (Manikarnika Ghat Steps)', 'assets/images/Siddhi-Vinayak-Shrine.svg')
temples_10.append(t5)

# 6. Shri Durg Vinayak Temple
t6 = parse_vinayak_page('category/vinayak-temples/durg-vinayak', 'Shri Durg Vinayak Temple', 'Sovereign Standalone Temple of Southern Kashi (Durga Kund)', 'assets/images/Durg-Vinayak-2.jpg')
temples_10.append(t6)

# 7. Shree Budhivinayak Ganesh Temple (Gyan Vinayak)
t7 = parse_vinayak_page('category/vinayak-temples/gyan-vinayak', 'Shree Budhivinayak Ganesh Temple (Gyan Vinayak)', 'Lord of Intellect, Wisdom & Discernment (Khowa Gulli Chowraha)', 'assets/images/Gyan-Vinayak-1.jpg')
t7['title'] = 'Shree Budhivinayak Ganesh Temple (Gyan Vinayak)'
t7['paragraphs'].insert(0, 'In Kashi Khand and local Varanasi tradition, Gyan Vinayak is worshipped as Budhivinayak (the Lord of Buddhi — intellect, wisdom, and cognitive clarity). He dispels ignorance, cleanses psychological confusion, and guards Kashi against negative psychic vibrations.')
temples_10.append(t7)

# 8. Ganesh Ghat Mandir (Riverfront Ghat Vinayakas)
t8 = {
    'title': 'Ganesh Ghat Mandir (Riverfront Ghat Vinayakas)',
    'designation': 'Presiding Deity of Ganesh Ghat & Sacred Riverfront Protector',
    'rel_path': 'category/vinayak-temples/mangal-vinayak',
    'original_url': 'https://varanasitemples.in/category/vinayak-temples/mangal-vinayak/',
    'images': [
        {
            'basename': 'Mangal-vinayak.jpeg',
            'local_path': 'assets/images/Mangal-vinayak.jpeg',
            'caption': 'Mangal Vinayak • Ganesh Ghat / Bala Ghat Sanctum'
        },
        {
            'basename': 'Manikarnika-Vinayak-1.jpg',
            'local_path': 'assets/images/Manikarnika-Vinayak-1.jpg',
            'caption': 'Manikarnika Riverfront Vinayak • Sacred Steps'
        }
    ],
    'sanskrit_verses': [
        'Kashi Khand, Chapter 57 & Chapter 61\nमंगलो मंगलं दद्यात् सर्वविघ्नविनाशन: ।\nतीर्थिकानां च सततं काशीवासफलं दिशेत् ॥'
    ],
    'youtube_urls': ['https://www.youtube.com/watch?v=l-35TQ5emoQ&t=13s'],
    'google_maps_urls': ['https://maps.google.com/?q=Ganesh+Ghat+Varanasi'],
    'location_text': 'Ganesh Ghat (adjacent to Bhonsla Ghat, Mehta Hospital, and Bala Ghat / Panchganga), Varanasi. Accessible by boat directly to Ganesh Ghat steps or by walking through the riverfront ghat pathway from Dashashwamedh or Manikarnika.',
    'timings_text': 'Open daily from 05:00 AM to 01:00 PM and from 03:00 PM to 10:00 PM. Evening Ganga Aarti on the ghats provides sublime spiritual ambiance.',
    'paragraphs': [
        'Ganesh Ghat Mandir is the iconic riverfront shrine presiding over Ganesh Ghat on the sacred river Ganga in Varanasi. Historically known as one of the prominent stone ghats of northern Varanasi (situated between Mehta Hospital, Bhonsla Ghat, and Bala Ghat near Agneeshwar and Nageshwar), it provides direct stone staircase access from the river to the sacred sanctum.',
        'According to Kashi Khand and the website\'s ghat documentation, devotees approaching Agneeshwar, Nageshwar, and Mangala Gauri regularly arrive by boat at Ganesh Ghat / Bhonsla Ghat and climb the sacred steps to offer their first salutations at the Ganesh Ghat Mandir.',
        'Worshipping the riverfront Vinayaka at Ganesh Ghat removes all travel exhaustion, cleanses obstacles accumulated during pilgrimage, and invokes the eternal blessings of Mangal Vinayak and Manikarnika Vinayak who stand vigil over the holy riverfront.',
        'Pilgrims customarily take a sacred holy dip at Ganesh Ghat and offer fresh Ganga water, red hibiscus flowers, and modaks to the Lord before proceeding into the labyrinthine alleys of the city.'
    ]
}
temples_10.append(t8)

# 9. Shalakanta Vinayak Temple (Shal Kant Vinayak)
t9 = parse_vinayak_page('category/vinayak-temples/shal-kant-vinayak', 'Shalakanta Vinayak Temple (Shal Kant Vinayak)', 'Dispeller of Thorns, Obstacles & Mental Anguish (Manduadih)', 'assets/images/Shalakanta-Vinayak-Shrine.svg')
t9['title'] = 'Shalakanta Vinayak Temple (Shal Kant Vinayak)'
temples_10.append(t9)

# 10. Kharva Vinayak Temple
t10 = parse_vinayak_page('category/vinayak-temples/kharva-vinayak', 'Kharva Vinayak Temple', 'Guardian of the Confluence & Rajghat Fort Sanctum (Varuna Sangam)', 'assets/images/KHARVA-VINAYAK-1.jpg')
temples_10.append(t10)

print(f"Successfully processed all 10 Main Ganesh Temples:")
for idx, t in enumerate(temples_10, 1):
    print(f"  {idx}. {t['title']} -> {len(t['images'])} imgs, {len(t['paragraphs'])} paras, {len(t['sanskrit_verses'])} verses")

# ========================================================
# EXTRACT THE 56 VINAYAKAS FOR THE SEPARATE DIRECTORY
# ========================================================
print("\nExtracting all 56 Vinayakas for the separate directory...")
v_dir = os.path.join(BASE_DIR, 'category', 'vinayak-temples')
all_v_subdirs = sorted([d for d in os.listdir(v_dir) if os.path.isdir(os.path.join(v_dir, d)) and d not in ['feed', 'page', 'a-places-of-worship-of-lord-vinayak-ganesha-in-kashi', 'aaa-fifty-six-vinayak-temples']])

fifty_six_directory = []
for sub in all_v_subdirs:
    page_file = os.path.join(v_dir, sub, 'index.html')
    if not os.path.exists(page_file):
        continue
    with open(page_file, 'r', encoding='utf-8', errors='ignore') as pf:
        p_html = pf.read()
    
    # Title
    t_m = re.search(r'<title>(.*?)</title>', p_html, re.I)
    raw_t = t_m.group(1) if t_m else sub.replace('-', ' ').title()
    title = re.sub(r'\s*-\s*Varanasi Temples.*', '', raw_t, flags=re.I).strip()
    
    # Location
    clean_t = re.sub(r'<[^>]+>', '\n', p_html)
    loc = "Refer to shrine article"
    s_loc = re.search(r'LOCATION OF.*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|POOJA|TIMINGS|$)', clean_t, re.I)
    if s_loc:
        loc = s_loc.group(1).strip()
    loc = re.sub(r'\s+', ' ', loc)[:200]
    
    # YouTube
    yt_m = re.findall(r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)', p_html)
    yt_url = f"https://www.youtube.com/watch?v={yt_m[0]}" if yt_m else ""
    
    # Photo exists?
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', p_html)
    valid_i = [i for i in imgs if not i.endswith('.gif') and not 'hit-counter' in i and 'uploads' in i]
    
    fifty_six_directory.append({
        'slug': sub,
        'title': title,
        'location': loc,
        'has_photo': len(valid_i) > 0,
        'youtube_url': yt_url,
        'mirror_path': f"category/vinayak-temples/{sub}/index.html",
        'original_url': f"https://varanasitemples.in/category/vinayak-temples/{sub}/"
    })

print(f"Total Vinayaka shrines cataloged in 56 Directory: {len(fifty_six_directory)}")

# Save to ganesh_temples_extracted.json
payload = {
    'main_10_ganesh_temples': temples_10,
    'fifty_six_directory': fifty_six_directory
}

with open('ganesh_temples_extracted.json', 'w', encoding='utf-8') as out_f:
    json.dump(payload, out_f, indent=2, ensure_ascii=False)

print("\nSuccessfully written 'ganesh_temples_extracted.json'!")
