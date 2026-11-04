#!/bin/bash
# JP Sales Agent Suite - Dual App Launcher (Linux/macOS)
# Runs both Streamlit apps: Sales Pipeline (8501) and Affiliate Studio (8502)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "🚀 JP Sales Agent Suite - Dual App Launcher"
echo "============================================================"

echo ""
echo "Starting Sales Pipeline on port 8501..."
cd "$SCRIPT_DIR/../sales-pipeline"
python -m streamlit run app.py --server.port 8501 --server.headless true &
SALES_PID=$!

echo "Starting Affiliate Studio on port 8502..."
sleep 3
cd "$SCRIPT_DIR/../affiliate-studio"
python -m streamlit run app.py --server.port 8502 --server.headless true &
JPFD_PID=$!

echo ""
echo "============================================================"
echo "✅ Both apps running!"
echo "============================================================"
echo "📊 Sales Pipeline:    http://localhost:8501"
echo "🛍️  Affiliate Studio: http://localhost:8502"
echo "============================================================"
echo ""
echo "Press Ctrl+C to stop both apps..."

# Trap Ctrl+C
trap 'echo ""; echo "🛑 Shutting down..."; kill $SALES_PID $JPFD_PID 2>/dev/null; wait $SALES_PID $JPFD_PID 2>/dev/null; echo "✅ All apps stopped"; exit 0' INT

# Wait for both processes
wait $SALES_PID
wait $JPFD_PID