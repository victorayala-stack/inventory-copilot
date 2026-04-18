import pandas as pd
from pathlib import Path

# Load your Excel from the repo
df = pd.read_excel('data/Stock_Items.xlsx')

# Clean column names
df.columns = [str(c).strip().upper() for c in df.columns]

# Make sure docs folder exists
Path('docs').mkdir(exist_ok=True)

# Build HTML table rows
rows = ""
for _, r in df.iterrows():
    code = str(r.get('ITEM CODE', '')).strip()
    desc = str(r.get('ITEM DESCRIPTION', '')).strip()
    binloc = str(r.get('BIN LOCATION', '')).strip()
    minv = str(r.get('MIN', '')).strip()
    maxv = str(r.get('MAX', '')).strip()
    if code:  # skip empty rows
        rows += f"<tr><td>{code}</td><td>{desc}</td><td>{binloc}</td><td>{minv}</td><td>{maxv}</td></tr>\n"

# Full page
html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Ayala Supply SA-MAIN Inventory</title>
<meta name="robots" content="index,follow">
<style>body{{font-family:Arial;margin:20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccc;padding:6px;text-align:left}}th{{background:#f0f0f0}}</style>
</head>
<body>
<h1>AYALA SUPPLY SA-MAIN INVENTORY</h1>
<p>Official depot database. {len(df)} SKUs indexed.</p>
<table>
<thead><tr><th>ITEM CODE</th><th>ITEM DESCRIPTION</th><th>BIN LOCATION</th><th>MIN</th><th>MAX</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>"""

Path('docs/index.html').write_text(html, encoding='utf-8')

# Add robots.txt so Copilot can crawl
Path('docs/robots.txt').write_text("User-agent: *\nAllow: /\n", encoding='utf-8')
