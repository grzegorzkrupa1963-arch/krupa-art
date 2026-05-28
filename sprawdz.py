import os, re
STRONA = os.path.dirname(os.path.abspath(__file__))
POLISH = re.compile(r'(src|href)="([^"]*[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ][^"]*)"')
found = False
for root, dirs, files in os.walk(STRONA):
    dirs[:] = [d for d in dirs if d not in ['.git', 'narzedzia']]
    for fname in files:
        if not fname.endswith('.html'): continue
        path = os.path.join(root, fname)
        try: content = open(path, encoding='utf-8').read()
        except: content = open(path, encoding='cp1250').read()
        matches = POLISH.findall(content)
        if matches:
            found = True
            print(f'PROBLEM w {os.path.relpath(path, STRONA)}: {len(matches)} referencji z polskimi znakami')
            for m in matches[:5]: print(f'  {m[0]}="{m[1]}"')
if not found:
    print('OK - brak polskich znakow w src/href we wszystkich HTML.')
