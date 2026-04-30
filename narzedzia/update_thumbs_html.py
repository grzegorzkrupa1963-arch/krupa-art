"""
Aktualizuje img src w plikach HTML galerii tak, aby wskazywały na thumbs/.
<a href> pozostaje bez zmian (oryginały).
"""
import re
from pathlib import Path

def thumb_src(m):
    path = m.group(1)
    slash = path.rfind('/')
    if slash < 0:
        return m.group(0)
    folder = path[:slash]
    fname  = path[slash+1:]
    dot    = fname.rfind('.')
    if dot < 0:
        return m.group(0)
    stem     = fname[:dot]
    ext      = fname[dot+1:].lower()
    thumb_ex = 'png' if ext == 'png' else 'jpg'
    return f'<img src="{folder}/thumbs/{stem}.{thumb_ex}"'


# ---- Irena ----
irena = Path(r"C:\PROJEKTY\projekt-krupa\strona\irena\index.html")
html = irena.read_text(encoding='utf-8')
new_html = re.sub(
    r'<img src="(\.\./\.\./irena-porebska-krupa/[^"]+)"',
    thumb_src, html
)
irena.write_text(new_html, encoding='utf-8')
changed = html.count('<img src="../../irena') - new_html.count('<img src="../../irena')
print(f"Irena: zaktualizowano src w {new_html.count('thumbs/') - html.count('thumbs/')} obrazach")


# ---- Józef: HTML galleries ----
jozef = Path(r"C:\PROJEKTY\projekt-krupa\strona\jozef\index.html")
html = jozef.read_text(encoding='utf-8')

new_html = re.sub(
    r'<img src="(\.\./\.\./jozef-krupa/[^"]+)"',
    thumb_src, html
)

# ---- Józef: JS buildGallery — dodaj thumbName() i zmień img.src ----
new_html = new_html.replace(
    'function buildGallery(selector, basePath, files) {',
    'function thumbName(f) {\n'
    '    const dot = f.lastIndexOf(".");\n'
    '    const stem = dot >= 0 ? f.slice(0, dot) : f;\n'
    '    const ext  = dot >= 0 ? f.slice(dot + 1).toLowerCase() : "";\n'
    '    return "thumbs/" + stem + (ext === "png" ? ".png" : ".jpg");\n'
    '  }\n\n'
    '  function buildGallery(selector, basePath, files) {'
)
new_html = new_html.replace(
    '    img.src = basePath + f; img.alt',
    '    img.src = basePath + thumbName(f); img.alt'
)

jozef.write_text(new_html, encoding='utf-8')
before_thumbs = html.count('thumbs/')
after_thumbs  = new_html.count('thumbs/')
print(f"Jozef:  zaktualizowano, thumbs/ pojawia sie {after_thumbs} razy (bylo {before_thumbs})")
