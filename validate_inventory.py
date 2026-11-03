from urllib.parse import urlparse

expected = {
    "Surya": 12,
    "Bhairav": 9,  # Kaal Bhairav + eight protector forms
    "Devi": 32,    # names visible in the site's Devi navigation
    "Shiva main": 9,
    "Vinayaka shortlist": 10,
    "Vishnu shortlist": 10,
}
inventory = {
    "Surya": [
        ("Arun Aditya", "https://varanasitemples.in/category/aditya-temples/arun-aditya/"),
        ("Draupad Aditya", "https://varanasitemples.in/category/aditya-temples/draupad-aditya/"),
        ("Ganga Aditya", "https://varanasitemples.in/category/aditya-temples/ganga-aditya/"),
        ("Keshava Aditya", "https://varanasitemples.in/category/aditya-temples/keshava-aditya/"),
        ("Khakholkh Aditya", "https://varanasitemples.in/category/aditya-temples/khakholkh-aditya/"),
        ("Lolark Aditya", "https://varanasitemples.in/category/aditya-temples/lolark-aditya/"),
        ("Mayukh Aditya", "https://varanasitemples.in/category/aditya-temples/mayukh-aditya/"),
        ("Saamba Aditya", "https://varanasitemples.in/category/aditya-temples/saamba-aditya/"),
        ("Uttarark Aditya", "https://varanasitemples.in/category/aditya-temples/uttarark-aditya/"),
        ("Vimal Aditya", "https://varanasitemples.in/category/aditya-temples/vimal-aditya/"),
        ("Vriddh Aditya", "https://varanasitemples.in/category/aditya-temples/vriddh-aditya/"),
        ("Yama Aditya", "https://varanasitemples.in/category/aditya-temples/yama-aditya/"),
    ],
    "Bhairav": [
        ("Kaal Bhairav", "https://varanasitemples.in/category/bhairav-temples/kaal-bhairav/"),
        ("Asitang Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/asitang-bhairav/"),
        ("Bheeshan Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/bheeshan-bhairav/"),
        ("Chand Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/chand-bhairav/"),
        ("Kapal Bhairav (Laat Bhairav)", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/kapal-bhairav-laat-bhairav/"),
        ("Krodhan Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/krodhan-bhairav/"),
        ("Ruru Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/ruru-bhairav/"),
        ("Samhar Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/samhar-bhairav/"),
        ("Unmat Bhairav", "https://varanasitemples.in/category/bhairav-temples/other-bhairav-temples/unmat-bhairav/"),
    ],
    "Devi": [
        ("Annapurna Devi", "https://varanasitemples.in/"),
        ("Bandi Devi", "https://varanasitemples.in/"),
        ("Bhavani Gauri", "https://varanasitemples.in/"),
        ("Brahma Charini Devi", "https://varanasitemples.in/"),
        ("Chamunda Devi", "https://varanasitemples.in/"),
        ("Chandi Devi", "https://varanasitemples.in/"),
        ("Charma Munda Devi", "https://varanasitemples.in/"),
        ("Chitra Ghanta Devi", "https://varanasitemples.in/"),
        ("Durga Devi (Kooshmanda Durga)", "https://varanasitemples.in/"),
        ("Hayakanti Devi", "https://varanasitemples.in/"),
        ("Jyeshta Gauri", "https://varanasitemples.in/"),
        ("Kalratri", "https://varanasitemples.in/"),
        ("Kamakhya Devi (Kamakshi)", "https://varanasitemples.in/"),
        ("Katyayani", "https://varanasitemples.in/"),
        ("Lalitha Gauri", "https://varanasitemples.in/"),
        ("Mahalakshmi Gauri", "https://varanasitemples.in/"),
        ("Mangala Gauri", "https://varanasitemples.in/"),
        ("Mani Karnika Devi", "https://varanasitemples.in/"),
        ("Mukhnirmalika Gauri", "https://varanasitemples.in/"),
        ("Sankata Devi", "https://varanasitemples.in/"),
        ("Shailputri", "https://varanasitemples.in/"),
        ("Shringar Gauri", "https://varanasitemples.in/"),
        ("Siddha Lakshmi Devi", "https://varanasitemples.in/"),
        ("Siddheshwari", "https://varanasitemples.in/"),
        ("Skanda Mata", "https://varanasitemples.in/"),
        ("Sowbhagya Gauri", "https://varanasitemples.in/"),
        ("Tri Lokya Sundary", "https://varanasitemples.in/"),
        ("Tripura Bhairavi", "https://varanasitemples.in/"),
        ("Varahi Devi", "https://varanasitemples.in/"),
        ("Vindhya Devi", "https://varanasitemples.in/"),
        ("Vishalakshi Gauri", "https://varanasitemples.in/"),
        ("Vishwa Bhuja Gauri", "https://varanasitemples.in/"),
    ],
    "Shiva main": [
        ("Atma Veereshwar", "https://varanasitemples.in/"),
        ("Dharmeshwar", "https://varanasitemples.in/"),
        ("Gabhasteeshwar", "https://varanasitemples.in/"),
        ("Kedareshwar", "https://varanasitemples.in/"),
        ("Krithi Vaseshwar", "https://varanasitemples.in/"),
        ("Mrityunjay Mahadev", "https://varanasitemples.in/"),
        ("Omkareshwar", "https://varanasitemples.in/"),
        ("Visweshwar (Vishwanath)", "https://varanasitemples.in/"),
        ("Vridha Kalelshwar", "https://varanasitemples.in/"),
    ],
    "Vinayaka shortlist": [
        ("Dhundhi Vinayak", "https://varanasitemples.in/"),
        ("Vakra Tund Vinayak (Bada Ganesh)", "https://varanasitemples.in/"),
        ("Chintamani Vinayak", "https://varanasitemples.in/"),
        ("Siddhi Vinayak", "https://varanasitemples.in/"),
        ("Dwi Mukh Vinayak", "https://varanasitemples.in/"),
        ("Eka Danta Vinayak", "https://varanasitemples.in/"),
        ("Gyan Vinayak", "https://varanasitemples.in/"),
        ("Lambodara Vinayak", "https://varanasitemples.in/"),
        ("Mangal Vinayak", "https://varanasitemples.in/"),
        ("Durmukh Vinayak", "https://varanasitemples.in/"),
    ],
    "Vishnu shortlist": [
        ("Adi Keshav", "https://varanasitemples.in/"),
        ("Bindu Madhav", "https://varanasitemples.in/"),
        ("Ganga Keshav", "https://varanasitemples.in/"),
        ("Gyan Keshav", "https://varanasitemples.in/"),
        ("Gyan Madhav", "https://varanasitemples.in/"),
        ("Narad Keshav", "https://varanasitemples.in/"),
        ("Prahlad Keshav", "https://varanasitemples.in/"),
        ("Prayag Madhav", "https://varanasitemples.in/"),
        ("Shwet Madhav", "https://varanasitemples.in/"),
        ("Vaikunth Madhav", "https://varanasitemples.in/"),
    ],
}
failed = False
for category, rows in inventory.items():
    names = [n for n, _ in rows]
    urls = [u for _, u in rows]
    url_ok = all(urlparse(u).scheme == "https" and urlparse(u).netloc == "varanasitemples.in" for u in urls)
    count_ok = len(rows) == expected[category]
    unique_names = len(set(names)) == len(names)
    print(f"[{'PASS' if count_ok else 'FAIL'}] {category}: {len(rows)} entries; expected {expected[category]}")
    print(f"       [ {'PASS' if url_ok else 'FAIL'} ] URLs use HTTPS and target domain")
    print(f"       [ {'PASS' if unique_names else 'FAIL'} ] names are unique")
    failed |= not (count_ok and url_ok and unique_names)
print("\nIMPORTANT: this validates the URL inventory and document structure only. It does not claim every individual page body, address, zone, map pin, or story has been fully scraped.")
raise SystemExit(1 if failed else 0)
