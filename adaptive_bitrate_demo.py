"""
Adaptive Audio Bitrate Streaming System - Advanced Demonstration
Comprehensive web application for analyzing audio features and simulating adaptive bitrate streaming
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import pandas as pd
from audio_analyzer import AudioFeatureAnalyzer
from network_simulator import NetworkSimulator
from adaptive_bitrate import AdaptiveBitrateSelector
import warnings
warnings.filterwarnings('ignore')
import soundfile as sf
import scipy.signal as signal
from scipy.io import wavfile


# Page configuration
st.set_page_config(
    page_title="Adaptive Audio Bitrate System",
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
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .description-text {
        color: #666;
        font-size: 16px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_analyzer():
    """Initialize audio analyzer"""
    return AudioFeatureAnalyzer(sr=44100)


def create_audio_features_chart(features_list, chunk_times, feature_name):
    """Create chart for audio feature"""
    values = [f[feature_name] for f in features_list]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chunk_times,
        y=values,
        mode='lines+markers',
        name=feature_name,
        line=dict(width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title=f"{feature_name.replace('_', ' ').title()} Over Time",
        xaxis_title="Time (seconds)",
        yaxis_title=feature_name.replace('_', ' ').title(),
        height=300,
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig


def create_complexity_chart(features_list, chunk_times):
    """Create complexity score chart"""
    complexity_scores = [f['complexity'] for f in features_list]
    content_types = [f['content_type'] for f in features_list]
    
    # Map colors to content types
    color_map = {'speech': '#FF6B6B', 'music': '#4ECDC4', 'mixed': '#FFE66D'}
    colors = [color_map[ct] for ct in content_types]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chunk_times,
        y=complexity_scores,
        mode='markers+lines',
        name='Complexity',
        line=dict(color='#1f77b4', width=2),
        marker=dict(
            size=8,
            color=colors,
            line=dict(width=2, color='white')
        ),
        text=[f"Type: {ct}<br>Complexity: {cs:.2f}" for ct, cs in zip(content_types, complexity_scores)],
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    fig.update_layout(
        title="Audio Complexity & Content Type",
        xaxis_title="Time (seconds)",
        yaxis_title="Complexity Score (0-1)",
        height=350,
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig


def create_bandwidth_chart(bandwidth_array, chunk_times, title="Network Bandwidth Over Time"):
    """Create bandwidth visualization"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chunk_times,
        y=bandwidth_array,
        mode='lines',
        name='Available Bandwidth',
        line=dict(color='#FF6B6B', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time (seconds)",
        yaxis_title="Bandwidth (kbps)",
        height=300,
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig


def create_bitrate_comparison_chart(actual_bitrate, bandwidth_array, chunk_times):
    """Create bitrate vs bandwidth comparison"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=chunk_times,
        y=bandwidth_array,
        mode='lines',
        name='Available Bandwidth',
        line=dict(color='#FF6B6B', width=2, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=chunk_times,
        y=actual_bitrate,
        mode='lines+markers',
        name='Selected Bitrate',
        line=dict(color='#2ECC71', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Adaptive Bitrate vs Available Bandwidth",
        xaxis_title="Time (seconds)",
        yaxis_title="Bitrate (kbps)",
        height=350,
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig


def create_content_distribution_chart(features_list):
    """Create content type distribution chart"""
    content_types = [f['content_type'] for f in features_list]
    type_counts = {
        'speech': content_types.count('speech'),
        'music': content_types.count('music'),
        'mixed': content_types.count('mixed')
    }
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            marker=dict(colors=['#FF6B6B', '#4ECDC4', '#FFE66D'])
        )
    ])
    
    fig.update_layout(
        title="Content Type Distribution",
        height=400
    )
    
    return fig


def simulate_audio_quality(audio, sr, bitrate_kbps):
    """
    Simulate audio quality at different bitrate by applying low-pass filtering.
    Higher bitrate = higher cutoff frequency = better quality.
    
    Bitrate to approximate cutoff frequency mapping:
    5 kbps -> 800 Hz (extremely low, comfort noise only)
    8 kbps -> 2000 Hz (very low, phone quality)
    16 kbps -> 3500 Hz (low, speech optimized)
    32 kbps -> 5500 Hz (moderate, speech good)
    64 kbps -> 8000 Hz (good, full spectrum)
    96 kbps -> 11000 Hz (very good)
    128 kbps -> 14000 Hz (excellent, full range)
    192 kbps -> 18000 Hz (premium)
    256 kbps -> 22050 Hz (lossless)
    """
    # Map bitrate to cutoff frequency
    bitrate_to_cutoff = {
        5: 800,
        8: 2000,
        16: 3500,
        32: 5500,
        64: 8000,
        96: 11000,
        128: 14000,
        192: 18000,
        256: 22050
    }
    
    # Find closest bitrate level
    available_bitrates = list(bitrate_to_cutoff.keys())
    closest_bitrate = min(available_bitrates, key=lambda x: abs(x - bitrate_kbps))
    cutoff_freq = bitrate_to_cutoff[closest_bitrate]
    
    # Normalize cutoff to Nyquist frequency
    nyquist = sr / 2
    if cutoff_freq >= nyquist:
        return audio  # No filtering needed
    
    normalized_cutoff = cutoff_freq / nyquist
    
    # Apply low-pass filter to simulate bitrate limitation
    b, a = signal.butter(4, normalized_cutoff, btype='low')
    filtered_audio = signal.filtfilt(b, a, audio)
    
    return filtered_audio


def create_playback_widget(audio, sr, features_list, chunk_times, selected_bitrates, bandwidth_array):
    """Create interactive audio playback widget"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🎵 Real-time Audio Playback")
        
        # Playback mode selection
        playback_mode = st.radio(
            "Select Playback Mode",
            ["Original Audio", "Simulated at Selected Bitrate", "Compare Bitrates"],
            horizontal=True,
            help="Play original or simulated audio at different bitrates"
        )
    
    with col2:
        st.markdown("### Audio Controls")
    
    if playback_mode == "Original Audio":
        st.info("🎵 Original uncompressed audio")
        st.audio(np.float32(audio / np.max(np.abs(audio))), sample_rate=sr, format="audio/wav")
        
        # Show original audio statistics
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Bitrate", "Lossless")
        with col_stats2:
            st.metric("Cutoff Freq", f"{sr/2:.0f} Hz")
        with col_stats3:
            st.metric("Quality", "Full Spectrum")
    
    elif playback_mode == "Simulated at Selected Bitrate":
        st.info("🎯 Audio simulated at adaptive bitrate selected by algorithm")
        
        # Calculate average bitrate
        avg_bitrate = np.mean(selected_bitrates)
        
        # Simulate audio
        simulated_audio = simulate_audio_quality(audio, sr, avg_bitrate)
        simulated_audio = np.float32(simulated_audio / np.max(np.abs(simulated_audio)))
        
        st.audio(simulated_audio, sample_rate=sr, format="audio/wav")
        
        # Show bitrate statistics
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Avg Bitrate", f"{avg_bitrate:.1f} kbps")
        with col_stats2:
            st.metric("Min Bitrate", f"{np.min(selected_bitrates):.1f} kbps")
        with col_stats3:
            st.metric("Max Bitrate", f"{np.max(selected_bitrates):.1f} kbps")
        
        # Show quality vs bitrate
        st.markdown("#### Bitrate Over Time")
        fig_playback = go.Figure()
        fig_playback.add_trace(go.Scatter(
            x=chunk_times,
            y=selected_bitrates,
            mode='lines+markers',
            name='Adaptive Bitrate',
            line=dict(color='#2ECC71', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.2)'
        ))
        fig_playback.update_layout(
            title="Bitrate Adaptation During Playback",
            xaxis_title="Time (seconds)",
            yaxis_title="Bitrate (kbps)",
            height=300,
            template='plotly_dark',
            hovermode='x unified'
        )
        st.plotly_chart(fig_playback, use_container_width=True)
    
    else:  # Compare Bitrates
        st.info("📊 Compare audio quality at different bitrate levels")
        
        selected_bitrates_to_compare = st.multiselect(
            "Select Bitrate Levels to Compare",
            [5, 8, 16, 32, 64, 96, 128, 192, 256],
            default=[32, 96, 256],
            help="Choose multiple bitrates to hear the difference"
        )
        
        if selected_bitrates_to_compare:
            # Sort for consistent ordering
            selected_bitrates_to_compare.sort()
            
            st.markdown(f"#### Comparing {len(selected_bitrates_to_compare)} Different Bitrates")
            
            # Create columns for each bitrate
            cols = st.columns(len(selected_bitrates_to_compare))
            
            for i, (col, bitrate) in enumerate(zip(cols, selected_bitrates_to_compare)):
                with col:
                    st.markdown(f"**{bitrate} kbps**")
                    
                    # Simulate audio at this bitrate
                    sim_audio = simulate_audio_quality(audio, sr, bitrate)
                    sim_audio = np.float32(sim_audio / np.max(np.abs(sim_audio)))
                    
                    st.audio(sim_audio, sample_rate=sr, format="audio/wav")
                    
                    # Quality assessment
                    if bitrate <= 8:
                        quality = "🔴 Very Low"
                    elif bitrate <= 16:
                        quality = "🟠 Low"
                    elif bitrate <= 32:
                        quality = "🟡 Fair"
                    elif bitrate <= 64:
                        quality = "🟢 Good"
                    elif bitrate <= 128:
                        quality = "🟢 Very Good"
                    else:
                        quality = "🟢 Excellent"
                    
                    st.caption(f"Quality: {quality}")


def main():
    """Main Streamlit application"""
    
    st.markdown('<div class="header-title">🎵 Adaptive Audio Bitrate System</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="description-text">Advanced analysis of audio features and adaptive bitrate streaming</div>',
                unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = init_analyzer()
    
    # Sidebar configuration
    st.sidebar.markdown("## Configuration")
    
    # Audio upload
    st.sidebar.markdown("### 📁 Audio File")
    uploaded_file = st.sidebar.file_uploader("Upload WAV file", type=['wav'])
    
    if uploaded_file is None:
        st.info("👈 Please upload a WAV audio file to get started")
        return
    
    # Load audio
    with st.spinner("Loading audio file..."):
        temp_path = Path("temp_audio.wav")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        audio, sr = analyzer.load_audio(str(temp_path))
    
    st.sidebar.success("✓ Audio loaded successfully")
    
    # Audio parameters
    st.sidebar.markdown("### ⚙️ Analysis Parameters")
    chunk_duration_ms = st.sidebar.slider(
        "Chunk Duration (ms)",
        min_value=50,
        max_value=500,
        value=100,
        step=50,
        help="Duration of each audio chunk for analysis"
    )
    
    # Analyze audio
    with st.spinner("Analyzing audio..."):
        features_list, chunk_times = analyzer.analyze_audio(audio, chunk_duration_ms)
        stats = analyzer.get_statistics(features_list)
    
    st.sidebar.markdown("### 📊 Audio Statistics")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Chunks", len(features_list))
        st.metric("Duration", f"{chunk_times[-1]:.2f}s")
    with col2:
        st.metric("Sample Rate", f"{sr} Hz")
        st.metric("Complexity", f"{stats['complexity_mean']:.2f}")
    
    # Network simulation
    st.sidebar.markdown("### 🌐 Network Simulation")
    
    network_sim = NetworkSimulator(chunk_times[-1], len(features_list))
    
    pattern_options = network_sim.get_pattern_options()
    selected_pattern = st.sidebar.selectbox(
        "Network Pattern",
        pattern_options,
        help="Select network bandwidth pattern"
    )
    
    bandwidth_array = network_sim.generate_bandwidth_pattern(selected_pattern)
    
    # Manual bandwidth override
    override_enabled = st.sidebar.checkbox("Manual Override", value=False)
    if override_enabled:
        override_value = st.sidebar.slider(
            "Fixed Bandwidth (kbps)",
            min_value=8,
            max_value=256,
            value=128,
            step=8
        )
        bandwidth_array = network_sim.apply_bandwidth_override(bandwidth_array, override_value)
    
    bandwidth_stats = network_sim.calculate_bandwidth_statistics(bandwidth_array)
    
    st.sidebar.markdown("### 📈 Bandwidth Statistics")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Mean BW", f"{bandwidth_stats['mean']:.1f} kbps")
        st.metric("Min BW", f"{bandwidth_stats['min']:.1f} kbps")
    with col2:
        st.metric("Max BW", f"{bandwidth_stats['max']:.1f} kbps")
        st.metric("Std Dev", f"{bandwidth_stats['std']:.1f} kbps")
    
    # Adaptive bitrate selection
    st.sidebar.markdown("### 🎯 Bitrate Algorithm")
    use_aggressive = st.sidebar.checkbox(
        "Aggressive Compression",
        value=False,
        help="Enable aggressive compression to reduce file size"
    )
    
    selector = AdaptiveBitrateSelector(use_aggressive_compression=use_aggressive)
    selected_bitrates, bitrate_reasons = selector.select_bitrate_batch(
        features_list, bandwidth_array, chunk_duration_ms
    )
    bitrate_stats = selector.calculate_statistics(selected_bitrates)
    
    st.sidebar.markdown("### 📊 Bitrate Statistics")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Mean", f"{bitrate_stats['mean']:.1f} kbps")
        st.metric("Min", f"{bitrate_stats['min']:.1f} kbps")
    with col2:
        st.metric("Max", f"{bitrate_stats['max']:.1f} kbps")
        st.metric("File Size", f"{selector.estimate_file_size(selected_bitrates, chunk_duration_ms):.2f} MB")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Audio Features",
        "🌐 Network Analysis",
        "🎯 Adaptive Bitrate",
        "📈 Metrics Comparison",
        "💾 Summary",
        "🎵 Audio Playback"
    ])
    
    with tab1:
        st.markdown("### Audio Feature Analysis")
        
        # Feature selection
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("#### RMS Energy")
            fig_rms = create_audio_features_chart(features_list, chunk_times, 'rms')
            st.plotly_chart(fig_rms, use_container_width=True)
        
        with feature_col2:
            st.markdown("#### Zero Crossing Rate")
            fig_zcr = create_audio_features_chart(features_list, chunk_times, 'zcr')
            st.plotly_chart(fig_zcr, use_container_width=True)
        
        feat_col1, feat_col2 = st.columns(2)
        
        with feat_col1:
            st.markdown("#### Spectral Centroid")
            fig_sc = create_audio_features_chart(features_list, chunk_times, 'spectral_centroid')
            st.plotly_chart(fig_sc, use_container_width=True)
        
        with feat_col2:
            st.markdown("#### Spectral Bandwidth")
            fig_sb = create_audio_features_chart(features_list, chunk_times, 'spectral_bandwidth')
            st.plotly_chart(fig_sb, use_container_width=True)
        
        st.markdown("#### Audio Complexity & Content Type")
        fig_complexity = create_complexity_chart(features_list, chunk_times)
        st.plotly_chart(fig_complexity, use_container_width=True)
    
    with tab2:
        st.markdown("### Network Bandwidth Simulation")
        
        st.markdown(f"**Pattern:** {selected_pattern}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            fig_bandwidth = create_bandwidth_chart(bandwidth_array, chunk_times)
            st.plotly_chart(fig_bandwidth, use_container_width=True)
        
        with col2:
            st.markdown("**Statistics**")
            st.metric("Mean", f"{bandwidth_stats['mean']:.1f} kbps")
            st.metric("Max", f"{bandwidth_stats['max']:.1f} kbps")
            st.metric("Min", f"{bandwidth_stats['min']:.1f} kbps")
            st.metric("Std Dev", f"{bandwidth_stats['std']:.1f} kbps")
            st.metric("Variance", f"{bandwidth_stats['variance']:.1f}")
    
    with tab3:
        st.markdown("### Adaptive Bitrate Selection")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            fig_adaptation = create_bitrate_comparison_chart(selected_bitrates, bandwidth_array, chunk_times)
            st.plotly_chart(fig_adaptation, use_container_width=True)
        
        with col2:
            st.markdown("**Bitrate Statistics**")
            st.metric("Mean", f"{bitrate_stats['mean']:.1f} kbps")
            st.metric("Max", f"{bitrate_stats['max']:.1f} kbps")
            st.metric("Min", f"{bitrate_stats['min']:.1f} kbps")
            st.metric("Median", f"{bitrate_stats['median']:.1f} kbps")
            st.metric("Std Dev", f"{bitrate_stats['std']:.1f} kbps")
        
        st.markdown("### Bitrate Selection Reasons")
        
        reason_df = pd.DataFrame({
            'Time (s)': chunk_times,
            'Selected (kbps)': selected_bitrates,
            'Available (kbps)': bandwidth_array,
            'Reason': bitrate_reasons
        })
        
        st.dataframe(reason_df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### Metrics Comparison")
        
        # Content distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig_content = create_content_distribution_chart(features_list)
            st.plotly_chart(fig_content, use_container_width=True)
        
        with col2:
            st.markdown("#### Audio Statistics Summary")
            
            summary_data = {
                'Metric': [
                    'Total Chunks',
                    'Speech Chunks',
                    'Music Chunks',
                    'Mixed Chunks',
                    'Avg RMS Energy',
                    'Max RMS Energy',
                    'Avg Complexity',
                    'Max Complexity',
                    'Avg ZCR',
                    'Avg Spectral Centroid (Hz)'
                ],
                'Value': [
                    f"{len(features_list)}",
                    f"{stats['speech_count']}",
                    f"{stats['music_count']}",
                    f"{stats['mixed_count']}",
                    f"{stats['rms_mean']:.4f}",
                    f"{stats['rms_max']:.4f}",
                    f"{stats['complexity_mean']:.4f}",
                    f"{stats['complexity_max']:.4f}",
                    f"{stats['zcr_mean']:.4f}",
                    f"{stats['spectral_centroid_mean']:.1f}"
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Bitrate distribution
        st.markdown("#### Bitrate Distribution")
        
        bitrate_counts = {}
        for br in selected_bitrates:
            br_int = int(br)
            bitrate_counts[br_int] = bitrate_counts.get(br_int, 0) + 1
        
        fig_bitrate_dist = go.Figure(data=[
            go.Bar(
                x=list(bitrate_counts.keys()),
                y=list(bitrate_counts.values()),
                marker=dict(color='#2ECC71')
            )
        ])
        
        fig_bitrate_dist.update_layout(
            title="Distribution of Selected Bitrates",
            xaxis_title="Bitrate (kbps)",
            yaxis_title="Frequency",
            height=300,
            template='plotly_dark'
        )
        
        st.plotly_chart(fig_bitrate_dist, use_container_width=True)
    
    with tab5:
        st.markdown("### Summary Report")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Audio Duration", f"{chunk_times[-1]:.2f}s")
        with col2:
            st.metric("Estimated Size", f"{selector.estimate_file_size(selected_bitrates, chunk_duration_ms):.2f} MB")
        with col3:
            st.metric("Avg Bitrate", f"{bitrate_stats['mean']:.1f} kbps")
        with col4:
            st.metric("Compression Enabled", "Yes" if use_aggressive else "No")
        
        st.markdown("### Configuration Summary")
        
        config_summary = f"""
        **Audio Analysis:**
        - Chunk Duration: {chunk_duration_ms} ms
        - Total Chunks Analyzed: {len(features_list)}
        - Average Complexity: {stats['complexity_mean']:.4f}
        
        **Network Simulation:**
        - Pattern: {selected_pattern}
        - Mean Bandwidth: {bandwidth_stats['mean']:.1f} kbps
        - Bandwidth Range: {bandwidth_stats['min']:.1f} - {bandwidth_stats['max']:.1f} kbps
        
        **Bitrate Selection:**
        - Algorithm: {"Aggressive Compression" if use_aggressive else "Standard"}
        - Mean Bitrate: {bitrate_stats['mean']:.1f} kbps
        - Bitrate Range: {bitrate_stats['min']:.1f} - {bitrate_stats['max']:.1f} kbps
        - Estimated File Size: {selector.estimate_file_size(selected_bitrates, chunk_duration_ms):.2f} MB
        
        **Content Distribution:**
        - Speech: {stats['speech_count']} chunks ({100*stats['speech_count']/len(features_list):.1f}%)
        - Music: {stats['music_count']} chunks ({100*stats['music_count']/len(features_list):.1f}%)
        - Mixed: {stats['mixed_count']} chunks ({100*stats['mixed_count']/len(features_list):.1f}%)
        """
        
        st.markdown(config_summary)
        
        st.markdown("### How It Works")
        
        explanation = """
        **Audio Feature Analysis:**
        1. **RMS Energy**: Measures loudness of each chunk
        2. **Zero Crossing Rate (ZCR)**: Counts frequency transitions, higher for speech
        3. **Spectral Centroid**: Indicates where audio energy is concentrated
        4. **Spectral Bandwidth**: Shows frequency spread of the audio
        5. **Spectral Flatness**: Measures how uniform the frequency distribution is
        
        **Complexity Scoring (0-1):**
        - Combines RMS energy, ZCR, spectral bandwidth, and flatness
        - Higher = more detail, needs higher bitrate
        - Lower = simpler content, can use lower bitrate
        
        **Content Classification:**
        - **Speech**: Higher ZCR, lower spectral centroid
        - **Music**: Lower ZCR, higher spectral centroid, more energy
        - **Mixed**: Intermediate characteristics
        
        **Adaptive Bitrate Selection:**
        - Determines minimum bitrate based on complexity and content type
        - Adjusts based on available bandwidth
        - Applies smoothing to avoid drastic bitrate changes
        - Considers buffer level for streaming stability
        
        **Network Patterns:**
        - **Stable**: Constant bandwidth (ideal conditions)
        - **Decreasing**: Bandwidth drops over time (network degradation)
        - **Sinusoidal**: Periodic fluctuations (realistic mobile conditions)
        - **Recovery**: Drop followed by recovery (network issue + recovery)
        - **Weak Network**: Low bandwidth with noise (poor connection)
        - **Random Spikes**: Sudden changes (unpredictable conditions)
        """
        
        st.markdown(explanation)

    with tab6:
        st.markdown("### 🎵 Real-time Audio Playback & Quality Comparison")
        
        create_playback_widget(audio, sr, features_list, chunk_times, selected_bitrates, bandwidth_array)


if __name__ == "__main__":
    main()
