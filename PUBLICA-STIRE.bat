@echo off
chcp 65001 >nul
title Publicare Stire - MehedintiAzi.ro

echo ================================================
echo   PUBLICARE STIRE - mehedintiazi.ro
echo ================================================

cd /d "C:\Users\MONTAJ\Desktop\folder site mehedinti\mehedintiazi"

echo.
echo [1/4] Actualizez sitemapul...
python genereaza-sitemap.py

echo [2/4] Adaug fisierele noi...
git add -A

echo [3/4] Commit...
set /p MSG=Titlu scurt stire (pentru commit):
git commit -m "%MSG%"

echo [4/4] Push pe GitHub + Cloudflare (master + main)...
git push origin master
git push origin master:main

echo.
echo ================================================
echo   Push GATA! Cloudflare deployeaza acum...
echo   Verificare automata in 60 secunde...
echo ================================================

timeout /t 60 /nobreak

echo.
echo Verific daca site-ul s-a actualizat...
start https://www.mehedintiazi.ro
echo Browserul s-a deschis. Verifica daca stirea apare pe homepage.

echo.
pause
