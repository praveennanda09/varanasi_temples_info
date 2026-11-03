# inspect_post_html.py
import re

with open('arun_aditya_post.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all occurrences of class="art-Post" or class="art-PostContent"
posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
print(f"Total art-PostContent blocks: {len(posts)}")
for i, p in enumerate(posts):
    print(f"\n--- Block {i} (len {len(p)}) ---")
    clean = re.sub(r'<[^>]+>', ' ', p)
    clean = ' '.join(clean.split())
    print(clean[:300])

# Find headings
headers = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.DOTALL | re.I)
print("\n--- Headings ---")
for h in headers:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print("Heading:", clean)
