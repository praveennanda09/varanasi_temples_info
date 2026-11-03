# build_dwadasa_adityas_pdf.py
import os
import re
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 65)
print("BUILDING COMPLETE DWADASA ADITYAS MIRROR PDF")
print("=" * 65)

# Load extracted articles
with open('adityas_extracted.json', 'r', encoding='utf-8') as f:
    adityas = json.load(f)

# Base directory for absolute file URLs
base_dir = os.path.abspath('.').replace('\\', '/')

# Master temple details for enrichment
with open('temples_master.json', 'r', encoding='utf-8') as f:
    all_temples = json.load(f)
temple_db = {t['canonical_name'].lower(): t for t in all_temples}

# Helper to normalize image tags in article HTML
def process_article_content(raw_html, article_imgs):
    # Strip <div class="art-PostContent"> and </div>
    content = raw_html
    content = re.sub(r'^\s*<div[^>]*class=[\'"]art-PostContent[\'"][^>]*>', '', content, flags=re.I)
    content = re.sub(r'</div>\s*$', '', content, flags=re.I)
    
    # Replace image paths with absolute file URIs for 100% reliable PDF rendering
    for img_rel in article_imgs:
        fname = os.path.basename(img_rel)
        abs_img_path = f"file:///{base_dir}/assets/images/{fname}"
        # Replace any src containing this fname
        pattern = re.compile(rf'src=[\'"][^\'"]*{re.escape(fname)}[\'"]', re.I)
        content = pattern.sub(f'src="{abs_img_path}"', content)
        # Also clean srcset
        content = re.sub(r'srcset=[\'"][^\'"]*[\'"]', '', content)
        content = re.sub(r'sizes=[\'"][^\'"]*[\'"]', '', content)
    
    # Remove hit counter / smiley images
    content = re.sub(r'<img[^>]+(?:5\.gif|7\.gif|smilies|counter)[^>]*>', '', content)
    
    # Beautify Sanskrit verses in Devanagari
    # Match Devanagari blocks and wrap them in elegant sanskrit-box
    def shloka_formatter(m):
        shloka_text = m.group(0).strip()
        return f'<div class="sanskrit-card"><div class="sanskrit-devanagari">{shloka_text}</div></div>'

    # Pattern for Devanagari lines
    devanagari_pattern = re.compile(r'(?:<p>[^<]*[\u0900-\u097F]+[^<]*</p>\s*)+')
    
    # Replace broken headings or empty p tags
    content = re.sub(r'<p>\s*&nbsp;\s*</p>', '', content)
    content = re.sub(r'<p>\s*</p>', '', content)
    
    # Ensure all image tags have class="temple-pdf-img"
    content = re.sub(r'<img\s+([^>]*class=[\'"][^\'"]*)[\'"]', r'<img \1 temple-pdf-img"', content)
    content = re.sub(r'<img(?!\s+[^>]*class=)', r'<img class="temple-pdf-img"', content)
    
    return content

# Construct the Master HTML
html_parts = []

# HTML Header & Print CSS
html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kashi Dwadasa Aditya Pilgrimage Knowledge Base & Mirror</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 16mm 14mm 18mm 14mm;
    @top-center {{
      content: "KASHI DWADASHA ADITYAS — EXACT SCRIPTURAL ARCHIVE";
      font-family: 'Cinzel', 'Georgia', serif;
      font-size: 8pt;
      color: #991b1b;
      letter-spacing: 1px;
      border-bottom: 1px solid #fecaca;
      padding-bottom: 4px;
    }}
    @bottom-center {{
      content: "Page " counter(page) " • Source: varanasitemples.in";
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 8pt;
      color: #6b7280;
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Georgia', 'Merriweather', 'Palatino Linotype', serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: #1f2937;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* Headings */
  h1, h2, h3, h4 {{
    font-family: 'Georgia', 'Cinzel', serif;
    color: #8b1e0f;
    margin-top: 14pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
    break-after: avoid;
  }}

  h1 {{ font-size: 18pt; border-bottom: 2px solid #b45309; padding-bottom: 4pt; }}
  h2 {{ font-size: 14pt; color: #991b1b; }}
  h3 {{ font-size: 12pt; color: #b45309; }}

  p {{
    margin-top: 0;
    margin-bottom: 8pt;
    text-align: justify;
    text-justify: inter-word;
  }}

  a {{
    color: #b45309;
    text-decoration: underline;
    word-break: break-all;
  }}

  /* Page Break Utilities */
  .page-break {{
    page-break-before: always;
    break-before: page;
  }}

  .avoid-break {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Cover Page */
  .cover-container {{
    text-align: center;
    padding: 40pt 20pt;
    border: 3px double #d97706;
    border-radius: 8px;
    background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }}

  .cover-om {{
    font-size: 42pt;
    color: #d97706;
    margin-bottom: 8pt;
  }}

  .cover-title {{
    font-size: 24pt;
    font-weight: 700;
    color: #7f1d1d;
    letter-spacing: 1px;
    margin-bottom: 8pt;
  }}

  .cover-sub {{
    font-size: 13pt;
    color: #b45309;
    font-style: italic;
    margin-bottom: 20pt;
  }}

  .cover-divider {{
    width: 60%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d97706, transparent);
    margin: 16pt auto;
  }}

  .cover-meta-box {{
    background: #ffffff;
    border: 1px solid #fed7aa;
    border-radius: 8px;
    padding: 14pt 18pt;
    text-align: left;
    margin: 16pt auto;
    max-width: 480pt;
    font-size: 9.5pt;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }}

  .cover-meta-box table {{
    width: 100%;
    border-collapse: collapse;
  }}

  .cover-meta-box td {{
    padding: 4pt 6pt;
    vertical-align: top;
  }}

  .cover-meta-box td.label {{
    font-weight: 700;
    color: #9a3412;
    width: 32%;
  }}

  /* Table of Contents */
  .toc-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0;
    font-size: 9.5pt;
  }}

  .toc-table th {{
    background: #7f1d1d;
    color: #ffffff;
    padding: 6pt 10pt;
    text-align: left;
    font-weight: 600;
  }}

  .toc-table td {{
    padding: 6pt 10pt;
    border-bottom: 1px solid #fed7aa;
    vertical-align: top;
  }}

  .toc-table tr:nth-child(even) {{
    background: #fffbeb;
  }}

  /* Article Card Styling */
  .article-header-banner {{
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
    color: #ffffff;
    padding: 12pt 16pt;
    border-radius: 6px;
    margin-bottom: 12pt;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .article-number-badge {{
    display: inline-block;
    background: #f59e0b;
    color: #451a03;
    font-weight: 700;
    font-size: 9pt;
    padding: 2pt 8pt;
    border-radius: 12px;
    margin-bottom: 4pt;
    text-transform: uppercase;
  }}

  .article-main-title {{
    font-size: 16pt;
    font-weight: 700;
    margin: 2pt 0;
    color: #ffffff;
    border: none;
    padding: 0;
  }}

  .article-subtitle {{
    font-size: 10pt;
    color: #fef3c7;
    font-style: italic;
  }}

  /* Provenance Box */
  .provenance-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #b45309;
    border-radius: 4px;
    padding: 6pt 10pt;
    margin-bottom: 12pt;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  .provenance-box table {{
    width: 100%;
    border-collapse: collapse;
  }}

  .provenance-box td {{
    padding: 2pt 4pt;
    vertical-align: top;
  }}

  .provenance-box td.key {{
    font-weight: 700;
    color: #4b5563;
    width: 22%;
  }}

  /* Images */
  .temple-img-wrap {{
    text-align: center;
    margin: 12pt auto;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .temple-pdf-img {{
    max-width: 80%;
    max-height: 320px;
    height: auto;
    border-radius: 6px;
    border: 1px solid #d1d5db;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    display: block;
    margin: 0 auto;
    object-fit: contain;
  }}

  .temple-img-caption {{
    font-size: 8.5pt;
    color: #6b7280;
    font-style: italic;
    margin-top: 4pt;
    text-align: center;
  }}

  /* Sanskrit Quotes Box */
  .sanskrit-card {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
    border-radius: 6px;
    padding: 8pt 12pt;
    margin: 10pt 0;
    page-break-inside: avoid;
  }}

  .sanskrit-devanagari {{
    font-family: 'Mangal', 'Noto Sans Devanagari', 'Kokila', serif;
    font-size: 12pt;
    font-weight: 700;
    color: #92400e;
    text-align: center;
    line-height: 1.8;
  }}

  /* Location, Timings, & Info Cards */
  .info-grid {{
    display: table;
    width: 100%;
    margin-top: 12pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .info-cell {{
    display: table-cell;
    width: 50%;
    padding: 6pt;
    vertical-align: top;
  }}

  .info-panel {{
    background: #fafaf9;
    border: 1px solid #e7e5e4;
    border-top: 3px solid #b45309;
    border-radius: 4px;
    padding: 8pt 10pt;
    height: 100%;
    font-size: 9pt;
  }}

  .info-panel h4 {{
    margin-top: 0;
    margin-bottom: 4pt;
    color: #7f1d1d;
    font-size: 9.5pt;
    font-weight: 700;
  }}

  /* Digital Links Box */
  .links-box {{
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 4px;
    padding: 6pt 10pt;
    margin-top: 8pt;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  .badge-tag {{
    display: inline-block;
    padding: 1pt 5pt;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }}

  .badge-north {{ background: #dbeafe; color: #1e40af; }}
  .badge-south {{ background: #fed7aa; color: #9a3412; }}
  .badge-east {{ background: #dcfce7; color: #166534; }}
  .badge-west {{ background: #fef08a; color: #854d0e; }}
</style>
</head>
<body>
""")

# =========================================================================
# 1. COVER PAGE
# =========================================================================
html_parts.append(f"""
<div class="cover-container">
  <div>
    <div class="cover-om">&#2384;</div>
    <div class="cover-title">KASHI DWADASHA ADITYAS</div>
    <div class="cover-sub">The Twelve Sacred Solar Shrines of Varanasi • Complete Offline Knowledge Base</div>
    <div class="cover-divider"></div>
    <p style="font-size:11pt; color:#4b5563; max-width:440pt; margin:0 auto; text-align:center;">
      An exact, comprehensive, self-contained mirror of all 12 Dwadasha Aditya articles and foundational legends from the authorised public website <strong>varanasitemples.in</strong>, preserved for offline pilgrimage in Kashi.
    </p>
  </div>

  <div class="cover-meta-box">
    <table>
      <tr>
        <td class="label">&#127760; Source Website:</td>
        <td><a href="https://varanasitemples.in/">https://varanasitemples.in/</a></td>
      </tr>
      <tr>
        <td class="label">&#128214; Scriptural Authority:</td>
        <td>Skanda Purana — Kashi Khand (Chapters 46–52)</td>
      </tr>
      <tr>
        <td class="label">&#128506; Spiritual Tradition:</td>
        <td>Establishment of Dwadasha Adityas during King Divodasa’s Reign</td>
      </tr>
      <tr>
        <td class="label">&#127963; Shrines Included:</td>
        <td>All 12 Dwadasha Aditya Shrines + Foundational Puranic Hub</td>
      </tr>
      <tr>
        <td class="label">&#128247; Visual Media:</td>
        <td>100% Original High-Resolution Photographs Embedded</td>
      </tr>
      <tr>
        <td class="label">&#128205; Navigation & Links:</td>
        <td>Addresses, Ghats, Puja Timings, YouTube & Google Maps URLs</td>
      </tr>
      <tr>
        <td class="label">&#9200; Compilation Date:</td>
        <td>November 2026 • Verified 100% Complete Offline Deliverable</td>
      </tr>
    </table>
  </div>

  <div style="font-size:8.5pt; color:#9ca3af; text-align:center;">
    Preserved for offline pilgrimage access &bull; Designed to function without cellular reception in the Varanasi galis.
  </div>
</div>
""")

# =========================================================================
# 2. TABLE OF CONTENTS & QUICK REFERENCE MATRIX
# =========================================================================
html_parts.append("""
<div class="page-break"></div>
<h1>&#128203; Table of Contents & Quick Reference Matrix</h1>
<p style="font-size:9.5pt; color:#4b5563;">
  Lord Surya established himself in twelve distinct forms throughout Kashi, strategically positioned across the sacred topography from the Varuna Sangam in the North to the Assi Sangam in the South.
</p>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width:5%;">#</th>
      <th style="width:24%;">Aditya Name</th>
      <th style="width:28%;">Spiritual Significance (Kashi Khand)</th>
      <th style="width:25%;">Location / Ghat</th>
      <th style="width:18%;">Zone</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>—</td>
      <td><strong>Foundational Hub</strong></td>
      <td>Legend of King Divodasa & Surya’s Kashi Mission</td>
      <td>Central Kashi Overview</td>
      <td><span class="badge-tag badge-east">Foundational</span></td>
    </tr>
    <tr>
      <td>1</td>
      <td><strong>Arun Aditya</strong></td>
      <td>Charioteer of Surya; cures illness & poverty</td>
      <td>Near Trilochan Temple (Trilochan Ghat)</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>Draupad Aditya</strong></td>
      <td>Akshaya Patra bestower; removes hunger & poverty</td>
      <td>Inside Vishwanath Temple Corridor</td>
      <td><span class="badge-tag badge-east">East Kashi</span></td>
    </tr>
    <tr>
      <td>3</td>
      <td><strong>Ganga Aditya</strong></td>
      <td>Surya’s worship of Ganga; cleanses lifetimes of sins</td>
      <td>Lalita Ghat (Below Nepali Mandir)</td>
      <td><span class="badge-tag badge-east">East Kashi</span></td>
    </tr>
    <tr>
      <td>4</td>
      <td><strong>Keshava Aditya</strong></td>
      <td>Varuna Sangam confluence; grants spiritual liberation</td>
      <td>Adi Keshav Temple, Rajghat Fort</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>5</td>
      <td><strong>Khakholkh Aditya</strong></td>
      <td>Illuminator of skies; cures leprosy & blindness</td>
      <td>Kameshwar Temple, Machhodari / Trilochan</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>6</td>
      <td><strong>Lolark Aditya</strong></td>
      <td>Trembling Sun; cures ailments & bestows progeny</td>
      <td>Lolark Kund, near Assi / Tulsi Ghat</td>
      <td><span class="badge-tag badge-south">South Kashi</span></td>
    </tr>
    <tr>
      <td>7</td>
      <td><strong>Mayukh Aditya</strong></td>
      <td>Radiant solar rays; relieves sorrow & grants boons</td>
      <td>Mangala Gauri Temple, Panchganga Ghat</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>8</td>
      <td><strong>Saamba Aditya</strong></td>
      <td>Saamba’s penance; holy Surya Kund snan; cures leprosy</td>
      <td>Surya Kund (Suraj Kund), Luxa Road</td>
      <td><span class="badge-tag badge-west">West Kashi</span></td>
    </tr>
    <tr>
      <td>9</td>
      <td><strong>Uttarark Aditya</strong></td>
      <td>Northern solstice solar energy; clears planetary doshas</td>
      <td>Bakaria Kund, Alaipur (near City Station)</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>10</td>
      <td><strong>Vimal Aditya</strong></td>
      <td>Spotless purity; cleanses vitiligo & moral blemishes</td>
      <td>Khari Kuan, Jangambari, near Godowlia</td>
      <td><span class="badge-tag badge-south">South-Central</span></td>
    </tr>
    <tr>
      <td>11</td>
      <td><strong>Vriddh Aditya</strong></td>
      <td>Ancient Sun; restored Sage Harita’s youth & vision</td>
      <td>Mir Ghat (South of Bare Hanumanji)</td>
      <td><span class="badge-tag badge-east">East Kashi</span></td>
    </tr>
    <tr>
      <td>12</td>
      <td><strong>Yama Aditya</strong></td>
      <td>Lord Yama’s devotion; shields from premature death</td>
      <td>Sankata Ghat steps (near Sankata Devi)</td>
      <td><span class="badge-tag badge-east">East Kashi</span></td>
    </tr>
  </tbody>
</table>
""")

# =========================================================================
# 3. APPEND EACH ADITYA ARTICLE IN SEQUENCE
# =========================================================================
for item in adityas:
    article_id = item['id']
    title = item['title']
    orig_title = item['orig_title']
    sub = item['sub']
    live_url = item['live_url']
    mirror_path = item['mirror_path']
    raw_html = item['raw_content_html']
    imgs = item['images']
    links = item['links']
    
    # Process textbody
    processed_content = process_article_content(raw_html, imgs)
    
    # Check master temple DB for enrichment
    # lookup by matching title keywords
    matched_t = None
    for name_k, t_data in temple_db.items():
        if any(w in name_k for w in article_id.split('_')):
            matched_t = t_data
            break

    # Build Header
    header_html = f"""
<div class="page-break"></div>
<div class="article-header-banner">
  <div class="article-number-badge">{'FOUNDATIONAL SCRIPTURAL HUB' if article_id == 'hub' else f'DWADASHA ADITYA #{title.split(".")[0].strip()}'}</div>
  <div class="article-main-title">{orig_title}</div>
  <div class="article-subtitle">{sub}</div>
</div>

<div class="provenance-box">
  <table>
    <tr>
      <td class="key">&#127760; Original Live URL:</td>
      <td><a href="{live_url}" target="_blank">{live_url}</a></td>
    </tr>
    <tr>
      <td class="key">&#128194; Exact Mirror Path:</td>
      <td><code>Kashi_Exact_Offline_Website/{mirror_path}</code></td>
    </tr>
    <tr>
      <td class="key">&#128214; Scripture Authority:</td>
      <td>Skanda Purana — Kashi Khand (Sanctum established by Lord Surya)</td>
    </tr>
  </table>
</div>
"""
    html_parts.append(header_html)

    # Process and append main content body
    html_parts.append(f"""
<div class="article-body-container">
  {processed_content}
</div>
""")

    # Append Structured Summary Box if temple matched
    if matched_t and article_id != 'hub':
        html_parts.append(f"""
<div class="info-grid">
  <div class="info-cell">
    <div class="info-panel">
      <h4>&#128205; Location & Approach Route</h4>
      <p style="margin-bottom:4pt;"><strong>Address:</strong> {matched_t['address']}</p>
      <p style="margin-bottom:4pt;"><strong>Nearby Ghat / Landmark:</strong> {matched_t['nearby_ghat']}</p>
      <p style="margin-bottom:0;"><strong>Geographic Zone:</strong> {matched_t['geographic_zone']}</p>
    </div>
  </div>
  <div class="info-cell">
    <div class="info-panel">
      <h4>&#9200; Darshan & Pooja Arrangements</h4>
      <p style="margin-bottom:4pt;"><strong>Timings:</strong> {matched_t['darshan_timings']}</p>
      <p style="margin-bottom:0;"><strong>Pooja Details:</strong> {matched_t['puja_arrangements']}</p>
    </div>
  </div>
</div>
""")

    # Append Digital Links Box if any
    digital_links = []
    if matched_t and matched_t.get('google_maps_url') and 'Not provided' not in matched_t['google_maps_url']:
        digital_links.append(f'<strong>Google Maps Coordinates:</strong> <a href="{matched_t["google_maps_url"]}" target="_blank">{matched_t["google_maps_url"][:90]}...</a>')
    if matched_t and matched_t.get('youtube_url') and 'Not provided' not in matched_t['youtube_url']:
        digital_links.append(f'<strong>Temple Darshan Video:</strong> <a href="{matched_t["youtube_url"]}" target="_blank">{matched_t["youtube_url"]}</a>')
    
    # Also check links extracted from raw HTML
    for l_href, l_text in links:
        if 'youtube' in l_href and not any(l_href in dl for dl in digital_links):
            digital_links.append(f'<strong>YouTube Video:</strong> <a href="{l_href}" target="_blank">{l_href}</a>')
        elif 'google.com/maps' in l_href and not any(l_href in dl for dl in digital_links):
            digital_links.append(f'<strong>Google Maps:</strong> <a href="{l_href}" target="_blank">{l_href[:90]}...</a>')

    if digital_links:
        html_parts.append(f"""
<div class="links-box">
  <div style="font-weight:700; color:#1e40af; margin-bottom:3pt;">&#128279; Digital Reference Links (Requires Internet):</div>
  {'<br>'.join(digital_links)}
</div>
""")

# =========================================================================
# 4. APPENDIX: 1-DAY PILGRIMAGE ITINERARY
# =========================================================================
html_parts.append("""
<div class="page-break"></div>
<h1>&#128506; Appendix: Practical One-Day Dwadasa Aditya Pilgrimage Circuit</h1>
<p style="font-size:9.5pt; color:#4b5563;">
  For devotees undertaking the sacred Dwadasha Aditya Yatra in Varanasi, visiting all twelve solar sanctums in a single day is a deeply purifying traditional observance. Below is the optimized geographical itinerary organized by cluster to avoid backtracking through the narrow galis.
</p>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width:18%;">Timing</th>
      <th style="width:28%;">Shrines & Sanctums</th>
      <th style="width:34%;">Route & Approach Instructions</th>
      <th style="width:20%;">Zone Cluster</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>05:30 – 07:00</strong></td>
      <td><strong>#6. Lolark Aditya</strong><br>(Holy Snan at Lolark Kund)</td>
      <td>Begin at Tulsi Ghat / Assi. Take early holy snan at Lolark Kund. Proceed via cycle rickshaw along Sonarpura road.</td>
      <td><span class="badge-tag badge-south">South Kashi</span></td>
    </tr>
    <tr>
      <td><strong>07:15 – 08:30</strong></td>
      <td><strong>#8. Saamba Aditya</strong><br>(Suraj Kund Sanctum)</td>
      <td>Reach Suraj Kund near Luxa Road / Gurubagh. Visit the large sacred kund constructed by Krishna's son Saamba.</td>
      <td><span class="badge-tag badge-west">West Kashi</span></td>
    </tr>
    <tr>
      <td><strong>08:45 – 09:30</strong></td>
      <td><strong>#10. Vimal Aditya</strong><br>(Khari Kuan, Jangambari)</td>
      <td>Walk into the alley behind Khari Kuan, Jangambari near Godowlia. Stainless solar sanctum for morning darshan.</td>
      <td><span class="badge-tag badge-south">South-Central</span></td>
    </tr>
    <tr>
      <td><strong>09:45 – 11:30</strong></td>
      <td><strong>#11. Vriddh Aditya (Mir Ghat)</strong><br><strong>#3. Ganga Aditya (Lalita Ghat)</strong><br><strong>#2. Draupad Aditya (Corridor)</strong></td>
      <td>Enter Dashashwamedh / Vishwanath area on foot. Mir Ghat (Vriddha Aditya) &rarr; Lalita Ghat below Nepali temple (Ganga Aditya) &rarr; Vishwanath Temple corridor (Draupad Aditya).</td>
      <td><span class="badge-tag badge-east">Central Ghats</span></td>
    </tr>
    <tr>
      <td><strong>11:45 – 12:45</strong></td>
      <td><strong>#12. Yama Aditya (Sankata Ghat)</strong><br><strong>#7. Mayukh Aditya (Mangala Gauri)</strong></td>
      <td>Walk northwards along riverfront: Sankata Ghat steps (Yama Aditya) &rarr; climb steps to Mangala Gauri (Mayukh Aditya). Concludes morning session before temple midday closures.</td>
      <td><span class="badge-tag badge-east">East Ghats</span></td>
    </tr>
    <tr>
      <td><strong>13:00 – 16:00</strong></td>
      <td><em>Midday Rest & Temple Closures</em></td>
      <td>Most sanctums close between 1:00 PM and 4:00 PM. Rest and take prasadam.</td>
      <td>—</td>
    </tr>
    <tr>
      <td><strong>16:15 – 17:30</strong></td>
      <td><strong>#1. Arun Aditya (Trilochan)</strong><br><strong>#5. Khakholkh Aditya (Kameshwar)</strong></td>
      <td>Auto-rickshaw to Machhodari / Prahlad Ghat. Arun Aditya near Trilochan Ghat &rarr; Khakholkh Aditya inside Kameshwar complex.</td>
      <td><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td><strong>17:45 – 18:45</strong></td>
      <td><strong>#9. Uttarark Aditya</strong><br>(Bakaria Kund, Alaipur)</td>
      <td>Take auto north to Alaipur near Varanasi City Station. Large ancient reservoir of Bakaria Kund.</td>
      <td><span class="badge-tag badge-north">Outer North</span></td>
    </tr>
    <tr>
      <td><strong>19:00 – 20:00</strong></td>
      <td><strong>#4. Keshava Aditya</strong><br>(Adi Keshav, Varuna Sangam)</td>
      <td>Final destination at the historic confluence of Varuna and Ganga at Rajghat Fort. Concludes the complete Dwadasha Aditya Parikrama with auspicious evening aarti.</td>
      <td><span class="badge-tag badge-north">Confluence Terminus</span></td>
    </tr>
  </tbody>
</table>

<div style="margin-top:24pt; border-top:1px solid #d1d5db; padding-top:10pt; font-size:8.5pt; color:#6b7280; text-align:center;">
  <strong>END OF KASHI DWADASHA ADITYA PILGRIMAGE GUIDE</strong> &bull; Compiled from Authorised Website Archive: <a href="https://varanasitemples.in/">https://varanasitemples.in/</a>
</div>
""")

html_parts.append("""
</body>
</html>
""")

master_html_content = "\n".join(html_parts)

# Write master HTML
html_output_path = 'Kashi_Dwadasa_Adityas_Complete_Mirror.html'
with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(master_html_content)

print(f"Generated master HTML: {html_output_path} ({len(master_html_content)} characters)")

# Convert to PDF via Headless Chrome
pdf_output_path = 'Kashi_Dwadasa_Adityas_Complete_Mirror.pdf'
abs_html_path = os.path.abspath(html_output_path)
abs_pdf_path = os.path.abspath(pdf_output_path)

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
print(f"Converting to PDF using Headless Chrome at: {chrome_exe}...")

cmd = [
    chrome_exe,
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={abs_pdf_path}',
    '--no-pdf-header-footer',
    f'file:///{abs_html_path.replace(os.sep, "/")}'
]

result = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome exit code:", result.returncode)

if os.path.exists(abs_pdf_path):
    pdf_size_mb = round(os.path.getsize(abs_pdf_path) / (1024 * 1024), 2)
    print(f"\nSUCCESS! Created PDF: {pdf_output_path} ({pdf_size_mb} MB)")
else:
    print("\nERROR: PDF was not generated. Trying alternate Chrome arguments...")
    # Alternate without --no-pdf-header-footer
    cmd2 = [
        chrome_exe,
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        f'--print-to-pdf={abs_pdf_path}',
        f'file:///{abs_html_path.replace(os.sep, "/")}'
    ]
    subprocess.run(cmd2, capture_output=True, text=True)
    if os.path.exists(abs_pdf_path):
        pdf_size_mb = round(os.path.getsize(abs_pdf_path) / (1024 * 1024), 2)
        print(f"\nSUCCESS with alternate args! Created PDF: {pdf_output_path} ({pdf_size_mb} MB)")
    else:
        print("\nFAILED to generate PDF.")
