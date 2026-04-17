#!/bin/bash
# Launch Streamlit Adaptive Audio Streaming Web Interface

echo "=========================================="
echo "Adaptive Audio Streaming - Streamlit"
echo "=========================================="
echo ""

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing required dependencies..."
    pip install streamlit plotly pandas numpy torch torchaudio soundfile librosa
    echo "✅ Dependencies installed"
    echo ""
fi

# Check if Python dependencies are available
echo "🔍 Checking Python dependencies..."
python3 << EOF
try:
    import streamlit
    import plotly
    import pandas
    import numpy
    import torch
    import torchaudio
    import soundfile
    print("✅ All dependencies available")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Please run: pip install -r requirements_streamlit.txt"
    exit 1
fi

echo ""
echo "🚀 Launching Streamlit application..."
echo "📊 Open your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py
