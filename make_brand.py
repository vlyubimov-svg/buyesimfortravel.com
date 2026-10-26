#!/usr/bin/env python3
"""Render og.png (1200x630) and logo.png (512x512) from this site's own logo.svg and site.json "brand".

The logo itself is drawn per site by hand (SVG in src/assets/img/logo.svg). This script only rasterizes it.
Usage: python3 make_brand.py   (needs: pip install playwright && playwright install chromium)
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
site = json.loads((ROOT / "site.json").read_text())
b = site["brand"]
logo = (ROOT / "src/assets/img/logo.svg").read_text().strip()
font = b.get("og_font", "Inter")
fam = font.replace(" ", "+")

og = f"""<html><head><link href="https://fonts.googleapis.com/css2?family={fam}:wght@600;700&display=swap" rel="stylesheet"></head>
<body style="margin:0;width:1200px;height:630px;background:{b['og_bg']};color:{b['og_ink']};font-family:'{font}',sans-serif;position:relative;overflow:hidden">
<div style="position:absolute;right:-140px;bottom:-200px;width:640px;height:640px;border-radius:50%;background:{b['og_accent']};opacity:.18"></div>
<div style="padding:70px 80px;position:relative">
<div style="display:flex;align-items:center;gap:18px;font-weight:700;font-size:32px"><div style="width:68px;height:68px">{logo}</div>{site['name']}</div>
<div style="font-weight:700;font-size:78px;line-height:1.04;letter-spacing:-1.5px;margin-top:70px;max-width:960px">{b['og_headline']}</div>
<div style="margin-top:36px;font-size:26px;opacity:.75">{site['domain']}</div></div></body></html>"""

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(og, wait_until="networkidle")
    pg.screenshot(path=str(ROOT / "src/assets/img/og.png"))
    pg = br.new_page(viewport={"width": 512, "height": 512})
    pg.set_content(f'<body style="margin:0;background:transparent"><div style="width:512px;height:512px">{logo}</div></body>')
    pg.screenshot(path=str(ROOT / "src/assets/img/logo.png"), omit_background=True)
    br.close()
print("og.png and logo.png written to src/assets/img/")
