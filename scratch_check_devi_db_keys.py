import sys
import master_temples_coordinates as mtc

sys.stdout.reconfigure(encoding='utf-8')

print("All keys in mtc.COORDINATES_DB:")
for k, v in mtc.COORDINATES_DB.items():
    if any(term in k for term in ['gauri', 'devi', 'durga', 'lakshmi', 'shail', 'brahma', 'chandra', 'kushmanda', 'skanda', 'katya', 'kalratri', 'annapurna', 'siddhi', 'vishal', 'sankata', 'tara', 'bhuvana', 'chinna', 'dhumavati', 'bagalamukhi', 'matangi', 'kamala', 'tri', 'kali', 'varahi', 'chamunda', 'bandi', 'chandi', 'charma', 'chitra', 'hayakanti', 'vindhya', 'vishwa']):
        print(f"  '{k}': {v['hindi']}")
