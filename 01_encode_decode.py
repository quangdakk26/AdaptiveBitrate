from pathlib import Path
import sys
import importlib.util
import torch
import torchaudio
import soundfile as sf
import numpy as np
from encodec import EncodecModel
from encodec.utils import convert_audio

# Import AudioEnergyCalculator from 03_audio_energy.py
spec = importlib.util.spec_from_file_location("audio_energy", Path(__file__).parent / "03_audio_energy.py")
audio_energy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_energy)
AudioEnergyCalculator = audio_energy.AudioEnergyCalculator

INPUT = Path("data/input/sample.wav")
OUTPUT_DIR = Path("data/output")

# Frame-wise bitrate configuration (energy level -> bitrate in kbps)
FRAME_BITRATE_CONFIG = {
    'high_bandwidth': {
        'high_energy': 24.0,
        'medium_energy': 12.0,
        'low_energy': 6.0
    },
    'medium_bandwidth': {
        'high_energy': 12.0,
        'medium_energy': 6.0,
        'low_energy': 3.0
    },
    'low_bandwidth': {
        'high_energy': 6.0,
        'medium_energy': 3.0,
        'low_energy': 1.5
    }
}

def calculate_frame_energy_levels(audio_path: str, frame_size: int = 2048, hop_size: int = 512) -> tuple:
    """
    Calculate frame-wise energy levels for adaptive bitrate selection.
    
    Args:
        audio_path: Path to input audio file
        frame_size: Size of each frame
        hop_size: Hop size between frames
        
    Returns:
        Tuple of (frame_energies, energy_stats, frame_bitrates, bandwidth_level)
    """
    calculator = AudioEnergyCalculator(audio_path)
    
    # Get frame energies
    frame_energies = calculator.frame_energy(frame_size=frame_size, hop_size=hop_size)
    stats = calculator.energy_statistics(frame_energies)
    
    return frame_energies, stats

def categorize_bandwidth(bandwidth_mbps: float) -> str:
    """Categorize bandwidth level."""
    if bandwidth_mbps >= 10:
        return 'high_bandwidth'
    elif bandwidth_mbps >= 3:
        return 'medium_bandwidth'
    else:
        return 'low_bandwidth'

def get_frame_bitrate(frame_energy: float, max_energy: float, bandwidth_level: str) -> float:
    """
    Get bitrate for a single frame based on its energy.
    
    Args:
        frame_energy: Energy value of the frame
        max_energy: Maximum energy across all frames
        bandwidth_level: 'high_bandwidth', 'medium_bandwidth', or 'low_bandwidth'
        
    Returns:
        Bitrate in kbps
    """
    # Normalize frame energy to 0-1 range
    normalized_energy = frame_energy / max_energy if max_energy > 0 else 0
    
    # Categorize energy level
    if normalized_energy > 0.6:
        energy_level = 'high_energy'
    elif normalized_energy > 0.3:
        energy_level = 'medium_energy'
    else:
        energy_level = 'low_energy'
    
    return FRAME_BITRATE_CONFIG[bandwidth_level][energy_level], energy_level

def apply_frame_wise_adaptive_bitrate(
    audio_path: str, 
    bandwidth_mbps: float = 10.0,
    frame_size: int = 2048,
    hop_size: int = 512
) -> tuple:
    """
    Apply frame-wise adaptive bitrate encoding.
    
    Args:
        audio_path: Path to input audio file
        bandwidth_mbps: Available bandwidth in Mbps
        frame_size: Size of each frame
        hop_size: Hop size between frames
        
    Returns:
        Tuple of (wav, model, bitrate_schedule, stats)
    """
    # Load audio
    wav, sr = torchaudio.load(audio_path)
    
    # Categorize bandwidth
    bandwidth_level = categorize_bandwidth(bandwidth_mbps)
    
    # Calculate frame energies
    frame_energies, stats = calculate_frame_energy_levels(
        audio_path, 
        frame_size=frame_size, 
        hop_size=hop_size
    )
    
    max_energy = stats['max']
    
    # Calculate bitrate for each frame
    bitrate_schedule = []
    energy_levels = []
    for frame_energy in frame_energies:
        bitrate, energy_level = get_frame_bitrate(frame_energy, max_energy, bandwidth_level)
        bitrate_schedule.append(bitrate)
        energy_levels.append(energy_level)
    
    # Print detailed diagnostics
    print(f"\n{'='*70}")
    print(f"FRAME-WISE ADAPTIVE BITRATE ANALYSIS")
    print(f"{'='*70}")
    print(f"Audio File: {audio_path}")
    print(f"Available Bandwidth: {bandwidth_mbps} Mbps ({bandwidth_level})")
    print(f"Sample Rate: {sr} Hz")
    print(f"Frame Size: {frame_size} samples | Hop Size: {hop_size} samples")
    print(f"\nEnergy Statistics:")
    print(f"  Total Energy: {stats['total']:.6e}")
    print(f"  Mean Energy:  {stats['mean']:.6e}")
    print(f"  Median Energy: {stats['median']:.6e}")
    print(f"  Std Dev:      {stats['std']:.6e}")
    print(f"  Max Energy:   {stats['max']:.6e}")
    print(f"  Min Energy:   {stats['min']:.6e}")
    print(f"\nNumber of Frames: {len(frame_energies)}")
    
    # Calculate bitrate statistics
    unique_bitrates = set(bitrate_schedule)
    bitrate_dist = {br: bitrate_schedule.count(br) for br in sorted(unique_bitrates)}
    avg_bitrate = np.mean(bitrate_schedule)
    
    print(f"\nBitrate Distribution:")
    print(f"  Average Bitrate: {avg_bitrate:.2f} kbps")
    for bitrate in sorted(unique_bitrates):
        count = bitrate_dist[bitrate]
        percentage = (count / len(bitrate_schedule)) * 100
        print(f"  {bitrate:5.1f} kbps: {count:4d} frames ({percentage:5.1f}%)")
    
    print(f"\nFirst 10 Frames:")
    print(f"{'Frame':<6} {'Energy':<12} {'Norm.Energy':<12} {'Energy Level':<15} {'Bitrate':<10}")
    print("-" * 65)
    for i in range(min(10, len(frame_energies))):
        norm_energy = frame_energies[i] / max_energy if max_energy > 0 else 0
        print(f"{i:<6} {frame_energies[i]:<12.6e} {norm_energy:<12.4f} {energy_levels[i]:<15} {bitrate_schedule[i]:>5.1f} kbps")
    
    if len(frame_energies) > 10:
        print(f"... ({len(frame_energies) - 10} more frames)")
    
    print(f"{'='*70}\n")
    
    # Initialize model
    model = EncodecModel.encodec_model_24khz()
    model.eval()
    
    # Convert audio to model format
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    
    return wav, model, bitrate_schedule, stats, bandwidth_level, energy_levels

def encode_with_chunk_adaptive_bitrate(
    audio_path: str,
    bandwidth_mbps: float = 10.0,
    chunk_duration: float = 0.5,
    frame_size: int = 2048,
    hop_size: int = 512
):
    """
    Encode audio with frame-wise adaptive bitrate by processing chunks.
    
    Args:
        audio_path: Path to input audio file
        bandwidth_mbps: Available bandwidth in Mbps
        chunk_duration: Duration of each chunk in seconds
        frame_size: Frame size for energy calculation
        hop_size: Hop size for energy calculation
    """
    # Get frame-wise analysis
    wav, model, bitrate_schedule, stats, bandwidth_level, energy_levels = apply_frame_wise_adaptive_bitrate(
        audio_path, 
        bandwidth_mbps=bandwidth_mbps,
        frame_size=frame_size,
        hop_size=hop_size
    )
    
    # Get frame energies
    calculator = AudioEnergyCalculator(audio_path)
    frame_energies = calculator.frame_energy(frame_size=frame_size, hop_size=hop_size)
    
    # Load original audio for reference
    original_wav, sr = torchaudio.load(audio_path)
    original_wav = convert_audio(original_wav, sr, model.sample_rate, model.channels)
    
    # Calculate chunk size in samples
    chunk_samples = int(chunk_duration * model.sample_rate)
    num_chunks = int(np.ceil(wav.shape[1] / chunk_samples))
    
    print(f"\nCHUNK-WISE ENCODING PROCESS")
    print(f"{'='*70}")
    print(f"Chunk Duration: {chunk_duration} seconds")
    print(f"Chunk Size: {chunk_samples} samples")
    print(f"Total Chunks: {num_chunks}")
    print(f"{'='*70}\n")
    
    decoded_chunks = []
    chunk_stats = []
    
    # Process each chunk with adaptive bitrate
    for chunk_idx in range(num_chunks):
        start_sample = chunk_idx * chunk_samples
        end_sample = min((chunk_idx + 1) * chunk_samples, wav.shape[1])
        
        chunk = wav[:, start_sample:end_sample].unsqueeze(0)
        
        # Determine frames that belong to this chunk
        frame_start = start_sample // hop_size
        frame_end = (end_sample + hop_size - 1) // hop_size
        
        # Get average bitrate for frames in this chunk
        chunk_frame_bitrates = bitrate_schedule[frame_start:min(frame_end, len(bitrate_schedule))]
        avg_bitrate = np.mean(chunk_frame_bitrates) if chunk_frame_bitrates else 12.0
        
        # Get dominant energy level in chunk
        chunk_energies = energy_levels[frame_start:min(frame_end, len(energy_levels))]
        energy_counts = {}
        for e in chunk_energies:
            energy_counts[e] = energy_counts.get(e, 0) + 1
        dominant_energy = max(energy_counts, key=energy_counts.get) if energy_counts else 'medium_energy'
        
        # Encode chunk
        model.set_target_bandwidth(avg_bitrate)
        
        with torch.no_grad():
            encoded = model.encode(chunk)
            decoded_chunk = model.decode(encoded).squeeze(0)
        
        decoded_chunks.append(decoded_chunk.cpu())
        
        chunk_duration_sec = (end_sample - start_sample) / model.sample_rate
        print(f"Chunk {chunk_idx + 1}/{num_chunks}:")
        print(f"  Duration: {chunk_duration_sec:.3f}s ({start_sample}-{end_sample} samples)")
        print(f"  Frames: {frame_start}-{min(frame_end, len(bitrate_schedule))}")
        print(f"  Energy Level: {dominant_energy}")
        print(f"  Bitrate: {avg_bitrate:.2f} kbps (avg of {len(chunk_frame_bitrates)} frames)")
        
        chunk_stats.append({
            'chunk_idx': chunk_idx,
            'bitrate': avg_bitrate,
            'energy_level': dominant_energy,
            'duration': chunk_duration_sec
        })
    
    # Concatenate all decoded chunks
    decoded = torch.cat(decoded_chunks, dim=1)
    
    # Save output
    output_filename = f"reconstructed_framewise_{bandwidth_level}_{len(decoded[0])/model.sample_rate:.1f}s.wav"
    output_path = OUTPUT_DIR / output_filename
    
    sf.write(str(output_path), decoded.T.numpy(), model.sample_rate)
    
    print(f"\n{'='*70}")
    print(f"✓ Frame-wise adaptive encoding completed!")
    print(f"✓ Output saved to: {output_path}")
    print(f"✓ Total duration: {decoded.shape[1] / model.sample_rate:.2f}s")
    print(f"{'='*70}\n")
    
    # Save bitrate schedule to file
    schedule_filename = f"bitrate_schedule_{bandwidth_level}_{len(decoded[0])/model.sample_rate:.1f}s.txt"
    schedule_path = OUTPUT_DIR / schedule_filename
    
    with open(schedule_path, 'w') as f:
        f.write(f"Frame-wise Bitrate Schedule\n")
        f.write(f"Bandwidth: {bandwidth_mbps} Mbps ({bandwidth_level})\n")
        f.write(f"Frame Size: {frame_size} samples\n")
        f.write(f"Hop Size: {hop_size} samples\n")
        f.write(f"Total Frames: {len(bitrate_schedule)}\n")
        f.write(f"\n{'Frame':<6} {'Energy':<15} {'Norm.Energy':<12} {'Energy_Level':<15} {'Bitrate':<10}\n")
        f.write("-" * 70 + "\n")
        for i, (energy, bitrate, elevel) in enumerate(zip(frame_energies, bitrate_schedule, energy_levels)):
            norm_energy = energy / stats['max'] if stats['max'] > 0 else 0
            f.write(f"{i:<6} {energy:<15.6e} {norm_energy:<12.4f} {elevel:<15} {bitrate:>5.1f} kbps\n")
    
    print(f"✓ Bitrate schedule saved to: {schedule_path}\n")
    
    return decoded, chunk_stats

def main(bandwidth_mbps: float = 10.0):
    """
    Main function to encode/decode audio with frame-wise adaptive bitrate.
    
    Args:
        bandwidth_mbps: Available bandwidth in Mbps (default: 10 Mbps)
    """
    encode_with_chunk_adaptive_bitrate(
        str(INPUT),
        bandwidth_mbps=bandwidth_mbps,
        chunk_duration=0.5,
        frame_size=2048,
        hop_size=512
    )

if __name__ == "__main__":
    import sys
    
    # Use bandwidth from command line argument or default
    if len(sys.argv) > 1:
        try:
            bandwidth = float(sys.argv[1])
            print(f"Using bandwidth: {bandwidth} Mbps")
        except ValueError:
            print("Invalid bandwidth value. Using default 10 Mbps")
            bandwidth = 10.0
    else:
        bandwidth = 10.0
    
    main(bandwidth_mbps=bandwidth)