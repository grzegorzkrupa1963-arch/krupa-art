@echo off
cd /d %~dp0
git add .
git commit -m "Aktualizacja %date% %time%"
git push
echo.
echo =====================================
echo   Strona zaktualizowana!
echo =====================================
pause
