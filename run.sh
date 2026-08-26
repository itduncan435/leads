#!/bin/bash
# AIO V18.0 Launcher Script
# Phone Number Gen - Grabber - Validator

cd "$(dirname "$0")"
source venv/bin/activate

if [ "$1" = "--gui" ]; then
    python3 gui_app.py
else
    python3 main.py "$@"
fi
