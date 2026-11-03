# build_seed_list.py
import re
from urllib.parse import urlparse, urljoin

with open('homepage_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all links matching varanasitemples.in
all_links = set(re.findall(r'href=[\'"](https?://varanasitemples\.in[^\'"#\s]*)[\'"]', html))

# Normalize links (remove trailing query params or index, normalize protocol)
normalized = set()
for l in all_links:
    # normalize scheme to https
    l = l.replace('http://', 'https://')
    # strip trailing slash differences or keep consistent
    if not l.endswith('/') and not '.' in l.split('/')[-1]:
        l = l + '/'
    normalized.add(l)

# Add primary hubs explicitly if not present
seeds = [
    'https://varanasitemples.in/',
    'https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/',
    'https://varanasitemples.in/category/jyotir-lings/',
]
for s in seeds:
    normalized.add(s)

category_urls = sorted([u for u in normalized if '/category/' in u])
other_urls = sorted([u for u in normalized if not '/category/' in u])

print(f"Total normalized unique URLs discovered from homepage: {len(normalized)}")
print(f"Categories: {len(category_urls)}")
print(f"Other pages: {len(other_urls)}")

with open('discovered_seeds.txt', 'w', encoding='utf-8') as f:
    for u in sorted(normalized):
        f.write(u + '\n')

print("Saved discovered_seeds.txt")
