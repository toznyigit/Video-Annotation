#!/usr/bin/env bash
# ==============================================================================
# Video Annotation Tool — Setup & Launch (macOS & Linux)
# Licensed under GNU General Public License v3.0 (GPL-3.0)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "============================================"
echo "  Video Annotation Tool (macOS / Linux)"
echo "============================================"
echo ""

# Find Python 3
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo " [ERROR] Python 3 not found. Please install Python 3 (https://www.python.org) and try again."
    exit 1
fi

echo " Using Python: $($PYTHON_BIN --version)"

# Create virtual environment if missing
if [ ! -d ".venv" ]; then
    echo " [1/3] Creating virtual environment in .venv..."
    $PYTHON_BIN -m venv .venv
    echo " [OK] Virtual environment created."
else
    echo " [1/3] Virtual environment (.venv) already exists."
fi

# Activate virtual environment
echo " [2/3] Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo " [3/3] Checking & installing requirements..."
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo " [OK] Requirements ready."
else
    echo " [WARN] requirements.txt not found, skipping dependency install."
fi

echo ""
echo "============================================"
echo "  Launching Video Annotation Tool..."
echo "============================================"
echo ""

python video_annotator.py

echo ""
echo " Application closed."
