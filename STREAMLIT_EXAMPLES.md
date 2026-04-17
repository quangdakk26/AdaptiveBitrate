# Adaptive Audio Streaming - Streamlit Usage Examples

## Basic Usage

### 1. Starting the Application

```bash
# Simple start
streamlit run streamlit_app.py

# Start on specific port
streamlit run streamlit_app.py --server.port=8502

# Start in headless mode (for servers)
streamlit run streamlit_app.py --server.headless=true --server.enableCORS=false
```

### 2. Basic Workflow

1. **Load Audio**:
   - Select "Generate Synthetic Audio"
   - Adjust duration (5-30 seconds)
   - Click "Generate" or reload the app

2. **Select Network Profile**:
   - Choose from sidebar options
   - Each profile simulates different bandwidth conditions

3. **View Results**:
   - Tab 1: Energy analysis
   - Tab 2: Bitrate adaptation
   - Tab 3: Quality metrics
   - Tab 4: System configuration

## Advanced Examples

### Example 1: Analyze Your Own Audio

```python
# Prepare your WAV file
# 1. Place file in samples/ directory
# 2. In Streamlit app sidebar, select "Upload WAV File"
# 3. Click upload and select your file
# 4. System will automatically analyze

# Or programmatically:
from pathlib import Path
import soundfile as sf

# Ensure file is mono, 44.1 kHz
audio, sr = sf.read("my_audio.wav")
if sr != 44100:
    # Resample if needed (implement yourself)
    pass
sf.write("my_audio_processed.wav", audio, 44100)
```

### Example 2: Custom Network Profile

Modify `streamlit_app.py` to add custom profile:

```python
# In AdaptiveBitrateSimulator.simulate_network():

elif profile == "Custom Profile":
    # Define custom bandwidth pattern
    t = np.linspace(0, 1, num_frames)
    
    # Example: Exponential decay
    bandwidth = 256 * np.exp(-2 * t)
    
    # Example: Step changes
    bandwidth = np.concatenate([
        np.full(num_frames//3, 256),
        np.full(num_frames//3, 128),
        np.full(num_frames - 2*(num_frames//3), 32)
    ])
    
    # Example: Sine wave with noise
    bandwidth = 128 + 64*np.sin(np.linspace(0, 4*np.pi, num_frames)) + np.random.normal(0, 10, num_frames)
    
    return np.maximum(bandwidth, 1.5)
```

Then add to selectbox:

```python
network_profile = st.sidebar.selectbox(
    "Select Network Profile",
    [
        "Excellent (>300 kbps)",
        "Good (128 kbps)",
        "Moderate (64 kbps)",
        "Poor (32 kbps)",
        "Very Poor (16 kbps)",
        "Variable/Mobile",
        "Custom Profile"  # Add this
    ]
)
```

### Example 3: Batch Analysis

Create `batch_analysis.py`:

```python
#!/usr/bin/env python3
"""Batch process multiple audio files"""

import streamlit as st
import importlib.util
from pathlib import Path
import pandas as pd
from src.streaming_engine import AdaptiveAudioStreamingEngine

@st.cache_resource
def load_audio_energy_module():
    spec = importlib.util.spec_from_file_location(
        "audio_energy",
        Path(__file__).parent / "03_audio_energy.py"
    )
    audio_energy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audio_energy)
    return audio_energy.AudioEnergyCalculator

def batch_analyze(audio_files: list, profiles: list) -> pd.DataFrame:
    """Analyze multiple files with multiple profiles"""
    
    results = []
    
    for audio_file in audio_files:
        AudioEnergyCalculator = load_audio_energy_module()
        calc = AudioEnergyCalculator(str(audio_file))
        
        for profile in profiles:
            # Run simulation
            # (implementation here)
            results.append({
                'file': audio_file.name,
                'profile': profile,
                'avg_bitrate': 12.5,
                'quality_score': 85.0,
                'underruns': 0
            })
    
    return pd.DataFrame(results)

# Usage
if __name__ == "__main__":
    files = list(Path("samples").glob("*.wav"))
    profiles = ["Good (128 kbps)", "Moderate (64 kbps)", "Poor (32 kbps)"]
    
    results_df = batch_analyze(files, profiles)
    print(results_df.to_string())
    results_df.to_csv("batch_results.csv", index=False)
```

### Example 4: Custom Visualization

Add to `streamlit_app.py`:

```python
import plotly.graph_objects as go

def create_custom_heatmap(bitrates, energies, num_bins=20):
    """Create 2D heatmap of bitrate vs energy"""
    
    # Create bins
    energy_bins = np.linspace(0, 1, num_bins)
    bitrate_bins = np.linspace(1.5, 48, num_bins)
    
    # Create 2D histogram
    heatmap_data, _, _ = np.histogram2d(energies, bitrates, 
                                        bins=[energy_bins, bitrate_bins])
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=bitrate_bins,
        y=energy_bins,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title='Bitrate vs Energy Distribution',
        xaxis_title='Bitrate (kbps)',
        yaxis_title='Energy Level',
        height=500
    )
    
    return fig

# In main app, add to tab3:
with tab3:
    st.markdown("### Bitrate-Energy Correlation")
    fig_heatmap = create_custom_heatmap(
        simulation_result['bitrates'],
        normalized_energies
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
```

### Example 5: Export Results

Add to `streamlit_app.py`:

```python
def export_results(simulation_result, energy_info, filename="streaming_results"):
    """Export simulation results to CSV"""
    
    data = {
        'Time_s': simulation_result['frame_times'] / 1000,
        'Bandwidth_kbps': simulation_result['bandwidth'],
        'Bitrate_kbps': simulation_result['bitrates'],
        'Energy': normalized_energies,
        'Buffer_ms': simulation_result['buffers'],
        'Quality_Score': simulation_result['quality_scores']
    }
    
    df = pd.DataFrame(data)
    
    # CSV export
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Results (CSV)",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )
    
    return df

# In tab3, add:
with col4:
    export_df = export_results(simulation_result, energy_info)
    if export_df is not None:
        st.success("✅ Ready to download")
```

### Example 6: Real-time Network Simulation

Create `realtime_simulation.py`:

```python
"""Real-time streaming simulation"""

import streamlit as st
import time
import numpy as np
from datetime import datetime

def realtime_stream(audio_file, duration_seconds=30):
    """Simulate real-time streaming"""
    
    # Load audio
    frames = load_and_process_audio(audio_file)
    
    # Create placeholders for updates
    network_ph = st.empty()
    bitrate_ph = st.empty()
    buffer_ph = st.empty()
    time_ph = st.empty()
    
    start_time = time.time()
    
    for i, frame in enumerate(frames):
        elapsed = time.time() - start_time
        
        # Simulate network metrics
        bandwidth = 128 + 30 * np.sin(elapsed / 10)
        
        # Update displays
        time_ph.metric("Elapsed", f"{elapsed:.1f}s")
        network_ph.metric("Bandwidth", f"{bandwidth:.1f} kbps")
        bitrate_ph.metric("Bitrate", f"{calculate_bitrate(frame)}kbps")
        buffer_ph.metric("Buffer", f"{calculate_buffer()} ms")
        
        time.sleep(0.001)  # Simulate frame processing
        
        if elapsed > duration_seconds:
            break
```

## Performance Tuning

### For Faster Performance

```python
# In streamlit_app.py, add at top:

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_audio_energy_module():
    """Load module once"""
    ...

@st.cache_resource  # Cache resource
def create_simulator():
    """Reuse simulator instance"""
    return AdaptiveBitrateSimulator()

# Use cached components:
simulator = create_simulator()
```

### For Lower Memory Usage

```python
# Process audio in chunks
CHUNK_SIZE = 10000  # Samples per chunk

def process_chunks(audio_tensor, chunk_size=CHUNK_SIZE):
    results = []
    for i in range(0, len(audio_tensor), chunk_size):
        chunk = audio_tensor[i:i+chunk_size]
        results.append(process_single_chunk(chunk))
    return np.concatenate(results)
```

## Integration Examples

### Example 7: REST API Integration

Create `api_server.py`:

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

@app.post("/analyze")
async def analyze_audio(file: UploadFile):
    """API endpoint for audio analysis"""
    
    contents = await file.read()
    
    # Process audio
    # Return results as JSON
    
    return {"status": "success", "metrics": {...}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Example 8: Multi-Session Support

```python
# In streamlit_app.py, add session management:

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'results_history' not in st.session_state:
    st.session_state.results_history = []

# Store results
st.session_state.results_history.append({
    'timestamp': datetime.now(),
    'profile': network_profile,
    'metrics': simulation_result
})

# Show history
if st.checkbox("Show Results History"):
    st.dataframe(
        pd.DataFrame([
            {
                'Time': r['timestamp'],
                'Profile': r['profile'],
                'Avg Bitrate': r['metrics']['avg_bitrate']
            }
            for r in st.session_state.results_history
        ])
    )
```

## Debugging Tips

### 1. View Performance Metrics

```python
import streamlit as st

@st.cache_resource
def get_performance_metrics():
    import psutil
    process = psutil.Process()
    return {
        'memory': process.memory_info().rss / 1024 / 1024,  # MB
        'cpu': process.cpu_percent(interval=1)
    }

# In app:
metrics = get_performance_metrics()
st.write(f"Memory: {metrics['memory']:.1f} MB")
st.write(f"CPU: {metrics['cpu']:.1f}%")
```

### 2. Add Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# In functions:
logger.debug(f"Processing frame {i}")
logger.info(f"Bitrate changed to {bitrate} kbps")
```

### 3. Add Error Handling

```python
try:
    simulation_result = simulator.simulate_streaming(...)
except Exception as e:
    st.error(f"❌ Simulation failed: {str(e)}")
    logger.error(f"Simulation error: {e}", exc_info=True)
```

## Best Practices

1. **Always cache expensive operations**:
   ```python
   @st.cache_data
   def expensive_computation(param):
       # Only runs once
   ```

2. **Use sessions to maintain state**:
   ```python
   if 'counter' not in st.session_state:
       st.session_state.counter = 0
   ```

3. **Provide user feedback**:
   ```python
   with st.spinner("Processing..."):
       result = long_operation()
   st.success("✅ Done!")
   ```

4. **Handle errors gracefully**:
   ```python
   st.try_widget(lambda: risky_operation())
   ```

5. **Document your extensions**:
   ```python
   def custom_function():
       """
       Brief description.
       
       Parameters:
           param: description
       
       Returns:
           description
       """
   ```

## Deployment

### Local Server
```bash
streamlit run streamlit_app.py
```

### Production (Gunicorn + Systemd)
See INSTALLATION_SETUP.md

### Docker
```bash
docker run -p 8501:8501 adaptive-streaming:latest
```

### Cloud (Streamlit Share)
Push to GitHub → Deploy on share.streamlit.io

---

For more examples and use cases, refer to the main documentation and individual module files.
