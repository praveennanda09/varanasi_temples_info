# Kashi Offline Guide Pack

An offline reference library for exploring temples, pilgrimage routes, and related sites in Kashi (Varanasi). The pack includes a locally browsable mirror, six deity-focused guides, printable PDFs, structured temple data, and the scripts and audit reports used to build and validate the collection.

> **Attribution:** The archived website content and photographs are credited to [varanasitemples.in](https://varanasitemples.in/). Refer to the included archive notes for the stated authorization and usage context.

## Start the guides

### Master pilgrimage index

With Python 3 installed, open a terminal in this folder and start a simple local server:

```powershell
python -m http.server 8080
```

Then open <http://localhost:8080/Kashi_Pilgrimage_Master_Index.html>. Stop the server with Ctrl+C.

### Exact offline website mirror

Run the included server from the website folder:

```powershell
python Kashi_Exact_Offline_Website/local_server.py
```

Then open <http://localhost:8080/index.html>. This server uses Python's standard library and needs no package installation or internet connection. If port 8080 is already in use, stop the other server first.

You can also open the HTML files directly in a browser. A local server is recommended for more consistent behavior with browser features and relative links.

## Contents

- `Kashi_Pilgrimage_Master_Index.html` — interactive index with guide links, search, geographic zones, and itinerary.
- `01_Surya_Dwadasa_Aditya.html` through `06_Vishnu_Temples.html` — six browsable deity-specific guides.
- `Kashi_*_Complete_Mirror.html` and matching PDFs — temple and pilgrimage reference editions.
- `Kashi_Exact_Offline_Website/` — website mirror, downloaded assets, category and article pages, and its local server.
- `*_Guide.md`, `MASTER_INDEX.md`, and `README_OFFLINE.txt` — text guides, archive notes, and methodology.
- `temples_master.csv` / `temples_master.json` — consolidated temple data.
- `crawl_manifest.*`, `visited_urls.txt`, and validation/missing-data reports — crawl and quality-audit records.
- Python scripts — extraction, database, mirror-building, download, and validation utilities.

## Geographic zones

The guides group locations into North, South, East (riverfront and ghats), and West Kashi to help with itinerary planning. Treat the zones as a planning aid; verify current opening times, access, and local conditions before travelling.

## Notes

- The collection is designed for offline reference; some pages may still contain external links or assets that are not included locally.
- Data and reports describe the archive/build state and may be incomplete or out of date. Check with local sources for current travel information.
- The full archive ZIP is stored with Git LFS because it exceeds GitHub's 100 MB per-file limit. Git LFS availability and quota may affect cloning or downloading that file; the browsable files are also included in the repository.
- Build and crawl scripts are provided as project artifacts. Some may require third-party Python packages or internet access; the local web servers do not.
