# Intelligent AML - Streaming Pipeline Launcher
# This script starts the Docker containers and opens separate windows for the API, Consumer, and a Mock Data Generator.

Write-Host "Starting Docker containers (Redpanda and Flink)..." -ForegroundColor Cyan
docker compose up -d

Write-Host "Waiting for Redpanda to initialize (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 1. Start the FastAPI Webhook in a new window
Write-Host "Launching FastAPI Webhook..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'FastAPI Streaming Webhook' -ForegroundColor Green; if (Test-Path venv\Scripts\Activate.ps1) { .\venv\Scripts\Activate.ps1 }; .\venv\Scripts\uvicorn.exe src.ingestion.streaming.api:app --reload --port 8000"

# 2. Start the PyFlink Consumer in a new window
Write-Host "Launching PyFlink Consumer..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'PyFlink Streaming Consumer' -ForegroundColor Green; if (Test-Path venv\Scripts\Activate.ps1) { .\venv\Scripts\Activate.ps1 }; Start-Sleep -Seconds 3; .\venv\Scripts\python.exe src/ingestion/streaming/flink_consumer.py"

# 3. Start a Mock Data Generator loop in a new window to simulate live traffic
Write-Host "Launching Mock Data Generator..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Realistic Live Data Generator' -ForegroundColor Green; if (Test-Path venv\Scripts\Activate.ps1) { .\venv\Scripts\Activate.ps1 }; .\venv\Scripts\python.exe src/ingestion/streaming/mock_data_generator.py"

Write-Host "All services launched! You should see 3 new PowerShell windows." -ForegroundColor Green
Write-Host "To stop the docker containers later, run: docker-compose down" -ForegroundColor Yellow
