import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 65)
print("FINAL VALIDATION OF ALL 7 PILGRIMAGE GUIDES (HTML & PDF)")
print("=" * 65)

guides = [
    ("Kashi_Dwadasa_Adityas_Complete_Mirror.html", "Kashi_Dwadasa_Adityas_Complete_Mirror.pdf", "Map_Dwadasa_Adityas.svg", 12),
    ("Kashi_Bhairav_Temples_Complete_Mirror.html", "Kashi_Bhairav_Temples_Complete_Mirror.pdf", "Map_Bhairav_Temples.svg", 10),
    ("Kashi_Devi_Temples_Complete_Mirror.html", "Kashi_Devi_Temples_Complete_Mirror.pdf", "Map_Devi_Temples.svg", 32),
    ("Kashi_Main_Shiva_Temples_Complete_Mirror.html", "Kashi_Main_Shiva_Temples_Complete_Mirror.pdf", "Map_Main_Shiva_Temples.svg", 23),
    ("Kashi_Main_Ganesh_Temples_Complete_Mirror.html", "Kashi_Main_Ganesh_Temples_Complete_Mirror.pdf", "Map_Main_Ganesh_Temples.svg", 10),
    ("Kashi_Main_Vishnu_Temples_Complete_Mirror.html", "Kashi_Main_Vishnu_Temples_Complete_Mirror.pdf", "Map_Main_Vishnu_Temples.svg", 30),
    ("Kashi_Ganga_and_Teerths_Complete_Mirror.html", "Kashi_Ganga_and_Teerths_Complete_Mirror.pdf", "Map_Ganga_and_Teerths.svg", 14),
]

all_passed = True

for html_file, pdf_file, map_svg, min_pins in guides:
    print(f"\n--- Checking: {pdf_file} ---")
    if not os.path.exists(pdf_file) or os.path.getsize(pdf_file) == 0:
        print(f"  [FAIL] PDF file missing or empty: {pdf_file}")
        all_passed = False
        continue
    pdf_mb = round(os.path.getsize(pdf_file) / (1024 * 1024), 2)
    print(f"  [+] PDF exists: {pdf_mb} MB")

    if not os.path.exists(html_file):
        print(f"  [FAIL] HTML file missing: {html_file}")
        all_passed = False
        continue

    with open(html_file, 'r', encoding='utf-8') as f:
        html_text = f.read()

    # Check for GPS Pin cards
    gps_card_count = html_text.count("VERIFIED EXACT GPS PINPOINT")
    print(f"  [+] Temple GPS Pinpoint cards found: {gps_card_count} (Expected >= {min_pins})")
    if gps_card_count < min_pins:
        print(f"  [WARN] Expected at least {min_pins} GPS cards, got {gps_card_count}")
        all_passed = False

    # Check for Map SVG Plate
    if map_svg in html_text:
        print(f"  [+] Visual Map SVG Plate referenced: {map_svg}")
    else:
        print(f"  [FAIL] Visual Map SVG Plate NOT found in HTML: {map_svg}")
        all_passed = False

    # Check for Master Directory Table
    if "Master GPS Pinpoint &amp; Direct Navigation Directory" in html_text or "Master GPS Pinpoint & Direct Navigation Directory" in html_text:
        print(f"  [+] Master GPS Navigation Directory Table found at end of document")
    else:
        print(f"  [FAIL] Master GPS Navigation Directory Table NOT found")
        all_passed = False

    # Check for Google Maps Links
    gmaps_links = len(re.findall(r'google\.com/maps', html_text))
    print(f"  [+] Total Google Maps URLs embedded: {gmaps_links}")

if all_passed:
    print("\n" + "=" * 65)
    print("ALL 7 PILGRIMAGE DELIVERABLES 100% VERIFIED & COMPLIANT!")
    print("=" * 65)
else:
    print("\n[!] Some checks failed.")
