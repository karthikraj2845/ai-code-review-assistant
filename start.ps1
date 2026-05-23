# AI Code Review Assistant - Quick Launcher

Write-Host "Starting AI Code Review Assistant Demo..." -ForegroundColor Green

# 1. Start Backend in a new visible window
Write-Host "Launching Backend API Server on http://127.0.0.1:8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

# 2. Start Frontend in a new visible window
Write-Host "Launching Frontend Dev Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

# 3. Wait a moment for servers to spin up, then open browser
Start-Sleep -Seconds 3
Write-Host "Opening web browser to the app..." -ForegroundColor Green
Start-Process "http://localhost:5174"

Write-Host "Launcher finished successfully!" -ForegroundColor Green
