@echo off
cd /d %~dp0
echo Uruchamianie lokalnego serwera...
echo Otworz przegladarke na: http://localhost:8080
echo Aby zatrzymac - nacisnij Ctrl+C
echo.
py -3 -m http.server 8080
pause
