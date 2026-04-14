# Adaptive Bitrate Web Dashboard

A modern, interactive web interface for the Adaptive Bitrate Audio Encoding System.

## Features

- 📊 **Real-time Energy Analysis**: Visualize frame-wise audio energy
- 🎚️ **Bandwidth Simulation**: Test different network conditions (1.5 Mbps - 100 Mbps)
- 📈 **Adaptive Bitrate Charts**: See how bitrate adapts to energy levels
- 🔧 **Frame-wise Optimization**: Adjust bitrate for each individual frame
- 📉 **Quality Metrics**: Compare SNR, MSE, and compression ratios
- 🎯 **Quick Scenarios**: Pre-configured bandwidth scenarios

## Installation

### 1. Create Virtual Environment

```bash
cd /home/imdakk/Documents/AdaptiveBitrate/AdaptiveBitrate
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements_web.txt
```

### 3. Create Data Directories

```bash
mkdir -p data/input
mkdir -p data/output
mkdir -p templates
mkdir -p static
```

### 4. Prepare Audio Files

Place your audio files (.wav format) in the `data/input/` directory:

```bash
cp your_audio_file.wav data/input/sample.wav
```

## Running the Web Application

### Start the Flask Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### 1. Select Audio File
- Choose an audio file from the dropdown menu
- Files must be in `data/input/` directory

### 2. Configure Bandwidth
- Use the slider to adjust available bandwidth (0.5 - 100 Mbps)
- Or click a pre-configured scenario button:
  - **Satellite/Low Mobile** (1.0 Mbps)
  - **Mobile 3G** (2.0 Mbps)
  - **Mobile 4G LTE** (5.0 Mbps)
  - **DSL/WiFi Home** (10.0 Mbps)
  - **Fast WiFi/Fiber** (25.0 Mbps)
  - **Gigabit Fiber** (100.0 Mbps)

### 3. Frame-wise Analysis (Optional)
- Check "Frame-wise Adaptive Bitrate" for per-frame analysis
- Adjust Frame Size (default: 2048)
- Adjust Hop Size (default: 512)

### 4. Analyze
- Click **📊 Analyze** to perform energy analysis
- View statistics and visualizations
- See energy levels and adaptive bitrate selection

### 5. Encode
- Click **⚙️ Encode** to encode the audio with adaptive bitrate
- View quality metrics (SNR, MSE, Compression Ratio)
- Output file is saved to `data/output/`

## Visualizations

### Frame-wise Energy & Bitrate Chart
- **Orange Line**: Frame energy levels (normalized)
- **Green Line**: Adaptive bitrate selected for each frame
- Shows how bitrate changes based on energy and bandwidth

### Bitrate Distribution Pie Chart
- Distribution of frames by energy level:
  - **Red**: High Energy (>60% of max)
  - **Orange**: Medium Energy (30-60% of max)
  - **Blue**: Low Energy (<30% of max)

### Quality Metrics Display
- **SNR (dB)**: Signal-to-Noise Ratio (higher is better)
- **MSE**: Mean Squared Error (lower is better)
- **Compression Ratio**: Original size / Compressed size
- **Duration**: Audio file duration in seconds
- **Original/Compressed Size**: File size comparison

## Bitrate Selection Matrix

The system uses this matrix to select optimal bitrate:

| Bandwidth | High Energy | Medium Energy | Low Energy |
|-----------|------------|---------------|------------|
| High (≥10 Mbps)      | 24 kbps    | 12 kbps       | 6 kbps     |
| Medium (3-10 Mbps)   | 12 kbps    | 6 kbps        | 3 kbps     |
| Low (<3 Mbps)        | 6 kbps     | 3 kbps        | 1.5 kbps   |

## API Endpoints

### `/api/analyze` (POST)
Analyze audio file energy

**Request:**
```json
{
  "filename": "sample.wav",
  "bandwidth": 10.0
}
```

**Response:**
```json
{
  "filename": "sample.wav",
  "bandwidth_mbps": 10.0,
  "energy_level": "medium_energy",
  "bandwidth_level": "medium_bandwidth",
  "selected_bitrate": 6.0,
  "energy_stats": {
    "mean": 0.123,
    "max": 0.654,
    "min": 0.001,
    "std": 0.087,
    "median": 0.105,
    "total": 123.456
  },
  "frame_energies": [0.001, 0.045, 0.123, ...],
  "total_frames": 1000,
  "sample_rate": 24000,
  "duration": 5.5
}
```

### `/api/framewise-adaptive` (POST)
Frame-wise adaptive bitrate analysis

**Request:**
```json
{
  "filename": "sample.wav",
  "bandwidth": 5.0,
  "frame_size": 2048,
  "hop_size": 512
}
```

**Response:**
```json
{
  "filename": "sample.wav",
  "bandwidth_mbps": 5.0,
  "bandwidth_level": "medium_bandwidth",
  "total_frames": 1000,
  "frame_energies": [0.001, 0.045, ...],
  "framewise_bitrates": [3.0, 6.0, 6.0, ...],
  "framewise_energy_levels": ["low_energy", "medium_energy", ...],
  "average_bitrate": 4.5,
  "bitrate_stats": {
    "min": 1.5,
    "max": 6.0,
    "mean": 4.5,
    "std": 1.2
  }
}
```

### `/api/encode` (POST)
Encode audio with adaptive bitrate

**Request:**
```json
{
  "filename": "sample.wav",
  "bandwidth": 10.0,
  "use_framewise": false
}
```

**Response:**
```json
{
  "filename": "sample.wav",
  "bandwidth_mbps": 10.0,
  "energy_level": "medium_energy",
  "bandwidth_level": "medium_bandwidth",
  "selected_bitrate": 6.0,
  "output_filename": "encoded_medium_bandwidth_medium_energy_6kbps.wav",
  "metrics": {
    "mse": 0.00123,
    "snr_db": 28.45,
    "compression_ratio": 2.5,
    "original_bits": 1920000,
    "compressed_bits": 768000,
    "duration": 5.5
  }
}
```

### `/api/scenarios` (GET)
Get predefined bandwidth scenarios

### `/api/bitrate-config` (GET)
Get bitrate configuration matrix

## Project Structure

```
AdaptiveBitrate/
├── app.py                          # Flask web server
├── 01_encode_decode.py            # Adaptive bitrate encoder
├── 02_compare_bitrates.py         # Bitrate comparison
├── 03_audio_energy.py             # Energy calculator
├── metrics.py                      # Quality metrics
├── requirements_web.txt           # Python dependencies
├── templates/
│   └── index.html                 # Web interface HTML
├── static/
│   ├── style.css                  # Styling
│   └── script.js                  # Frontend logic
├── data/
│   ├── input/                     # Input audio files
│   └── output/                    # Encoded output files
└── WEB_README.md                  # This file
```

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
python app.py --port 5001
# Or modify in app.py: app.run(port=5001)
```

### No Audio Files Found
- Ensure audio files are in `data/input/` directory
- Files must be in `.wav` format
- Supported sample rates: 8kHz, 16kHz, 24kHz, 44.1kHz, 48kHz

### Connection Refused Error
- Ensure Flask server is running
- Check if port 5000 is accessible
- Firewall might be blocking the connection

### Chart Not Rendering
- Clear browser cache
- Check browser console for errors (F12)
- Ensure Chart.js CDN is accessible

## Performance Tips

1. **Smaller Audio Files**: Use samples under 30 seconds for faster processing
2. **Reduce Frame Size**: Smaller frame size = faster analysis but less accuracy
3. **Browser Optimization**: Use Chrome/Firefox for best performance

## Advanced Configuration

### Customize Bitrate Matrix
Edit `app.py`:
```python
BITRATE_CONFIG = {
    'high_bandwidth': {
        'high_energy': 24.0,    # Adjust these values
        'medium_energy': 12.0,
        'low_energy': 6.0
    },
    # ... more levels
}
```

### Adjust Energy Thresholds
In `app.py`, modify the `get_energy_level()` function:
```python
def get_energy_level(mean_energy, max_energy):
    if mean_energy > max_energy * 0.6:  # Change 0.6 threshold
        return 'high_energy'
    # ... rest of function
```

## Performance Monitoring

Monitor server logs for encoding time and metrics:
```bash
# Run with verbose logging
python -u app.py
```

## Contributing

To extend the system:

1. Add new bandwidth scenarios in `app.py`
2. Create custom energy analysis methods in `03_audio_energy.py`
3. Add new metrics to `metrics.py`
4. Extend the web interface in `templates/index.html`

## License

This project is part of the Adaptive Bitrate Audio Encoding System.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in terminal output
3. Consult the Adaptive Bitrate documentation
