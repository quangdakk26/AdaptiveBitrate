"""
Real-time Audio Listening and Processing Module
Handles microphone recording, audio playback, and real-time visualization
"""

import streamlit as st
import numpy as np
import torch
import torchaudio
import soundfile as sf
from pathlib import Path
from typing import Tuple, Optional
import plotly.graph_objects as go
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
from collections import deque
import time


class RealtimeAudioListener:
    """Handle real-time audio listening from microphone"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.audio_buffer = deque(maxlen=int(sample_rate * 2))  # 2 seconds buffer
        self.energy_buffer = deque(maxlen=100)  # Store last 100 frame energies
        self.max_energy = 0.0
        
    def process_frame(self, frame: av.AudioFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Process incoming audio frame
        
        Args:
            frame: Audio frame from webrtc
            
        Returns:
            Tuple of (audio_array, energy_value)
        """
        # Convert frame to numpy array
        sound = frame.to_ndarray()
        
        # Convert stereo to mono if needed
        if len(sound.shape) > 1:
            sound = np.mean(sound, axis=1)
        
        # Normalize
        sound = sound / (np.max(np.abs(sound)) + 1e-8)
        
        # Add to buffer
        for sample in sound:
            self.audio_buffer.append(sample)
        
        # Calculate frame energy
        energy = float(np.sqrt(np.mean(sound ** 2)))
        self.energy_buffer.append(energy)
        self.max_energy = max(self.max_energy, energy)
        
        return sound, energy
    
    def get_buffer_array(self) -> np.ndarray:
        """Get current audio buffer as numpy array"""
        return np.array(list(self.audio_buffer))
    
    def get_energy_history(self) -> list:
        """Get energy history"""
        return list(self.energy_buffer)
    
    def clear_buffers(self):
        """Clear all buffers"""
        self.audio_buffer.clear()
        self.energy_buffer.clear()
        self.max_energy = 0.0


def create_audio_waveform_plot(audio: np.ndarray, sample_rate: int = 44100) -> go.Figure:
    """Create real-time waveform visualization"""
    
    time_axis = np.linspace(0, len(audio) / sample_rate, len(audio))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_axis,
        y=audio,
        mode='lines',
        name='Waveform',
        line=dict(color='#1f77b4', width=1),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="Real-time Audio Waveform",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        hovermode='x unified',
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_dark'
    )
    
    return fig


def create_energy_visualization(energy_history: list) -> go.Figure:
    """Create real-time energy visualization"""
    
    if not energy_history:
        energy_history = [0]
    
    frames = np.arange(len(energy_history))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frames,
        y=energy_history,
        mode='lines+markers',
        name='Frame Energy',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_hline(
        y=np.mean(energy_history),
        line_dash="dash",
        line_color="green",
        annotation_text="Mean Energy"
    )
    
    fig.update_layout(
        title="Real-time Audio Energy",
        xaxis_title="Frame Number",
        yaxis_title="Energy (RMS)",
        hovermode='x unified',
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_dark'
    )
    
    return fig


def create_frequency_spectrum_plot(audio: np.ndarray, sample_rate: int = 44100) -> go.Figure:
    """Create frequency spectrum visualization"""
    
    # Compute FFT
    fft = np.fft.fft(audio)
    frequencies = np.fft.fftfreq(len(audio), 1/sample_rate)
    magnitude = np.abs(fft)
    
    # Only positive frequencies
    positive_idx = frequencies > 0
    frequencies = frequencies[positive_idx]
    magnitude = magnitude[positive_idx]
    
    # Smooth for visualization
    magnitude_db = 20 * np.log10(magnitude + 1e-10)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frequencies,
        y=magnitude_db,
        mode='lines',
        name='Frequency',
        line=dict(color='#2ca02c', width=1),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="Frequency Spectrum",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)",
        xaxis_type="log",
        hovermode='x unified',
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_dark'
    )
    
    return fig


def save_recorded_audio(audio_array: np.ndarray, sample_rate: int = 44100, 
                       filename: str = "recorded_audio.wav") -> Path:
    """
    Save recorded audio to WAV file
    
    Args:
        audio_array: Audio data as numpy array
        sample_rate: Sample rate in Hz
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    output_path = Path(filename)
    sf.write(output_path, audio_array, sample_rate)
    return output_path


def streamlit_webrtc_component(key: str = "media-stream-processor"):
    """
    Create Streamlit WebRTC component for real-time audio processing
    
    Args:
        key: Unique key for component
        
    Returns:
        WebRTC connection info
    """
    RTC_CONFIGURATION = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    
    webrtc_ctx = webrtc_streamer(
        key=key,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )
    
    return webrtc_ctx


def calculate_realtime_bitrate(energy: float, available_bandwidth: float = 128.0) -> float:
    """
    Calculate adaptive bitrate based on real-time energy
    
    Args:
        energy: Current frame energy
        available_bandwidth: Available bandwidth in kbps
        
    Returns:
        Recommended bitrate in kbps
    """
    bitrate_levels = [1.5, 3.0, 6.0, 12.0, 24.0, 48.0]
    
    # Energy-based minimum bitrate
    if energy < 0.05:
        min_bitrate = 1.5  # Silence
    elif energy < 0.15:
        min_bitrate = 3.0  # Low energy
    elif energy < 0.35:
        min_bitrate = 6.0  # Medium energy
    elif energy < 0.6:
        min_bitrate = 12.0  # High energy
    else:
        min_bitrate = 24.0  # Very high energy
    
    # Select bitrate within available bandwidth
    selected_bitrate = min_bitrate
    for bitrate in bitrate_levels:
        if bitrate <= available_bandwidth and bitrate > selected_bitrate:
            selected_bitrate = bitrate
    
    return selected_bitrate


def display_realtime_metrics(energy: float, bitrate: float, bandwidth: float):
    """Display real-time metrics in Streamlit columns"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Energy (RMS)",
            f"{energy:.4f}",
            delta=None if energy > 0.05 else "Silence",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Selected Bitrate",
            f"{bitrate:.1f} kbps",
            delta=f"vs {bandwidth:.1f} available"
        )
    
    with col3:
        efficiency = (bitrate / bandwidth * 100) if bandwidth > 0 else 0
        st.metric(
            "Bandwidth Usage",
            f"{efficiency:.1f}%",
            delta="Efficient" if efficiency > 50 else "Conservative"
        )
    
    with col4:
        st.metric(
            "Status",
            "Recording" if energy > 0.05 else "Waiting...",
            delta="Active" if energy > 0.05 else "Silent"
        )
