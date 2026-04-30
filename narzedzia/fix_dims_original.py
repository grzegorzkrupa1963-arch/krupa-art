"""Aktualizuje data-pswp-width/height używając wymiarów ORYGINALNYCH plików (nie miniaturek)."""
import re
from pathlib import Path
from PIL import Image

BASE = Path(r"C:\PROJEKTY\projekt-krupa")

HTML_FILES = [
    BASE / "strona/irena/index.html",
    BASE / "strona/jozef/index.html",
]

PATTERN = re.compile(
    r'(<a\s[^>]*href="(\.\./\.\./[^"]+)"[^>]*data-pswp-width=")(\d+)("'
    r'\s+data-pswp-height=")(\d+)(")'
)

def get_dims(href_rel):
    clean = href_rel[6:]  # strip ../../
    path = BASE / clean
    if not path.exists():
        return None
    try:
        with Image.open(path) as im:
            return im.size  # (width, height)
    except Exception as e:
        print(f"  BLAD {path.name}: {e}")
        return None

for html_path in HTML_FILES:
    html = html_path.read_text(encoding="utf-8")
    changed = 0
    errors = 0

    def replace(m):
        global changed, errors
        href = m.group(2)
        dims = get_dims(href)
        if dims is None:
            errors += 1
            return m.group(0)
        w, h = dims
        changed += 1
        return m.group(1) + str(w) + m.group(4) + str(h) + m.group(6)

    new_html = PATTERN.sub(replace, html)
    html_path.write_text(new_html, encoding="utf-8")
    print(f"{html_path.name}: {changed} zaktualizowanych, {errors} bledow")
