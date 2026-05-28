#!/usr/bin/env python3
"""
Przemianowuje pliki i foldery z polskimi znakami na ASCII,
potem aktualizuje wszystkie referencje w plikach HTML.
"""
import os
import re

STRONA = os.path.dirname(os.path.abspath(__file__))

POLISH = str.maketrans(
    'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
    'acelnoszZACELNOSZZ'
)
# poprawka: wielkie litery osobno
POLISH = str.maketrans(
    'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
    'acelnoszzACELNOSZZ'
)

def ascii_name(name):
    return name.translate(POLISH)

def has_polish(name):
    return name != ascii_name(name)

# --- Krok 1: zbierz wszystkie ścieżki z polskimi znakami (foldery najpierw) ---
to_rename = []  # (stara_ścieżka, nowa_ścieżka)

for root, dirs, files in os.walk(STRONA, topdown=False):
    # pliki
    for fname in files:
        if has_polish(fname):
            old = os.path.join(root, fname)
            new = os.path.join(root, ascii_name(fname))
            to_rename.append((old, new))
    # foldery (topdown=False → dzieci przed rodzicem)
    for d in dirs:
        if has_polish(d):
            old = os.path.join(root, d)
            new = os.path.join(root, ascii_name(d))
            to_rename.append((old, new))

# --- Krok 2: buduj mapę zastępień dla HTML (względne ścieżki) ---
replacements = {}
for old_abs, new_abs in to_rename:
    old_rel = os.path.relpath(old_abs, STRONA).replace('\\', '/')
    new_rel = os.path.relpath(new_abs, STRONA).replace('\\', '/')
    replacements[old_rel] = new_rel
    # dodaj też tylko nazwę (dla ścieżek względnych z ../)
    old_name = os.path.basename(old_abs)
    new_name = os.path.basename(new_abs)
    if old_name not in replacements:
        replacements[old_name] = new_name

# --- Krok 3: przemianuj pliki i foldery lokalnie ---
renamed = 0
skipped = 0
for old, new in to_rename:
    if old == new:
        continue
    if os.path.exists(old):
        if os.path.exists(new):
            print(f"POMIŃ (już istnieje): {os.path.basename(new)}")
            skipped += 1
        else:
            os.rename(old, new)
            print(f"OK: {os.path.basename(old)} -> {os.path.basename(new)}")
            renamed += 1
    else:
        print(f"BRAK: {old}")

print(f"\nPrzemianowano: {renamed}, pominięto: {skipped}")

# --- Krok 4: zaktualizuj wszystkie pliki HTML ---
html_files = []
for root, dirs, files in os.walk(STRONA):
    # pomiń foldery narzędziowe
    dirs[:] = [d for d in dirs if d not in ['.git', 'narzedzia', '__pycache__']]
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

html_updated = 0
for html_path in html_files:
    with open(html_path, encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements.items():
        # zastąp tylko w atrybutach src= href= (nie w tekście widocznym)
        content = content.replace(f'src="{old}', f'src="{new}')
        content = content.replace(f'href="{old}', f'href="{new}')
        content = content.replace(f'/{old}"', f'/{new}"')
        content = content.replace(f'/{old}/', f'/{new}/')
    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"HTML zaktualizowany: {os.path.relpath(html_path, STRONA)}")
        html_updated += 1

print(f"\nZaktualizowano HTML: {html_updated} plików")
print("\nGotowe! Teraz uruchom aktualizuj.bat")
