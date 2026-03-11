@echo off
REM R U Serious? Backend - Quick Start Script for Windows

echo ============================================================
echo R U Serious? Backend - Quick Start
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python 3.11+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Warning: Some dependencies may have failed to install
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo Warning: .env file not found!
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo.
        echo Please edit .env and add your API keys before continuing
        pause
    )
)

REM Start server
echo.
echo ============================================================
echo Starting R U Serious? Backend Server...
echo ============================================================
echo.
python run.py --reload

pause
