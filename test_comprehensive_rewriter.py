# test_comprehensive_rewriter.py
import re
import os
import json
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIRROR_DIR = os.path.join(BASE_DIR, 'Kashi_Exact_Offline_Website')

with open('crawl_state.json', 'r', encoding='utf-8') as f:
    crawl_state = json.load(f)

with open('image_url_map.json', 'r', encoding='utf-8') as f:
    img_map = json.load(f)

visited = crawl_state.get('visited', {})

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

url_to_local_file = {}
for u in visited.keys():
    rel = url_to_rel_path(u)
    url_to_local_file[u] = rel
    clean_u = u.replace('http://', 'https://')
    url_to_local_file[clean_u] = rel
    if clean_u.endswith('/'):
        url_to_local_file[clean_u[:-1]] = rel
    else:
        url_to_local_file[clean_u + '/'] = rel

def get_relative_url(source_file, target_file):
    source_dir = os.path.dirname(source_file)
    rel = os.path.relpath(target_file, source_dir if source_dir else '.')
    return rel.replace('\\', '/')

def rewrite_page_content(html, current_rel_path):
    # Regex to find any URL pointing to varanasitemples.in or varanasi-temples.com
    # Match: (https?://(?:www\.)?varanasitemples\.in[^\s\'"\\<>]*)
    # Also handle trailing slash or query
    def replacer(m):
        full_url = m.group(0)
        # Check if it's an image
        if any(full_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            fname = os.path.basename(urllib.parse.urlparse(full_url).path)
            local_img_rel = f"assets/images/{fname}"
            return get_relative_url(current_rel_path, local_img_rel)

        # Check if it's in url_to_local_file
        norm_u = full_url.replace('http://', 'https://').split('?')[0]
        if norm_u in url_to_local_file:
            target_dest = url_to_local_file[norm_u]
            return get_relative_url(current_rel_path, target_dest)
        elif norm_u.rstrip('/') + '/' in url_to_local_file:
            target_dest = url_to_local_file[norm_u.rstrip('/') + '/']
            return get_relative_url(current_rel_path, target_dest)
        elif norm_u.rstrip('/') in url_to_local_file:
            target_dest = url_to_local_file[norm_u.rstrip('/')]
            return get_relative_url(current_rel_path, target_dest)

        # If it's the domain root
        if full_url.rstrip('/') in ['http://varanasitemples.in', 'https://varanasitemples.in', 'http://www.varanasitemples.in', 'https://www.varanasitemples.in']:
            return get_relative_url(current_rel_path, 'index.html')

        return full_url

    # Replace all varanasitemples.in and varanasi-temples.com occurrences
    pattern = r'https?://(?:www\.)?(?:varanasitemples\.in|varanasi-temples\.com)[^\s\'"\\<>]*'
    rewritten = re.sub(pattern, replacer, html)
    return rewritten

# Test on raw homepage
with open('homepage_raw.html', 'r', encoding='utf-8') as f:
    raw_home = f.read()

rewritten_home = rewrite_page_content(raw_home, 'index.html')

remaining = re.findall(r'https?://(?:www\.)?varanasitemples\.in[^\s\'"\\<>]*', rewritten_home)
print(f"Remaining varanasitemples.in in rewritten homepage: {len(remaining)}")
for r in remaining[:10]:
    print(" ", r)

# Check sample collapsItems string
sample_collaps = re.findall(r'collapsItems\[\'collapsCat-317:3\'\]\s*=\s*[\'"](.*?)[\'"];', rewritten_home)
if sample_collaps:
    print("\nSample collapsCat-317:3 after rewriting:")
    print(sample_collaps[0][:400])
