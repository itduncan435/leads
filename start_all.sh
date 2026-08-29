#!/bin/bash
# start_all.sh
# Start all servers for the AIO / Hacker Terminal project
# Usage: bash start_all.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv if available
if [ -d "venv" ]; then
    source venv/bin/activate
fi

mkdir -p logs

pkill -f "gui_app.py" 2>/dev/null || true
pkill -f "telegram_bot.py" 2>/dev/null || true

# Start Flask GUI
echo "[+] Starting Flask GUI (port 5000)..."
nohup python3 gui_app.py > logs/gui.log 2>&1 &
GUI_PID=$!
echo "    Flask GUI PID: $GUI_PID"

# Start Telegram Bot
echo "[+] Starting Telegram Bot..."
nohup python3 telegram_bot.py > logs/telegram_bot.log 2>&1 &
BOT_PID=$!
echo "    Telegram Bot PID: $BOT_PID"

# Start CLI main in background detached session
echo "[+] Starting CLI Main (background)..."
nohup python3 main.py > logs/cli_main.log 2>&1 &
CLI_PID=$!
echo "    CLI Main PID: $CLI_PID"

echo ""
echo "========================================"
echo " All servers started"
echo "========================================"
echo " Flask GUI : http://localhost:5000  (PID $GUI_PID)"
echo " Telegram  : Bot polling            (PID $BOT_PID)"
echo " CLI Main  : Background             (PID $CLI_PID)"
echo ""
echo " Logs:"
echo "  logs/gui.log"
echo "  logs/telegram_bot.log"
echo "  logs/cli_main.log"
echo ""
echo " Stop all: pkill -f 'gui_app.py|telegram_bot.py|main.py'"
