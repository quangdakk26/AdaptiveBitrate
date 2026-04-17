@echo off
REM Launch Streamlit Adaptive Audio Streaming Web Interface (Windows)

title Adaptive Audio Streaming - Streamlit
color 0A

echo.
echo ==========================================
echo Adaptive Audio Streaming - Streamlit
echo ==========================================
echo.

REM Check if Streamlit is installed
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 02 Installing required dependencies...
    pip install streamlit plotly pandas numpy torch torchaudio soundfile librosa
    echo 03 Dependencies installed
    echo.
)

REM Check Python dependencies
echo 04 Checking Python dependencies...
python3 -c "import streamlit, plotly, pandas, numpy, torch, torchaudio, soundfile; print('05 All dependencies available')" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Please run: pip install -r requirements_streamlit.txt
    pause
    exit /b 1
)

echo.
echo 06 Launching Streamlit application...
echo 07 Open your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py
pause
