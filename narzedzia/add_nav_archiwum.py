"""Dodaje 'Zdjęcia archiwalne Ireny' do menu we wszystkich plikach HTML."""
import re
from pathlib import Path

STRONA = Path(r"C:\PROJEKTY\projekt-krupa\strona")

# (plik, href do archiwum)
FILES = [
    (STRONA / "index.html",                                    "irena/index.html#archiwum"),
    (STRONA / "irena/index.html",                              "index.html#archiwum"),
    (STRONA / "jozef/index.html",                              "../irena/index.html#archiwum"),
    (STRONA / "ksiazki/index.html",                            "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/index.html",                   "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/bajki.html",                   "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/cos-zostao-cos-mineo.html",    "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/krotkie-historyjki.html",      "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/opowiadania-20222023.html",    "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/opowiadania-i-wspominki.html", "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/pozostae-teksty.html",         "../irena/index.html#archiwum"),
    (STRONA / "pisarstwo-jozefa/zestaw-opowiadan.html",        "../irena/index.html#archiwum"),
]

LABEL = "Zdjęcia archiwalne Ireny"

for path, href in FILES:
    html = path.read_text(encoding="utf-8")
    new_item = f'<li><a href="{href}">{LABEL}</a></li>'
    # Wstaw przed linkiem "Księga gości"
    new_html, n = re.subn(
        r'(<li><a href="[^"]*#ksiega-gosci">[^<]*</a></li>)',
        new_item + r'\n      \1',
        html
    )
    if n:
        path.write_text(new_html, encoding="utf-8")
        print(f"  OK  {path.relative_to(STRONA)}")
    else:
        print(f"  --  {path.relative_to(STRONA)} (nie znaleziono wzorca)")

# Dodaj id="archiwum" do sekcji w irenie
irena = STRONA / "irena/index.html"
html = irena.read_text(encoding="utf-8")
new_html = html.replace(
    '<section class="archive-section">',
    '<section class="archive-section" id="archiwum">',
    1  # tylko pierwsze wystąpienie
)
if new_html != html:
    irena.write_text(new_html, encoding="utf-8")
    print("  id='archiwum' dodane do sekcji w irena/index.html")
