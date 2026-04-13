import pandas as pd
from pathlib import Path

# read your Excel
df = pd.read_excel('data/Stock_Items.xlsx')
df.columns = [c.strip().upper() for c in df.columns]

Path('docs').mkdir(exist_ok=True)

# build one big HTML table
rows = ""
for _, r in df.iterrows():
    code = str(r.get('ITEM CODE','')).strip()
    desc = str(r.get('ITEM DESCRIPTION','')).strip()
    binloc = str(r.get('BIN LOCATION','')).strip()
    minv = str(r.get('MIN','')).strip()
    maxv = str(r.get('MAX','')).strip()
    rows += f"<tr><td>{code}</td><td>{desc}</td><td>{binloc}</td><td>{minv}</td><td>{maxv}</td></tr>\n"

html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Ayala Supply Inventory</title></head>
<body>
<h1>AYALA SUPPLY SA-MAIN INVENTORY</h1>
<p>Official depot database. 774 SKUs.</p>
<table border="1" cellpadding="5">
<thead><tr><th>ITEM CODE</th><th>ITEM DESCRIPTION</th><th>BIN LOCATION</th><th>MIN</th><th>MAX</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body></html>"""

Path('docs/index.html').write_text(html, encoding='utf-8')
