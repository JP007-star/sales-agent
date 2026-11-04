@echo off
REM JP Sales Agent Suite - Dual App Launcher (Windows Batch)
REM Runs both Streamlit apps: Sales Pipeline (8501) and Affiliate Studio (8502)

echo ============================================================
echo 🚀 JP Sales Agent Suite - Dual App Launcher
echo ============================================================

cd /d "%~dp0"

echo.
echo Starting Sales Pipeline on port 8501...
start "Sales Pipeline" cmd /k "cd /d "%~dp0..\sales-pipeline" && python -m streamlit run app.py --server.port 8501 --server.headless true"

echo.
echo Starting Affiliate Studio on port 8502...
timeout /t 3 /nobreak >nul
start "Affiliate Studio" cmd /k "cd /d "%~dp0..\affiliate-studio" && python -m streamlit run app.py --server.port 8502 --server.headless true"

echo.
echo ============================================================
echo ✅ Both apps launching!
echo ============================================================
echo 📊 Sales Pipeline:    http://localhost:8501
echo 🛍️  Affiliate Studio:  http://localhost:8502
echo ============================================================
echo.
echo Close this window to stop both apps.
pause