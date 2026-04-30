"""
Aktualizuje data-pswp-width/height w plikach HTML na podstawie
rzeczywistych wymiarów miniaturek (thumbs/).
"""
import re
from pathlib import Path
from PIL import Image

BASE = Path(r"C:\PROJEKTY\projekt-krupa")

# Miniaturki mają identyczny stosunek boków co oryginały
def thumb_for_href(href: str) -> Path | None:
    """../../irena-porebska-krupa/X/file.JPG  →  BASE/irena-porebska-krupa/X/thumbs/file.jpg"""
    clean = href.replace("../../", "")          # irena-porebska-krupa/X/file.JPG
    orig  = BASE / clean                        # bezwzględna ścieżka oryginału
    ext   = orig.suffix.lower()
    thumb_ext = ".png" if ext == ".png" else ".jpg"
    thumb = orig.parent / "thumbs" / (orig.stem + thumb_ext)
    return thumb if thumb.exists() else None


def get_dims(p: Path):
    try:
        with Image.open(p) as img:
            return img.size   # (width, height)
    except Exception:
        return None


def fix_html(html_path: Path) -> int:
    html  = html_path.read_text(encoding="utf-8")
    count = 0

    # Wzorzec: href="../../.../file.ext" data-pswp-width="NNN" data-pswp-height="MMM"
    pat = re.compile(
        r'href="(\.\./\.\./[^"]+)"\s+data-pswp-width="\d+"\s+data-pswp-height="\d+"'
    )

    def sub(m):
        nonlocal count
        href  = m.group(1)
        thumb = thumb_for_href(href)
        if thumb:
            dims = get_dims(thumb)
            if dims:
                count += 1
                return f'href="{href}" data-pswp-width="{dims[0]}" data-pswp-height="{dims[1]}"'
        return m.group(0)   # nie znaleziono — zostaw jak było

    new_html = pat.sub(sub, html)
    if count:
        html_path.write_text(new_html, encoding="utf-8")
    return count


n_irena = fix_html(BASE / "strona/irena/index.html")
n_jozef = fix_html(BASE / "strona/jozef/index.html")
print(f"Irena: {n_irena} obrazow zaktualizowanych")
print(f"Jozef: {n_jozef} obrazow zaktualizowanych")
