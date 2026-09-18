@echo off
setlocal enabledelayedexpansion
title Video Annotation Tool — Setup & Launch (Windows)

echo.
echo ============================================
echo   Video Annotation Tool (Windows)
echo ============================================
echo.

:: 1. Find Python executable (check py launcher first, then python)
set "PY_CMD="
where py >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=py -3"
) else (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_CMD=python"
    )
)

if "%PY_CMD%"=="" (
    echo  [ERROR] Python 3 was not found on your system.
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: 2. Check / Create Virtual Environment (.venv)
if not exist ".venv\Scripts\activate.bat" (
    if exist "venv\Scripts\activate.bat" (
        set "VENV_PATH=venv"
    ) else (
        echo  [1/3] Creating virtual environment (.venv)...
        %PY_CMD% -m venv .venv
        if errorlevel 1 (
            echo  [ERROR] Failed to create virtual environment.
            pause
            exit /b 1
        )
        set "VENV_PATH=.venv"
        echo  [OK] Virtual environment created.
    )
) else (
    set "VENV_PATH=.venv"
    echo  [1/3] Virtual environment already exists.
)

:: 3. Activate Virtual Environment
echo  [2/3] Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
if errorlevel 1 (
    echo  [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: 4. Install / Verify Dependencies
if exist "requirements.txt" (
    echo  [3/3] Checking dependencies...
    python -m pip install --quiet --upgrade pip
    python -m pip install --quiet -r requirements.txt
    if errorlevel 1 (
        echo  [ERROR] Failed to install requirements.
        pause
        exit /b 1
    )
    echo  [OK] Dependencies ready.
) else (
    echo  [WARN] requirements.txt not found, skipping install.
)

:: 5. Launch the Application
echo.
echo ============================================
echo   Launching Video Annotation Tool...
echo ============================================
echo.
python video_annotator.py

:: 6. Deactivate and Exit
call "%VENV_PATH%\Scripts\deactivate.bat" 2>nul
exit /b 0