<<<<<<< HEAD
# Quick Start Guide - Web Dashboard

## 🚀 Quick Start (5 minutes)

### Option 1: Linux/macOS

```bash
# Make script executable
chmod +x start_web.sh

# Run the startup script
./start_web.sh
```

### Option 2: Windows

Double-click: `start_web.bat`

Or manually:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements_web.txt
python app.py
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate          # Linux/macOS
# or
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements_web.txt

# Run the server
python app.py
```

## 📂 Prepare Your Files

1. **Create directories:**
   ```bash
   mkdir -p data/input
   mkdir -p data/output
   ```

2. **Add audio files:**
   - Copy your `.wav` files to `data/input/`
   - Example: `cp my_music.wav data/input/`

3. **Open the dashboard:**
   - Go to `http://localhost:5000` in your browser

## 🎯 First Analysis

1. **Select Audio File**
   - Choose a file from the dropdown

2. **Set Bandwidth**
   - Use slider or click a scenario button
   - Try "DSL/WiFi Home" (10 Mbps) first

3. **Click Analyze**
   - View energy statistics
   - See adaptive bitrate selection

4. **Click Encode**
   - Encode with adaptive settings
   - View quality metrics
   - Output file saved to `data/output/`

## 🔍 What to Look For

### Energy Analysis
- **Mean Energy**: Average audio power
- **Energy Level**: High/Medium/Low based on content
- **Selected Bitrate**: Automatically chosen for best quality/bandwidth ratio

### Visualizations
1. **Energy + Bitrate Chart**
   - Orange line = frame energy
   - Green line = adaptive bitrate
   - See how bitrate responds to energy

2. **Energy Distribution Pie**
   - What % of frames are High/Medium/Low energy
   - Helps understand audio content

3. **Quality Metrics**
   - **SNR**: Higher is better (>30 dB is good)
   - **MSE**: Lower is better
   - **Compression**: How much data was saved

## 💡 Example Scenarios

### Test 1: Slow Mobile (1 Mbps)
- Bandwidth: 1.0 Mbps
- Result: Bitrate drops to 1.5-3 kbps
- Use for: Emergency scenarios, rural areas

### Test 2: 4G LTE (5 Mbps)
- Bandwidth: 5.0 Mbps
- Result: Balanced quality/compression (3-6 kbps)
- Use for: Mobile streaming

### Test 3: Home WiFi (25 Mbps)
- Bandwidth: 25 Mbps
- Result: High quality (12-24 kbps)
- Use for: Local networks

## 🛠️ Troubleshooting

### "Address already in use"
Flask is already running. Kill the process:
```bash
# Linux/macOS
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "No audio files showing"
1. Ensure audio is in `data/input/`
2. Files must be `.wav` format
3. Refresh browser page

### Charts not showing
- Clear browser cache (Ctrl+Shift+Delete)
- Try a different browser
- Check browser console (F12) for errors

## 📊 Frame-wise Analysis

For detailed per-frame adaptation:

1. Check "Frame-wise Adaptive Bitrate"
2. Adjust Frame Size (default 2048)
   - Smaller = more detailed, slower
   - Larger = less detailed, faster
3. Click Analyze
4. See bitrate change for each frame

## 🎛️ Customize Settings

### Change Bitrate Matrix
Edit `app.py`:
```python
BITRATE_CONFIG = {
    'high_bandwidth': {
        'high_energy': 24.0,    # Adjust here
        'medium_energy': 12.0,
        'low_energy': 6.0
    },
    # ...
}
```

### Add New Scenarios
Edit the `/api/scenarios` endpoint in `app.py`:
```python
scenarios_data = [
    {'name': 'My Custom', 'bandwidth': 7.5, 'description': '...'},
    # ...
]
```

## 📝 Output Files

Encoded files are saved to `data/output/`:
- **Filename format**: `encoded_{bandwidth_level}_{energy_level}_{bitrate}kbps.wav`
- Example: `encoded_medium_bandwidth_high_energy_6kbps.wav`

## 🔗 API Testing

Test endpoints with curl:

```bash
# Analyze audio
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"filename": "sample.wav", "bandwidth": 10.0}'

# Get scenarios
curl http://localhost:5000/api/scenarios

# Get bitrate config
curl http://localhost:5000/api/bitrate-config
```

## 📈 Performance Tips

1. **Smaller files** = faster processing
2. **Reduce frame size** = faster analysis (less accurate)
3. **Close other apps** = better performance
4. **Use modern browser** = smoother UI

## 🚫 Known Limitations

- Maximum file size: ~100 MB (browser limitation)
- Sample rate: Auto-detected from audio file
- Only processes mono or stereo audio
- Requires Python 3.7+

## ✅ Next Steps

1. ✓ Start the web server
2. ✓ Add audio files to `data/input/`
3. ✓ Select and analyze files
4. ✓ Test different bandwidth scenarios
5. ✓ Review metrics and visualizations
6. ✓ Encode with optimal settings

## 📞 Support

For detailed information:
- See `WEB_README.md` for complete documentation
- Check `ADAPTIVE_BITRATE_README.md` for system details
- Review `app.py` for API endpoints

---

**Happy encoding! 🎵**
=======
# 🚀 QUICK START - 5 Minutes to Streaming!

## For the Impatient 👇

### Step 1: Install (1 minute)
```bash
cd AdaptiveBitrate
pip install streamlit plotly pandas numpy torch torchaudio soundfile
```

### Step 2: Launch (30 seconds)
```bash
streamlit run streamlit_app.py
```

### Step 3: Open Browser (30 seconds)
Visit: **http://localhost:8501**

### Step 4: Play! (3 minutes)
- Generate test audio
- Select a network profile
- Watch the magic happen ✨

**Done!** You're now streaming adaptively! 🎵

---

## What You're Looking At

### 📊 Energy Analysis
- Shows how energy changes over time
- Silence needs less bitrate
- Loud parts need more bitrate

### 🎯 Bitrate Adaptation
- Green line = what we're sending
- Gray line = what's available
- When bandwidth drops, bitrate drops (intelligent!)

### 📈 Metrics
- Quality Score: Higher is better
- Buffer Underruns: Should be 0
- Stability: How smooth is it

### ⚙️ Config
- Just for reference
- Don't need to touch anything

---

## Try These Scenarios

### Test 1: Good Network
- Select "Good (128 kbps)"
- Notice stable bitrate
- Quality stays high

### Test 2: Choppy Network
- Select "Poor (32 kbps)"
- Watch bitrate reduce
- Quality drops but no buffering

### Test 3: Mobile Network
- Select "Mobile/Variable"
- Constant adjustments
- Still keeps things smooth

---

## Pro Tips 💡

1. **Shorter Audio = Faster**: Use 5-10 seconds for quick tests
2. **Your Own Audio**: Upload any WAV file
3. **Export Results**: Download CSV in Metrics tab
4. **Debug Mode**: `streamlit run streamlit_app.py --logger.level=debug`

---

## Troubleshooting (30 seconds)

### App won't start?
```bash
pip install streamlit --upgrade
streamlit run streamlit_app.py
```

### Port 8501 already in use?
```bash
streamlit run streamlit_app.py --server.port=8502
```

### Missing dependencies?
```bash
pip install -r requirements_streamlit.txt
```

---

## What's Happening Behind the Scenes?

1. **Audio comes in** → Split into tiny frames
2. **Energy is calculated** → How loud is each frame?
3. **Network is simulated** → What bandwidth do we have?
4. **Bitrate is chosen** → Highest quality we can send
5. **Buffer is managed** → Smooth playback
6. **Results are displayed** → Charts and metrics

---

## Key Insight 💡

The system asks for each frame:
> "This audio is [ENERGY]. We have [BANDWIDTH]. Should we use bitrate X, Y, or Z?"

The answer tries to:
- ✅ Keep quality high
- ✅ Never exceed bandwidth
- ✅ Avoid buffering
- ✅ Make smooth transitions

---

## File Guide

| File | What it does |
|------|---|
| `streamlit_app.py` | The web app (everything you see) |
| `03_audio_energy.py` | Calculates audio energy |
| `run_streamlit.sh` | Launcher for Mac/Linux |
| `run_streamlit.bat` | Launcher for Windows |

## Documentation Files

| File | For |
|------|-----|
| `README_STREAMLIT.md` | Overview (start here!) |
| `STREAMLIT_GUIDE.md` | Full details |
| `INSTALLATION_SETUP.md` | Fixing problems |
| `STREAMLIT_EXAMPLES.md` | Advanced stuff |

---

## Common Questions ❓

**Q: Will this work with my audio?**  
A: Yes! WAV files only though. MP3/AAC coming soon.

**Q: Is this real streaming?**  
A: It simulates streaming perfectly. Real audio codecs in dev.

**Q: Can I change bitrates?**  
A: Yes! Edit line ~45 in `streamlit_app.py`

**Q: Does it need internet?**  
A: Nope! 100% local.

**Q: Can I run this on my server?**  
A: Yes! See INSTALLATION_SETUP.md

---

## Advanced: Want More?

See these files:
- Want to customize? → `STREAMLIT_EXAMPLES.md`
- Want to deploy? → `INSTALLATION_SETUP.md`
- Want all details? → `STREAMLIT_GUIDE.md`

---

## System Check (Optional)

```bash
# Verify everything is ready
python3 verify_streamlit.py
```

Should show all ✅ checks passing.

---

## Stats You'll See

- **Avg Bitrate**: Your average data rate
- **Quality Score**: 0-100 rating
- **Buffer Underruns**: Should be 0
- **Quality Stability**: Higher % = more consistent

---

## That's It!

You now know enough to:
✅ Run the app  
✅ Load audio  
✅ See bitrate adapt  
✅ Understand the metrics  

**Everything else is bonus!** 🎉

---

## Need Help?

1. Check `README_STREAMLIT.md`
2. Run `verify_streamlit.py`
3. See error message? Google it + "streamlit"
4. Still stuck? Check `INSTALLATION_SETUP.md`

---

## Want to Learn More?

- 📖 Full guide: `STREAMLIT_GUIDE.md`
- 💻 Code examples: `STREAMLIT_EXAMPLES.md`
- 🏗️ Architecture: `STREAMLIT_SUMMARY.md`
- 🗂️ Overview: `INDEX.md`

---

**Enjoy! Happy streaming! 🎵**

Last updated: April 17, 2026  
Questions? Start with README_STREAMLIT.md
>>>>>>> 2ecf02c (sua loi)
