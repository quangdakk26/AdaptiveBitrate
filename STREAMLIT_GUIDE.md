# Adaptive Audio Streaming - Streamlit Web Interface

## Quick Start

### 1. Install Dependencies

```bash
pip install streamlit plotly pandas numpy torch torchaudio soundfile
```

### 2. Run the Streamlit Application

```bash
streamlit run streamlit_app.py
```

The web interface will open at `http://localhost:8501`

### 3. Features

#### 📊 Energy Analysis Tab
- Visualize frame-by-frame audio energy profile
- See energy thresholds for different audio characteristics
- View energy statistics (min, max, mean, std dev)

#### 🎯 Bitrate Adaptation Tab
- Simulate adaptive bitrate selection for different network profiles
- View real-time bitrate adjustment based on bandwidth and energy
- Monitor buffer level changes over time
- Select from 5 network scenarios:
  - **Excellent**: ~300 kbps (stable high-speed)
  - **Good**: ~128 kbps (stable moderate speed)
  - **Moderate**: ~64 kbps (some fluctuations)
  - **Poor**: ~32 kbps (frequent drops)
  - **Very Poor**: ~16 kbps (severe limitations)
  - **Mobile/Variable**: ~50-80 kbps (realistic mobile conditions)

#### 📈 Metrics Tab
- Quality metrics summary table
- Key performance indicators (KPIs)
- Bitrate distribution histogram
- Overall quality score calculation

#### ⚙️ Configuration Tab
- View system configuration parameters
- See bitrate levels and energy thresholds
- Review frame processing settings
- Understand adaptation algorithm

## How to Use

1. **Load Audio**:
   - Generate synthetic audio (5-30 seconds) for testing
   - Or upload your own WAV file

2. **Select Network Conditions**:
   - Choose a network profile from the sidebar
   - System will simulate realistic bandwidth patterns

3. **Analyze Results**:
   - Review energy profile in the Energy Analysis tab
   - Check bitrate adaptation in the Bitrate Adaptation tab
   - Compare metrics across different network conditions

## System Architecture

### Audio Processing
```
WAV File
   ↓
Load & Resample to 44.1 kHz
   ↓
Split into 2048-sample frames
   ↓
Calculate frame energy
```

### Bitrate Adaptation Algorithm
```
For each frame:
  1. Get available bandwidth from network simulator
  2. Calculate frame energy level
  3. Determine minimum bitrate based on energy:
     - Silent (E < 0.1): 1.5 kbps
     - Low (0.1 ≤ E < 0.3): 3.0 kbps
     - Medium (0.3 ≤ E < 0.6): 6.0 kbps
     - High (E ≥ 0.6): 12.0 kbps
  4. Check buffer level constraints:
     - Critical (< 200ms): max 3.0 kbps
     - Low (500-1000ms): max 6.0 kbps
     - Healthy: max 80% of available bandwidth
  5. Apply exponential smoothing to avoid artifacts
  6. Snap to nearest available bitrate level
```

### Buffer Management
- Maximum: 5000 ms
- Low threshold: 500 ms (triggers quality reduction)
- Critical threshold: 200 ms (emergency reduction)

## Bitrate Levels

| Level | Bitrate | Usage |
|-------|---------|-------|
| Ultra-Low | 1.5 kbps | Silence, extreme low bandwidth |
| Very Low | 3.0 kbps | Low energy, poor network |
| Low | 6.0 kbps | Medium-low energy, moderate network |
| Medium | 12.0 kbps | Medium energy, good network |
| High | 24.0 kbps | High energy, excellent network |
| Ultra-High | 48.0 kbps | Very high energy, optimal conditions |

## Network Profiles

### Excellent Connection
- Stable 300 kbps bandwidth
- Zero packet loss
- Suitable for high-quality streaming

### Good Connection
- Stable 128 kbps bandwidth
- Minimal packet loss
- Smooth streaming with good quality

### Moderate Connection
- Fluctuates around 64 kbps
- Occasional packet loss
- Requires adaptive adjustment

### Poor Connection
- Drops to 32 kbps
- Higher packet loss rates
- Frequent bitrate adjustments

### Very Poor Connection
- Limited to 16 kbps
- Significant packet loss
- Minimum quality maintenance

### Mobile/Variable Connection
- Realistic mobile network patterns
- Signal strength variations (50-80 kbps)
- Frequent handovers and congestion

## Interpretation Guide

### Quality Score
- **90-100%**: Excellent streaming experience
- **70-89%**: Good quality with minor adjustments
- **50-69%**: Acceptable quality with noticeable changes
- **<50%**: Poor quality, frequent buffering

### Buffer Underruns
- **0**: Perfect stability
- **1-3**: Occasional brief disruptions
- **>3**: Significant streaming issues

### Quality Stability
- **>90%**: Very stable, consistent bitrate
- **70-90%**: Stable with minor adjustments
- **50-70%**: Moderate fluctuations
- **<50%**: Frequent significant changes

## Troubleshooting

### Application Won't Start
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with specific Python version
python3 -m streamlit run streamlit_app.py
```

### Audio File Issues
- Ensure WAV file is in valid format
- Check sample rate is 44.1 kHz or will be resampled
- Keep file size reasonable (<100 MB)

### Performance Issues
- Use shorter audio files for testing (5-10 seconds)
- Check available system memory
- Consider disabling verbose logging

## API Reference

### AdaptiveBitrateSimulator

```python
simulator = AdaptiveBitrateSimulator()

# Simulate network bandwidth
bandwidth = simulator.simulate_network(profile="Moderate (64 kbps)", num_frames=1000)

# Adapt bitrate for a frame
bitrate = simulator.adapt_bitrate(
    available_bandwidth=64.0,
    frame_energy=0.35,
    buffer_level=2000.0
)

# Run complete simulation
results = simulator.simulate_streaming(
    frame_energies=energy_values,
    network_profile="Good (128 kbps)",
    frame_duration_ms=46.44
)
```

## Advanced Usage

### Custom Network Profile
Modify `simulate_network()` method to create custom bandwidth patterns:

```python
# Create step-down bandwidth pattern
bandwidth = np.linspace(256, 16, num_frames)  # 256 kbps → 16 kbps
```

### Adjust Adaptation Parameters
Modify thresholds in `AdaptiveBitrateSimulator`:

```python
# Energy thresholds
min_bitrate_for_energy = {
    'silence': 1.5,
    'low': 3.0,
    'medium': 6.0,
    'high': 12.0
}

# Buffer thresholds
critical_buffer = 200  # ms
low_buffer = 500  # ms
```

## Performance Metrics

The system tracks:
- **Average Bitrate**: Mean bitrate over session
- **Buffer Underruns**: Number of buffer starvation events
- **Quality Stability**: Standard deviation of quality scores
- **Peak/Min Bitrate**: Extremes during streaming
- **Adaptation Frequency**: How often bitrate changes

## Example Scenarios

### Scenario 1: Stable High-Speed Network
- Profile: Excellent
- Expected: High bitrate maintained, zero underruns
- Quality Score: 95-100%

### Scenario 2: Mobile Network Dropout
- Profile: Mobile/Variable
- Expected: Frequent bitrate adjustments, occasional underruns
- Quality Score: 70-80%

### Scenario 3: Congested Network
- Profile: Poor to Very Poor
- Expected: Low bitrate maintained, possible underruns
- Quality Score: 50-70%

## Contributing

To extend the system:

1. Add new network profiles in `AdaptiveBitrateSimulator.simulate_network()`
2. Modify bitrate adaptation algorithm in `adapt_bitrate()`
3. Add new visualizations with Plotly
4. Implement additional audio analysis features

## License

Adaptive Bitrate Streaming System - Educational Demo

## References

- DASH (Dynamic Adaptive Streaming over HTTP)
- HLS (HTTP Live Streaming)
- MPEG-DASH standard
- Adaptive bitrate algorithms research
