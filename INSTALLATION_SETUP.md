# Adaptive Audio Streaming - Installation & Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: 4GB minimum (8GB recommended)
- **Disk**: 2GB for dependencies

## Installation Steps

### Step 1: Clone or Download Repository

```bash
cd /path/to/AdaptiveBitrate
```

### Step 2: Create Virtual Environment (Recommended)

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate
```

#### On Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements_streamlit.txt

# Or install individually
pip install streamlit plotly pandas numpy torch torchaudio soundfile librosa
```

**Installation Time**: 5-15 minutes (torch/torchaudio may take longer)

### Step 4: Verify Installation

```bash
python3 << EOF
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import torch
import torchaudio
import soundfile as sf

print("✅ All dependencies installed successfully!")
EOF
```

## Running the Application

### Option 1: Using Launch Script (Recommended)

#### On macOS/Linux:
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

#### On Windows:
```bash
run_streamlit.bat
```

### Option 2: Direct Command

```bash
streamlit run streamlit_app.py
```

### Option 3: With Custom Port

```bash
streamlit run streamlit_app.py --server.port=8502
```

### Option 4: With Custom Configuration

```bash
streamlit run streamlit_app.py \
  --server.headless=true \
  --server.port=8501 \
  --logger.level=info
```

## First Run

1. **Access Web Interface**:
   - Open browser to `http://localhost:8501`
   - The app will take a few seconds to load

2. **Initial Setup**:
   - Streamlit may ask for analytics approval (optional)
   - Create a cache directory for audio processing

3. **Generate Test Audio**:
   - Select "Generate Synthetic Audio" in sidebar
   - Set duration to 10 seconds
   - Click to run the app

## Configuration

### Streamlit Configuration File

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"

[server]
port = 8501
headless = true
runOnSave = true
enableCORS = true
```

### Audio Cache Configuration

```bash
# Clear Streamlit cache
streamlit cache clear

# Specific cache clear
rm -rf ~/.streamlit/cache
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**:
```bash
pip install streamlit
# Or reinstall all dependencies
pip install -r requirements_streamlit.txt --force-reinstall
```

### Issue: "Module 'torch' has no attribute 'cuda'"

**Solution** (if no GPU):
```bash
# This is normal - CPU-only PyTorch is fine
# The app will work with CPU
```

### Issue: Audio file upload fails

**Solution**:
- Ensure file is valid WAV format
- Check file size < 100 MB
- Try regenerating sample audio instead

### Issue: Streamlit port already in use

**Solution**:
```bash
# Use different port
streamlit run streamlit_app.py --server.port=8502

# Or kill process using port 8501
# Linux/macOS: lsof -ti :8501 | xargs kill -9
# Windows: netstat -ano | findstr :8501
```

### Issue: Application runs slowly

**Solution**:
- Use shorter audio duration (5-10 seconds)
- Close other applications
- Ensure sufficient RAM (check with `top` or Task Manager)
- Disable verbose logging

### Issue: Plots not displaying

**Solution**:
```bash
pip install --upgrade plotly

# Or clear cache
streamlit cache clear
```

## Development Setup

### For Contributors

```bash
# Clone repository
git clone <repository-url>
cd AdaptiveBitrate

# Create development environment
python3 -m venv dev_env
source dev_env/bin/activate  # or dev_env\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements_streamlit.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Format code
black *.py src/
```

## Performance Optimization

### For Large Audio Files

```python
# Reduce frame size for faster processing
frame_size = 1024  # Default 2048

# Use shorter duration
duration_seconds = 5  # Default 10
```

### For Low-End Systems

1. Disable animated visualizations
2. Reduce number of frames processed
3. Use CPU-only PyTorch
4. Increase cache timeout

```bash
streamlit run streamlit_app.py \
  --client.toolbarMode=viewer \
  --logger.level=warning
```

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

### Build and Run

```bash
# Build image
docker build -t adaptive-streaming:latest .

# Run container
docker run -p 8501:8501 adaptive-streaming:latest

# Run with volume mount
docker run -p 8501:8501 -v /path/to/audio:/app/data adaptive-streaming:latest
```

## Cloud Deployment

### Streamlit Cloud

1. Push repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Enter repository URL
4. Deploy with one click

### Heroku

```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.headless=true" > Procfile

# Create setup.sh
echo "mkdir -p ~/.streamlit/ && echo '[server]\nserverPort = \$PORT' > ~/.streamlit/config.toml" > setup.sh

# Deploy
heroku create your-app-name
git push heroku main
```

### AWS/Azure/GCP

1. Create VM instance
2. Install Python 3.10+
3. Clone repository and install dependencies
4. Use systemd service for auto-start

## Production Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements_streamlit.txt
- [ ] Test audio file generated successfully
- [ ] Web interface loads at http://localhost:8501
- [ ] Energy analysis tab displays correctly
- [ ] Bitrate adaptation simulation runs without errors
- [ ] Metrics are calculated and displayed
- [ ] Plots and visualizations render properly
- [ ] File upload functionality tested
- [ ] Different network profiles tested

## Support & Debugging

### Verbose Logging

```bash
streamlit run streamlit_app.py --logger.level=debug
```

### View Logs

```bash
# Streamlit logs are printed to console
# For persistent logs:
streamlit run streamlit_app.py > streamlit.log 2>&1 &
tail -f streamlit.log
```

### System Information

```bash
python3 << EOF
import platform
import torch
import streamlit as st

print(f"Python: {platform.python_version()}")
print(f"OS: {platform.system()} {platform.release()}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CPU Count: {torch.get_num_threads()}")
EOF
```

## Next Steps

1. **Customize Network Profiles**: Modify simulation parameters
2. **Add Custom Audio**: Upload your own WAV files
3. **Analyze Results**: Experiment with different scenarios
4. **Extend Features**: Add new visualizations or metrics
5. **Deploy**: Host on cloud platform or local server

## References

- [Streamlit Documentation](https://docs.streamlit.io)
- [PyTorch Audio](https://pytorch.org/audio)
- [Plotly Documentation](https://plotly.com/python)
- [DASH Adaptive Streaming](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)

## License & Attribution

Adaptive Audio Streaming - Educational Demo

Questions? Check the logs, verify dependencies, or refer to individual module documentation.
