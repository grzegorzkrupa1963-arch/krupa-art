from pathlib import Path
from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
THUMB_MAX = 400
BASE = Path(r"C:\PROJEKTY\projekt-krupa")

folders = [
    BASE / "irena-porebska-krupa/malarstwo/A. Malarstwo - Statki ryby",
    BASE / "irena-porebska-krupa/malarstwo/B. Malarstwo - Portrety",
    BASE / "irena-porebska-krupa/malarstwo/C. Malarstwo - Martwe natury",
    BASE / r"irena-porebska-krupa/malarstwo/D. Malarstwo - Pejzaże",
    BASE / "irena-porebska-krupa/rysunki",
    BASE / "irena-porebska-krupa/zdjecia-archiwalne",
    BASE / "jozef-krupa/malarstwo/Abstrakcje",
    BASE / "jozef-krupa/malarstwo/Powidoki_Sceniczne",
    BASE / "jozef-krupa/malarstwo/Rozne_obrazy",
    BASE / "jozef-krupa/grafiki",
    BASE / "jozef-krupa/Grafiki komputerowe",
    BASE / "jozef-krupa/minimal-ART/Minimal_ART_1",
    BASE / "jozef-krupa/minimal-ART/Minimal_ART_2",
    BASE / "jozef-krupa/fotografia/Bazantaria/Bazantaria_zbior_1",
    BASE / "jozef-krupa/fotografia/Parki/Parki_1",
    BASE / "jozef-krupa/fotografia/Pejzaze/Pejzaze_1",
    BASE / "jozef-krupa/fotografia/Pejzaze/Pejzaze_2",
    BASE / "jozef-krupa/fotografia/Inne/2022_A",
    BASE / "jozef-krupa/fotografia/Inne/2022_B",
    BASE / "jozef-krupa/rysunki",
    BASE / "jozef-krupa/zdjecia-archiwalne",
]

total_done = 0
total_skip = 0

for folder in folders:
    if not folder.is_dir():
        print(f"BRAK: {folder}")
        continue
    thumbs = folder / "thumbs"
    thumbs.mkdir(exist_ok=True)
    images = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)
    done = skip = 0
    for img_path in images:
        ext = img_path.suffix.lower()
        thumb_ext = ".jpg" if ext in {".jpg", ".jpeg", ".tif", ".tiff", ".bmp"} else ".png"
        thumb_path = thumbs / (img_path.stem + thumb_ext)
        if thumb_path.exists():
            done += 1
            continue
        try:
            with Image.open(img_path) as img:
                img = img.convert("RGB") if ext in {".tif", ".tiff", ".bmp"} else img
                img.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
                save_fmt = "JPEG" if thumb_ext == ".jpg" else "PNG"
                img.save(thumb_path, format=save_fmt, quality=85, optimize=True)
            done += 1
        except Exception as e:
            print(f"  BLAD {img_path.name}: {e}")
            skip += 1
    print(f"  {folder.name}: {done} miniaturek, {skip} bledow")
    total_done += done
    total_skip += skip

print(f"\nRAZEM: {total_done} miniaturek, {total_skip} bledow")
