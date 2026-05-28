import os, re

STRONA = os.path.dirname(os.path.abspath(__file__))
IMG_ATTR = re.compile(r'(src|href)="([^"]+\.(jpg|jpeg|png|gif|JPG|JPEG|PNG))"', re.IGNORECASE)

problems = []

for root, dirs, files in os.walk(STRONA):
    dirs[:] = [d for d in dirs if d not in ['.git', 'narzedzia', '__pycache__']]
    for fname in files:
        if not fname.endswith('.html'): continue
        html_path = os.path.join(root, fname)
        try: content = open(html_path, encoding='utf-8').read()
        except: content = open(html_path, encoding='cp1250').read()

        for m in IMG_ATTR.finditer(content):
            rel_ref = m.group(2)
            # rozwiaz sciezke wzgledem lokalizacji HTML
            abs_ref = os.path.normpath(os.path.join(root, rel_ref))
            if not os.path.exists(abs_ref):
                problems.append((os.path.relpath(html_path, STRONA), rel_ref, abs_ref))

if not problems:
    print('Wszystkie obrazki istnieja lokalnie.')
else:
    print(f'BRAKUJACE PLIKI ({len(problems)}):')
    for html_rel, ref, abs_path in problems:
        print(f'  HTML: {html_rel}')
        print(f'  ref:  {ref}')
        # sprawdz czy jest plik o podobnej nazwie (case mismatch)
        folder = os.path.dirname(abs_path)
        target = os.path.basename(abs_path)
        if os.path.isdir(folder):
            candidates = [f for f in os.listdir(folder) if f.lower() == target.lower()]
            if candidates:
                print(f'  CASE: znaleziono jako -> {candidates[0]}')
        print()
