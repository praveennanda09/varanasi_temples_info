# print_block1.py
import re

with open('arun_aditya_post.html', 'r', encoding='utf-8') as f:
    html = f.read()

posts = re.findall(r'<div class="art-PostContent">(.*?)</div>', html, re.DOTALL)
if len(posts) > 1:
    content = posts[1]
    # let's look at images inside content
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', content)
    print("Images in post body:", imgs)
    clean = re.sub(r'<br\s*/?>', '\n', content)
    clean = re.sub(r'</p>', '\n\n', clean)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    print("\n--- FULL ARTICLE BODY ---\n")
    print(clean)
