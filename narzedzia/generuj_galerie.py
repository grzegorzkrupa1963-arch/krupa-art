#!/usr/bin/env python3
"""
generuj_galerie.py — generator miniaturek i kodu HTML dla galerii PhotoSwipe v5.

Użycie:
    python generuj_galerie.py <folder_ze_zdjęciami>

Efekt:
    - Miniaturki (max 400px) w podfolderze thumbs\
    - Oryginały przeniesione do oryginaly\
    - Wygenerowany fragment HTML zapisany do galeria.html
    - Wymiary oryginałów odczytane i wstawione w data-pswp-width/height

Wymagania:
    pip install Pillow
"""

import sys
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Błąd: brakuje biblioteki Pillow.")
    print("Zainstaluj: pip install Pillow")
    sys.exit(1)

SUPPORTED = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
THUMB_MAX = 400


def make_thumb(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        img = img.convert("RGB") if src.suffix.lower() in {".tif", ".tiff"} else img
        img.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
        save_format = "JPEG" if src.suffix.lower() in {".jpg", ".jpeg", ".tif", ".tiff"} else "PNG"
        img.save(dst, format=save_format, quality=85, optimize=True)


def get_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size  # (width, height)


def build_html(items: list[dict]) -> str:
    lines = ['<div class="gallery-grid" id="gal-NAZWA">']
    for item in items:
        orig  = item["orig_rel"].replace("\\", "/")
        thumb = item["thumb_rel"].replace("\\", "/")
        w, h  = item["width"], item["height"]
        alt   = item["name"]
        lines.append(
            f'  <a href="{orig}" data-pswp-width="{w}" data-pswp-height="{h}">'
            f'<img src="{thumb}" alt="{alt}" loading="lazy"></a>'
        )
    lines.append("</div>")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        print(f"Błąd: folder nie istnieje: {folder}")
        sys.exit(1)

    images = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if not images:
        print(f"Brak obsługiwanych obrazów w: {folder}")
        sys.exit(0)

    thumbs_dir = folder / "thumbs"
    orig_dir   = folder / "oryginaly"
    thumbs_dir.mkdir(exist_ok=True)
    orig_dir.mkdir(exist_ok=True)

    items = []
    total = len(images)
    print(f"Znaleziono {total} obrazów w: {folder}")

    for i, img_path in enumerate(images, 1):
        print(f"  [{i}/{total}] {img_path.name}", end="", flush=True)

        # Wymiary oryginału przed przeniesieniem
        try:
            w, h = get_dimensions(img_path)
        except Exception as e:
            print(f" — pominięto (błąd odczytu: {e})")
            continue

        # Miniaturka w thumbs/
        thumb_ext  = ".jpg" if img_path.suffix.lower() in {".jpg", ".jpeg", ".tif", ".tiff"} else ".png"
        thumb_name = img_path.stem + thumb_ext
        thumb_path = thumbs_dir / thumb_name

        try:
            make_thumb(img_path, thumb_path)
        except Exception as e:
            print(f" — pominięto (błąd miniatury: {e})")
            continue

        # Przenieś oryginał
        orig_dest = orig_dir / img_path.name
        if orig_dest.exists():
            orig_dest = orig_dir / (img_path.stem + "_dup" + img_path.suffix)
        shutil.move(str(img_path), str(orig_dest))

        items.append({
            "name":      img_path.stem,
            "orig_rel":  f"oryginaly/{orig_dest.name}",
            "thumb_rel": f"thumbs/{thumb_name}",
            "width":     w,
            "height":    h,
        })
        print(f" — {w}×{h}px  →  miniatura {thumb_path.name}")

    if not items:
        print("Nic nie zostało przetworzone.")
        sys.exit(1)

    html = build_html(items)
    out_file = folder / "galeria.html"
    out_file.write_text(html, encoding="utf-8")

    print(f"\nGotowe!")
    print(f"  Miniaturki : {thumbs_dir}")
    print(f"  Oryginały  : {orig_dir}")
    print(f"  Kod HTML   : {out_file}")
    print()
    print("Fragment HTML (skopiuj do index.html, zmień id i dodaj PhotoSwipe):")
    print("-" * 60)
    print(html)


if __name__ == "__main__":
    main()
