# check_links.py
import re

with open('Kashi_Exact_Offline_Website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
print(f"Total hrefs in index.html: {len(hrefs)}")

live_varanasi = [h for h in hrefs if 'varanasitemples.in' in h]
relative = [h for h in hrefs if not h.startswith('http') and not h.startswith('#') and not h.startswith('mailto:')]
external = [h for h in hrefs if h.startswith('http') and 'varanasitemples.in' not in h]

print(f"Links pointing to live varanasitemples.in: {len(live_varanasi)}")
print(f"Relative local links: {len(relative)}")
print(f"External links: {len(external)}")

print("\nSample links to live varanasitemples.in:")
for h in live_varanasi[:15]:
    print(" ", h)

print("\nSample relative links:")
for h in relative[:15]:
    print(" ", h)
