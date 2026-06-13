@echo off
echo Starting NGO Impact Dashboard...
start "API" cmd /k "cd /d %~dp0api && ..\..\.venv\Scripts\uvicorn main:app --reload --host 127.0.0.1 --port 8000"
timeout /t 2 /nobreak >nul
start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo API:      http://localhost:8000
echo Dashboard: http://localhost:5173
echo.
echo For PostgreSQL: docker compose up -d postgres
echo Then run: python scripts\init_database.py
