# extract_temples_master.py
import os
import sys
import re
import json
import csv
import hashlib
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'raw_html_cache')
MIRROR_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website')

with open(os.path.join(BASE_DIR, 'crawl_state.json'), 'r', encoding='utf-8') as f:
    crawl_state = json.load(f)

with open(os.path.join(BASE_DIR, 'image_url_map.json'), 'r', encoding='utf-8') as f:
    img_map = json.load(f)

# Load URL to local mirror path mapping
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

# Helper to load cached html
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
    # replace <br> and </p> with newlines
    text = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.I)
    text = re.sub(r'</p>', '\n\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    # decode entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#8211;', '-').replace('&#8212;', '-').replace('&#8217;', "'").replace('&#8216;', "'")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines)

def extract_article_content(html):
    if not html:
        return "", "", []
    
    # Extract title
    m_title = re.findall(r'<h[12][^>]*class=[\'"]art-PostHeader[\'"][^>]*>(.*?)</h[12]>', html, re.I | re.DOTALL)
    title = clean_html_text(m_title[0]) if m_title else ""
    if not title:
        m_head = re.findall(r'<title>(.*?)</title>', html, re.I)
        title = m_head[0].split('-')[0].strip() if m_head else ""

    # Extract post content block
    posts = re.findall(r'<div class="art-PostContent">(.*?)</div>\s*(?:<div class="cleared">|<div class="art-PostFooter">|<!--|$)', html, re.DOTALL)
    content_html = ""
    for p in posts:
        # choose the largest block that isn't just navigation links
        if len(p) > len(content_html):
            content_html = p

    # If not found, try any art-PostContent
    if not content_html:
        posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
        if posts:
            content_html = max(posts, key=len)

    # Images inside content
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content_html, re.I)
    
    return title, content_html, imgs

def determine_zone(address, directions, full_text):
    combined = f"{address} {directions} {full_text}".lower()
    
    # Priority keywords for South
    south_keywords = ['assi', 'tulsi ghat', 'durga kund', 'durgakund', 'shivala', 'bhelupur', 'kedar ghat', 'kedareshwar', 'sonarpura', 'harishchandra', 'hanuman ghat', 'lolark kund', 'chitaipur', 'bhadaini', 'shankuldhara', 'rewari talab', 'gurudham']
    # Priority keywords for North
    north_keywords = ['rajghat', 'adi keshav', 'trilochan', 'panchganga', 'panchanada', 'alaipur', 'machhodari', 'bakaria kund', 'maidagin', 'golghar', 'bisheshwarganj', 'varuna', 'kameshwar', 'adampura', 'prahlada', 'telianala', 'prahlad ghat', 'trilochan ghat', 'gaighat', 'gai ghat']
    # Priority keywords for East (Riverfront Ghats / Manikarnika / Dashashwamedh)
    east_keywords = ['manikarnika', 'dashashwamedh', 'dasaswamedh', 'mir ghat', 'meer ghat', 'tripura bhairavi', 'sankata ghat', 'scindia ghat', 'lalita ghat', 'man mandir', 'nepali mandir', 'ganga mahal', 'ahilyabai ghat', 'drbhanga ghat', 'rana mahal', 'chousatti ghat', 'ghat steps']
    # Priority keywords for West (Inland / Chowk / Vishwanath Gali / Gyanvapi / Lahurabir / Godowlia)
    west_keywords = ['chowk', 'vishwanath gali', 'bansphatak', 'gyanvapi', 'gyan vapi', 'lahurabir', 'pisachmochan', 'pishach mochan', 'suraj kund', 'surya kund', 'jangambari', 'godowlia', 'godolia', 'luxa', 'sigra', 'kamachha', 'thatheri bazaar', 'kashipura', 'swarni', 'chitra ghanta', 'akshay vat']

    score_south = sum(1 for k in south_keywords if k in combined)
    score_north = sum(1 for k in north_keywords if k in combined)
    score_east = sum(1 for k in east_keywords if k in combined)
    score_west = sum(1 for k in west_keywords if k in combined)

    # Find highest score
    scores = [
        ('South Kashi', score_south),
        ('North Kashi', score_north),
        ('East Kashi', score_east),
        ('West Kashi', score_west)
    ]
    scores.sort(key=lambda x: x[1], reverse=True)
    best_zone, best_score = scores[0]

    if best_score >= 2:
        confidence = "High"
    elif best_score == 1:
        confidence = "Medium"
    else:
        best_zone = "Zone unverified — location evidence insufficient"
        confidence = "Low"

    evidence = []
    if score_south > 0:
        evidence.append(f"South landmarks: {[k for k in south_keywords if k in combined]}")
    if score_north > 0:
        evidence.append(f"North landmarks: {[k for k in north_keywords if k in combined]}")
    if score_east > 0:
        evidence.append(f"East/Riverfront landmarks: {[k for k in east_keywords if k in combined]}")
    if score_west > 0:
        evidence.append(f"West/Inland landmarks: {[k for k in west_keywords if k in combined]}")

    evidence_str = "; ".join(evidence) if evidence else "No distinct locality keyword matched in source text"
    return best_zone, confidence, evidence_str

print("Extractor module initialized.")
