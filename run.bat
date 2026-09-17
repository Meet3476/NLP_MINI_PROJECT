@echo off
title NLP Text Summarizer - Transformer Mini Project Launcher
echo ======================================================================
echo    Automatic Text Summarization Using Transformer Models (Flask)
echo ======================================================================
echo.

cd /d "%~dp0"

if not exist ".venv" (
    echo [*] Creating Python Virtual Environment...
    python -m venv .venv
    echo [*] Installing Required Dependencies...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo.
echo ======================================================================
echo [*] Launching Flask Web Server...
echo [*] Opening browser at: http://127.0.0.1:5000
echo ======================================================================
echo.

:: Automatically open browser after 2 seconds
start "" http://127.0.0.1:5000

:: Run Flask server using virtualenv python directly
.venv\Scripts\python.exe app.py

echo.
echo Server stopped. Press any key to exit.
pause
