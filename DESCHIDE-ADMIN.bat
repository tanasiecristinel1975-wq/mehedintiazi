@echo off
title MehedintiAzi.ro - Publica Stire
cd /d "C:\Users\MONTAJ\Desktop\folder site mehedinti\mehedintiazi"
echo.
echo  ==========================================
echo   MehedintiAzi.ro - Formular Publicare
echo  ==========================================
echo.
echo  Se deschide formularul in browser...
echo  Nu inchide aceasta fereastra cat timp folosesti formularul!
echo.
start "" "http://localhost:8181/admin/"
python -m http.server 8181
pause
