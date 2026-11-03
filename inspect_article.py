# inspect_article.py
import urllib.request
import re

url = 'https://varanasitemples.in/category/aditya-temples/arun-aditya/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Find permalink to post
links = re.findall(r'<h2 class=[\'"]art-PostHeader[\'"][^>]*>\s*<a href=[\'"]([^\'"]+)[\'"]', html, re.I)
print("Post permalink:", links)

# Find all images anywhere in HTML
all_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
print("All images on page:", all_imgs)

# If there is a post permalink, let's fetch it too!
if links:
    purl = links[0]
    print("\nFetching permalink:", purl)
    preq = urllib.request.Request(purl, headers=headers)
    with urllib.request.urlopen(preq, timeout=15) as pr:
        phtml = pr.read().decode('utf-8', errors='ignore')
    p_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', phtml, re.I)
    print("All images on post permalink page:", p_imgs)
    # Print some text of post
    clean_text = re.sub(r'<[^>]+>', ' ', phtml)
    clean_text = ' '.join(clean_text.split())
    # find ARUN ADITYA in text
    idx = clean_text.find("ARUN ADITYA")
    if idx != -1:
        print("\nExcerpt around ARUN ADITYA:\n", clean_text[idx:idx+1500])
