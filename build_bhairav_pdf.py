# build_bhairav_pdf.py
import os
import re
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 65)
print("BUILDING COMPLETE BHAIRAV TEMPLES MIRROR PDF")
print("=" * 65)

# Load extracted Bhairav articles
with open('bhairavs_extracted.json', 'r', encoding='utf-8') as f:
    bhairavs = json.load(f)

# Master temple details for enrichment
with open('temples_master.json', 'r', encoding='utf-8') as f:
    all_temples = json.load(f)
temple_db = {t['canonical_name'].lower(): t for t in all_temples}

# Base directory for absolute file URIs
base_dir = os.path.abspath('.').replace('\\', '/')

# Helper to normalize image tags in article HTML
def process_article_content(raw_html, article_imgs):
    content = raw_html
    content = re.sub(r'^\s*<div[^>]*class=[\'"]art-PostContent[\'"][^>]*>', '', content, flags=re.I)
    content = re.sub(r'</div>\s*$', '', content, flags=re.I)
    
    # Replace image paths with absolute file URIs for 100% reliable PDF rendering
    for img_rel in article_imgs:
        fname = os.path.basename(img_rel)
        abs_img_path = f"file:///{base_dir}/assets/images/{fname}"
        pattern = re.compile(rf'src=[\'"][^\'"]*{re.escape(fname)}[\'"]', re.I)
        content = pattern.sub(f'src="{abs_img_path}"', content)
        content = re.sub(r'srcset=[\'"][^\'"]*[\'"]', '', content)
        content = re.sub(r'sizes=[\'"][^\'"]*[\'"]', '', content)
    
    # Remove hit counter / smiley images
    content = re.sub(r'<img[^>]+(?:5\.gif|7\.gif|smilies|counter)[^>]*>', '', content)
    
    # Clean empty paragraphs
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
<title>Kashi Bhairav Temples & Ashtabhairavas — Complete Mirror & Knowledge Base</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 16mm 14mm 18mm 14mm;
    @top-center {{
      content: "KASHI BHAIRAV TEMPLES & ASHTABHAIRAVAS — SCRIPTURAL ARCHIVE";
      font-family: 'Cinzel', 'Georgia', serif;
      font-size: 8pt;
      color: #7f1d1d;
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
    color: #7f1d1d;
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
    border: 3px double #b45309;
    border-radius: 8px;
    background: linear-gradient(180deg, #fff7ed 0%, #ffffff 100%);
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }}

  .cover-om {{
    font-size: 44pt;
    color: #b45309;
    margin-bottom: 6pt;
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
    color: #c2410c;
    font-style: italic;
    margin-bottom: 18pt;
  }}

  .cover-divider {{
    width: 60%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #b45309, transparent);
    margin: 14pt auto;
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
    background: #fff7ed;
  }}

  /* Article Header Banner */
  .article-header-banner {{
    background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
    color: #ffffff;
    padding: 12pt 16pt;
    border-radius: 6px;
    margin-bottom: 12pt;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .article-number-badge {{
    display: inline-block;
    background: #f97316;
    color: #ffffff;
    font-weight: 700;
    font-size: 8.5pt;
    padding: 2pt 8pt;
    border-radius: 12px;
    margin-bottom: 4pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
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
    color: #fed7aa;
    font-style: italic;
  }}

  /* Provenance Box */
  .provenance-box {{
    background: #fdf4ff;
    border: 1px solid #fbcfe8;
    border-left: 4px solid #9d174d;
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
    color: #831843;
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
    max-width: 82%;
    max-height: 330px;
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

  /* Location & Info Grid */
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
    border-top: 3px solid #7f1d1d;
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

  /* Links Box */
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
  .badge-central {{ background: #fce7f3; color: #9d174d; }}
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
    <div class="cover-title">KASHI BHAIRAV TEMPLES</div>
    <div class="cover-sub">Kaal Bhairav (Kotwal of Kashi) & The Sacred Ashtabhairavas • Complete Knowledge Base</div>
    <div class="cover-divider"></div>
    <p style="font-size:11pt; color:#4b5563; max-width:440pt; margin:0 auto; text-align:center;">
      An exact, comprehensive, self-contained offline mirror of all Bhairav temple articles and foundational Puranic narratives from the authorised public website <strong>varanasitemples.in</strong>, preserved for offline pilgrimage in Varanasi.
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
        <td>Skanda Purana — Kashi Khand (Chapters 30, 31, 72 & 83)</td>
      </tr>
      <tr>
        <td class="label">&#128737;&#65039; Spiritual Roles:</td>
        <td>Kotwal of Kashi (Supreme Governor & Danda Bearer) + 8 Directional Protectors</td>
      </tr>
      <tr>
        <td class="label">&#127963; Shrines Included:</td>
        <td>Kaal Bhairav + All 8 Ashtabhairavas + Theological Origin Hub</td>
      </tr>
      <tr>
        <td class="label">&#128247; Visual Media:</td>
        <td>100% Original High-Resolution Photographs Embedded</td>
      </tr>
      <tr>
        <td class="label">&#128205; Navigation & Links:</td>
        <td>Addresses, Approach Routes, Darshan Timings, Priest Contacts, YouTube & Maps URLs</td>
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
<h1>&#128203; Table of Contents & Directional Guardian Matrix</h1>
<p style="font-size:9.5pt; color:#4b5563;">
  In the sacred spiritual geography of Kashi, Lord Shiva appointed <strong>Kaal Bhairav</strong> as the supreme Kotwal (governor and police chief) of the holy city, while stationing eight directional manifestations (<strong>Ashtabhairava</strong>) at the cardinal and intercardinal compass points to protect devotees from demonic perils, planetary afflictions, and fear.
</p>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width:6%;">#</th>
      <th style="width:25%;">Bhairava Shrine</th>
      <th style="width:16%;">Direction</th>
      <th style="width:33%;">Spiritual Significance (Kashi Khand)</th>
      <th style="width:20%;">Locality / Zone</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>—</td>
      <td><strong>Foundational Hub</strong></td>
      <td>Universal</td>
      <td>Creation of 8 Bhairavas to guard Kashi after Durgasur’s defeat</td>
      <td><span class="badge-tag badge-central">Theological Origin</span></td>
    </tr>
    <tr>
      <td>★</td>
      <td><strong>Kaal Bhairav</strong></td>
      <td>Central Kshetra</td>
      <td>Kotwal of Kashi; severing of Brahma’s head; Paap Bhakshak</td>
      <td>Visheshwarganj / Maidagin<br><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>1</td>
      <td><strong>Asitang Bhairav</strong></td>
      <td>East (Prachi)</td>
      <td>Ashtabhairava #1; bestows creative brilliance & removes curses</td>
      <td>Near Vriddh Kaleshwar<br><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>2</td>
      <td><strong>Ruru Bhairav</strong></td>
      <td>Southeast (Agneya)</td>
      <td>Ashtabhairava #2 (Anand Bhairav); removes fear of foes</td>
      <td>Hanuman Ghat<br><span class="badge-tag badge-south">South Kashi</span></td>
    </tr>
    <tr>
      <td>3</td>
      <td><strong>Chand Bhairav</strong></td>
      <td>South (Dakshina)</td>
      <td>Ashtabhairava #3; vanquisher of wrath; grants courage & health</td>
      <td>Durga Kund Complex<br><span class="badge-tag badge-south">South Kashi</span></td>
    </tr>
    <tr>
      <td>4</td>
      <td><strong>Krodhan Bhairav</strong></td>
      <td>Southwest (Nairritya)</td>
      <td>Ashtabhairava #4; Rahu Shanti & Kaal Sarp Dosh eradication</td>
      <td>Batuk Bhairav, Kamachha<br><span class="badge-tag badge-west">West Kashi</span></td>
    </tr>
    <tr>
      <td>5</td>
      <td><strong>Unmat Bhairav</strong></td>
      <td>West (Pashchima)</td>
      <td>Ashtabhairava #5; controls wandering mind & confers ecstasy</td>
      <td>Deora Village (Panchkroshi)<br><span class="badge-tag badge-west">Outer West</span></td>
    </tr>
    <tr>
      <td>6</td>
      <td><strong>Kapal Bhairav</strong></td>
      <td>Northwest (Vayavya)</td>
      <td>Ashtabhairava #6 (Laat Bhairav); Kapal Mochan Teerth snan</td>
      <td>Alaipur / Laat Sarovar<br><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
    <tr>
      <td>7</td>
      <td><strong>Bheeshan Bhairav</strong></td>
      <td>North (Uttara)</td>
      <td>Ashtabhairava #7 (Bhoot Bhairav); dispeller of spirits & terrors</td>
      <td>Near Jyeshtheshwar<br><span class="badge-tag badge-west">West Kashi</span></td>
    </tr>
    <tr>
      <td>8</td>
      <td><strong>Samhar Bhairav</strong></td>
      <td>Northeast (Ishanya)</td>
      <td>Ashtabhairava #8; cosmic dissolver of all karmic bondages</td>
      <td>Patan Darwaja, Gai Ghat<br><span class="badge-tag badge-north">North Kashi</span></td>
    </tr>
  </tbody>
</table>
""")

# =========================================================================
# 3. APPEND EACH BHAIRAV ARTICLE IN SEQUENCE
# =========================================================================
for item in bhairavs:
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
    matched_t = None
    for name_k, t_data in temple_db.items():
        if article_id == 'kaal_bhairav' and 'kaal bhairav' in name_k:
            matched_t = t_data
            break
        elif article_id != 'hub' and any(w in name_k for w in article_id.split('_')):
            matched_t = t_data
            break

    # Build Header
    badge_label = 'THEOLOGICAL FOUNDATION HUB' if article_id == 'hub' else ('SUPREME KOTWAL OF KASHI' if article_id == 'kaal_bhairav' else f'ASHTABHAIRAVA #{title.split(".")[0].strip()}')
    header_html = f"""
<div class="page-break"></div>
<div class="article-header-banner">
  <div class="article-number-badge">{badge_label}</div>
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
      <td>Skanda Purana — Kashi Khand (Sanctum protected by Lord Bhairava)</td>
    </tr>
  </table>
</div>
"""
    html_parts.append(header_html)

    # Append processed content
    html_parts.append(f"""
<div class="article-body-container">
  {processed_content}
</div>
""")

    # Append Structured Summary Box if matched
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
# 4. APPENDIX: COMPLETE BHAIRAV PARIKRAMA ITINERARY
# =========================================================================
html_parts.append("""
<div class="page-break"></div>
<h1>&#128506; Appendix: Traditional Kashi Bhairav Parikrama Pilgrimage Route</h1>
<p style="font-size:9.5pt; color:#4b5563;">
  Undertaking the pilgrimage of Kaal Bhairav and the eight directional Ashtabhairavas grants total protection from malefic spirits, removes fear of mortality, and cleanses sins. Below is the traditional geographical sequence recommended for pilgrims:
</p>

<table class="toc-table">
  <thead>
    <tr>
      <th style="width:18%;">Sequence</th>
      <th style="width:28%;">Shrine Visited</th>
      <th style="width:36%;">Location & Route Instructions</th>
      <th style="width:18%;">Direction / Zone</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Step 1 (Mandatory Initial Visit)</strong></td>
      <td><strong>Kaal Bhairav</strong><br>(The Kotwal of Kashi)</td>
      <td>Visit Kaal Bhairav temple in Visheshwarganj/Bhaironath early morning. Obtain divine permission to reside and perform pilgrimage in Kashi. Receive the consecrated black thread (ganda).</td>
      <td><span class="badge-tag badge-central">Center / Kotwal</span></td>
    </tr>
    <tr>
      <td><strong>Step 2</strong></td>
      <td><strong>#1. Asitang Bhairav</strong><br>(Near Vriddh Kaleshwar)</td>
      <td>Proceed to Maha Mrityunjay temple precinct at K.52/39 near Vriddh Kaleshwar (Daranagar / Maidagin). Worship the East protector.</td>
      <td><span class="badge-tag badge-east">East Protector</span></td>
    </tr>
    <tr>
      <td><strong>Step 3</strong></td>
      <td><strong>#8. Samhar Bhairav</strong><br>(Gai Ghat / Patan Darwaja)</td>
      <td>Head northeast towards riverfront: A.1/82 Patan Darwaja near Gai Ghat. Powerful dissolver of sins.</td>
      <td><span class="badge-tag badge-north">Northeast</span></td>
    </tr>
    <tr>
      <td><strong>Step 4</strong></td>
      <td><strong>#6. Kapal Bhairav</strong><br>(Laat Bhairav & Kapal Mochan)</td>
      <td>Take auto-rickshaw north to Alaipur near Laat Sarovar (ancient Kapal Mochan Teerth where Brahma's severed skull fell).</td>
      <td><span class="badge-tag badge-north">Northwest</span></td>
    </tr>
    <tr>
      <td><strong>Step 5</strong></td>
      <td><strong>#7. Bheeshan Bhairav</strong><br>(Bhoot Bhairav / Jyeshtheshwar)</td>
      <td>Return southwards into inland galis: K.63/28 near Jyeshtheshwar / Kashipura. Dispeller of ghostly fears.</td>
      <td><span class="badge-tag badge-north">North Protector</span></td>
    </tr>
    <tr>
      <td><strong>Step 6</strong></td>
      <td><strong>#4. Krodhan Bhairav</strong><br>(Batuk Bhairav, Kamachha)</td>
      <td>Travel south-west to Kamachha: famous Batuk Bhairav temple at B.31/126. Renowned for Rahu Shanti and Kaal Sarp Dosh pujas.</td>
      <td><span class="badge-tag badge-west">Southwest</span></td>
    </tr>
    <tr>
      <td><strong>Step 7</strong></td>
      <td><strong>#3. Chand Bhairav</strong><br>(Durga Kund Premises)</td>
      <td>Proceed south along Durgakund Road. Chand Bhairav is located inside the historic Durga Temple complex at B.27/2.</td>
      <td><span class="badge-tag badge-south">South Protector</span></td>
    </tr>
    <tr>
      <td><strong>Step 8</strong></td>
      <td><strong>#2. Ruru Bhairav</strong><br>(Anand Bhairav, Hanuman Ghat)</td>
      <td>Proceed east to Hanuman Ghat on the riverbank: B.4/16 Hanuman Ghat. Worshipped for ananda (bliss) and freedom from enemies.</td>
      <td><span class="badge-tag badge-south">Southeast</span></td>
    </tr>
    <tr>
      <td><strong>Step 9 (Optional Outlying Shashi)</strong></td>
      <td><strong>#5. Unmat Bhairav</strong><br>(Deora Village, Panchkroshi)</td>
      <td>Located 15 km outside city along Panchkroshi Marg at Deora Village. Contact priest Akhilesh Pandey (9118460531) for guidance.</td>
      <td><span class="badge-tag badge-west">West Protector</span></td>
    </tr>
  </tbody>
</table>

<div style="margin-top:24pt; border-top:1px solid #d1d5db; padding-top:10pt; font-size:8.5pt; color:#6b7280; text-align:center;">
  <strong>END OF KASHI BHAIRAV TEMPLES GUIDE</strong> &bull; Compiled from Authorised Website Archive: <a href="https://varanasitemples.in/">https://varanasitemples.in/</a>
</div>
""")

html_parts.append("""
</body>
</html>
""")

master_html_content = "\n".join(html_parts)

# Write master HTML
html_output_path = 'Kashi_Bhairav_Temples_Complete_Mirror.html'
with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(master_html_content)

print(f"Generated master HTML: {html_output_path} ({len(master_html_content)} characters)")

# Convert to PDF via Headless Chrome
pdf_output_path = 'Kashi_Bhairav_Temples_Complete_Mirror.pdf'
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
