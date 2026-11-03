import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('devis_extracted.json', 'r', encoding='utf-8') as f:
    devis = json.load(f)

print("First devi keys:", list(devis[0].keys()))
for i, d in enumerate(devis):
    print(f"{i+1}. name='{d.get('name')}', orig_title='{d.get('orig_title')}', temple_name='{d.get('temple_name')}'")
