
@echo off
set "ROOT=%~dp0"

echo Starting ResQ...

start "ResQ Backend" cmd /k "cd /d "%ROOT%backend" && call .venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000"

start "ResQ Frontend" cmd /k "cd /d "%ROOT%frontend" && py -m http.server 5173"

timeout /t 3 >nul
start http://localhost:5173/

echo ResQ launch commands sent.
