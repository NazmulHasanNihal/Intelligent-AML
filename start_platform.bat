@echo off
title Intelligent-AML Enterprise Platform Launcher
cls
echo =====================================================================
echo   🏛️ Intelligent-AML (C-STGB) — Enterprise Web Platform
echo   Production Spatio-Temporal Graph Neural Surveillance Desk
echo =====================================================================
echo.

cd /d "%~dp0"

echo [1/2] Launching High-Throughput FastAPI Streaming Backend (Port 8000)...
if exist ".\venv\Scripts\python.exe" (
    start "Intelligent-AML Backend" cmd /k ".\venv\Scripts\python.exe -m uvicorn src.engine.api:app --host 127.0.0.1 --port 8000 --reload"
) else if exist ".\.venv\Scripts\python.exe" (
    start "Intelligent-AML Backend" cmd /k ".\.venv\Scripts\python.exe -m uvicorn src.engine.api:app --host 127.0.0.1 --port 8000 --reload"
) else (
    start "Intelligent-AML Backend" cmd /k "python -m uvicorn src.engine.api:app --host 127.0.0.1 --port 8000 --reload"
)

echo [2/2] Launching React 18 + Vite Web Dashboard (Port 3000)...
cd frontend
start "Intelligent-AML Frontend" cmd /k "npm run dev"
cd ..

timeout /t 3 >nul
echo.
echo Launching Default Browser at http://localhost:3000...
start http://localhost:3000

echo.
echo =====================================================================
echo   ✅ Intelligent-AML Surveillance Platform is LIVE!
echo   • Frontend UI:    http://localhost:3000
echo   • API Swagger:   http://127.0.0.1:8000/docs
echo   • ReDoc Specs:   http://127.0.0.1:8000/redoc
echo =====================================================================
echo.
pause
