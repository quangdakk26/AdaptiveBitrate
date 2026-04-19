"""
Network Bandwidth Simulator Module
Simulates various network conditions for adaptive bitrate streaming
"""

import numpy as np
from typing import List, Dict, Tuple


class NetworkSimulator:
    """Simulates network bandwidth patterns"""
    
    def __init__(self, duration_seconds: float, num_chunks: int):
        """Initialize network simulator
        
        Args:
            duration_seconds: Total duration in seconds
            num_chunks: Number of audio chunks
        """
        self.duration = duration_seconds
        self.num_chunks = num_chunks
        self.current_bandwidth = 256.0
    
    def generate_stable_bandwidth(self, bandwidth: float = 256.0) -> np.ndarray:
        """Generate stable bandwidth (constant)"""
        return np.full(self.num_chunks, bandwidth)
    
    def generate_decreasing_bandwidth(self, start: float = 256.0, end: float = 10.0) -> np.ndarray:
        """Generate linearly decreasing bandwidth (256→10 kbps)"""
        return np.linspace(start, end, self.num_chunks)
    
    def generate_sinusoidal_bandwidth(self, center: float = 64.0, amplitude: float = 40.0) -> np.ndarray:
        """Generate sinusoidal bandwidth fluctuation (center 64, ~24-104 kbps)"""
        t = np.linspace(0, 4 * np.pi, self.num_chunks)  # 2 full cycles
        bandwidth = center + amplitude * np.sin(t)
        return np.maximum(bandwidth, 10.0)  # Minimum 10 kbps
    
    def generate_recovery_bandwidth(self) -> np.ndarray:
        """Generate bandwidth that drops then recovers (lower levels, min 10 kbps)"""
        bandwidth = np.full(self.num_chunks, 64.0)
        
        # Drop phase (first 30%)
        drop_idx = int(self.num_chunks * 0.3)
        bandwidth[:drop_idx] = np.linspace(64, 10, drop_idx)
        
        # Recovery phase (next 50%)
        recovery_end = int(self.num_chunks * 0.8)
        bandwidth[drop_idx:recovery_end] = np.linspace(10, 64, recovery_end - drop_idx)
        
        # Stable phase (last 20%)
        bandwidth[recovery_end:] = 64
        
        return bandwidth
    
    def generate_weak_network_bandwidth(self, center: float = 48.0) -> np.ndarray:
        """Generate weak network bandwidth (48 kbps with fluctuation)"""
        noise = np.random.normal(0, 8, self.num_chunks)
        bandwidth = center + noise
        return np.maximum(np.minimum(bandwidth, 64), 16)  # Keep between 16-64 kbps
    
    def generate_very_weak_network_bandwidth(self, center: float = 10.0) -> np.ndarray:
        """Generate very weak network bandwidth (10 kbps with noise - ultra low)"""
        noise = np.random.normal(0, 2, self.num_chunks)
        bandwidth = center + noise
        return np.maximum(np.minimum(bandwidth, 16), 5)  # Keep between 5-16 kbps
    
    def generate_random_spikes_bandwidth(self, base: float = 64.0) -> np.ndarray:
        """Generate bandwidth with random spikes and drops (base 64, min 10)"""
        bandwidth = np.full(self.num_chunks, base)
        
        # Add random spikes (increases)
        num_spikes = self.num_chunks // 20
        spike_indices = np.random.choice(self.num_chunks, num_spikes, replace=False)
        for idx in spike_indices:
            spike_duration = np.random.randint(2, 8)
            end_idx = min(idx + spike_duration, self.num_chunks)
            spike_height = np.random.uniform(1.5, 3.0)
            bandwidth[idx:end_idx] *= spike_height
        
        # Add random drops
        num_drops = self.num_chunks // 20
        drop_indices = np.random.choice(self.num_chunks, num_drops, replace=False)
        for idx in drop_indices:
            drop_duration = np.random.randint(2, 8)
            end_idx = min(idx + drop_duration, self.num_chunks)
            drop_factor = np.random.uniform(0.2, 0.7)
            bandwidth[idx:end_idx] *= drop_factor
        
        return np.maximum(bandwidth, 10)  # Minimum 10 kbps
    
    def get_pattern_options(self) -> List[str]:
        """Get list of available bandwidth patterns"""
        return [
            "Stable (256 kbps)",
            "Decreasing (256→10 kbps)",
            "Sinusoidal Fluctuation",
            "Recovery Pattern",
            "Weak Network (48 kbps)",
            "Very Weak Network (10 kbps)",
            "Random Spikes & Drops"
        ]
    
    def generate_bandwidth_pattern(self, pattern: str) -> np.ndarray:
        """Generate bandwidth pattern
        
        Args:
            pattern: Name of the pattern
            
        Returns:
            Bandwidth array for each chunk
        """
        if "Stable" in pattern:
            return self.generate_stable_bandwidth(256.0)
        elif "Decreasing" in pattern:
            return self.generate_decreasing_bandwidth(256.0, 48.0)
        elif "Sinusoidal" in pattern:
            return self.generate_sinusoidal_bandwidth(256.0, 100.0)
        elif "Recovery" in pattern:
            return self.generate_recovery_bandwidth()
        elif "Very Weak" in pattern:
            return self.generate_very_weak_network_bandwidth(10.0)
        elif "Weak" in pattern:
            return self.generate_weak_network_bandwidth(48.0)
        elif "Random" in pattern:
            return self.generate_random_spikes_bandwidth(128.0)
        else:
            return self.generate_stable_bandwidth(256.0)
    
    def apply_bandwidth_override(self, bandwidth: np.ndarray, override_value: float) -> np.ndarray:
        """Apply manual bandwidth override
        
        Args:
            bandwidth: Current bandwidth array
            override_value: Manual override value (0 = use pattern, >0 = fixed value)
            
        Returns:
            Modified bandwidth array
        """
        if override_value > 0:
            return np.full(len(bandwidth), override_value)
        return bandwidth
    
    def calculate_bandwidth_statistics(self, bandwidth: np.ndarray) -> Dict:
        """Calculate bandwidth statistics"""
        return {
            'mean': float(np.mean(bandwidth)),
            'max': float(np.max(bandwidth)),
            'min': float(np.min(bandwidth)),
            'std': float(np.std(bandwidth)),
            'variance': float(np.var(bandwidth)),
        }
