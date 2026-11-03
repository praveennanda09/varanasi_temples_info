# inspect_post_content.py
import urllib.request
import re

url = 'https://varanasitemples.in/aditya-temples/arun-aditya/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Save post html
with open('arun_aditya_post.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved arun_aditya_post.html, size:", len(html))

# Let's inspect the article body
# Find between <div class="art-PostContent"> and </div>
matches = re.findall(r'<div class="art-PostContent">(.*?)</div>\s*<div class="cleared"></div>', html, re.DOTALL)
if matches:
    content = matches[0]
    print("art-PostContent length:", len(content))
    # extract clean text
    clean = re.sub(r'<[^>]+>', '\n', content)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    for l in lines[:25]:
        print("  ", l)
else:
    print("Could not find art-PostContent")
