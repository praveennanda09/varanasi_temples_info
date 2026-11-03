# extract_exact_aditya_html.py
import os
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

aditya_list = [
    {
        'id': 'hub',
        'title': 'ALL PLACES OF WORSHIP OF LORD SURYA (ADITYA) IN KASHI',
        'sub': 'Foundational Puranic Origin • Kashi Khand Legendary Context',
        'rel_file': 'category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/',
    },
    {
        'id': 'arun_aditya',
        'title': '1. ARUN ADITYA',
        'sub': 'Charioteer of Surya • Dispeller of Poverty & Chronic Ailments',
        'rel_file': 'category/aditya-temples/arun-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/arun-aditya/',
    },
    {
        'id': 'draupad_aditya',
        'title': '2. DRAUPAD ADITYA',
        'sub': 'Bestower of the Akshaya Patra • Sovereign Sustainer of Pilgrims',
        'rel_file': 'category/aditya-temples/draupad-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/draupad-aditya/',
    },
    {
        'id': 'ganga_aditya',
        'title': '3. GANGA ADITYA',
        'sub': 'Sacred Riverfront Solar Sanctum • Lalita Ghat Celestial Confluence',
        'rel_file': 'category/aditya-temples/ganga-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/ganga-aditya/',
    },
    {
        'id': 'keshava_aditya',
        'title': '4. KESHAVA ADITYA',
        'sub': 'Confluence of Holy Varuna & Ganga • Rajghat Primordial Sanctuary',
        'rel_file': 'category/aditya-temples/keshava-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/keshava-aditya/',
    },
    {
        'id': 'khakholkh_aditya',
        'title': '5. KHAKHOLKH ADITYA',
        'sub': 'Celestial Illuminator of the Cosmic Skies • Healer of Severe Afflictions',
        'rel_file': 'category/aditya-temples/khakholkh-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/khakholkh-aditya/',
    },
    {
        'id': 'lolark_aditya',
        'title': '6. LOLARK ADITYA',
        'sub': 'The Trembling Solar God • Miraculous Sunken Stepwell of Progeny',
        'rel_file': 'category/aditya-temples/lolark-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/lolark-aditya/',
    },
    {
        'id': 'mayukh_aditya',
        'title': '7. MAYUKH ADITYA',
        'sub': 'Divine Radiant Rays of Surya • Mangala Gauri Gabhasteeshwar Sanctum',
        'rel_file': 'category/aditya-temples/mayukh-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/mayukh-aditya/',
    },
    {
        'id': 'saamba_aditya',
        'title': '8. SAAMBA ADITYA',
        'sub': 'Curative Tapasya of Krishna’s Son Saamba • Surya Kund Golden Sanctuary',
        'rel_file': 'category/aditya-temples/saamba-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/saamba-aditya/',
    },
    {
        'id': 'uttarark_aditya',
        'title': '9. UTTARARK ADITYA',
        'sub': 'Northern Solstice Uttarayana Aspect • Bakaria Kund Solar Guardian',
        'rel_file': 'category/aditya-temples/uttarark-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/uttarark-aditya/',
    },
    {
        'id': 'vimal_aditya',
        'title': '10. VIMAL ADITYA',
        'sub': 'Stainless Purity • Dispeller of Leprosy & Generational Afflictions',
        'rel_file': 'category/aditya-temples/vimal-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/vimal-aditya/',
    },
    {
        'id': 'vriddh_aditya',
        'title': '11. VRIDDH ADITYA',
        'sub': 'The Ancient Sun • Restorer of Sage Harita’s Youth & Vitality',
        'rel_file': 'category/aditya-temples/vriddh-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/vriddh-aditya/',
    },
    {
        'id': 'yama_aditya',
        'title': '12. YAMA ADITYA',
        'sub': 'Lord Dharmaraja’s Devotion • Shield from Premature Death & Torments',
        'rel_file': 'category/aditya-temples/yama-aditya/index.html',
        'live_url': 'https://varanasitemples.in/category/aditya-temples/yama-aditya/',
    }
]

mirror_base = 'Kashi_Exact_Offline_Website'
extracted_data = []

for item in aditya_list:
    full_path = os.path.join(mirror_base, item['rel_file'])
    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Find the article container
    # In category pages, find art-Post
    # Get title
    m_h = re.findall(r'<h[12][^>]*class=[\'"]art-PostHeader[\'"][^>]*>([\s\S]*?)</h[12]>', html)
    orig_title = re.sub(r'<[^>]+>', ' ', m_h[0]).strip() if m_h else item['title']

    # Find content after the title
    title_idx = html.find(orig_title)
    if title_idx == -1: title_idx = 0
    c_start = html.find('<div class="art-PostContent">', title_idx)
    if c_start == -1: c_start = html.find('<div class="art-PostContent">')
    
    # End before next post or footer
    c_end = html.find('<div class="cleared"></div>', c_start)
    if c_end == -1: c_end = html.find('<!-- /art-postcontent -->', c_start)
    
    raw_content = html[c_start:c_end]
    
    # Extract images from content
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', raw_content)
    clean_imgs = []
    for im in imgs:
        if not any(x in im for x in ['smilies', 'flag', 'audio-player', '7.gif', '5.gif', 'counter']):
            clean_imgs.append(im)

    # Extract links
    links = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>([\s\S]*?)</a>', raw_content)
    clean_links = [(href, re.sub(r'<[^>]+>', '', text).strip()) for href, text in links]

    extracted_data.append({
        'id': item['id'],
        'title': item['title'],
        'orig_title': orig_title,
        'sub': item['sub'],
        'live_url': item['live_url'],
        'mirror_path': item['rel_file'],
        'raw_content_html': raw_content,
        'images': clean_imgs,
        'links': clean_links
    })

print(f"Extracted {len(extracted_data)} articles successfully.")
for d in extracted_data:
    print(f"  {d['title']}: {len(d['raw_content_html'])} HTML chars, {len(d['images'])} images, {len(d['links'])} links")

with open('adityas_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=2, ensure_ascii=False)
print("Saved to adityas_extracted.json.")
