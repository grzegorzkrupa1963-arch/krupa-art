"""
Oblicza wymiary oryginalnych plików dla galerii JS Józefa
i wstawia je do strona/jozef/index.html jako const DIMS = {...}.
"""
import json, re
from pathlib import Path
from PIL import Image

BASE  = Path(r"C:\PROJEKTY\projekt-krupa\strona")
JOZEF = BASE / "jozef-krupa"
HTML  = BASE / "jozef/index.html"

def dims(path):
    try:
        with Image.open(path) as im:
            return list(im.size)
    except Exception as e:
        print(f"  BLAD {path}: {e}")
        return [0, 0]

def find(directory, name):
    """Case-insensitive lookup."""
    d = Path(directory)
    nl = name.lower()
    for f in d.iterdir():
        if f.name.lower() == nl:
            return f
    return None

def seq(start, end, skip=None, ext='.JPG'):
    if skip is None: skip = []
    return [f"{n}{ext}" for n in range(start, end+1) if n not in skip]

def gallery_dims(directory, files):
    d = Path(directory)
    result = []
    for f in files:
        p = find(d, f)
        result.append(dims(p) if p else [0, 0])
    return result

print("Obliczam wymiary galerii JS...")

GALLERIES = {}

GALLERIES['powidoki'] = gallery_dims(
    JOZEF / "malarstwo/Powidoki_Sceniczne",
    seq(2, 76)
)
print(f"  powidoki: {len(GALLERIES['powidoki'])} plików")

rysunki_files = (
    ['1.PNG'] + seq(2, 6) +
    ['11.JPG','12.JPG','14.JPG','15.JPG','16.JPG','17.JPG','18.JPG','19.JPG'] +
    seq(20, 28) +
    ['29.jpg','30.jpg','31.png','32.jpg'] +
    seq(33, 45) + ['46.jpg'] +
    seq(47, 59) +
    ['60.jpg','61.jpg','62.jpg','63.JPG','64.jpg','65.JPG','66.JPG',
     '67.jpg','68.JPG','69.jpg'] +
    seq(70, 82) +
    ['83.jpg','84.JPG','85.jpg','86.jpg','87.jpg','88.jpg','89.jpg',
     '90.jpg','91.jpg','92.jpg','93.jpg','94.JPG','95.jpg','96.JPG',
     '97.JPG','98.JPG','99.JPG','100.jpg','101.jpg']
)
GALLERIES['rysunki'] = gallery_dims(JOZEF / "rysunki", rysunki_files)
print(f"  rysunki: {len(GALLERIES['rysunki'])} plików")

grafiki_files = [
    '3.png','6.png','8.png','9.png','10.png','11.png','12.JPG','13.JPG',
    '14.jpg','15.jpg','16.jpg','17.jpg','18.JPG','19.JPG','20.JPG','21.JPG',
    '22.JPG','23.jpg','24.JPG','25.jpg','26.png','27.png','28.jpg','29.png',
    '30.png','31.png','33.jpg','34.jpg','35.jpg','36.jpg','37.jpg','38.JPG',
    '39.JPG','40.JPG','41.JPG','42.JPG','43.PNG','44.JPG','45.PNG','46.JPG',
    '47.JPG','48.JPG','49.png','51.png','52.jpg','58.png','65.png','70.png',
    '72.jpg','100.JPG','101.jpg',
]
GALLERIES['grafiki'] = gallery_dims(JOZEF / "grafiki", grafiki_files)
print(f"  grafiki: {len(GALLERIES['grafiki'])} plików")

grafkom_files = [
    '208z.JPG','385756.png','9.jpg','Bez nazwy.png',
    'Foto Paint 1271271200.png','Foto Paint 127127129 \u2014 kopia.png','Foto Paint 127127129.png',
    "Gra 111'77.png",'PAIINTeD Kwa 00821021.png','PAINTeD 002847564.png',
    'PAINTeD 2022    P.S.LXXXV.jpg','PAINTeD 2023        P.S. LIV.png',
    'PAINTeD KWA 00112232.jpg','PAINTeD KWA 00131.jpg','PAINTeD KWA 00133.jpg',
    'PAINTeD KWA 00147.jpg','PAINTeD KWA 00162.jpg','PAINTeD KWA 00177.jpg',
    'PAINTeD KWA 00227.jpg','PAINTeD KWA 00332211.jpg','PAINTeD KWA 00333.png',
    'PAINTeD KWA 00338.jpg','PAINTeD KWA 00432.jpg','PAINTeD KWA 00437.jpg',
    'PAINTeD KWA 0044111.jpg','PAINTeD KWA 00444.jpg','PAINTeD KWA 00527.jpg',
    'PAINTeD KWA 005270.jpg','PAINTeD KWA 128128.png','PAINTeD KWA 23.png',
    'PAINTeD Kwa --39562.png','PAINTeD Kwa 00100025.png','PAINTeD Kwa 00284754.png',
    'PAINTeD Kwa 00373710.png','PAINTeD Kwa 00384753.png','PAINTeD Kwa 00386400.jpg',
    'PAINTeD Kwa 0047280.png','PAINTeD Kwa 004r736524.png','PAINTeD kwa 00283753.png',
    'PAINTeD kwa 0057773.png','PAINTed 00812743.png','PAINTed Kwa 0028375.png',
    'PAINTed Kwa 00371101.png','PAINTed Kwa 0037563.jpg','PAINTed Kwa 0087465.png',
    'Paint  Kwadrat 7..png','Paint KW 16.png','Paint Kwadrat  4..png',
]
GALLERIES['grafkom'] = gallery_dims(JOZEF / "Grafiki komputerowe", grafkom_files)
print(f"  grafkom: {len(GALLERIES['grafkom'])} plików")

GALLERIES['min1'] = gallery_dims(JOZEF / "minimal-ART/Minimal_ART_1", seq(1, 100))
print(f"  min1: {len(GALLERIES['min1'])} plików")

GALLERIES['min2'] = gallery_dims(JOZEF / "minimal-ART/Minimal_ART_2", seq(1, 100, [62]))
print(f"  min2: {len(GALLERIES['min2'])} plików")

GALLERIES['parki'] = gallery_dims(JOZEF / "fotografia/Parki/Parki_1", seq(1, 100))
print(f"  parki: {len(GALLERIES['parki'])} plików")

GALLERIES['pej1'] = gallery_dims(JOZEF / "fotografia/Pejzaze/Pejzaze_1", seq(1, 101, [8]))
print(f"  pej1: {len(GALLERIES['pej1'])} plików")

GALLERIES['pej2'] = gallery_dims(JOZEF / "fotografia/Pejzaze/Pejzaze_2", seq(1, 100))
print(f"  pej2: {len(GALLERIES['pej2'])} plików")

inna_files = seq(1, 98) + ['99.png', '100.JPG']
GALLERIES['inna'] = gallery_dims(JOZEF / "fotografia/Inne/2022_A", inna_files)
print(f"  inna: {len(GALLERIES['inna'])} plików")

GALLERIES['innb'] = gallery_dims(JOZEF / "fotografia/Inne/2022_B", seq(1, 100))
print(f"  innb: {len(GALLERIES['innb'])} plików")

# Sprawdź ile zer
zeros = sum(1 for g in GALLERIES.values() for d in g if d == [0, 0])
print(f"\nNie znalezione pliki: {zeros}")

# Generuj kompaktowy JS
js_lines = ["const DIMS = {"]
for key, data in GALLERIES.items():
    # Każda para [w,h] jako "[w,h]", bez spacji
    pairs = ','.join(f'[{w},{h}]' for w, h in data)
    js_lines.append(f"  {key}:[{pairs}],")
js_lines.append("};")
DIMS_JS = "\n".join(js_lines)

# Wstaw do HTML
html = HTML.read_text(encoding="utf-8")

# Zastąp stary blok DIMS (jeśli istnieje) lub wstaw przed buildGallery
MARKER_START = "/* ===== DIMS"
MARKER_END   = "/* ===== BUDOWANIE"

if MARKER_START in html:
    html = re.sub(
        r'/\* ===== DIMS.*?(?=/\* ===== BUDOWANIE)',
        DIMS_JS + "\n\n  ",
        html, flags=re.DOTALL
    )
else:
    html = html.replace(
        "  /* ===== BUDOWANIE GALERII =====",
        f"  /* ===== DIMS: wymiary oryginałów ===== */\n  {DIMS_JS}\n\n  /* ===== BUDOWANIE GALERII ====="
    )

# Zaktualizuj buildGallery żeby przyjmował dims
OLD_BUILD = """  function buildGallery(selector, basePath, files) {
    const c = document.querySelector(selector);
    if (!c) return;
    files.forEach(f => {
      const a = document.createElement('a');
      a.href = basePath + f;
      const img = document.createElement('img');
      img.src = basePath + thumbName(f);
      img.alt = '';
      img.loading = 'lazy';
      a.appendChild(img);
      c.appendChild(a);
    });
  }"""

NEW_BUILD = """  function buildGallery(selector, basePath, files, dims) {
    const c = document.querySelector(selector);
    if (!c) return;
    files.forEach((f, i) => {
      const a = document.createElement('a');
      a.href = basePath + f;
      if (dims && dims[i]) {
        a.dataset.pswpWidth  = dims[i][0];
        a.dataset.pswpHeight = dims[i][1];
      }
      const img = document.createElement('img');
      img.src = basePath + thumbName(f);
      img.alt = '';
      img.loading = 'lazy';
      a.appendChild(img);
      c.appendChild(a);
    });
  }"""

html = html.replace(OLD_BUILD, NEW_BUILD)

# Zaktualizuj wywołania buildGallery żeby przekazywać dims
replacements = [
    ("buildGallery('#gal-powidoki', '../../jozef-krupa/malarstwo/Powidoki_Sceniczne/', seq(2, 76));",
     "buildGallery('#gal-powidoki', '../../jozef-krupa/malarstwo/Powidoki_Sceniczne/', seq(2, 76), DIMS.powidoki);"),
    ("buildGallery('#gal-min1', '../../jozef-krupa/minimal-ART/Minimal_ART_1/', seq(1, 100));",
     "buildGallery('#gal-min1', '../../jozef-krupa/minimal-ART/Minimal_ART_1/', seq(1, 100), DIMS.min1);"),
    ("buildGallery('#gal-min2', '../../jozef-krupa/minimal-ART/Minimal_ART_2/', seq(1, 100, [62]));",
     "buildGallery('#gal-min2', '../../jozef-krupa/minimal-ART/Minimal_ART_2/', seq(1, 100, [62]), DIMS.min2);"),
    ("buildGallery('#gal-parki', '../../jozef-krupa/fotografia/Parki/Parki_1/', seq(1, 100));",
     "buildGallery('#gal-parki', '../../jozef-krupa/fotografia/Parki/Parki_1/', seq(1, 100), DIMS.parki);"),
    ("buildGallery('#gal-pej1',  '../../jozef-krupa/fotografia/Pejzaze/Pejzaze_1/', seq(1, 101, [8]));",
     "buildGallery('#gal-pej1',  '../../jozef-krupa/fotografia/Pejzaze/Pejzaze_1/', seq(1, 101, [8]), DIMS.pej1);"),
    ("buildGallery('#gal-pej2',  '../../jozef-krupa/fotografia/Pejzaze/Pejzaze_2/', seq(1, 100));",
     "buildGallery('#gal-pej2',  '../../jozef-krupa/fotografia/Pejzaze/Pejzaze_2/', seq(1, 100), DIMS.pej2);"),
    ("buildGallery('#gal-innb',  '../../jozef-krupa/fotografia/Inne/2022_B/', seq(1, 100));",
     "buildGallery('#gal-innb',  '../../jozef-krupa/fotografia/Inne/2022_B/', seq(1, 100), DIMS.innb);"),
]

# Rysunki - wieloliniowe
html = re.sub(
    r"buildGallery\('#gal-rysunki'[^;]+;\n  \]\);",
    lambda m: m.group(0).rstrip(');') + ", DIMS.rysunki);",
    html
)
html = re.sub(
    r"buildGallery\('#gal-grafiki'[^;]+;\n  \]\);",
    lambda m: m.group(0).rstrip(');') + ", DIMS.grafiki);",
    html
)
html = re.sub(
    r"buildGallery\('#gal-grafkom'[^;]+;\n  \]\);",
    lambda m: m.group(0).rstrip(');') + ", DIMS.grafkom);",
    html
)
html = re.sub(
    r"buildGallery\('#gal-inna'[^;]+\]\);",
    lambda m: m.group(0).rstrip(');') + ", DIMS.inna);",
    html
)

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f"  UWAGA: nie znaleziono: {old[:60]}")

HTML.write_text(html, encoding="utf-8")
print("\nZaktualizowano jozef/index.html.")
