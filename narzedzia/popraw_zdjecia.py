"""
popraw_zdjecia.py — poprawa jakości zdjęć malarstwa

Dla każdego pliku obrazu w podanym folderze:
  1. Auto-levels (rozciągnięcie histogramu per kanał, percentyl 1%-99%)
  2. Odszumianie bilateralne (zachowuje krawędzie / pociągnięcia pędzla)
  3. Wyostrzanie unsharp mask
  4. Zapis jako JPG 85%

Użycie:
    py popraw_zdjecia.py <folder>
    py popraw_zdjecia.py <folder> --backup          # kopia oryginałów w _oryginaly/
    py popraw_zdjecia.py <folder> --rekurencyjnie   # przetwarza wszystkie podfoldery

Obsługiwane formaty wejściowe: jpg, jpeg, png, tif, tiff, bmp
"""

import sys
import argparse
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp'}
SKIP_DIRS  = {'thumbs', '_oryginaly'}


def auto_levels(img: np.ndarray) -> np.ndarray:
    """Rozciągnięcie histogramu per kanał (percentyl 1%–99%)."""
    out = img.astype(np.float32)
    for c in range(3):
        ch = out[:, :, c]
        lo, hi = np.percentile(ch, 1), np.percentile(ch, 99)
        if hi > lo:
            out[:, :, c] = np.clip((ch - lo) / (hi - lo) * 255, 0, 255)
    return out.astype(np.uint8)


def denoise_bilateral(img: np.ndarray) -> np.ndarray:
    """
    Filtr bilateralny — wygładza szum, zachowuje krawędzie.
    Wielokrotnie szybszy niż NLM, dobry dla faktur malarskich.
    """
    # Dla bardzo dużych obrazów przetwarzamy w oryginalnym rozmiarze;
    # bilateralFilter jest O(n·d²) — manageable dla d=9.
    return cv2.bilateralFilter(img, d=9, sigmaColor=60, sigmaSpace=60)


def unsharp_mask(img: np.ndarray,
                 sigma: float = 1.2,
                 strength: float = 0.65) -> np.ndarray:
    """Wyostrzanie metodą unsharp mask."""
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def process_file(path: Path, backup_dir: Path | None) -> str:
    try:
        pil = Image.open(path).convert('RGB')
    except Exception as e:
        return f"BLAD odczytu: {e}"

    img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

    if backup_dir is not None:
        backup_dir.mkdir(exist_ok=True)
        shutil.copy2(path, backup_dir / path.name)

    img = auto_levels(img)
    img = denoise_bilateral(img)
    img = unsharp_mask(img)

    out_path = path.with_suffix('.jpg')
    ok, buf = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    if not ok:
        return "BLAD kodowania"
    out_path.write_bytes(buf.tobytes())

    if path.suffix.lower() not in ('.jpg', '.jpeg') and out_path != path:
        path.unlink()
        return f"-> {out_path.name}  (z {path.suffix})"

    return "OK"


def process_folder(folder: Path, backup: bool) -> int:
    files = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )
    if not files:
        return 0

    backup_dir = folder / "_oryginaly" if backup else None
    print(f"\n{folder}  ({len(files)} plików)")

    for i, f in enumerate(files, 1):
        status = process_file(f, backup_dir)
        print(f"  [{i:>3}/{len(files)}] {f.name:<50} {status}")

    return len(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--rekurencyjnie", action="store_true")
    args = parser.parse_args()

    root = Path(args.folder)
    if not root.is_dir():
        print(f"Nie znaleziono folderu: {root}")
        sys.exit(1)

    total = 0

    if args.rekurencyjnie:
        dirs = sorted({
            f.parent for f in root.rglob("*")
            if f.is_file()
            and f.suffix.lower() in EXTENSIONS
            and not any(s in f.parts for s in SKIP_DIRS)
        })
        for d in dirs:
            total += process_folder(d, args.backup)
    else:
        total = process_folder(root, args.backup)

    print(f"\nGotowe. Przetworzono {total} plików.")


if __name__ == "__main__":
    main()
