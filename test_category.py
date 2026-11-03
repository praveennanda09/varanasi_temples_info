# test_category.py
import urllib.request
import re

urls = [
    'https://varanasitemples.in/category/aditya-temples/all-places-of-worship-of-lord-surya-aditya-in-kashi/',
    'https://varanasitemples.in/category/aditya-temples/arun-aditya/',
    'https://varanasitemples.in/category/jyotir-lings/',
    'https://varanasitemples.in/category/bhairav-temples/kaal-bhairav/'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for u in urls:
    print("=" * 60)
    print("Fetching:", u)
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    title = re.findall(r'<title>(.*?)</title>', html, re.I)
    print("Title:", title[0] if title else "No title")
    
    # Check for posts inside this category
    post_titles = re.findall(r'<h2 class=[\'"]art-PostHeader[\'"][^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL | re.I)
    print("Post headers found:", len(post_titles))
    for pt in post_titles[:3]:
        print(" - Post:", re.sub(r'<[^>]+>', '', pt).strip())
    
    # Check for images inside post content
    imgs = re.findall(r'<div class=[\'"]art-PostContent[\'"][^>]*>.*?</div>', html, re.DOTALL | re.I)
    if imgs:
        content_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', imgs[0])
        print("Images in post content:", len(content_imgs), content_imgs[:3])
    else:
        print("No art-PostContent found")
