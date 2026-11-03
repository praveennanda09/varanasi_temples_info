# pdf_map_and_pins_builder.py
# Helper module to generate verified GPS Pinpoint cards and Map Plate directories for all 7 Kashi Pilgrimage PDFs

import os
import master_temples_coordinates as mtc

def generate_gps_card_html(key_or_title, orig_map_url=None, custom_landmark=None):
    """
    Renders an elegant, high-visibility GPS Pinpoint box for each individual temple article.
    If an original blog Google Maps URL exists, it retains it and renders the verified pin directly below it.
    """
    meta = mtc.get_coords_and_meta(key_or_title)
    lat = meta['lat']
    lon = meta['lon']
    hindi_title = meta['hindi']
    subtitle = meta['subtitle']
    landmark = custom_landmark or meta['landmark']
    v_pin_url = mtc.get_google_maps_pin_url(lat, lon)

    orig_row = ""
    if orig_map_url and orig_map_url != 'Not provided' and 'google.com/maps' in orig_map_url:
        orig_row = f"""
    <tr>
      <td style="font-weight:700; color:#9a3412; padding:3pt 0; vertical-align:top;">Original Blog Maps Link:</td>
      <td><a href="{orig_map_url}" target="_blank" style="color:#b45309; text-decoration:underline; font-size:8pt; word-break:break-all;">{orig_map_url}</a> <span style="font-size:7.5pt; color:#6b7280;">(Preserved from blog source)</span></td>
    </tr>
"""

    html = f"""
<div class="gps-pin-card" style="background:#f0fdf4; border:1.5px solid #86efac; border-left:5px solid #16a34a; border-radius:6px; padding:7pt 10pt; margin-top:9pt; page-break-inside:avoid; break-inside:avoid;">
  <div style="font-weight:700; color:#15803d; font-size:9pt; margin-bottom:3pt; display:flex; align-items:center;">
    <span style="font-size:12pt; margin-right:5pt;">&#128205;</span>
    VERIFIED EXACT GPS PINPOINT &amp; SATELLITE NAVIGATION
  </div>
  <table style="width:100%; border-collapse:collapse; font-size:8.5pt;">
    <tr>
      <td style="width:28%; font-weight:700; color:#166534; padding:2pt 0;">Exact Coordinates:</td>
      <td style="font-family:'Courier New', monospace; font-weight:700; color:#0f172a;">{lat:.5f}&deg; N, {lon:.5f}&deg; E</td>
    </tr>
    {orig_row}
    <tr>
      <td style="font-weight:700; color:#166534; padding:2pt 0; vertical-align:top;">Verified Google Maps Pin:</td>
      <td><a href="{v_pin_url}" target="_blank" style="color:#2563eb; font-weight:700; text-decoration:underline; font-size:8.5pt; word-break:break-all;">{v_pin_url}</a></td>
    </tr>
    <tr>
      <td style="font-weight:700; color:#166534; padding:2pt 0; vertical-align:top;">Sanctum Landmark:</td>
      <td style="color:#334155;">{landmark}</td>
    </tr>
    <tr>
      <td style="font-weight:700; color:#166534; padding:2pt 0; vertical-align:top;">Spiritual Significance:</td>
      <td style="color:#0369a1; font-style:italic;">{subtitle}</td>
    </tr>
  </table>
</div>
"""
    return html

def generate_map_appendix_html(base_dir, guide_title, guide_subtitle, svg_filename, temple_items, banner_bg="#1e3a8a"):
    """
    Renders the dedicated final Appendix:
    1. Graphic Header Banner
    2. Introduction explaining the pilgrimage geography
    3. Full High-Resolution Vector Map with all pins & callout cards matching the screenshot
    4. Tabular Master Coordinates Directory
    """
    abs_svg_path = f"file:///{base_dir}/assets/images/{svg_filename}"

    table_rows = []
    for idx, t in enumerate(temple_items):
        t_key = t.get('key', t.get('id', t.get('slug', t.get('canonical_name', t.get('title', '')))))
        t_title = t.get('title', t.get('canonical_name', t_key))
        meta = mtc.get_coords_and_meta(t_key)
        lat = meta['lat']
        lon = meta['lon']
        hindi = meta['hindi']
        landmark = t.get('landmark', meta['landmark'])
        subtitle = meta['subtitle']
        pin_url = mtc.get_google_maps_pin_url(lat, lon)

        table_rows.append(f"""
    <tr>
      <td style="text-align:center; font-weight:700; color:#475569;">{idx + 1}</td>
      <td>
        <div style="font-weight:700; color:#0f172a;">{t_title}</div>
        <div style="font-size:7.5pt; color:#475569;">{hindi}</div>
      </td>
      <td style="font-family:'Courier New', monospace; font-size:7.5pt; color:#0f172a;">
        <strong>{lat:.5f}&deg; N</strong><br>{lon:.5f}&deg; E
      </td>
      <td style="font-size:7.5pt; color:#334155;">
        {landmark}
      </td>
      <td style="font-size:7.5pt;">
        <a href="{pin_url}" target="_blank" style="color:#2563eb; font-weight:700; text-decoration:underline;">Open Pin &#8599;</a><br>
        <span style="font-size:7pt; color:#64748b; word-break:break-all;">{pin_url}</span>
      </td>
    </tr>
""")

    appendix_html = f"""
<div class="page-break"></div>
<!-- APPENDIX: GEOGRAPHIC PILGRIMAGE MAP & PIN DIRECTORY -->
<div style="background:{banner_bg}; color:#ffffff; padding:12pt 16pt; border-radius:6px; margin-bottom:12pt; page-break-after:avoid;">
  <div style="font-size:8.5pt; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:1px;">Cartographic Plate &bull; Precision Satellite Navigation</div>
  <h2 style="font-size:17pt; margin:3pt 0; color:#ffffff; border:none; padding:0;">&#128506; GEOGRAPHIC PILGRIMAGE MAP &amp; MASTER PIN DIRECTORY</h2>
  <div style="font-size:9.5pt; color:#e0e7ff;">{guide_title} &bull; {guide_subtitle} ({len(temple_items)} Sanctums)</div>
</div>

<p style="font-size:9pt; color:#374151; margin-bottom:10pt; line-height:1.5;">
  The plate below displays the exact geographic pinpoint of each sacred sanctum across the Varanasi pilgrimage corridor. Shrines are marked with circular <strong>&#2384; pins</strong> connected to three-line descriptive callouts (English title, Devanagari Hindi designation, and scriptural role) as surveyed on the ground. Following the visual cartography plate is the master GPS directory with direct 1-click Google Maps pin links.
</p>

<!-- Full Visual Cartographic Plate -->
<div style="text-align:center; margin:14pt 0; page-break-inside:avoid;">
  <img src="{abs_svg_path}" style="width:100%; max-height:560px; border-radius:6px; border:1.5px solid #cbd5e1; box-shadow:0 3px 8px rgba(0,0,0,0.12);" alt="{guide_title} Map Plate">
  <div style="font-size:7.5pt; color:#64748b; font-style:italic; margin-top:4pt;">
    Plate: Verified Kashi Pilgrimage GIS Vector Map &bull; River Ganga Flow, Roads, and Sanctum Coordinates &bull; Map data &#169;2026
  </div>
</div>

<div class="page-break"></div>
<h3 style="font-size:12pt; color:#1e3a8a; border-bottom:1.5px solid #bfdbfe; padding-bottom:4pt; margin-top:10pt;">
  &#128205; Master GPS Pinpoint &amp; Direct Navigation Directory
</h3>

<table class="toc-table" style="font-size:8pt; margin-top:8pt;">
  <thead>
    <tr>
      <th style="width:4%; text-align:center;">#</th>
      <th style="width:28%;">Sanctum &amp; Hindi Name</th>
      <th style="width:18%;">Coordinates</th>
      <th style="width:26%;">Access Route / Landmark</th>
      <th style="width:24%;">Google Maps Pin</th>
    </tr>
  </thead>
  <tbody>
    {''.join(table_rows)}
  </tbody>
</table>
"""
    return appendix_html
