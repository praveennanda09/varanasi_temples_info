# inspect_collaps_detailed.py
import re

with open('Kashi_Exact_Offline_Website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all occurrences of varanasitemples.in anywhere in index.html
all_occurrences = re.findall(r'https?://(?:www\.)?varanasitemples\.in[^\s\'"\\<>]*', html)
print(f"Total occurrences of varanasitemples.in in index.html: {len(all_occurrences)}")
print(f"Unique URLs: {len(set(all_occurrences))}")

for u in list(set(all_occurrences))[:20]:
    print(" ", u)
