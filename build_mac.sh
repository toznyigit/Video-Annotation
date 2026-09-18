#!/usr/bin/env bash
# ==============================================================================
# Build Standalone Executable for macOS (PyInstaller)
# Produces dist/VideoAnnotator.app and dist/VideoAnnotator-macOS.zip
# Preserves symlinks, code signatures, and excludes unused plugins
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
echo " [1/4] Cleaning previous build folders..."
rm -rf build dist *.spec

# Build with PyInstaller
echo " [2/4] Compiling standalone macOS bundle..."
pyinstaller \
    --name="VideoAnnotator" \
    --windowed \
    --noconfirm \
    --clean \
    --osx-bundle-identifier="com.toznyigit.videoannotator" \
    --add-data="USER_MANUAL.md:." \
    --add-data="LICENSE:." \
    --hidden-import="openpyxl" \
    --hidden-import="openpyxl.styles" \
    --hidden-import="PyQt6.QtCore" \
    --hidden-import="PyQt6.QtGui" \
    --hidden-import="PyQt6.QtWidgets" \
    --hidden-import="PyQt6.QtMultimedia" \
    --hidden-import="PyQt6.QtMultimediaWidgets" \
    --collect-all="PyQt6.QtMultimedia" \
    --collect-all="PyQt6.QtMultimediaWidgets" \
    --exclude-module="PyQt6.QtQml" \
    --exclude-module="PyQt6.QtQuick" \
    --exclude-module="PyQt6.QtWebEngineCore" \
    --exclude-module="PyQt6.QtWebEngineWidgets" \
    --exclude-module="PyQt6.QtLocation" \
    --exclude-module="PyQt6.QtPositioning" \
    --exclude-module="PyQt6.QtSensors" \
    --exclude-module="PyQt6.QtBluetooth" \
    --exclude-module="PyQt6.Qt3DCore" \
    --exclude-module="PyQt6.Qt3DRender" \
    --exclude-module="PyQt6.Qt3DQuick" \
    video_annotator.py

# Re-sign the entire .app bundle deeply to satisfy macOS ARM64 PAC security
echo " [3/4] Deep signing application bundle for macOS ARM64..."
codesign --force --deep --sign - "dist/VideoAnnotator.app"

# Package into zip with symlink preservation (-y)
echo " [4/4] Creating distribution archive (VideoAnnotator-macOS.zip)..."
cd dist
cp ../USER_MANUAL.md ./
cp ../LICENSE ./
# Note: -y preserves symlinks which are vital for macOS framework resolution!
zip -r -y -q "VideoAnnotator-macOS.zip" "VideoAnnotator.app" "USER_MANUAL.md" "LICENSE"
cd ..

echo ""
echo "============================================"
echo "  [SUCCESS] Build Complete!"
echo "  Output App:    dist/VideoAnnotator.app"
echo "  Output Zip:    dist/VideoAnnotator-macOS.zip"
echo "============================================"
