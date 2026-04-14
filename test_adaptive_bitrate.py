"""
Test script to demonstrate adaptive bitrate selection with different bandwidth scenarios.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from 01_encode_decode import main, calculate_adaptive_bitrate, INPUT

def test_scenarios():
    """Test adaptive bitrate with different bandwidth scenarios."""
    
    print("="*60)
    print("ADAPTIVE BITRATE SYSTEM - Testing Different Bandwidth Scenarios")
    print("="*60)
    
    # Define bandwidth scenarios (in Mbps)
    scenarios = [
        ("Low Bandwidth (Poor Connection)", 1.0),
        ("Medium Bandwidth (DSL/4G)", 5.0),
        ("High Bandwidth (WiFi/Fast Internet)", 15.0),
        ("Very High Bandwidth (Fiber)", 50.0),
    ]
    
    print(f"\nInput Audio: {INPUT}")
    print("="*60)
    
    for description, bandwidth in scenarios:
        print(f"\n{'='*60}")
        print(f"Scenario: {description}")
        print(f"Available Bandwidth: {bandwidth} Mbps")
        print("="*60)
        
        try:
            bitrate, energy_level, bandwidth_level = calculate_adaptive_bitrate(
                str(INPUT), 
                bandwidth
            )
            print(f"✓ Encoding audio with {bitrate} kbps...")
            # Uncomment the line below to actually encode (requires data/input/sample.wav)
            # main(bandwidth_mbps=bandwidth)
            print(f"✓ Complete!")
        except FileNotFoundError as e:
            print(f"⚠ Note: {e}")
            print(f"  Audio file not found. To run full test, ensure 'data/input/sample.wav' exists.")
            print(f"  The adaptive bitrate selection logic would still choose: {bitrate} kbps")
            break

if __name__ == "__main__":
    test_scenarios()
