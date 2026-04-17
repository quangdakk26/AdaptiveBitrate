# 🎵 Adaptive Audio Streaming - Web Interface

> Interactive web application for simulating adaptive bitrate audio streaming with real-time visualization and network condition simulation.

## ✨ Features

### 🎯 Core Capabilities
- **Real-time Audio Analysis** - Frame-by-frame energy calculation and classification
- **Adaptive Bitrate Selection** - Intelligent bitrate adjustment based on audio content and network
- **Network Simulation** - 6 different bandwidth profiles to test various scenarios
- **Interactive Visualization** - Professional charts and graphs with Plotly
- **Quality Metrics** - Comprehensive performance indicators and statistics

### 📊 User Interface
- **Clean Dashboard** - 4 main tabs for different views
- **Responsive Design** - Works on desktop and tablet
- **Real-time Updates** - Instant metric calculations
- **Dark Mode Support** - Streamlit's native theme support
- **Professional Styling** - Custom CSS for enhanced UX

### 🔧 Advanced Features
- **Synthetic Audio Generation** - Create test audio with varying characteristics
- **Custom WAV Upload** - Analyze your own audio files
- **Export Results** - Download simulation data as CSV
- **Batch Analysis** - Test multiple scenarios simultaneously
- **Performance Monitoring** - Track system resource usage

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum
- Modern web browser

### Installation (1 minute)

```bash
# Clone/navigate to repository
cd AdaptiveBitrate

# Install dependencies
pip install -r requirements_streamlit.txt
```

### Launch Application

**Windows:**
```bash
run_streamlit.bat
```

**macOS/Linux:**
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

**Direct:**
```bash
streamlit run streamlit_app.py
```

Then open: **http://localhost:8501**

## 🎮 How to Use

### 1️⃣ Load Audio
- Select "Generate Synthetic Audio" for quick testing
- Or upload your own WAV file
- System automatically analyzes energy profile

### 2️⃣ Choose Network Profile
- **Excellent**: Stable >300 kbps
- **Good**: Stable ~128 kbps  
- **Moderate**: Fluctuating ~64 kbps
- **Poor**: Dropping to ~32 kbps
- **Very Poor**: Limited to ~16 kbps
- **Mobile**: Realistic patterns ~50-80 kbps

### 3️⃣ Analyze Results

**Energy Analysis Tab** 📊
- View audio energy over time
- See energy classifications
- Check statistical breakdown

**Bitrate Adaptation Tab** 🎯
- Watch bitrate adjustment in real-time
- Monitor buffer levels
- See network impact

**Metrics Tab** 📈
- Comprehensive performance statistics
- Quality score calculation
- Bitrate distribution

**Configuration Tab** ⚙️
- System parameters
- Algorithm explanation
- Threshold values

## 📈 Key Metrics

| Metric | Description | Good Value |
|--------|-------------|-----------|
| **Average Bitrate** | Mean bitrate during stream | 12-24 kbps |
| **Quality Stability** | Consistency of quality | >90% |
| **Buffer Underruns** | Playback interruptions | 0 |
| **Quality Score** | Overall 0-100 rating | >80 |

## 🏗️ System Architecture

```
Audio Input
    ↓
Energy Analysis (RMS calculation)
    ↓
Network Simulation (Bandwidth patterns)
    ↓
Bitrate Adaptation Algorithm
├─ Energy-based minimum
├─ Network-based maximum
├─ Buffer constraints
└─ Smoothing filter
    ↓
Output Metrics & Visualization
```

## 🔌 Integration

The web app integrates with:
- **Audio Processing**: `03_audio_energy.py` - Energy calculation
- **Encoding/Decoding**: `01_encode_decode.py` - Compression
- **Metrics**: `metrics.py` - Quality assessment

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `STREAMLIT_GUIDE.md` | Comprehensive user guide and tutorials |
| `INSTALLATION_SETUP.md` | Detailed installation and deployment |
| `STREAMLIT_EXAMPLES.md` | Code examples and customization |
| `STREAMLIT_SUMMARY.md` | Complete system overview |

## 🎓 Adaptation Algorithm

For each audio frame:

1. **Analyze Content** - Calculate frame energy level
2. **Monitor Network** - Get available bandwidth
3. **Assess Buffer** - Check playback buffer level
4. **Select Bitrate** - Choose optimal bitrate:
   - Energy-based minimum (silence needs less)
   - Network-based maximum (can't exceed bandwidth)
   - Buffer-aware constraints (if buffer low, reduce)
5. **Apply Smoothing** - Gradual transitions to avoid artifacts

## 🎬 Demo Scenarios

### Scenario 1: Stable Network
- ✅ Maintains high bitrate
- ✅ Zero buffer underruns
- ✅ Quality score: 95%+

### Scenario 2: Mobile with Drops
- ⚠️ Frequent adjustments
- ⚠️ Occasional underruns
- ⚠️ Quality score: 70-80%

### Scenario 3: Poor Network
- 🔴 Low bitrate maintained
- 🔴 Possible underruns  
- 🔴 Quality score: 50-70%

## 💻 System Requirements

| Component | Requirement |
|-----------|------------|
| **Python** | 3.8 - 3.11 |
| **RAM** | 4GB minimum, 8GB+ recommended |
| **Storage** | 500MB for dependencies |
| **Browser** | Modern (Chrome, Firefox, Safari) |
| **Network** | Local only (no cloud needed) |

## 📦 Dependencies

```
streamlit>=1.28.0        # Web framework
plotly>=5.17.0           # Interactive charts
pandas>=2.0.0            # Data analysis
numpy>=1.24.0            # Numerical computing
torch>=2.0.0             # Audio processing
torchaudio>=2.0.0        # Audio library
soundfile>=0.12.1        # WAV file I/O
librosa>=0.10.0          # Audio analysis
```

## 🌐 Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Auto-deployed! 🚀

### Docker
```bash
docker build -t adaptive-streaming .
docker run -p 8501:8501 adaptive-streaming
```

### Cloud Platforms
- AWS EC2, Azure VM, GCP Compute Engine
- Heroku, DigitalOcean, Render
- Kubernetes clusters

See `INSTALLATION_SETUP.md` for detailed deployment.

## 🎨 Customization

### Add Custom Network Profile
```python
# Edit streamlit_app.py
elif profile == "Your Profile":
    bandwidth = your_bandwidth_function(num_frames)
    return np.maximum(bandwidth, 1.5)
```

### Change Bitrate Levels
```python
# In AdaptiveBitrateSimulator
self.bitrate_levels = [1.5, 3.0, 6.0, 12.0, 24.0, 48.0, 96.0]
```

### Modify Energy Thresholds
```python
# In adapt_bitrate()
if frame_energy < 0.15:  # Customize threshold
    min_bitrate = 1.5
```

See `STREAMLIT_EXAMPLES.md` for more examples.

## 🐛 Troubleshooting

### App Won't Start
```bash
# Clear cache
streamlit cache clear

# Reinstall dependencies
pip install -r requirements_streamlit.txt --force-reinstall
```

### Port 8501 In Use
```bash
# Use different port
streamlit run streamlit_app.py --server.port=8502
```

### Audio Upload Fails
- Ensure WAV format
- Check file size (<100MB)
- Try generated audio instead

### Performance Issues
- Use shorter audio (5-10s)
- Close other applications
- Check available RAM

See `INSTALLATION_SETUP.md` for more troubleshooting.

## 📊 Output Example

```
═════════════════════════════════════════════
STREAMING SESSION SUMMARY
═════════════════════════════════════════════

Profile: Good (128 kbps)

Key Metrics:
  • Average Bitrate: 18.5 kbps
  • Quality Score: 87.3 / 100
  • Buffer Underruns: 0
  • Quality Stability: 94.2%

Bitrate Range:
  • Peak: 24.0 kbps
  • Minimum: 3.0 kbps

Audio Analysis:
  • Max Energy: 0.876
  • Mean Energy: 0.452
  • Std Deviation: 0.213

═════════════════════════════════════════════
```

## 🚀 What Can You Do With This?

✅ **Learn** - Understand adaptive streaming algorithms  
✅ **Test** - Experiment with different scenarios  
✅ **Simulate** - Model real-world network conditions  
✅ **Develop** - Extend with custom features  
✅ **Deploy** - Run in production environments  
✅ **Teach** - Use for educational demonstrations  

## 📖 Learning Outcomes

After using this system, you'll understand:
- How adaptive bitrate streaming works
- Audio energy analysis techniques
- Buffer management strategies
- Network condition simulation
- Real-time visualization with Plotly
- Web development with Streamlit

## 🔗 Useful Links

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python)
- [PyTorch Audio](https://pytorch.org/audio)
- [DASH Streaming Standard](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)
- [HLS Streaming](https://developer.apple.com/streaming)

## 📄 File Guide

```
AdaptiveBitrate/
├── streamlit_app.py           ← Main application
├── requirements_streamlit.txt ← Dependencies
├── run_streamlit.sh           ← Launch (Unix)
├── run_streamlit.bat          ← Launch (Windows)
├── STREAMLIT_GUIDE.md         ← User guide
├── INSTALLATION_SETUP.md      ← Setup instructions
├── STREAMLIT_EXAMPLES.md      ← Code examples
└── STREAMLIT_SUMMARY.md       ← Full overview
```

## 💡 Tips & Tricks

- Use shorter audio for faster testing
- Try all network profiles to see differences
- Export results for further analysis
- Customize bitrate levels for your use case
- Monitor system resources while running

## ❓ FAQ

**Q: Can I use my own audio?**  
A: Yes! Upload WAV files in the sidebar.

**Q: Is the network simulation realistic?**  
A: It simulates typical patterns; use real network data for production.

**Q: Can I modify bitrate levels?**  
A: Yes, edit `AdaptiveBitrateSimulator` class.

**Q: Does it require internet?**  
A: No, runs completely locally by default.

**Q: Can I deploy this online?**  
A: Yes, see deployment section above.

## 📧 Support

- 📖 Read documentation files
- 🔍 Check troubleshooting section
- 🐛 Enable debug logging: `--logger.level=debug`
- 💻 Review code comments in `streamlit_app.py`

## 📜 License

Adaptive Audio Streaming - Web Interface (Educational Demo)

---

## ✨ Status

**Current Version:** 1.0.0  
**Last Updated:** April 17, 2026  
**Status:** ✅ Production Ready  

**Features Implemented:**
- ✅ Energy analysis with visualization
- ✅ Bitrate adaptation algorithm
- ✅ Network condition simulation
- ✅ Interactive metrics dashboard
- ✅ Multiple output formats
- ✅ Professional UI/UX
- ✅ Complete documentation
- ✅ Deployment guides

---

## 🎉 Getting Started Today!

```bash
# 1. Navigate to project
cd AdaptiveBitrate

# 2. Install dependencies (first time only)
pip install -r requirements_streamlit.txt

# 3. Run the app
streamlit run streamlit_app.py

# 4. Open browser
# → http://localhost:8501
```

**That's it! Enjoy exploring adaptive audio streaming!** 🎵

---

For more details, check the documentation files or visit the configuration tab in the app.
