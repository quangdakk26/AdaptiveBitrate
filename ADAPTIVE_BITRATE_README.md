# Adaptive Bitrate Audio Encoding System

## Overview

This system automatically selects the optimal audio bitrate based on:
- **Audio Energy Analysis**: Content complexity and average energy levels
- **Available Bandwidth**: Network conditions and connection speed

The system intelligently adapts to maximize audio quality while preventing transmission issues (lag, stuttering, data loss) in bandwidth-constrained environments.

## How It Works

### 1. Energy-Based Classification

The system analyzes the audio file's energy statistics using `03_audio_energy.py`:

- **High Energy**: Mean energy > 60% of max energy
  - Indicates rich, complex audio content (music, speech with variations)
  - Requires higher bitrates to preserve detail
  
- **Medium Energy**: Mean energy between 30-60% of max energy
  - Balanced content with moderate complexity
  - Uses standard bitrates
  
- **Low Energy**: Mean energy < 30% of max energy
  - Sparse or quiet content (silence, minimal sounds)
  - Can use lower bitrates without quality loss

### 2. Bandwidth Classification

The system categorizes available bandwidth:

- **High Bandwidth** (≥ 10 Mbps): Fiber, Fast WiFi
  - Bitrates: 6-24 kbps
  
- **Medium Bandwidth** (3-10 Mbps): DSL, 4G LTE
  - Bitrates: 3-12 kbps
  
- **Low Bandwidth** (< 3 Mbps): Slow Mobile, Satellite
  - Bitrates: 1.5-6 kbps

### 3. Bitrate Selection Matrix

| Bandwidth | High Energy | Medium Energy | Low Energy |
|-----------|------------|---------------|------------|
| High      | 24 kbps    | 12 kbps       | 6 kbps     |
| Medium    | 12 kbps    | 6 kbps        | 3 kbps     |
| Low       | 6 kbps     | 3 kbps        | 1.5 kbps   |

## Usage

### Command Line Usage

**Default (10 Mbps bandwidth):**
```bash
python 01_encode_decode.py
```

**With specific bandwidth:**
```bash
python 01_encode_decode.py 5.0    # 5 Mbps (Medium bandwidth)
python 01_encode_decode.py 1.0    # 1 Mbps (Low bandwidth)
python 01_encode_decode.py 50.0   # 50 Mbps (Very high bandwidth)
```

### Programmatic Usage

```python
from 01_encode_decode import main, calculate_adaptive_bitrate

# Get adaptive bitrate information
bitrate, energy_level, bandwidth_level = calculate_adaptive_bitrate(
    "data/input/sample.wav", 
    bandwidth_mbps=5.0
)

# Encode with adaptive settings
main(bandwidth_mbps=5.0)
```

## Output

When you run the system, you'll see diagnostic output:

```
--- Adaptive Bitrate Selection ---
Audio Energy Statistics:
  Mean Energy: 0.123456
  Max Energy:  0.654321
  Std Dev:     0.087654
  Energy Level: medium_energy

Available Bandwidth: 5 Mbps
Bandwidth Level: medium_bandwidth

Selected Bitrate: 6 kbps
-----------------------------------

✓ Encoded and decoded successfully!
✓ Output saved to: data/output/reconstructed_medium_energy_medium_bandwidth_6kbps.wav
```

## Files

- **01_encode_decode.py**: Main adaptive encoding system
- **02_compare_bitrates.py**: Comparison script for different bitrates
- **03_audio_energy.py**: Audio energy analysis module
- **metrics.py**: Quality metrics (SNR, MSE, compression ratio)
- **test_adaptive_bitrate.py**: Test scenarios demonstration
- **data/input/**: Input audio files
- **data/output/**: Encoded output files

## Scenarios Example

### Scenario 1: High-Quality LTE Streaming (5 Mbps)
- Input: Music with rich instrumentation (high energy)
- Bandwidth: 5 Mbps
- **Selected Bitrate: 12 kbps**
- Result: High-quality audio, smooth streaming

### Scenario 2: Satellite Communication (1 Mbps)
- Input: Speech content (low energy)
- Bandwidth: 1 Mbps
- **Selected Bitrate: 1.5 kbps**
- Result: Minimal bandwidth usage, acceptable speech quality

### Scenario 3: Fiber Connection (50 Mbps)
- Input: Complex audio (high energy)
- Bandwidth: 50 Mbps
- **Selected Bitrate: 24 kbps**
- Result: Maximum quality, no bandwidth constraints

## Customization

You can modify the `BITRATE_CONFIG` dictionary in `01_encode_decode.py` to adjust thresholds:

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

Adjust energy thresholds in the `calculate_adaptive_bitrate()` function:

```python
if mean_energy > max_energy * 0.6:  # Change 0.6 to adjust threshold
    energy_level = 'high_energy'
```

## Energy Metrics Explained

From `03_audio_energy.py`:

- **Total Energy**: Sum of all squared samples
- **RMS Energy**: Root mean square of audio signal
- **Frame Energy**: Energy calculated for each audio frame
- **Mean Energy**: Average frame-wise energy
- **Std Dev**: Standard deviation for energy variation
- **Median Energy**: Middle value of energy distribution

## Requirements

- Python 3.8+
- torch
- torchaudio
- encodec
- soundfile
- numpy
- pandas

## Installation

```bash
pip install torch torchaudio encodec soundfile numpy pandas
```

## Future Enhancements

- Real-time bandwidth detection
- Dynamic bitrate adjustment during playback
- Model-specific sample rate selection
- Advanced energy classification using ML
- Network quality of service (QoS) integration
