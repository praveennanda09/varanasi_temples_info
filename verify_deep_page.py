# verify_deep_page.py
import re

deep_page = 'Kashi_Exact_Offline_Website/category/aditya-temples/arun-aditya/index.html'
with open(deep_page, 'r', encoding='utf-8') as f:
    html = f.read()

# Check sample collapsCat in this deep page
m_js = re.findall(r'collapsItems\[\'collapsCat-317:3\'\]\s*=\s*[\'"](.*?)[\'"];', html)
if m_js:
    print("collapsCat-317:3 in deep page:")
    print(m_js[0][:400])

# Check images in this deep page
imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html)
print(f"\nImages in deep page: {len(imgs)}")
for im in imgs[:5]:
    print(" ", im)

# Check remaining varanasitemples.in
rem = re.findall(r'https?://(?:www\.)?varanasitemples\.in[^\s\'"\\<>]*', html)
print(f"\nRemaining varanasitemples.in in deep page: {len(rem)}")
for r in rem:
    print(" ", r)
