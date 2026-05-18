#!/bin/bash
# 🏈 CapCommander NFL: Multi-Service Production Runner
# Ensures both Backend (FastAPI) and Frontend (Streamlit) run persistently.

APP_DIR="/home/lohith/CapCommanderNFL"
VENV_PYTHON="$APP_DIR/venv/bin/python"
LOG_DIR="$APP_DIR/logs"

mkdir -p "$LOG_DIR"

echo "🛑 Cleaning up old CapCommander processes..."
# Kill uvicorn (backend) and streamlit (frontend)
pkill -f "backend.app.main:app"
pkill -f "streamlit run app.py"

echo "🚀 Starting FastAPI Backend (Port 8000)..."
cd "$APP_DIR"
nohup "$VENV_PYTHON" -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

echo "🚀 Starting Streamlit Frontend (Port 8502)..."
nohup "$APP_DIR/venv/bin/streamlit" run app.py --server.port 8502 --server.address 0.0.0.0 > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

echo "✅ CapCommander Suite is now running in the background."
echo "   - Backend PID: $BACKEND_PID (Logs: $LOG_DIR/backend.log)"
echo "   - Frontend PID: $FRONTEND_PID (Logs: $LOG_DIR/frontend.log)"
echo "🔗 Streamlit: http://localhost:8502"
echo "🔗 API Docs: http://localhost:8000/docs"
