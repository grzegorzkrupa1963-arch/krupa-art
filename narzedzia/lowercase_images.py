"""
Przemianowuje wszystkie pliki graficzne na małe litery
i aktualizuje odwołania w plikach HTML.
"""
import os
import re
from pathlib import Path

STRONA = Path(__file__).parent.parent
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp'}

# --- Krok 1: zbierz wszystkie pliki do przemianowania ---
renames = {}  # stara_nazwa_pliku -> nowa_nazwa_pliku (tylko basename)

for root, dirs, files in os.walk(STRONA):
    # Pomiń folder narzedzia
    dirs[:] = [d for d in dirs if d != 'narzedzia']
    for fname in files:
        ext = Path(fname).suffix.lower()
        if ext not in IMAGE_EXTS:
            continue
        lower = fname.lower()
        if fname != lower:
            renames[os.path.join(root, fname)] = os.path.join(root, lower)

print(f"Pliki do przemianowania: {len(renames)}")

# --- Krok 2: przemianuj pliki (przez nazwę tymczasową, bo Windows) ---
renamed_ok = 0
renamed_err = 0
for old_path, new_path in renames.items():
    try:
        if old_path.lower() == new_path.lower() and old_path != new_path:
            # Ten sam plik wg Windows — trzeba przez temp
            tmp_path = new_path + '.__tmp__'
            os.rename(old_path, tmp_path)
            os.rename(tmp_path, new_path)
        elif not os.path.exists(new_path):
            os.rename(old_path, new_path)
        else:
            print(f"  POMINIĘTO (już istnieje): {new_path}")
            continue
        renamed_ok += 1
    except Exception as e:
        print(f"  BŁĄD: {old_path} -> {e}")
        renamed_err += 1

print(f"Przemianowano: {renamed_ok}, błędów: {renamed_err}")

# --- Krok 3: aktualizuj odwołania w HTML ---
# Buduj mapę: stara_basename -> nowa_basename
basename_map = {
    Path(old).name: Path(new).name
    for old, new in renames.items()
}

html_files = list(STRONA.rglob('*.html'))
html_updated = 0

for html_path in html_files:
    try:
        text = html_path.read_text(encoding='utf-8', errors='replace')
        original = text
        for old_name, new_name in basename_map.items():
            # Zamień wszystkie wystąpienia starej nazwy na nową
            text = text.replace(old_name, new_name)
        if text != original:
            html_path.write_text(text, encoding='utf-8')
            html_updated += 1
            print(f"  Zaktualizowano: {html_path.relative_to(STRONA)}")
    except Exception as e:
        print(f"  BŁĄD HTML: {html_path} -> {e}")

print(f"\nZaktualizowano plików HTML: {html_updated}")
print("Gotowe!")
