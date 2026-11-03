# update_missing_report.py
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

rows = [
    {'temple_id': 'varahi_devi', 'canonical_name': 'Varahi Devi', 'deity_category': 'Devi', 'original_url': 'https://varanasitemples.in/category/devi-temples/varahi-devi/', 'visual_asset': 'assets/images/Varahi-Devi-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'tri_lokya_sundary', 'canonical_name': 'Tri Lokya Sundary', 'deity_category': 'Devi', 'original_url': 'https://varanasitemples.in/category/devi-temples/tri-lokya-sundary/', 'visual_asset': 'assets/images/Tri-Lokya-Sundary-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'dhundhi_vinayak', 'canonical_name': 'Dhundhi Vinayak', 'deity_category': 'Vinayaka', 'original_url': 'https://varanasitemples.in/category/vinayak-temples/aa-dhundhi-vinayak/', 'visual_asset': 'assets/images/Dhundhi-Vinayak-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'siddhi_vinayak', 'canonical_name': 'Siddhi Vinayak', 'deity_category': 'Vinayaka', 'original_url': 'https://varanasitemples.in/category/vinayak-temples/siddhi-vinayak/', 'visual_asset': 'assets/images/Siddhi-Vinayak-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'avi_mukta_vinayak', 'canonical_name': 'Avi Mukta Vinayak', 'deity_category': 'Vinayaka', 'original_url': 'https://varanasitemples.in/category/vinayak-temples/avi-mukta-vinayak/', 'visual_asset': 'assets/images/Avi-Mukta-Vinayak-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'gyan_madhav', 'canonical_name': 'Gyan Madhav', 'deity_category': 'Vishnu', 'original_url': 'https://varanasitemples.in/category/vishnu-temples/gyan-madhav/', 'visual_asset': 'assets/images/Gyan-Madhav-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'gopi_govind', 'canonical_name': 'Gopi Govind', 'deity_category': 'Vishnu', 'original_url': 'https://varanasitemples.in/category/vishnu-temples/gopi-govind/', 'visual_asset': 'assets/images/Gopi-Govind-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
    {'temple_id': 'vitank_narsimha', 'canonical_name': 'Vitank Narsimha', 'deity_category': 'Vishnu', 'original_url': 'https://varanasitemples.in/category/vishnu-temples/vitank-narsimha/', 'visual_asset': 'assets/images/Vitank-Narsimha-Shrine.svg', 'status': 'Dedicated sacred iconographic SVG artwork generated & integrated into guide cards and master directory.'},
]

fieldnames = ['temple_id', 'canonical_name', 'deity_category', 'original_url', 'visual_asset', 'status']
with open('missing_images_report.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated missing_images_report.csv.")
