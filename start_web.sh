#!/bin/bash
# Startup script for Adaptive Bitrate Web Dashboard

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Adaptive Bitrate Audio System - Web Dashboard            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "📥 Installing dependencies..."
pip install -r requirements_web.txt -q

# Check if data directories exist
echo "📁 Creating data directories..."
mkdir -p data/input
mkdir -p data/output

# Check if audio file exists
if [ ! -f "data/input/sample.wav" ]; then
    echo ""
    echo "⚠️  No sample.wav found in data/input/"
    echo "📝 Please add audio files to data/input/ before analyzing"
    echo ""
fi

# Print instructions
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 Starting Server                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "The web dashboard will be available at:"
echo ""
echo "   🌐 http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask app
python app.py
