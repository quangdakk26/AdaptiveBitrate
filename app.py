"""
Flask web application for Adaptive Bitrate Audio Encoding System
Displays energy analysis, bitrate adaptation, and encoding metrics
"""

from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import json
import numpy as np
import torch
import torchaudio
import soundfile as sf
from encodec import EncodecModel
from encodec.utils import convert_audio
import importlib.util

# Import modules
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load AudioEnergyCalculator from 03_audio_energy.py
spec = importlib.util.spec_from_file_location("audio_energy", Path(__file__).parent / "03_audio_energy.py")
audio_energy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_energy_module)
AudioEnergyCalculator = audio_energy_module.AudioEnergyCalculator

# Load metrics
from metrics import snr_db, mse, compression_ratio

# Configuration
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BITRATE_CONFIG = {
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

def get_energy_level(mean_energy, max_energy):
    """Categorize energy level."""
    if mean_energy > max_energy * 0.6:
        return 'high_energy'
    elif mean_energy > max_energy * 0.3:
        return 'medium_energy'
    else:
        return 'low_energy'

def get_bandwidth_level(bandwidth_mbps):
    """Categorize bandwidth level."""
    if bandwidth_mbps >= 10:
        return 'high_bandwidth'
    elif bandwidth_mbps >= 3:
        return 'medium_bandwidth'
    else:
        return 'low_bandwidth'

def get_available_files():
    """Get list of available audio files."""
    if not INPUT_DIR.exists():
        return []
    return [f.name for f in INPUT_DIR.glob("*.wav")]

@app.route('/')
def index():
    """Main page."""
    files = get_available_files()
    return render_template('index.html', audio_files=files)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze audio file and return energy metrics."""
    try:
        data = request.json
        filename = data.get('filename', '')
        bandwidth = float(data.get('bandwidth', 10.0))
        
        audio_path = INPUT_DIR / filename
        
        if not audio_path.exists():
            return jsonify({'error': f'File not found: {filename}'}), 404
        
        # Calculate energy
        calculator = AudioEnergyCalculator(str(audio_path))
        frame_energies = calculator.frame_energy()
        stats = calculator.energy_statistics(frame_energies)
        
        # Get bitrate
        mean_energy = stats['mean']
        max_energy = stats['max']
        energy_level = get_energy_level(mean_energy, max_energy)
        bandwidth_level = get_bandwidth_level(bandwidth)
        bitrate = BITRATE_CONFIG[bandwidth_level][energy_level]
        
        # Prepare response
        response = {
            'filename': filename,
            'bandwidth_mbps': bandwidth,
            'energy_level': energy_level,
            'bandwidth_level': bandwidth_level,
            'selected_bitrate': bitrate,
            'energy_stats': {
                'mean': float(stats['mean']),
                'max': float(stats['max']),
                'min': float(stats['min']),
                'std': float(stats['std']),
                'median': float(stats['median']),
                'total': float(stats['total'])
            },
            'frame_energies': frame_energies.tolist(),
            'total_frames': len(frame_energies),
            'sample_rate': calculator.sr,
            'duration': calculator.audio.shape[-1] / calculator.sr
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/framewise-adaptive', methods=['POST'])
def framewise_adaptive():
    """Calculate frame-wise adaptive bitrate."""
    try:
        data = request.json
        filename = data.get('filename', '')
        bandwidth = float(data.get('bandwidth', 10.0))
        frame_size = int(data.get('frame_size', 2048))
        hop_size = int(data.get('hop_size', 512))
        
        audio_path = INPUT_DIR / filename
        if not audio_path.exists():
            return jsonify({'error': f'File not found: {filename}'}), 404
        
        # Calculate energy
        calculator = AudioEnergyCalculator(str(audio_path))
        frame_energies = calculator.frame_energy(frame_size, hop_size)
        stats = calculator.energy_statistics(frame_energies)
        
        max_energy = stats['max']
        bandwidth_level = get_bandwidth_level(bandwidth)
        
        # Calculate adaptive bitrate for each frame
        framewise_bitrates = []
        framewise_energy_levels = []
        
        for energy in frame_energies:
            # Normalize to 0-1 range
            normalized = energy / max_energy if max_energy > 0 else 0
            
            # Determine energy level for this frame
            if normalized > 0.6:
                energy_level = 'high_energy'
            elif normalized > 0.3:
                energy_level = 'medium_energy'
            else:
                energy_level = 'low_energy'
            
            framewise_energy_levels.append(energy_level)
            bitrate = BITRATE_CONFIG[bandwidth_level][energy_level]
            framewise_bitrates.append(bitrate)
        
        response = {
            'filename': filename,
            'bandwidth_mbps': bandwidth,
            'bandwidth_level': bandwidth_level,
            'frame_size': frame_size,
            'hop_size': hop_size,
            'total_frames': len(frame_energies),
            'frame_energies': frame_energies.tolist(),
            'framewise_bitrates': framewise_bitrates,
            'framewise_energy_levels': framewise_energy_levels,
            'average_bitrate': float(np.mean(framewise_bitrates)),
            'bitrate_stats': {
                'min': float(np.min(framewise_bitrates)),
                'max': float(np.max(framewise_bitrates)),
                'mean': float(np.mean(framewise_bitrates)),
                'std': float(np.std(framewise_bitrates))
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/encode', methods=['POST'])
def encode():
    """Encode and decode audio with adaptive bitrate."""
    try:
        data = request.json
        filename = data.get('filename', '')
        bandwidth = float(data.get('bandwidth', 10.0))
        use_framewise = data.get('use_framewise', False)
        
        audio_path = INPUT_DIR / filename
        if not audio_path.exists():
            return jsonify({'error': f'File not found: {filename}'}), 404
        
        # Load audio
        wav, sr = torchaudio.load(str(audio_path))
        original = wav.numpy()
        
        # Initialize model
        model = EncodecModel.encodec_model_24khz()
        model.eval()
        
        # Apply adaptive bitrate
        calculator = AudioEnergyCalculator(str(audio_path))
        frame_energies = calculator.frame_energy()
        stats = calculator.energy_statistics(frame_energies)
        
        energy_level = get_energy_level(stats['mean'], stats['max'])
        bandwidth_level = get_bandwidth_level(bandwidth)
        bitrate = BITRATE_CONFIG[bandwidth_level][energy_level]
        
        model.set_target_bandwidth(bitrate)
        
        # Convert and encode
        wav = convert_audio(wav, sr, model.sample_rate, model.channels)
        wav = wav.unsqueeze(0)
        
        with torch.no_grad():
            encoded = model.encode(wav)
            decoded = model.decode(encoded)
        
        decoded_audio = decoded.squeeze(0).cpu().numpy()
        
        # Calculate metrics
        original_flat = original.flatten()
        decoded_flat = decoded_audio.flatten()
        
        mse_val = mse(original_flat, decoded_flat)
        snr_val = snr_db(original_flat, decoded_flat)
        
        original_bits = original.size * 16
        compressed_bits = bitrate * 1000 * (original.shape[-1] / sr)
        cr = compression_ratio(original_bits, compressed_bits)
        
        # Save output
        output_filename = f"encoded_{bandwidth_level}_{energy_level}_{bitrate}kbps.wav"
        output_path = OUTPUT_DIR / output_filename
        sf.write(str(output_path), decoded_audio.T, model.sample_rate)
        
        response = {
            'filename': filename,
            'bandwidth_mbps': bandwidth,
            'energy_level': energy_level,
            'bandwidth_level': bandwidth_level,
            'selected_bitrate': bitrate,
            'output_filename': output_filename,
            'metrics': {
                'mse': float(mse_val),
                'snr_db': float(snr_val),
                'compression_ratio': float(cr),
                'original_bits': int(original_bits),
                'compressed_bits': int(compressed_bits),
                'duration': float(original.shape[-1] / sr)
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenarios', methods=['GET'])
def scenarios():
    """Get predefined bandwidth scenarios."""
    scenarios_data = [
        {
            'name': 'Satellite/Low Mobile',
            'bandwidth': 1.0,
            'description': 'Very poor connection'
        },
        {
            'name': 'Mobile 3G',
            'bandwidth': 2.0,
            'description': 'Poor mobile connection'
        },
        {
            'name': 'Mobile 4G LTE',
            'bandwidth': 5.0,
            'description': 'Good mobile connection'
        },
        {
            'name': 'DSL/WiFi Home',
            'bandwidth': 10.0,
            'description': 'Average home broadband'
        },
        {
            'name': 'Fast WiFi/Fiber',
            'bandwidth': 25.0,
            'description': 'High-speed connection'
        },
        {
            'name': 'Gigabit Fiber',
            'bandwidth': 100.0,
            'description': 'Premium connection'
        }
    ]
    return jsonify(scenarios_data)

@app.route('/api/bitrate-config', methods=['GET'])
def bitrate_config():
    """Get bitrate configuration matrix."""
    return jsonify(BITRATE_CONFIG)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
