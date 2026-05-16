@echo off
chcp 65001 >nul
title Generator Stire - MehedintiAzi.ro

echo ================================================
echo   GENERATOR STIRE - mehedintiazi.ro
echo ================================================
echo.
echo PASUL 1: Completeaza STIRE-NOUA.txt
echo  - Salveaza cu Ctrl+S
echo  - Inchide Notepad cand ai terminat
echo.
pause

cd /d "%~dp0"
notepad STIRE-NOUA.txt

echo.
echo [2/4] Generez fisierul HTML...
python genereaza-stire.py
if errorlevel 1 goto EROARE

echo.
echo [3/4] Actualizez sitemapul...
python genereaza-sitemap.py

echo.
echo [4/4] Trimit pe site (push automat)...
git add -A

set COMMIT_MSG=Stire noua
if exist .commit_msg.txt (
    set /p COMMIT_MSG=<.commit_msg.txt
    del .commit_msg.txt
)

git commit -m "%COMMIT_MSG%"
git push origin main

echo.
echo ================================================
echo   GATA! Stirea e live in ~60 secunde.
echo   Se deschide site-ul automat...
echo ================================================

timeout /t 60 /nobreak
start https://www.mehedintiazi.ro
goto FINAL

:EROARE
echo.
echo ================================================
echo   EROARE! Verifica textul de mai sus.
echo   Corecteaza STIRE-NOUA.txt si ruleaza din nou.
echo ================================================

:FINAL
pause
