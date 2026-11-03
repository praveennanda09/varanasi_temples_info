# repack_archive.py
import os
import zipfile
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

zip_filename = 'Kashi_Complete_Offline_Pilgrimage_Archive.zip'
print(f"Repackaging complete offline archive into {zip_filename}...")

files_to_include_in_root = [
    'Kashi_Dwadasa_Adityas_Complete_Mirror.pdf',
    'Kashi_Dwadasa_Adityas_Complete_Mirror.html',
    'Kashi_Bhairav_Temples_Complete_Mirror.pdf',
    'Kashi_Bhairav_Temples_Complete_Mirror.html',
    'Kashi_Devi_Temples_Complete_Mirror.pdf',
    'Kashi_Devi_Temples_Complete_Mirror.html',
    'Kashi_Main_Shiva_Temples_Complete_Mirror.pdf',
    'Kashi_Main_Shiva_Temples_Complete_Mirror.html',
    'Kashi_Main_Ganesh_Temples_Complete_Mirror.pdf',
    'Kashi_Main_Ganesh_Temples_Complete_Mirror.html',
    'Kashi_Main_Vishnu_Temples_Complete_Mirror.pdf',
    'Kashi_Main_Vishnu_Temples_Complete_Mirror.html',
    'Kashi_Ganga_and_Teerths_Complete_Mirror.pdf',
    'Kashi_Ganga_and_Teerths_Complete_Mirror.html',
    'shiva_temples_extracted.json',
    'ganesh_temples_extracted.json',
    'vishnu_temples_extracted.json',
    'ganga_teerths_extracted.json',
    'Kashi_Pilgrimage_Master_Index.html',
    '01_Surya_Dwadasa_Aditya.html',
    '02_Bhairav_Temples.html',
    '03_Devi_and_Dashamaha_Vidya.html',
    '04_Shiva_and_Kashi_Jyotirlingas.html',
    '05_Vinayaka_Temples.html',
    '06_Vishnu_Temples.html',
    'temples_master.json',
    'temples_master.csv',
    'crawl_manifest.csv',
    'crawl_manifest.json',
    'missing_data_report.csv',
    'missing_images_report.csv',
    'external_asset_hosts.csv',
    'validation_report.json',
    'README_OFFLINE.txt',
    'local_server.py',
]

folders_to_include = [
    'assets',
    'Kashi_Exact_Offline_Website'
]

BASE_DIR = os.path.abspath('.')
temp_zip = 'Kashi_Complete_Offline_Pilgrimage_Archive_tmp.zip'

start_time = time.time()
with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    # 1. Add root files
    for fname in files_to_include_in_root:
        if os.path.exists(fname):
            zipf.write(fname, arcname=fname)
            print(f"Added root file: {fname}")
        else:
            print(f"Warning: {fname} not found for zipping")

    # 2. Add folders
    total_files = 0
    for folder in folders_to_include:
        if os.path.exists(folder):
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, BASE_DIR)
                    zipf.write(full_path, arcname=rel_path)
                    count += 1
            print(f"Added folder '{folder}' ({count} files)")
            total_files += count

# Replace old zip with new zip
if os.path.exists(zip_filename):
    os.remove(zip_filename)
os.rename(temp_zip, zip_filename)

zip_size_mb = round(os.path.getsize(zip_filename) / (1024 * 1024), 2)
elapsed = round(time.time() - start_time, 1)
print(f"\nSUCCESS! Re-created {zip_filename} ({zip_size_mb} MB, {total_files + len(files_to_include_in_root)} total files) in {elapsed}s.")
