#!/usr/bin/env bash
# ==============================================================================
# Build Standalone Executable for macOS (PyInstaller)
# Produces dist/VideoAnnotator.app and dist/VideoAnnotator-macOS.zip
# No Python installation required by end users!
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Building Video Annotator for macOS"
echo "============================================"

# Activate virtual environment if available
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
fi

# Ensure PyInstaller is installed
if ! command -v pyinstaller >/dev/null 2>&1; then
    echo " [INFO] Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous build artifacts
echo " [1/3] Cleaning previous build folders..."
rm -rf build dist *.spec

# Build with PyInstaller
echo " [2/3] Compiling standalone macOS bundle..."
pyinstaller \
    --name="VideoAnnotator" \
    --windowed \
    --noconfirm \
    --clean \
    --add-data="USER_MANUAL.md:." \
    --add-data="LICENSE:." \
    --hidden-import="openpyxl" \
    --hidden-import="openpyxl.styles" \
    --hidden-import="PyQt6.QtMultimedia" \
    --hidden-import="PyQt6.QtMultimediaWidgets" \
    --collect-all="PyQt6" \
    video_annotator.py

# Package into zip with User Manual and License for easy distribution
echo " [3/3] Creating distribution archive (VideoAnnotator-macOS.zip)..."
cd dist
cp ../USER_MANUAL.md ./
cp ../LICENSE ./
zip -r -q "VideoAnnotator-macOS.zip" "VideoAnnotator.app" "USER_MANUAL.md" "LICENSE"
cd ..

echo ""
echo "============================================"
echo "  [SUCCESS] Build Complete!"
echo "  Output App:    dist/VideoAnnotator.app"
echo "  Output Zip:    dist/VideoAnnotator-macOS.zip"
echo "============================================"
