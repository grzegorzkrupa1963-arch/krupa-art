#!/usr/bin/env python3
"""
Aktualizuje referencje w plikach HTML - zamienia polskie znaki
w atrybutach src= i href= na ASCII.
Obsługuje pliki w UTF-8 i Windows-1250.
"""
import os
import re

STRONA = os.path.dirname(os.path.abspath(__file__))

POLISH = str.maketrans(
    'acelnoszZACELNOSZZ',  # dummy - overridden below
    'acelnoszZACELNOSZZ'
)
POLISH = str.maketrans(
    'acelnoszZACELNOSZZ',
    'acelnoszZACELNOSZZ'
)
POLISH = {
    ord('a'): 'a', ord('c'): 'c',  # dummy reset
}
POLISH = str.maketrans(
    'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
    'acelnoszzACELNOSZZ'
)

def ascii_name(text):
    return text.translate(POLISH)

def fix_attr_value(val):
    """Zamień polskie znaki w wartości atrybutu src/href."""
    return ascii_name(val)

def fix_html(content):
    """Zamień polskie znaki tylko w atrybutach src= i href=."""
    def replace_attr(m):
        attr = m.group(1)   # src lub href
        val  = m.group(2)   # wartość atrybutu
        fixed = fix_attr_value(val)
        return f'{attr}="{fixed}"'
    return re.sub(r'(src|href)="([^"]*)"', replace_attr, content)

def read_file(path):
    for enc in ('utf-8', 'utf-8-sig', 'cp1250', 'latin-1'):
        try:
            with open(path, encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Nie mozna odczytac: {path}")

html_files = []
for root, dirs, files in os.walk(STRONA):
    dirs[:] = [d for d in dirs if d not in ['.git', 'narzedzia', '__pycache__']]
    for fname in files:
        if fname.endswith('.html'):
            html_files.append(os.path.join(root, fname))

updated = 0
for path in html_files:
    content, enc = read_file(path)
    fixed = fix_html(content)
    if fixed != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        rel = os.path.relpath(path, STRONA)
        print(f"Zaktualizowano ({enc}): {rel}")
        updated += 1
    else:
        rel = os.path.relpath(path, STRONA)
        print(f"Bez zmian: {rel}")

print(f"\nZaktualizowano {updated} plikow HTML.")
print("Gotowe! Uruchom aktualizuj.bat")
