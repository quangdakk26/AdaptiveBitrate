@echo off
REM Startup script for Adaptive Bitrate Web Dashboard (Windows)

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     Adaptive Bitrate Audio System - Web Dashboard            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo 📥 Installing dependencies...
pip install -r requirements_web.txt -q

REM Check if data directories exist
echo 📁 Creating data directories...
if not exist "data\input" mkdir data\input
if not exist "data\output" mkdir data\output

REM Check if audio file exists
if not exist "data\input\sample.wav" (
    echo.
    echo ⚠️  No sample.wav found in data\input\
    echo 📝 Please add audio files to data\input\ before analyzing
    echo.
)

REM Print instructions
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 Starting Server                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo The web dashboard will be available at:
echo.
echo    🌐 http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Flask app
python app.py
pause
