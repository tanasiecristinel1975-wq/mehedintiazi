@echo off
cd /d "%~dp0"
python ACTUALIZEAZA-BREAKING-NEWS.py
if %errorLevel% neq 0 (
    echo [!!] Eroare la rulare! Verifica Python.
    pause
) else (
    echo.
    echo [OK] Breaking News actualizat cu succes!
    timeout /t 3 /nobreak >nul
)
