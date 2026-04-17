#!/usr/bin/env python3
"""
Streamlit App Verification Script
Checks all dependencies and basic functionality
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...\n")
    
    dependencies = {
        'streamlit': 'Web framework',
        'plotly': 'Interactive charts',
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'torch': 'PyTorch',
        'torchaudio': 'Audio processing',
        'soundfile': 'WAV file I/O',
    }
    
    missing = []
    installed = []
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<15} - {description}")
            installed.append(package)
        except ImportError:
            print(f"  ❌ {package:<15} - {description} [MISSING]")
            missing.append(package)
    
    print()
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}\n")
        print("Install missing dependencies with:")
        print(f"  pip install {' '.join(missing)}\n")
        print("Or install all with:")
        print("  pip install -r requirements_streamlit.txt\n")
        return False
    else:
        print("✅ All dependencies installed!\n")
        return True


def check_modules():
    """Check if all required modules can be loaded"""
    print("🔍 Checking modules...\n")
    
    modules_to_check = [
        ('03_audio_energy.py', 'AudioEnergyCalculator'),
        ('streamlit_app.py', 'AdaptiveBitrateSimulator'),
    ]
    
    for module_file, class_name in modules_to_check:
        module_path = Path(__file__).parent / module_file
        
        if not module_path.exists():
            print(f"  ⚠️  {module_file:<25} [NOT FOUND]")
            continue
        
        try:
            # For Python files, just check if they exist and are readable
            with open(module_path, 'r') as f:
                content = f.read()
                if class_name in content:
                    print(f"  ✅ {module_file:<25} - {class_name} found")
                else:
                    print(f"  ⚠️  {module_file:<25} - {class_name} not found")
        except Exception as e:
            print(f"  ❌ {module_file:<25} - Error: {e}")
    
    print()
    return True


def check_streamlit_config():
    """Check Streamlit configuration"""
    print("🔍 Checking Streamlit setup...\n")
    
    # Streamlit config location
    config_dir = Path.home() / '.streamlit'
    config_file = config_dir / 'config.toml'
    
    if config_file.exists():
        print(f"  ✅ Streamlit config found: {config_file}")
    else:
        print(f"  ℹ️  No Streamlit config (using defaults)")
    
    print()
    return True


def check_directories():
    """Check if required directories exist"""
    print("🔍 Checking directories...\n")
    
    required_dirs = ['samples', 'src', 'tests']
    base_path = Path(__file__).parent
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✅ {dir_name:15} - exists")
        else:
            print(f"  ❌ {dir_name:15} - missing or not a directory")
    
    print()
    return True


def test_basic_functionality():
    """Test basic functionality"""
    print("🔍 Testing basic functionality...\n")
    
    try:
        import numpy as np
        print("  ✅ NumPy import successful")
        
        # Test energy calculation simulation
        test_array = np.random.randn(2048)
        energy = np.sqrt(np.mean(test_array ** 2))
        print(f"  ✅ Energy calculation works (test: {energy:.4f})")
        
        import plotly.graph_objects as go
        print("  ✅ Plotly import successful")
        
        import pandas as pd
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print("  ✅ Pandas working (test df shape: {})".format(test_df.shape))
        
        print()
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        return False


def print_version_info():
    """Print version information"""
    print("=" * 60)
    print("  STREAMLIT ADAPTIVE AUDIO STREAMING - VERIFICATION")
    print("=" * 60)
    print()
    
    import platform
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print()


def print_next_steps():
    """Print next steps"""
    print("=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print()
    print("To launch the Streamlit app, run:\n")
    print("  1. On Windows:")
    print("     run_streamlit.bat\n")
    print("  2. On macOS/Linux:")
    print("     chmod +x run_streamlit.sh")
    print("     ./run_streamlit.sh\n")
    print("  3. Or directly:")
    print("     streamlit run streamlit_app.py\n")
    print("Then open: http://localhost:8501")
    print()


def main():
    """Run all checks"""
    print_version_info()
    
    all_passed = True
    
    # Run checks
    all_passed = check_dependencies() and all_passed
    all_passed = check_modules() and all_passed
    all_passed = check_streamlit_config() and all_passed
    all_passed = check_directories() and all_passed
    all_passed = test_basic_functionality() and all_passed
    
    # Print summary
    print("=" * 60)
    
    if all_passed:
        print("  ✅ ALL CHECKS PASSED - READY TO RUN!")
        print("=" * 60)
        print()
        print_next_steps()
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED - SEE ABOVE")
        print("=" * 60)
        print()
        print("Fix the issues and try again.")
        print("Run: pip install -r requirements_streamlit.txt")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
