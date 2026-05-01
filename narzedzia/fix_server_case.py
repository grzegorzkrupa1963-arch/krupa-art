"""
Parsuje log WinSCP, wykrywa pliki z DUŻYMI literami w rozszerzeniu na serwerze
i generuje skrypt WinSCP z komendami mv do ich przemianowania.
"""
import re
from pathlib import Path

LOG   = Path(__file__).parent.parent / "sync_log.txt"
OUT   = Path(__file__).parent.parent / "rename_server.wsc"

# Szukamy wpisów z listingu serwera: "type=file;...;  FILENAME"
# Poprzedza je wpis CWD z aktualnym katalogiem na serwerze
dir_re  = re.compile(r'CWD (/public_html/[^\r\n]+)')
file_re = re.compile(r'type=file;.*?; ([^\r\n]+\.(JPG|PNG|JPEG|GIF|BMP|TIFF?))$', re.IGNORECASE)

renames = []  # lista (remote_path_old, remote_path_new)
current_dir = None

with open(LOG, encoding='utf-8', errors='replace') as f:
    for line in f:
        # Aktualizuj bieżący katalog
        m = dir_re.search(line)
        if m:
            current_dir = m.group(1).rstrip('/')
            continue

        # Szukaj pliku z dużą literą w rozszerzeniu
        m = file_re.search(line)
        if m and current_dir:
            fname = m.group(1)
            lower = fname.lower()
            if fname != lower:  # ma wielką literę
                old = f"{current_dir}/{fname}"
                new = f"{current_dir}/{lower}"
                renames.append((old, new))

# Usuń duplikaty
renames = list(dict.fromkeys(renames))

# Oddziel pliki ASCII od tych z polskimi znakami
ascii_renames = [(o, n) for o, n in renames if o.isascii()]
nonascii_renames = [(o, n) for o, n in renames if not o.isascii()]

print(f"Znaleziono {len(renames)} plików do przemianowania")
print(f"  ASCII: {len(ascii_renames)}, z polskimi znakami: {len(nonascii_renames)}")

# Generuj skrypt WinSCP — tylko pliki ASCII (WinSCP używa cp1250 na Windows)
with open(OUT, 'w', encoding='utf-8-sig') as f:  # utf-8-sig = UTF-8 z BOM
    f.write("option batch continue\n")
    f.write("open ftp://vh16153:HASLO@ftp.vh16153.vh.net.pl/\n")
    for old, new in ascii_renames + nonascii_renames:
        f.write(f'mv "{old}" "{new}"\n')
    f.write("exit\n")

print(f"Skrypt zapisany: {OUT}")
