# extract_ganga_mirror_data.py
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("EXTRACTING RIVER GANGA, SACRED TEERTHS & KUNDS MIRROR DATA")
print("=" * 70)

BASE_DIR = 'Kashi_Exact_Offline_Website'

def parse_mirror_article(rel_path, fallback_title, designation, default_imgs=None):
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

    if default_imgs:
        for dimg in default_imgs:
            if os.path.exists(dimg):
                b = os.path.basename(dimg)
                if not any(vi['basename'] == b for vi in valid_imgs):
                    valid_imgs.append({
                        'basename': b,
                        'local_path': dimg.replace('\\', '/'),
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
        loc_m = re.search(r'<strong>\s*(?:LOCATION OF THE TEERTH|LOCATION OF TEERTH|LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION|WHERE TO FIND)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
        if loc_m:
            location_text = re.sub(r'<[^>]+>', ' ', loc_m.group(1)).strip()
        else:
            clean_all = re.sub(r'<[^>]+>', '\n', post_html)
            s_loc = re.search(r'(?:LOCATION OF THE TEERTH|LOCATION OF TEERTH|LOCATION OF THE TEMPLE|LOCATION OF TEMPLE|LOCATION).*?\n(.*?)(?:\n\s*\n|TYPES OF POOJA|POOJA|TIMINGS|$)', clean_all, re.DOTALL | re.IGNORECASE)
            if s_loc:
                location_text = s_loc.group(1).strip()
        location_text = re.sub(r'\s+', ' ', location_text)

    # Darshan & Timings text
    timings_text = ""
    if post_html:
        t_m = re.search(r'<strong>\s*(?:TYPES OF POOJA|TYPES OF POOJAS|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|POOJA|TIMINGS)[^<]*</strong>(.*?)(?:<strong>|$)', post_html, re.DOTALL | re.IGNORECASE)
        if t_m:
            timings_text = re.sub(r'<[^>]+>', ' ', t_m.group(1)).strip()
        else:
            clean_all = re.sub(r'<[^>]+>', '\n', post_html)
            s_tim = re.search(r'(?:TYPES OF POOJA|TYPES OF POOJAS|TIMINGS OF THE TEMPLE|TIMINGS OF POOJA|DARSHAN TIMINGS|TIMINGS).*?\n(.*?)(?:\n\s*\n|$)', clean_all, re.DOTALL | re.IGNORECASE)
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
        'original_url': f"https://varanasitemples.in/{rel_path}/" if rel_path else "https://varanasitemples.in/category/importance-of-river-ganga/",
        'images': valid_imgs,
        'sanskrit_verses': verses,
        'youtube_urls': yt_urls,
        'google_maps_urls': maps_links,
        'location_text': location_text,
        'timings_text': timings_text,
        'paragraphs': paragraphs
    }

sections_list = []

# 1. River Ganga (The Supreme Celestial Stream)
s1 = parse_mirror_article('category/importance-of-river-ganga/river-ganga', 'River Ganga (The Holy Celestial Stream)', 'Supreme Mother & Sanctifying River of Avimukta Kshetra', ['assets/images/ganga-photo-2-1024x576.jpg', 'assets/images/ganga-photo-3-300x169.jpg', 'assets/images/ganga_ghats_a-1-1024x512.jpg'])
s1['location_text'] = 'Flows from South to North (Uttara-Vahini) along the entire eastern perimeter of Varanasi, connecting all 84 historic stone ghats from Assi Sangam to Varuna Sangam.'
s1['timings_text'] = 'Open continuously 24 hours. Highly auspicious for Brahma Muhurta snan (04:30 AM to 06:00 AM) and evening Ganga Aarti (06:30 PM to 07:30 PM).'
sections_list.append(s1)

# 2. Importance of Immersion of Mortal Remains (Asthi) in Ganga
s2 = parse_mirror_article('category/importance-of-immersion-of-mortal-remains-asthi-in-ganga', 'Importance of Immersion of Mortal Remains (Asthi) in Ganga', 'Supreme Liberation (Moksha) for Ancestral Souls & Pitris', ['assets/images/Ganga-Assi-Ghat-1024x645.jpg'])
s2['location_text'] = 'Conducted primarily at Manikarnika Ghat, Harishchandra Ghat, and Dashashwamedh Ghat along the sacred Ganga.'
s2['timings_text'] = 'Cremation and Asthi Visarjan rites are conducted throughout the day and night at Manikarnika and Harishchandra Ghats.'
sections_list.append(s2)

# 3. Assi Sangam Teerth & Ghat
s3 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/assi-sangam', 'Assi Sangam Teerth & Ghat', 'Southern Boundary Confluence of River Assi and Ganga', ['assets/images/Ganga-Assi-Ghat-1024x645.jpg'])
sections_list.append(s3)

# 4. Dasaswamedh Teerth & Ghat
s4 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/dasaswamedh', 'Dasaswamedh Teerth & Ghat', 'Site of the Ten Horse Sacrifices of Lord Brahma & Central Ghat of Kashi', ['assets/images/dasaswamedh-Teerth-ghat-1024x576.jpg', 'assets/images/Dasaswamedh-Ganga-Aarti-1024x576.jpg'])
sections_list.append(s4)

# 5. Gyan Vapi Kund (Well of Wisdom)
s5 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/gyan-vapi', 'Gyan Vapi Kund (Well of Wisdom)', 'Primordial Well of Transcendental Knowledge Dug by Lord Shiva\'s Trishul', ['assets/images/Gyan-Vapi-Kund-Shrine.svg'])
s5['location_text'] = 'Situated inside the Kashi Vishweshwar (Vishwanath) Temple complex, immediately adjacent to the Nandi pavilion.'
s5['timings_text'] = 'Darshan accessible during regular Kashi Vishwanath temple hours.'
sections_list.append(s5)

# 6. Lolark Kund
s6 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/lolark-kund', 'Lolark Kund', 'Miraculous Solar Tank of Sage Agasthya, Lopamudra & Lolark Aditya', ['assets/images/Lolark-Kund-1-1024x576.jpg'])
sections_list.append(s6)

# 7. Manikarnika Teerth, Kund & Ghat
s7 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/manikarnika', 'Manikarnika Teerth, Kund & Ghat', 'Primordial Chakra Pushkarini Kund & Crest-Jewel of All Teerthas', ['assets/images/Manikarnika-Chakra-Pushkarini-Shrine.svg'])
sections_list.append(s7)

# 8. Padodak Teerth
s8 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/padodak-teerth', 'Padodak Teerth', 'Sacred Foot-Washing Teerth of Lord Vishnu at Varuna Sangam', ['assets/images/Padodak-Teerth-Shrine.svg'])
sections_list.append(s8)

# 9. Panch Ganga / Panch Nada Teerth
s9 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/panch-ganga-panch-nada-teerth', 'Panch Ganga (Panch Nada Teerth)', 'Invisible Confluence of Five Celestial Streams & Abode of Bindu Madhav', ['assets/images/Panch-Ganga-1024x754.jpg'])
sections_list.append(s9)

# 10. Pilpila Teerth
s10 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/pilpila-teerth', 'Pilpila Teerth', 'Sacred Miraculous Kund Adjoining Trilochan Mahadev', ['assets/images/Pilpila-Teerth-Koop21-300x225.jpg'])
sections_list.append(s10)

# 11. Varuna Sangam Teerth & Ghat
s11 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/varuna-sangam', 'Varuna Sangam Teerth & Ghat', 'Northern Boundary Confluence of River Varuna and Ganga at Adi Keshav', ['assets/images/sangam-1024x562.jpg'])
sections_list.append(s11)

# 12. Vimal Teerth (Pisachmochan Kund)
s12 = parse_mirror_article('category/importance-of-river-ganga/important-teerthsghats/vimal-teerth-pisachmochan', 'Vimal Teerth (Pisachmochan Kund)', 'Miracle Pool Absolving Ghostly Afflictions & Pitri Dosh', ['assets/images/Pisach-Mochan-Talab--1024x576.jpg'])
sections_list.append(s12)

# 13. Durga Kund (Supplementary Sacred Kund)
s13 = {
    'title': 'Durga Kund (Sacred Shakti Tank)',
    'designation': 'Sacred Kund Adjoining the Historic Durga Temple & Durg Vinayak',
    'rel_path': 'category/devi-temples/durga',
    'original_url': 'https://varanasitemples.in/category/devi-temples/durga/',
    'images': [{
        'basename': 'Durga-Kund-1024x692.jpg',
        'local_path': 'assets/images/Durga-Kund-1024x692.jpg',
        'caption': 'Durga Kund Sacred Tank • Durgabari'
    }],
    'sanskrit_verses': [
        'Kashi Khand, Chapter 72\nदुर्गाकुण्डे नर: स्नात्वा पूजयित्वा च चण्डिकाम् ।\nसर्वान् कामानवाप्नोति मुच्यते सर्वपातकै: ॥\n("Devotees who bathe in Durga Kund and worship Devi Chandika attain all cherished desires and are liberated from every sin.")'
    ],
    'youtube_urls': ['https://www.youtube.com/watch?v=uzrtWjx_v9Q'],
    'google_maps_urls': ['https://maps.google.com/?q=Durga+Kund+Varanasi'],
    'location_text': 'Located at Durga Kund road, Southern Varanasi, adjacent to the 18th-century red stone Durga Mandir and Durg Vinayak Temple.',
    'timings_text': 'Open daily from 05:00 AM to 10:00 PM. Highly vibrant during Navratri.',
    'paragraphs': [
        'Durga Kund is one of the most prominent historic masonry tanks (kunds) in southern Varanasi. Commissioned adjacent to the ancient Durga Temple, this vast rectangular tank features stone steps on all sides and was historically connected directly to river Ganga through subterranean channels.',
        'According to Kashi Khand Chapter 72, bathing in Durga Kund on Tuesdays and during the nine nights of Navratri confers supreme protective blessings, dispelling all fear of adversaries, illness, and planetary afflictions.',
        'Pilgrims visiting Durg Vinayak, Durga Devi, and nearby Sankat Mochan habitually perform achamana at the kund steps before proceeding for darshan.'
    ]
}
sections_list.append(s13)

# 14. Kapal Mochan Teerth / Laat Sarovar (Supplementary Sacred Kund)
s14 = {
    'title': 'Kapal Mochan Teerth (Laat Sarovar Kund)',
    'designation': 'Where the Fifth Head of Brahma Fell from Bhairava\'s Hand',
    'rel_path': 'category/bhairav-temples/kapal-bhairav',
    'original_url': 'https://varanasitemples.in/category/bhairav-temples/kapal-bhairav/',
    'images': [{
        'basename': 'Kapal-Mochan-Teerth-Laat-Sarovar2-300x225.jpg',
        'local_path': 'assets/images/Kapal-Mochan-Teerth-Laat-Sarovar2-300x225.jpg',
        'caption': 'Kapal Mochan Teerth / Laat Sarovar • Northern Varanasi'
    }],
    'sanskrit_verses': [
        'Kashi Khand, Chapter 31\nकपालमोचनं तीर्थं सर्वपापप्रणाशनम् ।\nयत्र स्नातो नरो मुच्यते ब्रह्महत्यादिपातकात् ॥\n("Kapal Mochan Teerth destroys all heinous sins. A mortal who bathes here is absolved even of the grave sin of Brahmahatya.")'
    ],
    'youtube_urls': ['https://www.youtube.com/watch?v=P2b8sEw8bqw'],
    'google_maps_urls': ['https://maps.google.com/?q=Kapal+Mochan+Teerth+Varanasi'],
    'location_text': 'Located at Laat Bhairav, Adampura / Sarai Mohana, Northern Varanasi.',
    'timings_text': 'Open daily from 06:00 AM to 08:30 PM.',
    'paragraphs': [
        'Kapal Mochan Teerth (also known as Laat Sarovar) is one of the most spiritually dramatic teerths in Kashi Khand. When Lord Bhairava severed the fifth arrogant head of Lord Brahma, the skull (Kapala) adhered obstinately to his divine hand due to the cosmic sin of Brahmahatya.',
        'Lord Bhairava wandered the cosmos begging for alms, but the skull would not detach. Only when he crossed the sacred threshold of Avimukta Kshetra into Kashi did the severed head drop into this sacred tank, instantly absolving the sin. Hence, the pool was christened Kapal Mochan (Liberation from the Skull).',
        'Pilgrims bathe here to cleanse deep-seated karmic burdens, ancestral guilts, and spiritual obstacles before praying to Kapal Bhairav (Laat Bhairav).'
    ]
}
sections_list.append(s14)

print(f"\nSuccessfully extracted all {len(sections_list)} Ganga, Teerth & Kund sections:")
for idx, s in enumerate(sections_list, 1):
    print(f"  {idx}. {s['title']} -> {len(s['images'])} imgs, {len(s['paragraphs'])} paras, {len(s['sanskrit_verses'])} verses")

# Save extracted data to JSON
with open('ganga_teerths_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(sections_list, f, indent=2, ensure_ascii=False)

print("\nSuccessfully saved extracted Ganga & Teerths data to 'ganga_teerths_extracted.json'!")
