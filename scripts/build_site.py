#!/usr/bin/env python3
import pandas as pd, re, html, os
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1]
DATA_FILE = BASE / 'data' / 'Stock_Items.xlsx'
DOCS = BASE / 'docs'
ITEMS = DOCS / 'items'

ORG = os.getenv('GITHUB_REPOSITORY_OWNER', 'REPLACE-ORG')
REPO = os.getenv('GITHUB_REPOSITORY_NAME', 'inventory-copilot')
BING_VERIFICATION = os.getenv('BING_VERIFICATION', '')
SITE_URL = f"https://{ORG}.github.io/{REPO}"

def get_zone(bin_loc):
    if not bin_loc or str(bin_loc).strip() == '':
        return "NOT FOUND"
    b = str(bin_loc).strip().upper()
    if b in {'PIPE RACK','DOCK','WALL','FLOOR','RACK','CON','CON2','ZZ1'}:
        return b
    if re.fullmatch(r'[A-Z]\d[A-Z]', b):
        return b
    m = re.match(r'^([A-Z]\d[A-Z])', b)
    return m.group(1) if m else (b if len(b) <= 12 else "NOT FOUND")

def main():
    df = pd.read_excel(DATA_FILE, dtype=str).fillna('')
    df.columns = [c.strip().upper() for c in df.columns]
    df['ZONE'] = df['BIN LOCATION'].apply(get_zone)
    df['ITEM CODE'] = df['ITEM CODE'].str.strip()
    df['ITEM DESCRIPTION'] = df['ITEM DESCRIPTION'].str.strip()
    df['MIN'] = df['MIN'].str.strip()
    df['MAX'] = df['MAX'].str.strip()
    df = df.sort_values('ITEM CODE')

    ITEMS.mkdir(parents=True, exist_ok=True)
    meta = f'<meta name="msvalidate.01" content="{BING_VERIFICATION}" />' if BING_VERIFICATION else ''

    for _, r in df.iterrows():
        code = r['ITEM CODE']
        safe = re.sub(r'[^A-Za-z0-9_-]', '_', code)
        htmlc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(code)} - Ayala Supply</title>{meta}<meta name="robots" content="index,follow"><style>body{{font-family:Arial,sans-serif;margin:40px;background:#f5f5f5}}pre{{background:white;padding:20px;border-left:4px solid #3D4F2E}}</style></head><body><h1>{html.escape(code)}</h1><pre>Item: {code}
Description: {r['ITEM DESCRIPTION']}
Min/Max: {r['MIN']}/{r['MAX']}
Bin: {r['ZONE']}
Full Location: {r['BIN LOCATION']}</pre><p><a href="../">Back to Index</a></p></body></html>"""
        (ITEMS / f"{safe}.html").write_text(htmlc, 'utf-8')

    rows = ''.join([f'<tr><td><a href="{re.sub(r"[^A-Za-z0-9_-]","_",c)}.html">{html.escape(c)}</a></td><td>{html.escape(d[:60])}</td><td>{html.escape(z)}</td><td>{m}/{x}</td></tr>' for c,d,z,m,x in zip(df['ITEM CODE'], df['ITEM DESCRIPTION'], df['ZONE'], df['MIN'], df['MAX'])])
    (ITEMS / 'index.html').write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Inventory - Ayala Supply</title>{meta}<style>body{{font-family:Arial;margin:20px}}table{{border-collapse:collapse;width:100%}}th{{background:#3D4F2E;color:white;padding:8px;text-align:left}}td{{padding:6px;border-bottom:1px solid #ddd}}</style></head><body><h1>Inventory - {len(df)} SKUs</h1><table><tr><th>Code</th><th>Description</th><th>Bin</th><th>Min/Max</th></tr>{rows}</table></body></html>", 'utf-8')

    (DOCS / 'index.html').write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Ayala Supply KB</title>{meta}</head><body style='font-family:Arial;text-align:center;margin-top:100px'><h1>AYALA SUPPLY INVENTORY KB</h1><p>{len(df)} parts indexed</p><p><a href='items/' style='background:#3D4F2E;color:white;padding:15px 30px;text-decoration:none'>Browse Inventory</a></p></body></html>", 'utf-8')

    (DOCS / 'robots.txt').write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", 'utf-8')

    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc in ['/', '/items/'] + [f"/items/{re.sub(r'[^A-Za-z0-9_-]','_',c)}.html" for c in df['ITEM CODE']]:
        u = ET.SubElement(urlset, 'url'); ET.SubElement(u, 'loc').text = f"{SITE_URL}{loc}"
    ET.ElementTree(urlset).write(DOCS / 'sitemap.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__': main()
