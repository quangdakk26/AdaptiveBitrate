from pathlib import Path
import numpy as np
import torch
import torchaudio
import soundfile as sf


class AudioEnergyCalculator:
    """Calculate various energy metrics from audio signals."""
    
    def __init__(self, audio_path: str):
        """
        Initialize with audio file path.
        
        Args:
            audio_path: Path to audio file (.wav, .mp3, etc.)
        """
        self.audio_path = Path(audio_path)
        self.audio, self.sr = torchaudio.load(str(self.audio_path))
        
        # Convert to mono if necessary
        if self.audio.shape[0] > 1:
            self.audio = torch.mean(self.audio, dim=0, keepdim=True)
    
    def total_energy(self) -> float:
        """Calculate total energy (sum of squared samples)."""
        return float(torch.sum(self.audio ** 2).item())
    
    def rms_energy(self) -> float:
        """Calculate RMS (Root Mean Square) energy."""
        return float(torch.sqrt(torch.mean(self.audio ** 2)).item())
    
    def frame_energy(self, frame_size: int = 2048, hop_size: int = 512) -> np.ndarray:
        """
        Calculate frame-wise energy.
        
        Args:
            frame_size: Size of each frame
            hop_size: Hop size between frames
            
        Returns:
            Array of energy values for each frame
        """
        audio_np = self.audio.numpy().squeeze()
        num_frames = (len(audio_np) - frame_size) // hop_size + 1
        
        frame_energies = []
        for i in range(num_frames):
            start = i * hop_size
            end = start + frame_size
            frame = audio_np[start:end]
            energy = np.sum(frame ** 2)
            frame_energies.append(energy)
        
        return np.array(frame_energies)
    
    def log_energy(self, frame_energies: np.ndarray = None, epsilon: float = 1e-10) -> np.ndarray:
        """
        Calculate log energy (useful for visualization).
        
        Args:
            frame_energies: Array of frame energies (calculates if None)
            epsilon: Small value to avoid log(0)
            
        Returns:
            Log-scaled energy values
        """
        if frame_energies is None:
            frame_energies = self.frame_energy()
        
        return np.log10(frame_energies + epsilon)
    
    def energy_statistics(self, frame_energies: np.ndarray = None) -> dict:
        """
        Calculate statistics of frame energy.
        
        Args:
            frame_energies: Array of frame energies (calculates if None)
            
        Returns:
            Dictionary with energy statistics
        """
        if frame_energies is None:
            frame_energies = self.frame_energy()
        
        return {
            'total': np.sum(frame_energies),
            'mean': np.mean(frame_energies),
            'std': np.std(frame_energies),
            'min': np.min(frame_energies),
            'max': np.max(frame_energies),
            'median': np.median(frame_energies)
        }


def calculate_energy_from_file(input_path: str, output_stats_path: str = None) -> dict:
    """
    Calculate energy metrics from audio file.
    
    Args:
        input_path: Path to input audio file
        output_stats_path: Optional path to save stats as text file
        
    Returns:
        Dictionary with energy metrics
    """
    calc = AudioEnergyCalculator(input_path)
    
    # Calculate metrics
    total_energy = calc.total_energy()
    rms_energy = calc.rms_energy()
    frame_energies = calc.frame_energy()
    frame_stats = calc.energy_statistics(frame_energies)
    
    results = {
        'file': str(input_path),
        'sample_rate': calc.sr,
        'duration_seconds': calc.audio.shape[1] / calc.sr,
        'total_energy': total_energy,
        'rms_energy': rms_energy,
        'frame_energy_stats': frame_stats,
        'num_frames': len(frame_energies)
    }
    
    # Save statistics if requested
    if output_stats_path:
        with open(output_stats_path, 'w') as f:
            f.write(f"Audio Energy Analysis\n")
            f.write(f"{'='*50}\n")
            f.write(f"File: {results['file']}\n")
            f.write(f"Sample Rate: {results['sample_rate']} Hz\n")
            f.write(f"Duration: {results['duration_seconds']:.2f} seconds\n")
            f.write(f"\nEnergy Metrics:\n")
            f.write(f"  Total Energy: {results['total_energy']:.6e}\n")
            f.write(f"  RMS Energy: {results['rms_energy']:.6f}\n")
            f.write(f"  Number of Frames: {results['num_frames']}\n")
            f.write(f"\nFrame Energy Statistics:\n")
            for key, value in frame_stats.items():
                f.write(f"  {key.capitalize()}: {value:.6e}\n")
    
    return results


def main():
    """Example usage."""
    input_path = Path("data/input/sample.wav")
    output_stats_path = Path("data/output/energy_stats.txt")
    
    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        return
    
    print(f"Calculating energy for: {input_path}")
    results = calculate_energy_from_file(str(input_path), str(output_stats_path))
    
    print(f"\nResults:")
    print(f"  Total Energy: {results['total_energy']:.6e}")
    print(f"  RMS Energy: {results['rms_energy']:.6f}")
    print(f"  Frame Energy Mean: {results['frame_energy_stats']['mean']:.6e}")
    print(f"  Frame Energy Std: {results['frame_energy_stats']['std']:.6e}")
    print(f"\nStatistics saved to: {output_stats_path}")


if __name__ == "__main__":
    main() 