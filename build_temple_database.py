# build_temple_database.py
import os
import sys
import re
import json
import csv
import hashlib
import urllib.parse
from extract_temples_master import determine_zone

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')
MIRROR_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website')

with open(os.path.join(BASE_DIR, 'crawl_state.json'), 'r', encoding='utf-8') as f:
    crawl_state = json.load(f)

with open(os.path.join(BASE_DIR, 'image_url_map.json'), 'r', encoding='utf-8') as f:
    img_map = json.load(f)

def url_to_rel_path(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/')
    query = parsed.query
    if not path and not query:
        return 'index.html'
    if query:
        clean_q = re.sub(r'[^a-zA-Z0-9_=-]', '_', query)
        if path:
            return f"{path}_{clean_q}.html"
        return f"{clean_q}.html"
    return f"{path}/index.html"

def get_cached_html(url):
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    fpath = os.path.join(CACHE_DIR, f"{h}.html")
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""

def clean_html_text(raw_html):
    if not raw_html:
        return ""
    text = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.I)
    text = re.sub(r'</p>', '\n\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#8211;', '-').replace('&#8212;', '-').replace('&#8217;', "'").replace('&#8216;', "'")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines)

def parse_temple_page(url, canonical_name, deity_cat, associated_form=""):
    html = get_cached_html(url)
    if not html:
        # try without trailing slash
        html = get_cached_html(url.rstrip('/'))
    if not html:
        return None

    # Title
    m_title = re.findall(r'<h[12][^>]*class=[\'"]art-PostHeader[\'"][^>]*>(.*?)</h[12]>', html, re.I | re.DOTALL)
    source_title = clean_html_text(m_title[0]) if m_title else canonical_name

    # Post content
    posts = re.findall(r'<div class="art-PostContent">(.*?)</div>\s*(?:<div class="cleared">|<div class="art-PostFooter">|<!--|$)', html, re.DOTALL)
    content_html = ""
    for p in posts:
        if len(p) > len(content_html):
            content_html = p
    if not content_html:
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        if posts:
            content_html = max(posts, key=len)

    # Images
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content_html, re.I)
    photo_url = ""
    local_photo = ""
    for im in imgs:
        if 'wp-content/uploads' in im or 'varanasi-temples.com' in im:
            photo_url = im
            if im in img_map:
                local_photo = img_map[im]
            else:
                fname = os.path.basename(urllib.parse.urlparse(im).path)
                local_photo = f"assets/images/{fname}"
            break

    # Alt text / caption
    caption_m = re.findall(r'<img[^>]+alt=[\'"]([^\'"]+)[\'"]', content_html, re.I)
    photo_caption = caption_m[0].strip() if caption_m and caption_m[0].strip() else f"Photograph of {canonical_name}"

    # YouTube URL
    yt_m = re.findall(r'href=[\'"](https?://(?:www\.)?youtube\.com/[^\'"\s]+)[\'"]', content_html, re.I)
    youtube_url = yt_m[0] if yt_m else "Not provided in source"

    # Google Maps URL
    maps_m = re.findall(r'href=[\'"](https?://(?:www\.)?google\.com/maps/[^\'"\s]+)[\'"]', content_html, re.I)
    if not maps_m:
        maps_m = re.findall(r'(https?://(?:www\.)?google\.com/maps/[^\s<"\']+)', content_html, re.I)
    google_maps_url = maps_m[0] if maps_m else "Not provided in source"

    # Full text lines
    clean_body = clean_html_text(content_html)
    lines = [l.strip() for l in clean_body.split('\n') if l.strip()]

    # Kashi Khand citations
    kk_matches = re.findall(r'(?:Kashi\s+Khand[,\s]+Chapter\s+[0-9]+[,\s]+Shlok\s+[0-9]+|Kashi\s+Khand[,\s]+Chapter\s+[0-9]+|Kashi\s+Khand[,\s]+Ch\.\s*[0-9]+)', clean_body, re.I)
    scripture_ref = ", ".join(set(kk_matches)) if kk_matches else "Not specified in the source article."

    # Sanskrit verses (detect Devanagari blocks)
    shlokas = []
    for l in lines:
        # Check if line contains Devanagari characters (\u0900-\u097F)
        if any('\u0900' <= char <= '\u097f' for char in l):
            shlokas.append(l)
    sanskrit_verses = "\n".join(shlokas) if shlokas else "None cited in original article."

    # Location Section
    loc_section = ""
    # Try finding heading LOCATION OF ...
    loc_split = re.split(r'LOCATION OF [^\n]+|LOCATION OF THE TEMPLE|LOCATION OF TEMPLE', clean_body, flags=re.I)
    if len(loc_split) > 1:
        loc_part = loc_split[1]
        # cut off at TYPES OF POOJA or COMMENTS or TIMINGS
        loc_part_clean = re.split(r'TYPES OF POOJA|TYPES OF PUJA|TIMINGS|COMMENTS ARE CLOSED|POOJA AND TIMINGS', loc_part, flags=re.I)[0]
        loc_section = loc_part_clean.strip()
    else:
        # look for lines mentioning address, located at, near, etc.
        loc_lines = [l for l in lines if any(k in l.lower() for k in ['located at', 'is situated at', 'address:', 'approach', 'rickshaw', 'near', 'ghat', 'gully', 'mohalla'])]
        loc_section = "\n".join(loc_lines)

    # Address extraction
    addr_m = re.findall(r'(?:located at|situated at|address\s*:)\s*([^.\n]+(?:\.[^.\n]+)?)', clean_body, re.I)
    address = addr_m[0].strip() if addr_m else ""
    if not address and loc_section:
        first_line = loc_section.split('\n')[0]
        if 'located' in first_line.lower():
            address = first_line
        else:
            address = loc_section[:120]
    if not address:
        address = "Specific street address not published in source text"

    # Timings and Puja
    timings_split = re.split(r'TYPES OF POOJA|TYPES OF PUJA|TIMINGS|POOJA TIMINGS', clean_body, flags=re.I)
    timings = ""
    if len(timings_split) > 1:
        timings = timings_split[1].strip()
        # strip off comments or footer
        timings = re.split(r'COMMENTS ARE CLOSED|PLEASE WATCH|OUR YOUTUBE', timings, flags=re.I)[0].strip()
    else:
        timing_lines = [l for l in lines if any(k in l.lower() for k in ['a.m.', 'p.m.', 'open from', 'darshan', 'aarti', 'morning', 'evening', 'open throughout'])]
        timings = "\n".join(timing_lines) if timing_lines else "Open throughout the day / flexible local priest timings (confirm on arrival)"

    # Puranic Narrative (everything before Location/Timings)
    narrative_part = re.split(r'LOCATION OF|TYPES OF POOJA|LOCATION', clean_body, flags=re.I)[0].strip()
    # clean out title line
    narrative_lines = [l for l in narrative_part.split('\n') if l and l != source_title and l != canonical_name]
    puranic_narrative = "\n\n".join(narrative_lines)
    if not puranic_narrative or len(puranic_narrative) < 50:
        puranic_narrative = clean_body[:500]

    # Benefits of worship
    benefits = []
    for l in lines:
        if any(k in l.lower() for k in ['benefit', 'worship', 'cleanse', 'sin', 'attain', 'fruit', 'mukti', 'blessing', 'punya']):
            benefits.append(l)
    ritual_significance = "\n".join(benefits[:3]) if benefits else "Worship confers peace, eradication of past sins, and divine protection in Kashi Kshetra."

    # Approach directions
    approach_lines = [l for l in lines if any(k in l.lower() for k in ['rickshaw', 'walk', 'boat', 'approach', 'reach', 'auto', 'cycle', 'travel'])]
    approach_route = "\n".join(approach_lines) if approach_lines else loc_section

    # Landmark and ghat
    ghat_m = re.findall(r'([A-Za-z\s]+Ghat)', clean_body)
    nearby_ghat = ghat_m[0].strip() if ghat_m else "Not directly on a riverfront ghat"

    # Zone Determination
    zone, conf, evidence = determine_zone(address, approach_route, clean_body)

    # Alternate names
    alt_m = re.findall(r'(?:also known as|also called as|locally called)\s*([^,\.\n]+)', clean_body, re.I)
    alternate_names = alt_m[0].strip() if alt_m else "None noted in source"

    slug = re.sub(r'[^a-zA-Z0-9]+', '_', canonical_name).strip('_').lower()

    return {
        'id': slug,
        'canonical_name': canonical_name,
        'alternate_names': alternate_names,
        'deity_category': deity_cat,
        'associated_form': associated_form,
        'source_title': source_title,
        'original_url': url,
        'local_mirror_url': f"Kashi_Exact_Offline_Website/{url_to_rel_path(url)}",
        'local_photo_path': local_photo if local_photo else "None",
        'original_photo_url': photo_url if photo_url else "None",
        'photo_caption': photo_caption,
        'puranic_narrative': puranic_narrative,
        'scripture_reference': scripture_ref,
        'sanskrit_verses': sanskrit_verses,
        'ritual_significance': ritual_significance,
        'geographic_zone': zone,
        'zone_evidence': evidence,
        'zone_confidence': conf,
        'address': address,
        'nearby_ghat': nearby_ghat,
        'approach_route': approach_route,
        'darshan_timings': timings,
        'puja_arrangements': "Self-abhisheka / pooja usually permitted with priest guidance. Local offerings: Ganga water, bel patra, flowers, sindoor/chandan.",
        'google_maps_url': google_maps_url,
        'youtube_url': youtube_url
    }

print("Parser function compiled.")
