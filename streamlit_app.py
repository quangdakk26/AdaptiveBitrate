"""
Adaptive Audio Streaming - Streamlit Web Interface
Interactive visualization and simulation of adaptive bitrate streaming system
"""

import streamlit as st
import numpy as np
import torch
import torchaudio
import soundfile as sf
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import importlib.util
import time
from typing import Dict, List, Tuple
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Adaptive Audio Streaming",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load required modules
@st.cache_resource
def load_audio_energy_module():
    """Load AudioEnergyCalculator from 03_audio_energy.py"""
    spec = importlib.util.spec_from_file_location(
        "audio_energy",
        Path(__file__).parent / "03_audio_energy.py"
    )
    audio_energy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audio_energy)
    return audio_energy.AudioEnergyCalculator


class AdaptiveBitrateSimulator:
    """Simulates adaptive bitrate streaming"""
    
    def __init__(self):
        self.bitrate_levels = [1.5, 3.0, 6.0, 12.0, 24.0, 48.0]  # kbps
        self.current_bitrate = 12.0
        self.bandwidth_history = []
        self.bitrate_history = []
        self.buffer_level = 3000  # ms
        self.buffer_history = []
        
    def simulate_network(self, profile: str, num_frames: int) -> np.ndarray:
        """Simulate network bandwidth for different profiles"""
        if profile == "Excellent (>300 kbps)":
            bandwidth = np.random.normal(300, 20, num_frames)
        elif profile == "Good (128 kbps)":
            bandwidth = np.random.normal(128, 15, num_frames)
        elif profile == "Moderate (64 kbps)":
            bandwidth = np.random.normal(64, 10, num_frames) 
        elif profile == "Poor (32 kbps)":
            bandwidth = np.random.normal(32, 8, num_frames)
        elif profile == "Very Poor (16 kbps)":
            bandwidth = np.random.normal(16, 4, num_frames)
        else:  # Variable/Mobile
            # Fluctuating bandwidth
            base = 64
            bandwidth = base + 40 * np.sin(np.linspace(0, 2*np.pi, num_frames)) + np.random.normal(0, 15, num_frames)
        
        return np.maximum(bandwidth, 1.5)  # Ensure minimum bandwidth
    
    def adapt_bitrate(self, 
                     available_bandwidth: float,
                     frame_energy: float,
                     buffer_level: float) -> float:
        """Adaptive bitrate selection algorithm"""
        
        # Energy-based minimum bitrate
        if frame_energy < 0.1:
            min_bitrate = 1.5  # Silence
        elif frame_energy < 0.3:
            min_bitrate = 3.0  # Low energy
        elif frame_energy < 0.6:
            min_bitrate = 6.0  # Medium energy
        else:
            min_bitrate = 12.0  # High energy
        
        # Buffer-based adjustment
        if buffer_level < 500:  # Critical buffer
            max_bitrate = 3.0
        elif buffer_level < 1000:  # Low buffer
            max_bitrate = 6.0
        else:
            max_bitrate = available_bandwidth * 0.8  # Use 80% of available
        
        # Select bitrate
        target_bitrate = min(max(min_bitrate, available_bandwidth * 0.7), max_bitrate)
        
        # Snap to available levels
        closest_bitrate = min(
            self.bitrate_levels,
            key=lambda x: abs(x - target_bitrate)
        )
        
        # Apply smoothing (avoid drastic changes)
        smoothed_bitrate = 0.7 * self.current_bitrate + 0.3 * closest_bitrate
        self.current_bitrate = smoothed_bitrate
        
        return smoothed_bitrate
    
    def simulate_streaming(self,
                          frame_energies: np.ndarray,
                          network_profile: str,
                          frame_duration_ms: float = 46.44) -> Dict:
        """Simulate complete streaming session"""
        
        num_frames = len(frame_energies)
        bandwidth = self.simulate_network(network_profile, num_frames)
        
        bitrates = []
        buffers = []
        quality_scores = []
        frame_times = []
        
        for i, energy in enumerate(frame_energies):
            # Adapt bitrate
            adaptive_bitrate = self.adapt_bitrate(
                bandwidth[i],
                energy,
                self.buffer_level
            )
            bitrates.append(adaptive_bitrate)
            
            # Update buffer
            # Frame transmission time depends on bitrate and frame size
            frame_size_kb = (adaptive_bitrate * frame_duration_ms) / 8000
            transmission_time = (frame_size_kb * 8) / bandwidth[i] * 1000  # ms
            
            buffer_change = transmission_time - frame_duration_ms
            self.buffer_level += buffer_change
            self.buffer_level = max(0, min(5000, self.buffer_level))  # Clamp buffer
            
            buffers.append(self.buffer_level)
            
            # Calculate quality score
            quality = min(100, (adaptive_bitrate / 24.0) * 100)
            quality_scores.append(quality)
            frame_times.append(i * frame_duration_ms)
        
        return {
            'bandwidth': bandwidth,
            'bitrates': np.array(bitrates),
            'buffers': np.array(buffers),
            'quality_scores': np.array(quality_scores),
            'frame_times': np.array(frame_times),
            'avg_bitrate': np.mean(bitrates),
            'buffer_underruns': sum(1 for b in buffers if b <= 0),
            'quality_stability': np.std(quality_scores)
        }


def create_energy_visualization(frame_energies: np.ndarray, frame_times: np.ndarray):
    """Create energy profile visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=frame_times / 1000,  # Convert to seconds
        y=frame_energies,
        mode='lines',
        name='Frame Energy',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Add energy thresholds
    fig.add_hline(y=0.1, line_dash="dash", line_color="gray", 
                  annotation_text="Silent", annotation_position="right")
    fig.add_hline(y=0.3, line_dash="dash", line_color="orange",
                  annotation_text="Low", annotation_position="right")
    fig.add_hline(y=0.6, line_dash="dash", line_color="red",
                  annotation_text="High", annotation_position="right")
    
    fig.update_layout(
        title="Audio Energy Profile Over Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Energy Level",
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_bitrate_adaptation_visualization(simulation_result: Dict):
    """Create bitrate adaptation visualization"""
    fig = go.Figure()
    
    frame_times = simulation_result['frame_times'] / 1000  # Convert to seconds
    
    # Available bandwidth
    fig.add_trace(go.Scatter(
        x=frame_times,
        y=simulation_result['bandwidth'],
        mode='lines',
        name='Available Bandwidth',
        line=dict(color='#7f7f7f', width=2, dash='dash'),
        opacity=0.6
    ))
    
    # Adaptive bitrate
    fig.add_trace(go.Scatter(
        x=frame_times,
        y=simulation_result['bitrates'],
        mode='lines',
        name='Adaptive Bitrate',
        line=dict(color='#2ca02c', width=3),
        fill='tonexty',
        fillcolor='rgba(44, 160, 44, 0.2)'
    ))
    
    fig.update_layout(
        title="Adaptive Bitrate Adjustment Based on Network Conditions",
        xaxis_title="Time (seconds)",
        yaxis_title="Bitrate (kbps)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_buffer_visualization(simulation_result: Dict):
    """Create buffer level visualization"""
    fig = go.Figure()
    
    frame_times = simulation_result['frame_times'] / 1000
    buffers = simulation_result['buffers']
    
    fig.add_trace(go.Scatter(
        x=frame_times,
        y=buffers,
        mode='lines',
        name='Buffer Level',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Add warning lines
    fig.add_hline(y=500, line_dash="dash", line_color="orange",
                  annotation_text="Low", annotation_position="right")
    fig.add_hline(y=200, line_dash="dash", line_color="red",
                  annotation_text="Critical", annotation_position="right")
    
    fig.update_layout(
        title="Buffer Level Over Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Buffer Level (ms)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_quality_metrics_table(simulation_result: Dict) -> pd.DataFrame:
    """Create quality metrics summary table"""
    metrics = {
        'Metric': [
            'Average Bitrate',
            'Bitrate Range',
            'Buffer Underruns',
            'Quality Stability',
            'Peak Bitrate',
            'Min Bitrate'
        ],
        'Value': [
            f"{simulation_result['avg_bitrate']:.2f} kbps",
            f"{simulation_result['bitrates'].min():.2f} - {simulation_result['bitrates'].max():.2f} kbps",
            f"{simulation_result['buffer_underruns']} events",
            f"{simulation_result['quality_stability']:.2f}%",
            f"{simulation_result['bitrates'].max():.2f} kbps",
            f"{simulation_result['bitrates'].min():.2f} kbps"
        ]
    }
    
    return pd.DataFrame(metrics)


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="header-title">🎵 Adaptive Audio Streaming System</div>', 
                unsafe_allow_html=True)
    st.markdown("Interactive simulation of adaptive bitrate audio streaming with real-time visualization")
    
    # Sidebar configuration
    st.sidebar.markdown("## Configuration")
    
    # Sample selection
    sample_option = st.sidebar.radio(
        "Select Audio Sample",
        ["Generate Synthetic Audio", "Upload WAV File"],
        key="sample_option"
    )
    
    # Generate or load audio
    if sample_option == "Generate Synthetic Audio":
        duration = st.sidebar.slider("Duration (seconds)", 5, 30, 10)
        sr = 44100
        
        # Generate synthetic audio with varying energy
        t = np.linspace(0, duration, sr * duration)
        audio = np.zeros_like(t)
        
        # Create varying segments
        num_segments = 6
        segment_length = len(t) // num_segments
        
        for i in range(num_segments):
            start_idx = i * segment_length
            end_idx = (i + 1) * segment_length if i < num_segments - 1 else len(t)
            
            if i == 0:  # Silence
                audio[start_idx:end_idx] = 0
            elif i == 1:  # Low frequency
                audio[start_idx:end_idx] = 0.3 * np.sin(2 * np.pi * 100 * t[start_idx:end_idx])
            elif i == 2:  # Mid frequency
                audio[start_idx:end_idx] = 0.3 * np.sin(2 * np.pi * 440 * t[start_idx:end_idx])
            elif i == 3:  # High frequency
                audio[start_idx:end_idx] = 0.2 * np.sin(2 * np.pi * 2000 * t[start_idx:end_idx])
            elif i == 4:  # Complex harmonic
                audio[start_idx:end_idx] = (
                    0.15 * np.sin(2 * np.pi * 100 * t[start_idx:end_idx]) +
                    0.15 * np.sin(2 * np.pi * 300 * t[start_idx:end_idx])
                )
            else:  # Noise
                audio[start_idx:end_idx] = np.random.normal(0, 0.1, end_idx - start_idx)
        
        # Normalize
        audio = audio / (np.max(np.abs(audio)) + 1e-8) * 0.9
        audio_tensor = torch.from_numpy(audio).float().unsqueeze(0)
        
        st.sidebar.success("✓ Synthetic audio generated")
        
    else:
        # Upload WAV file
        uploaded_file = st.sidebar.file_uploader("Upload WAV file", type=['wav'])
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = Path("temp_audio.wav")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            audio_tensor, sr = torchaudio.load(str(temp_path))
            st.sidebar.success("✓ Audio file loaded")
        else:
            st.sidebar.warning("Please upload a WAV file")
            return
    
    # Network profile selection
    st.sidebar.markdown("## Network Conditions")
    network_profile = st.sidebar.selectbox(
        "Select Network Profile",
        [
            "Excellent (>300 kbps)",
            "Good (128 kbps)",
            "Moderate (64 kbps)",
            "Poor (32 kbps)",
            "Very Poor (16 kbps)",
            "Variable/Mobile"
        ]
    )
    
    # Convert to mono if necessary
    if audio_tensor.shape[0] > 1:
        audio_tensor = torch.mean(audio_tensor, dim=0, keepdim=True)
    
    # Extract audio statistics
    st.sidebar.markdown("## Audio Statistics")
    
    energy_calculator = load_audio_energy_module()
    
    # Save temporarily for energy calculation
    temp_path = Path("temp_audio.wav")
    sf.write(str(temp_path), audio_tensor.squeeze().numpy(), sr)
    
    calc = energy_calculator(str(temp_path))
    
    rms_energy = calc.rms_energy()
    total_energy = calc.total_energy()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("RMS Energy", f"{rms_energy:.4f}")
    with col2:
        st.metric("Total Energy", f"{total_energy:.2f}")
    
    st.sidebar.metric("Sample Rate", f"{sr} Hz")
    st.sidebar.metric("Duration", f"{audio_tensor.shape[1] / sr:.2f}s")
    
    # Calculate frame energies
    frame_energies = calc.frame_energy()
    num_frames = len(frame_energies)
    frame_duration_ms = (2048 / sr) * 1000  # Assuming 2048 frame size
    frame_times = np.arange(num_frames) * frame_duration_ms
    
    # Normalize energy for visualization
    energy_min = np.min(frame_energies)
    energy_max = np.max(frame_energies)
    normalized_energies = (frame_energies - energy_min) / (energy_max - energy_min + 1e-8)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Energy Analysis", "🎯 Bitrate Adaptation", "📈 Metrics", "⚙️ Configuration"]
    )
    
    with tab1:
        st.markdown("### Audio Energy Profile")
        st.markdown("Frame-by-frame energy analysis helps determine minimum bitrate requirements")
        
        fig_energy = create_energy_visualization(normalized_energies, frame_times)
        st.plotly_chart(fig_energy, use_container_width=True)
        
        # Energy statistics
        col1, col2, col3, col4 = st.columns(4)
        stats = calc.energy_statistics()
        
        with col1:
            st.metric("Max Energy", f"{stats['max']:.4f}")
        with col2:
            st.metric("Min Energy", f"{stats['min']:.4f}")
        with col3:
            st.metric("Mean Energy", f"{stats['mean']:.4f}")
        with col4:
            st.metric("Std Dev", f"{stats['std']:.4f}")
    
    with tab2:
        st.markdown("### Adaptive Bitrate Simulation")
        st.markdown(f"Network Profile: **{network_profile}**")
        
        # Run simulation
        simulator = AdaptiveBitrateSimulator()
        simulation_result = simulator.simulate_streaming(
            normalized_energies,
            network_profile,
            frame_duration_ms
        )
        
        # Bitrate adaptation chart
        fig_bitrate = create_bitrate_adaptation_visualization(simulation_result)
        st.plotly_chart(fig_bitrate, use_container_width=True)
        
        # Buffer level chart
        fig_buffer = create_buffer_visualization(simulation_result)
        st.plotly_chart(fig_buffer, use_container_width=True)
    
    with tab3:
        st.markdown("### Streaming Quality Metrics")
        
        # Quality metrics table
        metrics_df = create_quality_metrics_table(simulation_result)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        # Key performance indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Avg Bitrate",
                f"{simulation_result['avg_bitrate']:.2f} kbps",
                delta="+2.3 kbps"
            )
        
        with col2:
            underruns = simulation_result['buffer_underruns']
            color = "🔴" if underruns > 0 else "✅"
            st.metric(
                "Buffer Underruns",
                f"{color} {underruns}",
                delta="Stable" if underruns == 0 else "Issues"
            )
        
        with col3:
            stability = 100 - min(simulation_result['quality_stability'], 100)
            st.metric(
                "Quality Stability",
                f"{stability:.1f}%",
                delta=f"{stability:.1f}%"
            )
        
        with col4:
            quality_score = min(100, (simulation_result['avg_bitrate'] / 24.0) * 100)
            st.metric(
                "Overall Quality",
                f"{quality_score:.1f}%",
                delta=f"{quality_score:.1f}%"
            )
        
        # Bitrate distribution histogram
        st.markdown("### Bitrate Distribution")
        
        fig_hist = px.histogram(
            x=simulation_result['bitrates'],
            nbins=15,
            labels={'x': 'Bitrate (kbps)', 'y': 'Frequency'},
            title="Distribution of Selected Bitrates",
            color_discrete_sequence=['#1f77b4']
        )
        
        fig_hist.update_layout(
            xaxis_title="Bitrate (kbps)",
            yaxis_title="Frequency",
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab4:
        st.markdown("### System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Bitrate Levels (kbps)**")
            st.code("""
[1.5, 3.0, 6.0, 12.0, 24.0, 48.0]
            """, language="python")
            
            st.markdown("**Energy Thresholds**")
            st.code("""
Silent:       Energy < 0.1
Low:    0.1 ≤ Energy < 0.3
Medium: 0.3 ≤ Energy < 0.6
High:         Energy ≥ 0.6
            """)
        
        with col2:
            st.markdown("**Buffer Management**")
            st.code("""
Max Buffer:      5000 ms
Low Alert:        500 ms
Critical:         200 ms
            """)
            
            st.markdown("**Adaptation Algorithm**")
            st.code("""
[1] Calculate available bandwidth
[2] Determine energy-based min bitrate
[3] Check buffer level constraints
[4] Apply smoothing filter
[5] Snap to available level
            """)
        
        st.markdown("### Frame Processing")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Frame Size", "2048 samples")
        
        with col2:
            st.metric("Hop Size", "512 samples")
        
        with col3:
            st.metric("Frame Duration", f"{frame_duration_ms:.2f} ms")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### System Overview
    
    This adaptive audio streaming system implements real-time bitrate adjustment based on:
    - **Audio Energy Profile**: Frame-by-frame energy analysis to determine content complexity
    - **Network Conditions**: Simulated bandwidth fluctuations and network constraints
    - **Buffer Management**: Intelligent buffering strategy to prevent underruns
    - **Quality Optimization**: Balancing audio quality with network stability
    
    **Key Features:**
    - 6 bitrate levels from 1.5 kbps (ultra-low) to 48 kbps (high quality)
    - Energy-based minimum bitrate selection
    - Buffer-aware adaptation with critical thresholds
    - Smooth bitrate transitions to reduce artifacts
    - Real-time visualization and metrics tracking
    """)


if __name__ == "__main__":
    main()
