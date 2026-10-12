# =====================================================================
#   🏛️ Intelligent-AML (C-STGB) — Enterprise Web Platform Launcher
# =====================================================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  🏛️ Intelligent-AML (C-STGB) — Enterprise Web Platform Launcher" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

$RepoRoot = Resolve-Path "$PSScriptRoot\.."

$PythonExe = if (Test-Path "$RepoRoot\.venv\Scripts\python.exe") { "$RepoRoot\.venv\Scripts\python.exe" } elseif (Test-Path "$RepoRoot\venv\Scripts\python.exe") { "$RepoRoot\venv\Scripts\python.exe" } else { "python" }
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "Set-Location '$RepoRoot'; & '$PythonExe' -m uvicorn src.engine.api:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Starting React 18 + Vite Web Dashboard on http://localhost:3000..." -ForegroundColor Yellow
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "Set-Location '$RepoRoot\frontend'; npm run dev"

Start-Sleep -Seconds 3
Write-Host "`n🚀 Opening Browser..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host "`n=====================================================================" -ForegroundColor Green
Write-Host "  ✅ Platform is Live!" -ForegroundColor Green
Write-Host "  • Frontend UI:    http://localhost:3000" -ForegroundColor White
Write-Host "  • Backend API:   http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Green
