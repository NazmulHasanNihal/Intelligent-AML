@echo off
title Intelligent-AML Platform Launcher
echo =====================================================================
echo   🏛️ Intelligent-AML (C-STGB) — Enterprise Web Platform
echo =====================================================================
echo.

cd /d "%~dp0\.."

echo [1/2] Launching FastAPI Backend Microservice (Port 8000)...
start "Intelligent-AML Backend" cmd /k ".\venv\Scripts\python.exe -m uvicorn src.engine.api:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Launching React 18 + Vite Web Dashboard (Port 3000)...
cd frontend
start "Intelligent-AML Web Platform" cmd /k "npm run dev"

echo.
echo =====================================================================
echo   🚀 All systems active!
echo   • Web Dashboard:  http://localhost:3000
echo   • API Swagger:    http://127.0.0.1:8000/docs
echo =====================================================================
pause
