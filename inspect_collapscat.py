# inspect_collapscat.py
import re

with open('Kashi_Exact_Offline_Website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for widget-collapscat
m = re.findall(r'<ul id="widget-collapscat[^>]*>(.*?)</ul>', html, re.DOTALL)
if m:
    widget_html = m[0]
    widget_hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', widget_html)
    print(f"Total hrefs in widget: {len(widget_hrefs)}")
    print("Sample widget hrefs:")
    for h in widget_hrefs[:20]:
        print(" ", h)
else:
    print("Widget not found!")

# Check JavaScript collapsItems in index.html!
m_js = re.findall(r'collapsItems\[.*?\]\s*=\s*[\'"](.*?)[\'"];', html)
print(f"Total collapsItems JS strings: {len(m_js)}")
if m_js:
    for s in m_js:
        if 'href' in s:
            print("Found href inside collapsItems JS string:")
            js_hrefs = re.findall(r'href=\\?[\'"]([^\'"]+)\\?[\'"]', s)
            for jh in js_hrefs[:10]:
                print("   JS href:", jh)
            break
