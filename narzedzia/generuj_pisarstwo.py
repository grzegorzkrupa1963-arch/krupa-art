"""
Generuje strony HTML z tekstami Józefa Krupy.
- .docx → python-docx
- .doc  → win32com (Word)
Styl dopasowany do strony głównej.
"""
import re, unicodedata, os
from pathlib import Path
import docx as docxlib

BASE_SRC = Path(r"C:\PROJEKTY\projekt-krupa\jozef-krupa\pisarstwo")
BASE_OUT = Path(r"C:\PROJEKTY\projekt-krupa\strona\pisarstwo-jozefa")

CATEGORIES = [
    ("Bajki",                    "Bajki"),
    ("Krotkie historyjki",       "Krótkie historyjki"),
    ("Opowiadania i wspominki",  "Opowiadania i wspominki"),
    ("Opowiadania  2022,  2023", "Opowiadania 2022\u20132023"),
    ("Zestaw opowiadań",         "Zestaw opowiadań"),
    ("Cos zostalo, cos minelo",  "Coś zostało, coś minęło"),
    ("Pozostałe teksty",         "Pozostałe teksty"),
]

# ---------------------------------------------------------------------------
# Konwersja
# ---------------------------------------------------------------------------

def docx_to_html(path: Path) -> str:
    try:
        doc = docxlib.Document(path)
    except Exception as e:
        return f'<p class="text-error">Błąd odczytu: {e}</p>'
    parts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            parts.append('<br>')
            continue
        style = (para.style.name or "").lower()
        if "heading 1" in style or "title" in style:
            parts.append(f'<h3>{_esc(text)}</h3>')
        elif "heading 2" in style:
            parts.append(f'<h4>{_esc(text)}</h4>')
        elif "heading 3" in style:
            parts.append(f'<h5>{_esc(text)}</h5>')
        else:
            inner = ""
            for run in para.runs:
                t = _esc(run.text)
                if run.bold and run.italic:
                    t = f"<strong><em>{t}</em></strong>"
                elif run.bold:
                    t = f"<strong>{t}</strong>"
                elif run.italic:
                    t = f"<em>{t}</em>"
                inner += t
            if inner.strip():
                parts.append(f"<p>{inner}</p>")
    html = "\n".join(parts)
    # usuń nadmiarowe <br> na początku/końcu
    html = re.sub(r'^(<br>\s*)+', '', html)
    html = re.sub(r'(<br>\s*)+$', '', html)
    return html or '<p><em>(brak treści)</em></p>'


_word_app = None

def _get_word():
    global _word_app
    if _word_app is None:
        import win32com.client
        _word_app = win32com.client.Dispatch("Word.Application")
        _word_app.Visible = False
    return _word_app


def doc_to_html(path: Path) -> str:
    try:
        word = _get_word()
        doc  = word.Documents.Open(str(path.resolve()), ReadOnly=True)
        parts = []
        for i in range(1, doc.Paragraphs.Count + 1):
            para  = doc.Paragraphs(i)
            text  = para.Range.Text.strip().rstrip('\r\x07')
            if not text:
                parts.append('<br>')
                continue
            style = para.Style.NameLocal.lower()
            if any(s in style for s in ("heading 1", "nagłówek 1", "tytuł", "title")):
                parts.append(f'<h3>{_esc(text)}</h3>')
            elif any(s in style for s in ("heading 2", "nagłówek 2")):
                parts.append(f'<h4>{_esc(text)}</h4>')
            else:
                parts.append(f'<p>{_esc(text)}</p>')
        doc.Close(False)
        html = "\n".join(parts)
        html = re.sub(r'^(<br>\s*)+', '', html)
        html = re.sub(r'(<br>\s*)+$', '', html)
        return html or '<p><em>(brak treści)</em></p>'
    except Exception as e:
        return f'<p class="text-error">Błąd odczytu: {e}</p>'


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s_-]+', '-', text)


# ---------------------------------------------------------------------------
# Szablon HTML
# ---------------------------------------------------------------------------

def page(title: str, body: str, *, depth: int = 1) -> str:
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_esc(title)} — Józef Krupa</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{up}style.css">
  <style>
    /* ---- Accordion tekstów ---- */
    .text-accordion {{ margin-top: 1.5rem; }}
    .text-accordion details {{
      border-bottom: 1px solid var(--beige-dark);
    }}
    .text-accordion details:first-child {{ border-top: 1px solid var(--beige-dark); }}
    .text-accordion summary {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.85rem 0.25rem;
      font-family: var(--font-serif);
      font-size: 1.1rem;
      color: var(--sepia-dark);
      cursor: pointer;
      list-style: none;
      user-select: none;
      transition: color var(--transition);
    }}
    .text-accordion summary::-webkit-details-marker {{ display: none; }}
    .text-accordion summary::after {{
      content: "▸";
      flex-shrink: 0;
      color: var(--sepia-light);
      font-size: 0.85rem;
      transition: transform 0.2s;
    }}
    .text-accordion details[open] summary::after {{ transform: rotate(90deg); }}
    .text-accordion summary:hover {{ color: var(--sepia); }}

    /* ---- Treść tekstu ---- */
    .text-body {{
      padding: 1.5rem 0.25rem 2.5rem;
      max-width: 72ch;
    }}
    .text-body p {{
      font-family: var(--font-serif);
      font-size: 1.05rem;
      line-height: 1.9;
      color: var(--ink);
      margin: 0 0 0.9em;
      text-indent: 1.5em;
    }}
    .text-body p:first-of-type {{ text-indent: 0; }}
    .text-body h3, .text-body h4, .text-body h5 {{
      font-family: var(--font-serif);
      color: var(--sepia-dark);
      margin: 1.75em 0 0.4em;
      font-weight: 500;
    }}
    .text-body h3 {{ font-size: 1.25rem; }}
    .text-body h4 {{ font-size: 1.1rem; font-style: italic; }}
    .text-body br {{ display: block; height: 0.5em; content: ""; }}
    .text-error {{ color: var(--muted); font-style: italic; font-size: 0.9rem; }}
    .text-unavail {{
      font-family: var(--font-serif);
      font-style: italic;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    /* ---- Nawigacja kategorii ---- */
    .cat-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 2.5rem;
    }}
    .cat-pills a {{
      font-family: var(--font-sans);
      font-size: 0.82rem;
      padding: 0.35rem 1rem;
      border-radius: 99px;
      border: 1px solid var(--beige-dark);
      color: var(--sepia-dark);
      text-decoration: none;
      transition: background var(--transition), color var(--transition);
    }}
    .cat-pills a:hover {{ background: var(--beige); }}
    .cat-pills a.active {{
      background: var(--sepia-dark);
      color: var(--white);
      border-color: var(--sepia-dark);
    }}

    /* ---- Siatka kart (index) ---- */
    .cat-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
      gap: 1.5rem;
      margin-top: 2rem;
    }}
    .cat-card {{
      background: var(--white);
      border: 1px solid var(--beige-dark);
      border-radius: calc(var(--radius) * 2);
      overflow: hidden;
      box-shadow: 0 4px 20px var(--shadow);
      transition: transform var(--transition), box-shadow var(--transition);
    }}
    .cat-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 8px 32px rgba(92,66,9,.18);
    }}
    .cat-card__spine {{
      height: 6px;
      background: linear-gradient(90deg, var(--sepia-dark), var(--sepia-light));
    }}
    .cat-card__body {{
      padding: 1.5rem 1.75rem 1.75rem;
    }}
    .cat-card__title {{
      font-family: var(--font-serif);
      font-size: 1.25rem;
      color: var(--sepia-dark);
      text-decoration: none;
      display: block;
      margin-bottom: 0.5rem;
    }}
    .cat-card__title:hover {{ color: var(--sepia); }}
    .cat-card__meta {{
      font-family: var(--font-sans);
      font-size: 0.8rem;
      color: var(--muted);
    }}
  </style>
</head>
<body>

<header class="artist-header">
  <div class="container">
    <h1>Józef Krupa — Pisarstwo</h1>
    <p class="artist-roles">opowiadania · bajki · wspomnienia · historyjki</p>
  </div>
</header>

<nav class="site-nav" aria-label="Nawigacja główna">
  <div class="container">
    <span class="nav-brand">Krupa — twórczość</span>
    <ul class="nav-links">
      <li><a href="{up}index.html">Strona główna</a></li>
      <li><a href="{up}irena/index.html">Irena</a></li>
      <li><a href="{up}jozef/index.html">Józef</a></li>
      <li><a href="{up}index.html#razem">Razem</a></li>
      <li><a href="{up}ksiazki/index.html">Życiorysy i wydane książki</a></li>
      <li><a href="{up}pisarstwo-jozefa/index.html" aria-current="page">Pisarstwo Józefa</a></li>
      <li><a href="{up}irena/index.html#archiwum">Zdjęcia archiwalne Ireny</a></li>
      <li><a href="{up}index.html#ksiega-gosci">Księga gości</a></li>
    </ul>
  </div>
</nav>

{body}

<footer class="site-footer">
  <div class="container">
    <p>Irena Porębska-Krupa &amp; Józef Krupa</p>
    <span class="footer-ornament"></span>
    <p>Strona poświęcona ich twórczości</p>
  </div>
</footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Nawigacja kategorii (pigułki)
# ---------------------------------------------------------------------------

def cat_pills(active_slug: str) -> str:
    items = ['<a href="index.html">Wszystkie</a>']
    for _, label in CATEGORIES:
        sl = slugify(label)
        cls = ' class="active"' if sl == active_slug else ""
        items.append(f'<a href="{sl}.html"{cls}>{label}</a>')
    return '<div class="cat-pills">' + "\n    ".join(items) + "\n  </div>"


# ---------------------------------------------------------------------------
# Strona kategorii
# ---------------------------------------------------------------------------

def build_category(folder: str, label: str) -> None:
    src_dir = BASE_SRC / folder
    if not src_dir.is_dir():
        return
    slug = slugify(label)

    files = sorted(src_dir.iterdir(), key=lambda p: p.stem.lower())
    doc_files  = [f for f in files if f.suffix.lower() == ".doc"
                                   and not f.name.endswith(".docx")]
    docx_files = [f for f in files if f.suffix.lower() == ".docx"]
    all_files  = sorted(docx_files + doc_files, key=lambda p: p.stem.lower())

    items_html = []
    total = len(all_files)
    for i, f in enumerate(all_files, 1):
        print(f"    [{i}/{total}] {f.name}", end="\r", flush=True)
        if f.suffix.lower() == ".docx":
            content = docx_to_html(f)
        else:
            content = doc_to_html(f)
        items_html.append(
            f'<details>\n'
            f'  <summary>{_esc(f.stem)}</summary>\n'
            f'  <div class="text-body">\n{content}\n  </div>\n'
            f'</details>'
        )
    print()  # newline po \r

    accordion = (
        '<div class="text-accordion">\n' +
        "\n".join(items_html) +
        "\n</div>"
    ) if items_html else "<p><em>Brak tekstów w tej kategorii.</em></p>"

    body = f"""
<section style="background:var(--cream);padding-block:clamp(2rem,5vw,4rem)">
  <div class="container">
    <div class="section-header">
      <h2>{_esc(label)}</h2>
      <span class="section-divider"></span>
    </div>
    {cat_pills(slug)}
    {accordion}
  </div>
</section>"""

    out = BASE_OUT / f"{slug}.html"
    out.write_text(page(label, body, depth=1), encoding="utf-8")
    print(f"  {label}: {len(all_files)} tekstow -> {out.name}")


# ---------------------------------------------------------------------------
# Strona główna pisarstwa
# ---------------------------------------------------------------------------

def build_index() -> None:
    cards = []
    for folder, label in CATEGORIES:
        src = BASE_SRC / folder
        n = len(list(src.glob("*.doc*"))) if src.is_dir() else 0
        sl = slugify(label)
        cards.append(
            f'<div class="cat-card">'
            f'<div class="cat-card__spine"></div>'
            f'<div class="cat-card__body">'
            f'<a class="cat-card__title" href="{sl}.html">{_esc(label)}</a>'
            f'<span class="cat-card__meta">{n} tekstów</span>'
            f'</div></div>'
        )

    body = f"""
<section style="background:var(--cream);padding-block:clamp(2rem,5vw,4rem)">
  <div class="container">
    <div class="section-header">
      <h2>Wszystkie kategorie</h2>
      <span class="section-divider"></span>
    </div>
    <p style="font-family:var(--font-serif);font-style:italic;color:var(--ink-soft);margin-bottom:0.5rem">
      Józef Krupa pisał przez całe życie — opowiadania, wspomnienia, bajki i krótkie historyjki.
    </p>
    <div class="cat-grid">
      {"".join(cards)}
    </div>
  </div>
</section>"""

    out = BASE_OUT / "index.html"
    out.write_text(page("Pisarstwo Józefa Krupy", body, depth=1), encoding="utf-8")
    print(f"  Indeks -> {out.name}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    BASE_OUT.mkdir(parents=True, exist_ok=True)
    print("Generowanie stron pisarstwa...")
    build_index()
    for folder, label in CATEGORIES:
        print(f"  {label}:")
        build_category(folder, label)

    if _word_app is not None:
        try:
            _word_app.Quit()
        except Exception:
            pass
    print("Gotowe.")
