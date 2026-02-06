@echo off
echo Fishing Bot GUI - Build and Run Script
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
python -m pip install -r requirements_gui.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Build executable
echo Building executable...
python build_executable.py
if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

REM Test the executable
echo Testing executable...
python test_executable.py
if errorlevel 1 (
    echo Warning: Executable test failed, but continuing...
)

REM Run the executable
echo Starting Fishing Bot GUI...
cd dist
start FishingBotGUI.exe

echo Done! The GUI should now be running.
pause
