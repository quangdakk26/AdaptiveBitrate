"""
Adaptive Bitrate Selection Module
Determines optimal bitrate based on audio features and network conditions
"""

import numpy as np
from typing import Dict, List, Tuple


class AdaptiveBitrateSelector:
    """Selects optimal bitrate based on audio features and network bandwidth"""
    
    # Predefined bitrate levels (kbps)
    BITRATE_LEVELS = [8, 16, 32, 64, 96, 128, 192, 256]
    
    # Bitrate requirements for different content types (kbps)
    BITRATE_REQUIREMENTS = {
        'speech': {
            'low': 8,       # Low complexity speech
            'medium': 16,   # Normal speech
            'high': 32,     # High complexity speech
        },
        'music': {
            'low': 32,      # Low complexity music
            'medium': 96,   # Normal music
            'high': 192,    # High complexity music
        },
        'mixed': {
            'low': 16,      # Low complexity mixed
            'medium': 64,   # Normal mixed
            'high': 128,    # High complexity mixed
        },
        'silence': 8,       # Silence/comfort noise
    }
    
    def __init__(self, use_aggressive_compression: bool = False):
        """Initialize adaptive bitrate selector
        
        Args:
            use_aggressive_compression: If True, prioritize bandwidth saving
        """
        self.use_aggressive = use_aggressive_compression
        self.last_bitrate = 64  # Initial bitrate
    
    def select_bitrate(self, 
                      features: Dict,
                      available_bandwidth: float,
                      buffer_level_ms: float = 1000) -> Tuple[float, str]:
        """Select bitrate for audio chunk
        
        Args:
            features: Audio features dict
            available_bandwidth: Available bandwidth in kbps
            buffer_level_ms: Current buffer level in ms
            
        Returns:
            Tuple of (selected_bitrate, reason)
        """
        # Check for silence
        if features['rms'] < 0.01:
            return 8.0, "silence"
        
        # Determine content type
        content_type = features['content_type']
        
        # Estimate complexity level
        complexity = features['complexity']
        if complexity < 0.33:
            complexity_level = 'low'
        elif complexity < 0.67:
            complexity_level = 'medium'
        else:
            complexity_level = 'high'
        
        # Get base bitrate requirement for content
        base_bitrate = self.BITRATE_REQUIREMENTS[content_type][complexity_level]
        
        # Adjust based on buffer level
        if buffer_level_ms < 500:  # Low buffer
            # Reduce bitrate to fill buffer
            adjusted_bitrate = base_bitrate * 0.7
        elif buffer_level_ms > 5000:  # High buffer
            # Can afford higher bitrate
            adjusted_bitrate = base_bitrate * 1.2
        else:
            adjusted_bitrate = base_bitrate
        
        # Apply aggressive compression if enabled
        if self.use_aggressive:
            adjusted_bitrate *= 0.8
        
        # Ensure within available bandwidth
        final_bitrate = min(adjusted_bitrate, available_bandwidth * 0.9)
        
        # Snap to available bitrate levels
        final_bitrate = self._snap_to_level(final_bitrate)
        
        # Apply smoothing (avoid drastic changes)
        smoothed_bitrate = 0.7 * self.last_bitrate + 0.3 * final_bitrate
        smoothed_bitrate = self._snap_to_level(smoothed_bitrate)
        
        self.last_bitrate = smoothed_bitrate
        
        reason = f"{content_type}_{complexity_level}"
        
        return smoothed_bitrate, reason
    
    def _snap_to_level(self, bitrate: float) -> float:
        """Snap bitrate to nearest available level"""
        return float(min(self.BITRATE_LEVELS, key=lambda x: abs(x - bitrate)))
    
    def select_bitrate_batch(self,
                            features_list: List[Dict],
                            bandwidth_list: np.ndarray,
                            chunk_duration_ms: float = 100) -> Tuple[np.ndarray, List[str]]:
        """Select bitrates for all chunks
        
        Args:
            features_list: List of audio features
            bandwidth_list: Array of available bandwidth
            chunk_duration_ms: Duration of each chunk in ms
            
        Returns:
            Tuple of (bitrate_array, reason_list)
        """
        bitrates = []
        reasons = []
        buffer_level = 3000  # Initial buffer (ms)
        
        for i, (features, bandwidth) in enumerate(zip(features_list, bandwidth_list)):
            # Calculate buffer level
            # Simplified: assume we transmit current chunk at selected bitrate
            chunk_size_bytes = (bitrates[-1] * chunk_duration_ms / 8000) if bitrates else (64 * chunk_duration_ms / 8000)
            transmission_time = (chunk_size_bytes * 8) / (bandwidth * 1000)  # seconds
            
            buffer_change = chunk_duration_ms - transmission_time * 1000
            buffer_level = max(0, buffer_level + buffer_change)
            
            # Select bitrate
            bitrate, reason = self.select_bitrate(features, bandwidth, buffer_level)
            bitrates.append(bitrate)
            reasons.append(reason)
        
        return np.array(bitrates), reasons
    
    def get_bitrate_levels(self) -> List[float]:
        """Get available bitrate levels"""
        return self.BITRATE_LEVELS
    
    def calculate_statistics(self, bitrates: np.ndarray) -> Dict:
        """Calculate bitrate statistics"""
        return {
            'mean': float(np.mean(bitrates)),
            'max': float(np.max(bitrates)),
            'min': float(np.min(bitrates)),
            'std': float(np.std(bitrates)),
            'median': float(np.median(bitrates)),
        }
    
    def estimate_file_size(self, bitrates: np.ndarray, chunk_duration_ms: float = 100) -> float:
        """Estimate file size in MB
        
        Args:
            bitrates: Array of selected bitrates
            chunk_duration_ms: Duration of each chunk
            
        Returns:
            Estimated file size in MB
        """
        total_duration_seconds = len(bitrates) * chunk_duration_ms / 1000
        avg_bitrate = np.mean(bitrates)
        
        # File size = (bitrate in kbps) * duration (seconds) / 8 / 1000
        file_size_mb = (avg_bitrate * total_duration_seconds) / 8 / 1000
        return file_size_mb
