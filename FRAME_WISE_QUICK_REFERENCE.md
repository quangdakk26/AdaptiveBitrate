# Frame-wise Adaptive Bitrate - Quick Reference

## What Changed?

### Before (Global Adaptive)
```
Input Audio → Analyze Overall Energy → Select Single Bitrate → Encode All
```
- One bitrate for entire audio (e.g., 6 kbps for all frames)

### Now (Frame-wise Adaptive)
```
Input Audio → Analyze Each Frame Energy → Assign Bitrate per Frame → Encode Chunks
```
- Different bitrate for each frame based on its energy
- Quiet frames: 1.5-3 kbps | Normal frames: 6-12 kbps | Loud frames: 12-24 kbps

## Key Commands

### Run with Default Settings (10 Mbps)
```bash
python 01_encode_decode.py
```

### Run with Specific Bandwidth
```bash
python 01_encode_decode.py 5.0    # 5 Mbps
python 01_encode_decode.py 1.0    # 1 Mbps (low bandwidth)
python 01_encode_decode.py 50.0   # 50 Mbps (high bandwidth)
```

### Analyze Frame Distribution (Test Only)
```bash
python test_framewise_adaptive.py
```

## Output Files

| File | Description |
|------|-------------|
| `reconstructed_framewise_*.wav` | Encoded audio with frame-wise adaptive bitrate |
| `bitrate_schedule_*.txt` | Frame-by-frame bitrate mapping |

## Frame Processing Parameters

```python
# In 01_encode_decode.py main() function:
encode_with_chunk_adaptive_bitrate(
    str(INPUT),
    bandwidth_mbps=bandwidth_mbps,      # Your available bandwidth
    chunk_duration=0.5,                 # Time size of each encoding chunk (seconds)
    frame_size=2048,                    # Analysis frame size (samples)
    hop_size=512                        # Frame advance (samples)
)
```

### Adjusting Chunk Duration
```python
chunk_duration=0.25   # Smaller = more CPU, finer control
chunk_duration=0.5    # Default = good balance
chunk_duration=1.0    # Larger = less CPU, smoother encoding
chunk_duration=2.0    # Very large = archive mode
```

## Bandwidth Categories

| Category | Bandwidth | Use Case |
|----------|-----------|----------|
| Low | < 3 Mbps | Satellite, rural areas |
| Medium | 3-10 Mbps | 4G LTE, DSL, home broadband |
| High | ≥ 10 Mbps | Fiber, fast WiFi, office networks |

## Energy-Based Bitrate Assignment

Each frame gets a bitrate based on **its energy level normalized to [0,1]**:

```
Normalized Energy: current_frame_energy / max_frame_energy

Thresholds:
- High Energy:   normalized_energy > 0.6 (60%)
- Medium Energy: normalized_energy 0.3-0.6 (30-60%)
- Low Energy:    normalized_energy < 0.3 (30%)
```

## Expected Output

### Console Output
Shows detailed analysis:
- Energy statistics (mean, median, std dev, max, min)
- Bitrate distribution across frames
- First 10 frames detailed breakdown
- Chunk-by-chunk encoding progress

### Bitrate Schedule File
Tab-separated values for each frame:
```
Frame | Energy | Normalized Energy | Energy Level | Bitrate
0     | 1.2e-4 | 0.1234           | low_energy   | 3.0 kbps
1     | 5.6e-4 | 0.5679           | medium_energy| 6.0 kbps
2     | 1.0e-3 | 1.0000           | high_energy  | 12.0 kbps
```

## Performance Tips

### For Faster Encoding
```python
chunk_duration = 1.0  # Larger chunks = fewer encoding iterations
```

### For Better Bandwidth Savings
```python
chunk_duration = 0.25  # Smaller chunks = more precise bitrate selection
```

### For Storage/Archive
```python
chunk_duration = 2.0   # Very large chunks for batch processing
bandwidth_mbps = 50.0  # High bandwidth to preserve quality
```

## Understanding the Output

### Bitrate Distribution Example
```
Scenario: 5 Mbps DSL connection with music
Output: Average Bitrate 6.23 kbps

Distribution:
  1.5 kbps:   45 frames ( 8.65%) - Silent passages
  3.0 kbps:  230 frames (44.23%) - Verse sections
  6.0 kbps:  189 frames (36.35%) - Chorus sections
 12.0 kbps:   56 frames (10.77%) - Climax moments
```

### Bandwidth Efficiency
- **Fixed bitrate** @ 6 kbps: Uses 6 kbps throughout
- **Frame-wise adaptive** @ avg 6.23 kbps: Uses adapted bitrate per frame
  - Quiet parts use 1.5-3 kbps (saves bandwidth)
  - Loud parts use 12 kbps (preserves quality)
- **Result**: Better perceived quality with similar avg bandwidth

## Common Tasks

### Test Frame Analysis Without Encoding
```bash
python test_framewise_adaptive.py
```
This shows frame distribution for 6 different bandwidth scenarios without creating output files.

### Encode with Custom Bandwidth
```bash
# Edit main() function or pass as argument
python 01_encode_decode.py 2.5
```

### View Bitrate Schedule
```bash
# After encoding, open the schedule file
cat data/output/bitrate_schedule_*.txt

# Or with column formatting
column -t -s '|' data/output/bitrate_schedule_*.txt
```

### Compare Different Bandwidth Results
```bash
# Run multiple times with different bandwidths
python 01_encode_decode.py 1.0
python 01_encode_decode.py 5.0
python 01_encode_decode.py 10.0

# Compare output files
ls -lh data/output/reconstructed_*.wav
ls -lh data/output/bitrate_schedule_*.txt
```

## Troubleshooting

### Problem: All frames get same bitrate
**Solution**: Check if audio has dynamic content
```bash
# Verify with test script
python test_framewise_adaptive.py
# Look for distribution across multiple bitrates
```

### Problem: Bitrate too low/high
**Adjust** in `FRAME_BITRATE_CONFIG`:
```python
FRAME_BITRATE_CONFIG = {
    'medium_bandwidth': {
        'high_energy': 16.0,   # Increase from 12.0
        'medium_energy': 8.0,  # Increase from 6.0
        'low_energy': 2.0      # Increase from 1.5
    }
}
```

### Problem: Encoding takes too long
**Try**:
```python
chunk_duration = 1.0   # Increase chunk size
frame_size = 4096      # Increase frame size (less granular)
```

### Problem: Output quality poor
**Try**:
```python
chunk_duration = 0.25  # Decrease chunk size (finer control)
frame_size = 1024      # Decrease frame size (more granular)
```

## File Organization

```
data/
├── input/
│   └── sample.wav                          # Your audio
└── output/
    ├── reconstructed_framewise_*.wav       # Encoded output
    └── bitrate_schedule_*.txt              # Frame mapping
```

## Next Steps

1. **Test**: Run `python test_framewise_adaptive.py`
2. **Encode**: Run `python 01_encode_decode.py 5.0` (with your bandwidth)
3. **Review**: Check outputs in `data/output/`
4. **Customize**: Modify `FRAME_BITRATE_CONFIG` as needed
5. **Compare**: Use `02_compare_bitrates.py` to compare quality

## API Functions

### Main Encoding Function
```python
encode_with_chunk_adaptive_bitrate(
    audio_path: str,           # Input audio file
    bandwidth_mbps: float,     # Available bandwidth
    chunk_duration: float,     # Chunk duration in seconds
    frame_size: int,           # Frame size for analysis
    hop_size: int              # Frame hop size
) → (int, list)               # (decoded_audio, chunk_stats)
```

### Analysis Function
```python
apply_frame_wise_adaptive_bitrate(
    audio_path: str,
    bandwidth_mbps: float,
    frame_size: int,
    hop_size: int
) → (tensor, model, list, dict, str, list)
  # Returns: (wav, model, bitrate_schedule, stats, bandwidth_level, energy_levels)
```

### Frame Bitrate Function
```python
get_frame_bitrate(
    frame_energy: float,       # Energy of this frame
    max_energy: float,         # Maximum energy in audio
    bandwidth_level: str       # 'high/medium/low_bandwidth'
) → (float, str)              # (bitrate_kbps, energy_level)
```

## References

- **Energy Analysis**: See `03_audio_energy.py` for energy calculation details
- **Quality Metrics**: See `metrics.py` for SNR, MSE, compression ratio
- **Full Documentation**: See `FRAME_WISE_ADAPTIVE_README.md`
- **Comparison Tool**: See `02_compare_bitrates.py` for bitrate comparison
