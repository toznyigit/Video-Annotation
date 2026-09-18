@echo off
setlocal enabledelayedexpansion
title Build Standalone Executable for Windows (PyInstaller)

echo ============================================
echo   Building Video Annotator for Windows
echo ============================================
echo.

:: 1. Activate Virtual Environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: 2. Ensure PyInstaller is installed
where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo  [INFO] Installing PyInstaller...
    pip install pyinstaller
)

:: 3. Clean previous build artifacts
echo  [1/3] Cleaning previous build folders...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /f /q "*.spec"

:: 4. Build with PyInstaller
echo  [2/3] Compiling standalone Windows .exe...
pyinstaller ^
    --name="VideoAnnotator" ^
    --onefile ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --add-data="USER_MANUAL.md;." ^
    --add-data="LICENSE;." ^
    --hidden-import="openpyxl" ^
    --hidden-import="openpyxl.styles" ^
    --hidden-import="PyQt6.QtMultimedia" ^
    --hidden-import="PyQt6.QtMultimediaWidgets" ^
    --collect-all="PyQt6" ^
    video_annotator.py

if %errorlevel% neq 0 (
    echo  [ERROR] Build failed!
    pause
    exit /b 1
)

:: 5. Package into zip with User Manual and License
echo  [3/3] Packaging distribution archive (VideoAnnotator-Windows.zip)...
cd dist
copy ..\USER_MANUAL.md .\ >nul
copy ..\LICENSE .\ >nul
powershell -Command "Compress-Archive -Path 'VideoAnnotator.exe', 'USER_MANUAL.md', 'LICENSE' -DestinationPath 'VideoAnnotator-Windows.zip' -Force"
cd ..

echo.
echo ============================================
echo   [SUCCESS] Build Complete!
echo   Output Executable: dist\VideoAnnotator.exe
echo   Output Zip:        dist\VideoAnnotator-Windows.zip
echo ============================================
echo.
pause
