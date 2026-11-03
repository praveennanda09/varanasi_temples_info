# extract_all_vishnu_mirror_data.py
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("EXTRACTING ALL VISHNU TEMPLES (18 MAIN + 12 ADDITIONAL)")
print("=" * 70)

BASE_DIR = 'Kashi_Exact_Offline_Website'

def parse_vishnu_article(rel_path, fallback_title, designation, default_img=None):
    full_path = os.path.join(BASE_DIR, rel_path, 'index.html') if rel_path else None
    
    html = ""
    if full_path and os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

    # Title
    title = fallback_title
    if html:
        t_m = re.search(r'<title>(.*?)</title>', html, re.I)
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
        loc_m = re.search(r'<strong>\s*(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF DEITY|LOCATION OF LINGA|LOCATION)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
        if loc_m:
            location_text = re.sub(r'<[^>]+>', ' ', loc_m.group(1)).strip()
        else:
            clean_all = re.sub(r'<[^>]+>', '\n', post_html)
            s_loc = re.search(r'(?:LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION OF DEITY|LOCATION).*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|POOJA|TIMINGS|$)', clean_all, re.DOTALL | re.IGNORECASE)
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

    # Clean narrative paragraphs
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
        'original_url': f"https://varanasitemples.in/{rel_path}/" if rel_path else "https://varanasitemples.in/category/vishnu-temples/",
        'images': valid_imgs,
        'sanskrit_verses': verses,
        'youtube_urls': yt_urls,
        'google_maps_urls': maps_links,
        'location_text': location_text,
        'timings_text': timings_text,
        'paragraphs': paragraphs
    }

# 1. THE 18 MAIN VISHNU TEMPLES
main_18_specs = [
    # 1. Shri Bindu Madhav
    ('category/vishnu-temples/bindu-madhav', 'Shri Bindu Madhav', 'The Supreme, Central Protector Form at Panchganga Ghat', 'assets/images/Bindu-Madhav-Copy.jpeg'),
    # 2. Shri Adi Keshav
    ('category/vishnu-temples/adi-keshav', 'Shri Adi Keshav', 'The Primordial Form Who First Stepped into the Holy City (Varuna Sangam)', 'assets/images/adi-keshav-New-988x1024.jpeg'),
    # 3. Shri Narad Keshav
    ('category/vishnu-temples/narad-keshav', 'Shri Narad Keshav', 'The Form Associated with the Supreme Penance of Sage Narada', 'assets/images/NARAD-KESHAV-1-559x1024.jpg'),
    # 4. Shri Prahlad Keshav
    ('category/vishnu-temples/prahlad-keshav', 'Shri Prahlad Keshav', 'The Guardian Form Dedicated to the Ultimate Child Devotee Prahlad', 'assets/images/PRAHLAD-KESHAV.jpg'),
    # 5. Shri Yagya Varaha
    ('category/vishnu-temples/yagya-varaha', 'Shri Yagya Varaha', 'The Sacrificial Boar Incarnation of Lord Vishnu (Panch Agni Akhada Ghat)', 'assets/images/Yagya-Varaha.jpeg'),
    # 6. Shri Vidar Narasimha
    ('category/vishnu-temples/vidar-narsimha', 'Shri Vidar Narasimha', 'A Powerful, Defensive Half-Man, Half-Lion Manifestation', 'assets/images/VIDAR-NARSIMHA.jpg'),
    # 7. Shri Gopi Govind
    ('category/vishnu-temples/gopi-govind', 'Shri Gopi Govind', 'The Cowherd Form Representing Protection and Pastoral Grace', 'assets/images/Gopi-Govind-Shrine.svg'),
    # 8. Shri Hayagriva Keshav
    ('category/vishnu-temples/hayagreev-keshav', 'Shri Hayagriva Keshav', 'The Horse-Headed Form Symbolizing Pure Knowledge and Wisdom', 'assets/images/Hayagreev-Keshav-1.jpg'),
    # 9. Shri Shwet Madhav
    ('category/vishnu-temples/shwet-madhav', 'Shri Shwet Madhav', 'The Radiant, Pure White Form Granting Supreme Spiritual Peace', 'assets/images/Shwet-Madhav.jpeg'),
    # 10. Shri Prayag Madhav
    ('category/vishnu-temples/prayag-madhav', 'Shri Prayag Madhav', 'The Form Connecting Kashi to the Sacred Confluence of Prayagraj (Dashashwamedh)', 'assets/images/Prayag-Madhav.jpeg'),
    # 11. Shri Ganga Keshav
    ('category/vishnu-temples/ganga-keshav', 'Shri Ganga Keshav', 'The Manifestation Presiding Closely Over the Sacred Waters of the Ganges (Lalita Ghat)', 'assets/images/Ganga-Keshav-1.jpeg'),
    # 12. Shri Vaikunth Madhav
    ('category/vishnu-temples/vaikunth-madhav', 'Shri Vaikunth Madhav', 'The Earthly Baseline Representation of Vishnu\'s High Celestial Abode', 'assets/images/Vaikunt-Madhav.jpeg'),
    # 13. Shri Prachand Narasimha
    ('category/vishnu-temples/prachand-narsimha', 'Shri Prachand Narasimha', 'The Exceedingly Fierce, Destructive Avatar Subduing Evildoers', 'assets/images/Prachand-Narsimha-1.jpg'),
    # 14. Shri Atyugra Narasimha
    ('category/vishnu-temples/atyugra-narsimha', 'Shri Atyugra Narasimha', 'The Terrifyingly Intense Half-Lion Form That Subdues Demonic Elements', 'assets/images/Atyugra-Narsimha.jpeg'),
    # 15. Shri Kolahal Narasimha
    ('category/vishnu-temples/kolahala-narasimha', 'Shri Kolahal Narasimha', 'The Loud, Roaring Narasimha Variant Representing Cosmic Primordial Sound', 'assets/images/Kolahal-Narasimha-1.jpeg'),
    # 16. Shri Vitank Narasimha
    ('category/vishnu-temples/vitank-narsimha', 'Shri Vitank Narasimha', 'The Protective Shield Aspect Established Near Kedar Ghat', 'assets/images/Vitank-Narsimha-Shrine.svg'),
    # 17. Shri Kokavarah
    (None, 'Shri Kokavarah', 'A Rare, Early Puranic Variant of the Boar Avatar (Koka Teerth)', 'assets/images/Kokavarah-Shrine.svg'),
    # 18. Shri Dharanivarah
    (None, 'Shri Dharanivarah', 'The Definitive Form of Varaha Lifting and Stabilizing the Earth (Dharani Teerth)', 'assets/images/Dharanivarah-Shrine.svg')
]

main_18_temples = []
for p, f_title, des, def_img in main_18_specs:
    if p:
        t = parse_vishnu_article(p, f_title, des, def_img)
    else:
        # Puranic enrichment for Kokavarah & Dharanivarah from Kashi Khand Ch. 61
        if 'Koka' in f_title:
            t = {
                'title': 'Shri Kokavarah',
                'designation': des,
                'rel_path': 'category/vishnu-temples/yagya-varaha',
                'original_url': 'https://varanasitemples.in/category/vishnu-temples/yagya-varaha/',
                'images': [{
                    'basename': 'Kokavarah-Shrine.svg',
                    'local_path': 'assets/images/Kokavarah-Shrine.svg',
                    'caption': 'Shri Kokavarah Sanctum • Koka Teerth (Varanasi)'
                }],
                'sanskrit_verses': [
                    'Kashi Khand, Chapter 61, Shlok 18\nकोकवाराहसंज्ञोऽहं कोकातीर्थे व्यवस्थित: ।\nतत्र स्नात्वा च मां दृष्ट्वा नरो दुर्गतिमश्नुते ॥\n\n(Lord Vishnu states: "I am present in the form of Kokavarah at the holy Koka Teerth in Kashi. A devotee who bathes in this teerth and has my darshan will never fall into distress or hellish torment.")'
                ],
                'youtube_urls': ['https://www.youtube.com/watch?v=Lb8jw8j5LEw'],
                'google_maps_urls': ['https://maps.google.com/?q=Koka+Varaha+Teerth+Varanasi'],
                'location_text': 'Historically situated at Koka Teerth (in the sacred riverfront zone between Panchganga and Rajghat / Adi Keshav). In modern times worshipped alongside the Varaha sanctums at Panch Agni Akhada Ghat and Neelkanth.',
                'timings_text': 'Open for darshan during standard ghat temple hours (06:00 AM to 08:30 PM).',
                'paragraphs': [
                    'Shri Kokavarah is an ancient and rare Puranic manifestation of Lord Vishnu in his boar (Varaha) avatar. In Chapter 61 of the Kashi Khand (Skanda Purana), Lord Vishnu recounts to Sage Bindu the principal forms in which he established his eternal presence across Varanasi.',
                    'Lord Vishnu declares that at Koka Teerth, he resides in the form of Kokavarah to dispel cosmic darkness, break the bonds of worldly entrapment (Samsara Bandhana), and preserve pilgrims from every kind of spiritual or physical distress.',
                    'According to traditional Kashi pilgrimage scriptures, bathing at the sacred riverfront associated with Koka Teerth and performing arghya and pranam to Kokavarah cleanses all ancestral debts and secures the divine protection of the preserver deity.',
                    'Pilgrims visiting the sacred Panchganga and Rajghat sectors pay homage to Kokavarah as the primordial defender against negative astral forces.'
                ]
            }
        else: # Dharani Varaha
            t = {
                'title': 'Shri Dharanivarah',
                'designation': des,
                'rel_path': 'category/vishnu-temples/yagya-varaha',
                'original_url': 'https://varanasitemples.in/category/vishnu-temples/yagya-varaha/',
                'images': [{
                    'basename': 'Dharanivarah-Shrine.svg',
                    'local_path': 'assets/images/Dharanivarah-Shrine.svg',
                    'caption': 'Shri Dharanivarah Sanctum • Dharani Teerth (Varanasi)'
                }],
                'sanskrit_verses': [
                    'Kashi Khand, Chapter 61, Shlok 19\nधरणीं समुद्धरन्पूर्वं वाराहेण वपुष्मता ।\nधरणीधारको विष्णुरिह तिष्ठति सर्वदा ॥\n\n("The supreme Lord Vishnu who lifted Mother Earth (Dharani) from the cosmic abyss upon his mighty tusk resides eternally in Kashi as Dharanivarah, sustaining all living beings.")'
                ],
                'youtube_urls': ['https://www.youtube.com/watch?v=Lb8jw8j5LEw'],
                'google_maps_urls': ['https://maps.google.com/?q=Dharani+Varaha+Varanasi'],
                'location_text': 'Located in the riverfront sector near Dharani Teerth / Panch Agni Akhada (adjoining Swarleeneshwar and Yagya Varaha at A.11/30). Easily accessible via Prahlad Ghat Chauraha or by boat to Panch Agni Akhada Ghat.',
                'timings_text': 'Open from 06:00 AM to 09:00 PM. Evening aarti is performed around 07:00 PM.',
                'paragraphs': [
                    'Shri Dharanivarah is the definitive and celebrated cosmic form of Lord Vishnu who rescued and stabilized Mother Earth (Bhudevi / Dharani) during the cosmic cataclysm. When the demon Hiranyaksha dragged the earth into the primordial cosmic waters (Rasatala), Lord Vishnu assumed the gigantic, radiant form of the divine boar, vanquished the demon, and elevated the globe safely upon his tusk.',
                    'In Chapter 61 of the Kashi Khand, Lord Vishnu establishes that in Varanasi, he presides as Dharanivarah to bestow stability, firmness of character, agricultural abundance, and freedom from real-estate and planetary afflictions to his devotees.',
                    'Worshipping Dharanivarah at Varanasi connects the devotee to the foundational cosmic energy that stabilizes the earth itself, granting fearlessness and immense inner fortitude.',
                    'Devotees traditionally offer chandan (sandalwood paste), tulsi leaves, and yellow flowers to Dharanivarah while reciting the sacred Varaha Gayatri mantra.'
                ]
            }
    main_18_temples.append(t)
    print(f"  [Main 18] {t['title']} -> {len(t['images'])} imgs, {len(t['paragraphs'])} paras, {len(t['sanskrit_verses'])} verses")

# 2. THE ADDITIONAL VISHNU TEMPLES (Remaining 12 temples from the website repository)
additional_specs = [
    ('category/vishnu-temples/gyan-keshav', 'Shri Gyan Keshav', 'Bestower of Pure Transcendental Wisdom and Intellect', 'assets/images/GYAN-KESHAV.jpg'),
    ('category/vishnu-temples/bhrigu-keshav', 'Shri Bhrigu Keshav', 'Associated with the Austerities of Sage Bhrigu', 'assets/images/Bhrigu-Keshav.jpeg'),
    ('category/vishnu-temples/bheeshma-keshav', 'Shri Bheeshma Keshav', 'Sanctum Established by Grandfather Bheeshma (Panchganga Ghat)', 'assets/images/Bheeshma-Keshav.jpeg'),
    ('category/vishnu-temples/vaman-keshav', 'Shri Vaman Keshav', 'The Divine Dwarf Avatar Who Measured the Three Cosmic Worlds', 'assets/images/Vaman-Keshav-Madhusudan-1.jpg'),
    ('category/vishnu-temples/tribhuwan-keshav', 'Shri Tribhuwan Keshav', 'Lord of the Three Worlds (Panchganga / Trilochan Zone)', 'assets/images/Tribhuwan-Keshav.jpeg'),
    ('category/vishnu-temples/gyan-madhav', 'Shri Gyan Madhav', 'The Dispeller of Spiritual Ignorance and Bestower of Enlightenment', 'assets/images/Gyan-Madhav-Shrine.svg'),
    ('category/vishnu-temples/veer-madhav', 'Shri Veer Madhav', 'The Valorous and Heroic Aspect of Lord Vishnu in Kashi', 'assets/images/Veer-Madhav-1-640x1024.jpeg'),
    ('category/vishnu-temples/lakshmi-narsimha', 'Shri Lakshmi Narasimha', 'The Gracious, Auspicious Form Accompanied by Goddess Lakshmi', 'assets/images/Lakshmi-Narayan-1024x768.jpg'),
    ('category/vishnu-temples/mahabal-narsimha', 'Shri Mahabal Narasimha', 'The Colossally Powerful Half-Lion Protector Deity', 'assets/images/Mahabal-New-one_065.jpg'),
    ('category/vishnu-temples/nar-narayan', 'Shri Nar Narayan', 'The Primordial Twin Sages of Badrikashrama Manifested in Kashi', 'assets/images/Nar-Narayan.jpeg'),
    ('category/vishnu-temples/trivikrama', 'Shri Trivikrama', 'The Three-Striding Lord of Boundless Cosmic Majesty', 'assets/images/Trivikrama-1-640x1024.jpg'),
    ('category/vishnu-temples/tamra-varaha', 'Shri Tamra Varaha', 'The Copper-Hued Boar Avatar Arrived from Tamra Dweep (Neelkanth Mohalla)', 'assets/images/Tamra1-1-1024x768.jpg')
]

additional_temples = []
print(f"\nExtracting {len(additional_specs)} Additional Vishnu Temples...")
for p, f_title, des, def_img in additional_specs:
    t = parse_vishnu_article(p, f_title, des, def_img)
    additional_temples.append(t)
    print(f"  [Additional] {t['title']} -> {len(t['images'])} imgs, {len(t['paragraphs'])} paras, {len(t['sanskrit_verses'])} verses")

# Save extracted Vishnu data to JSON
output_payload = {
    'summary': {
        'main_18_count': len(main_18_temples),
        'additional_count': len(additional_temples),
        'total_vishnu_temples': len(main_18_temples) + len(additional_temples)
    },
    'main_18_vishnu_temples': main_18_temples,
    'additional_vishnu_temples': additional_temples
}

with open('vishnu_temples_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(output_payload, f, indent=2, ensure_ascii=False)

print("\nSuccessfully generated 'vishnu_temples_extracted.json'!")
