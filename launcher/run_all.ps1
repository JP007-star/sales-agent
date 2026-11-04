<#
.SYNOPSIS
    JP Sales Agent Suite - Dual App Launcher (PowerShell)
    Runs both Streamlit apps: Sales Pipeline (8501) and Affiliate Studio (8502)
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 JP Sales Agent Suite - Dual App Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "`nStarting Sales Pipeline on port 8501..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\..\sales-pipeline'; python -m streamlit run app.py --server.port 8501 --server.headless true"

Write-Host "Starting Affiliate Studio on port 8502..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\..\affiliate-studio'; python -m streamlit run app.py --server.port 8502 --server.headless true"

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "✅ Both apps launching!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "📊 Sales Pipeline:    http://localhost:8501" -ForegroundColor Cyan
Write-Host "🛍️  Affiliate Studio: http://localhost:8502" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green
Write-Host "`nClose the PowerShell windows to stop the apps."
Write-Host "Press any key to exit this launcher..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")