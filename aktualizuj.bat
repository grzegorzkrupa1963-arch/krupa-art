@echo off
cd /d %~dp0

echo [1/3] Zapisywanie do Git...
git add .
git commit -m "Aktualizacja %date% %time%"
git push
echo.

echo [2/3] Wgrywanie na serwer VH.pl...

:: Wczytaj haslo z pliku
set /p FTP_PASS=<haslo_ftp.txt

:: Zastap HASLO w skrypcie WinSCP aktualnym haslem
powershell -Command "(Get-Content sync_vh.wsc) -replace 'HASLO', '%FTP_PASS%' | Set-Content sync_vh_tmp.wsc -Encoding UTF8"

:: Sprawdz czy WinSCP jest zainstalowany
if exist "C:\Program Files (x86)\WinSCP\WinSCP.com" (
    "C:\Program Files (x86)\WinSCP\WinSCP.com" /script=sync_vh_tmp.wsc /log=sync_log.txt
) else if exist "C:\Program Files\WinSCP\WinSCP.com" (
    "C:\Program Files\WinSCP\WinSCP.com" /script=sync_vh_tmp.wsc /log=sync_log.txt
) else (
    echo BLAD: WinSCP nie jest zainstalowany!
    echo Pobierz ze strony: https://winscp.net/eng/download.php
    del sync_vh_tmp.wsc 2>nul
    pause
    exit /b 1
)

:: Usun tymczasowy plik z haslem
del sync_vh_tmp.wsc 2>nul

echo.
echo =====================================
echo   Strona zaktualizowana na serwerze!
echo =====================================
pause
