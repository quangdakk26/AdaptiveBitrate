"""
Audio Feature Analyzer Module
Analyzes audio chunks for features used in adaptive bitrate streaming
"""

import numpy as np
import librosa
from typing import Tuple, Dict, List
from scipy import signal
import soundfile as sf


class AudioFeatureAnalyzer:
    """Analyzes audio features for adaptive bitrate decisions"""
    
    def __init__(self, sr: int = 44100):
        self.sr = sr
    
    def load_audio(self, filepath: str) -> Tuple[np.ndarray, int]:
        """Load audio file"""
        audio, sr = librosa.load(filepath, sr=self.sr, mono=True)
        return audio, sr
    
    def split_into_chunks(self, audio: np.ndarray, chunk_duration_ms: float = 100) -> List[np.ndarray]:
        """Split audio into chunks"""
        chunk_samples = int(self.sr * chunk_duration_ms / 1000)
        num_chunks = len(audio) // chunk_samples
        chunks = [audio[i*chunk_samples:(i+1)*chunk_samples] for i in range(num_chunks)]
        return chunks
    
    def calculate_rms_energy(self, chunk: np.ndarray) -> float:
        """Calculate RMS energy"""
        return float(np.sqrt(np.mean(chunk ** 2)))
    
    def calculate_zero_crossing_rate(self, chunk: np.ndarray) -> float:
        """Calculate Zero Crossing Rate"""
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(chunk)))
        return zcr
    
    def calculate_spectral_centroid(self, chunk: np.ndarray) -> float:
        """Calculate Spectral Centroid"""
        centroid = librosa.feature.spectral_centroid(y=chunk, sr=self.sr)[0]
        return float(np.mean(centroid))
    
    def calculate_spectral_bandwidth(self, chunk: np.ndarray) -> float:
        """Calculate Spectral Bandwidth"""
        bandwidth = librosa.feature.spectral_bandwidth(y=chunk, sr=self.sr)[0]
        return float(np.mean(bandwidth))
    
    def calculate_spectral_flatness(self, chunk: np.ndarray) -> float:
        """Calculate Spectral Flatness (Wiener Entropy)"""
        S = np.abs(librosa.stft(chunk))
        power = np.mean(S ** 2, axis=1)
        
        # Geometric mean
        geometric_mean = np.exp(np.mean(np.log(power + 1e-10)))
        # Arithmetic mean
        arithmetic_mean = np.mean(power)
        
        flatness = geometric_mean / (arithmetic_mean + 1e-10)
        return float(np.clip(flatness, 0, 1))
    
    def classify_content(self, features: Dict) -> str:
        """Classify audio content type"""
        zcr = features['zcr']
        spectral_centroid = features['spectral_centroid']
        rms = features['rms']
        
        # Speech characteristics: higher ZCR, lower spectral centroid
        # Music characteristics: lower ZCR, higher spectral centroid, more energy
        
        if zcr > 0.1 and spectral_centroid < 2000:
            return "speech"
        elif zcr < 0.05 and spectral_centroid > 2000 and rms > 0.05:
            return "music"
        else:
            return "mixed"
    
    def estimate_complexity(self, features: Dict) -> float:
        """Estimate audio complexity (0-1)
        
        Higher complexity = more detail, needs higher bitrate
        """
        rms = features['rms']
        zcr = features['zcr']
        spectral_bandwidth = features['spectral_bandwidth']
        flatness = features['spectral_flatness']
        
        # Complexity factors:
        # - Higher RMS (louder) = more energy detail
        # - Higher ZCR (more transitions) = more complexity
        # - Higher spectral bandwidth = more frequency content
        # - Lower flatness = more structured (higher complexity)
        
        complexity = (
            np.clip(rms * 10, 0, 1) * 0.3 +           # Energy component
            np.clip(zcr * 5, 0, 1) * 0.3 +              # Transition component
            np.clip(spectral_bandwidth / 8000, 0, 1) * 0.2 +  # Frequency spread
            (1 - flatness) * 0.2                        # Structure component
        )
        
        return float(np.clip(complexity, 0, 1))
    
    def analyze_chunk(self, chunk: np.ndarray) -> Dict:
        """Analyze a single audio chunk"""
        if len(chunk) < 512:
            return None
        
        features = {
            'rms': self.calculate_rms_energy(chunk),
            'zcr': self.calculate_zero_crossing_rate(chunk),
            'spectral_centroid': self.calculate_spectral_centroid(chunk),
            'spectral_bandwidth': self.calculate_spectral_bandwidth(chunk),
            'spectral_flatness': self.calculate_spectral_flatness(chunk),
        }
        
        features['content_type'] = self.classify_content(features)
        features['complexity'] = self.estimate_complexity(features)
        
        return features
    
    def analyze_audio(self, audio: np.ndarray, chunk_duration_ms: float = 100) -> Tuple[List[Dict], List[float]]:
        """Analyze entire audio file"""
        chunks = self.split_into_chunks(audio, chunk_duration_ms)
        
        features_list = []
        chunk_times = []
        
        chunk_samples = int(self.sr * chunk_duration_ms / 1000)
        
        for i, chunk in enumerate(chunks):
            features = self.analyze_chunk(chunk)
            if features is not None:
                features_list.append(features)
                chunk_times.append((i + 1) * chunk_duration_ms / 1000)
        
        return features_list, chunk_times
    
    def get_statistics(self, features_list: List[Dict]) -> Dict:
        """Get statistics from features list"""
        if not features_list:
            return {}
        
        stats = {
            'rms_mean': np.mean([f['rms'] for f in features_list]),
            'rms_max': np.max([f['rms'] for f in features_list]),
            'rms_min': np.min([f['rms'] for f in features_list]),
            'zcr_mean': np.mean([f['zcr'] for f in features_list]),
            'complexity_mean': np.mean([f['complexity'] for f in features_list]),
            'complexity_max': np.max([f['complexity'] for f in features_list]),
            'spectral_centroid_mean': np.mean([f['spectral_centroid'] for f in features_list]),
            'content_types': [f['content_type'] for f in features_list],
        }
        
        # Count content types
        stats['speech_count'] = stats['content_types'].count('speech')
        stats['music_count'] = stats['content_types'].count('music')
        stats['mixed_count'] = stats['content_types'].count('mixed')
        
        return stats
