"""
Demonstration script for frame-wise adaptive bitrate system.
Tests different bandwidth scenarios and shows frame-wise bitrate assignment.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from 01_encode_decode import (
    apply_frame_wise_adaptive_bitrate, 
    categorize_bandwidth,
    INPUT
)
import numpy as np

def analyze_frame_distribution(bitrate_schedule, energy_levels):
    """Analyze and display frame distribution statistics."""
    unique_bitrates = sorted(set(bitrate_schedule))
    unique_energies = sorted(set(energy_levels))
    
    print("\n" + "="*70)
    print("FRAME DISTRIBUTION ANALYSIS")
    print("="*70)
    
    # Bitrate distribution
    print("\nBitrate Distribution:")
    for bitrate in unique_bitrates:
        count = bitrate_schedule.count(bitrate)
        percentage = (count / len(bitrate_schedule)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {bitrate:5.1f} kbps: {count:4d} frames ({percentage:5.1f}%) {bar}")
    
    # Energy distribution
    print("\nEnergy Level Distribution:")
    energy_order = ['low_energy', 'medium_energy', 'high_energy']
    for energy in energy_order:
        if energy in unique_energies:
            count = energy_levels.count(energy)
            percentage = (count / len(energy_levels)) * 100
            bar = "▓" * int(percentage / 2)
            print(f"  {energy:<15}: {count:4d} frames ({percentage:5.1f}%) {bar}")
    
    # Statistics
    print("\nBitrate Statistics:")
    print(f"  Average: {np.mean(bitrate_schedule):.2f} kbps")
    print(f"  Median:  {np.median(bitrate_schedule):.2f} kbps")
    print(f"  Min:     {np.min(bitrate_schedule):.2f} kbps")
    print(f"  Max:     {np.max(bitrate_schedule):.2f} kbps")
    print(f"  Std Dev: {np.std(bitrate_schedule):.2f} kbps")
    
    print("="*70)

def test_single_scenario(description: str, bandwidth: float):
    """Test a single bandwidth scenario."""
    print(f"\n{'='*70}")
    print(f"SCENARIO: {description}")
    print(f"{'='*70}")
    print(f"Bandwidth: {bandwidth} Mbps")
    print(f"Bandwidth Level: {categorize_bandwidth(bandwidth)}")
    
    try:
        wav, model, bitrate_schedule, stats, bandwidth_level, energy_levels = apply_frame_wise_adaptive_bitrate(
            str(INPUT),
            bandwidth_mbps=bandwidth,
            frame_size=2048,
            hop_size=512
        )
        
        # Analyze distribution
        analyze_frame_distribution(bitrate_schedule, energy_levels)
        
        print(f"\n✓ Frame-wise analysis complete for {description}")
        return True
    
    except FileNotFoundError as e:
        print(f"\n⚠ Note: {e}")
        print(f"To run full test, ensure 'data/input/sample.wav' exists.")
        print(f"The frame-wise analysis would be available once audio file is present.")
        return False

def main():
    """Run demonstration of frame-wise adaptive bitrate system."""
    
    print("\n" + "="*70)
    print("FRAME-WISE ADAPTIVE BITRATE SYSTEM - DEMONSTRATION")
    print("="*70)
    print(f"Input Audio: {INPUT}")
    
    # Define test scenarios
    scenarios = [
        ("Satellite/Low Bandwidth (1 Mbps)", 1.0),
        ("Rural/Mobile (2 Mbps)", 2.0),
        ("4G LTE (5 Mbps)", 5.0),
        ("DSL/Cable (10 Mbps)", 10.0),
        ("WiFi/Fiber (25 Mbps)", 25.0),
        ("High-Speed Fiber (50 Mbps)", 50.0),
    ]
    
    success_count = 0
    failed_once = False
    
    for description, bandwidth in scenarios:
        success = test_single_scenario(description, bandwidth)
        if success:
            success_count += 1
        elif not failed_once:
            failed_once = True
            print("\n" + "!"*70)
            print("To run the full frame-wise encoding:")
            print("1. Place an audio file at: data/input/sample.wav")
            print("2. Run: python 01_encode_decode.py <bandwidth_mbps>")
            print("3. Output will be saved to: data/output/")
            print("!"*70)
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print(f"\nSuccessfully analyzed: {success_count}/{len(scenarios)} scenarios")
    print("\nNext Steps:")
    print("1. Review the frame-wise analysis output above")
    print("2. Notice how bitrate distribution varies with bandwidth")
    print("3. Run full encoding with: python 01_encode_decode.py <bandwidth>")
    print("4. Check 'data/output/' for encoded audio and schedule files")
    print("\nFor more information, see FRAME_WISE_ADAPTIVE_README.md")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
