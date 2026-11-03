# test_img_dl.py
import urllib.request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://varanasitemples.in/',
}

test_urls = [
    'http://varanasitemples.in/wp-content/uploads/2010/05/Arun-Aditya-1024x746.jpg',
    'http://varanasi-temples.com/wp-content/uploads/2010/05/annapurna1.jpg',
    'http://varanasitemples.in/wp-content/uploads/2010/05/annapurna1.jpg',
]

for u in test_urls:
    print("Testing:", u)
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
            print("  SUCCESS! Bytes:", len(data))
    except Exception as e:
        print("  FAILED:", e)
