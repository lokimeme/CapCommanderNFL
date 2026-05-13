#!/bin/bash
# CapCommanderNFL Production Runner
# Detaches the app from the terminal and ensures it runs in the background.

APP_DIR="/home/lohith/CapCommanderNFL"
VENV_BIN="$APP_DIR/venv/bin/streamlit"
LOG_FILE="$APP_DIR/logs/streamlit_prod.log"

mkdir -p "$APP_DIR/logs"

echo "Stopping any existing CapCommander sessions..."
# Use a more specific pkill to avoid hitting the NBA app
pgrep -f "streamlit run app.py" | while read pid; do
    if grep -q "CapCommanderNFL" "/proc/$pid/cmdline" 2>/dev/null; then
        kill $pid
    fi
done

echo "Starting CapCommanderNFL in background mode..."
cd "$APP_DIR"
nohup "$VENV_BIN" run app.py --server.port 8502 --server.address 0.0.0.0 > "$LOG_FILE" 2>&1 &

echo "App started. Logs are being written to $LOG_FILE"
echo "Process ID: $!"
