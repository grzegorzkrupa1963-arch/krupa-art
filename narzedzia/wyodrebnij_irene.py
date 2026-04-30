"""
Wyodrębnia rozdziały ze Wspomnień Ireny Porębskiej-Krupy i tworzy strony HTML.
"""
import re, fitz
from pathlib import Path

PDF  = Path(r"C:\PROJEKTY\projekt-krupa\irena-porebska-krupa\pisarstwo\Irena Porębska-Krupa - Wspomnienia.pdf")
OUT  = Path(r"C:\PROJEKTY\projekt-krupa\strona\pisarstwo-jozefa")

# --- Wyodrębnij cały tekst ---
doc = fitz.open(str(PDF))
pages = []
for page in doc:
    pages.append(page.get_text())
full_text = "\n".join(pages)

# --- Podziel na rozdziały ---
# Rozdziały zaczynają się od samotnego "I", "II"... lub "Epilog" w linii
pattern = r'\n(I{1,3}V?|VI?|Epilog)\s*\n'
parts = re.split(pattern, full_text)

chapters = []
i = 1
while i < len(parts):
    title = parts[i].strip()
    text  = parts[i+1].strip() if i+1 < len(parts) else ""
    # Oczyść numerki stron (samotne cyfry w linii)
    text = re.sub(r'\n\d{1,3} \n', '\n', text)
    text = re.sub(r'^\d{1,3} \n', '', text)
    text = text.strip()
    if text:
        chapters.append((title, text))
    i += 2

print(f"Znaleziono {len(chapters)} rozdziałów:")
for t, txt in chapters:
    print(f"  {t}: {txt[:60]}...")

# --- Szablon HTML rozdziału ---
NAV = """<nav class="site-nav" aria-label="Nawigacja główna">
  <div class="container">
    <ul class="nav-links">
      <li><a href="../index.html">Strona główna</a></li>
      <li><a href="../irena/index.html">Irena</a></li>
      <li><a href="../jozef/index.html">Józef</a></li>
      <li><a href="index.html" aria-current="page">Twórczość literacka</a></li>
      <li><a href="../archiwum/index.html">Zdjęcia archiwalne</a></li>
      <li><a href="../index.html#ksiega-gosci">Księga gości</a></li>
    </ul>
  </div>
</nav>"""

def text_to_html(text):
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    return "\n".join(f"      <p>{p.replace(chr(10), ' ')}</p>" for p in paragraphs)

ROMAN = {'I': 'I', 'II': 'II', 'III': 'III', 'IV': 'IV', 'V': 'V', 'VI': 'VI', 'Epilog': 'Epilog'}

for idx, (title, text) in enumerate(chapters):
    slug = f"irena-wspomnienia-{title.lower().replace(' ', '-')}"
    html_body = text_to_html(text)
    prev_link = ""
    next_link = ""
    if idx > 0:
        pt, _ = chapters[idx-1]
        prev_slug = f"irena-wspomnienia-{pt.lower().replace(' ', '-')}.html"
        prev_link = f'<a href="{prev_slug}" class="cat-nav__prev">← Rozdział {pt}</a>'
    if idx < len(chapters) - 1:
        nt, _ = chapters[idx+1]
        next_slug = f"irena-wspomnienia-{nt.lower().replace(' ', '-')}.html"
        next_link = f'<a href="{next_slug}" class="cat-nav__next">Rozdział {nt} →</a>'

    if title == "Epilog":
        heading = "Epilog"
    else:
        heading = f"Rozdział {title}"

    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Irena Porębska-Krupa — Wspomnienia, {heading}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="artist-header">
  <div class="container">
    <h1>Irena Porębska-Krupa</h1>
    <p class="artist-roles">Wspomnienia — {heading}</p>
  </div>
</header>

{NAV}

<section style="background:var(--cream);padding-block:clamp(2rem,5vw,4rem)">
  <div class="container">
    <div class="section-header">
      <h2>{heading}</h2>
      <span class="section-divider"></span>
    </div>
    <div class="text-body">
{html_body}
    </div>
    <nav class="cat-nav" style="display:flex;justify-content:space-between;margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--beige-dark)">
      <span>{prev_link}</span>
      <a href="index.html">↑ Spis treści</a>
      <span>{next_link}</span>
    </nav>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <p>Irena Porębska-Krupa &amp; Józef Krupa</p>
    <span class="footer-ornament"></span>
    <p>Strona poświęcona ich twórczości</p>
  </div>
</footer>
</body>
</html>"""

    out_file = OUT / f"{slug}.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"  Zapisano: {out_file.name}")

print("\nGotowe!")
