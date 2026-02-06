#!/usr/bin/env python3
# rebuild_clean.py
# Clean and rebuild the executable

import os
import sys
import shutil
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    current_dir = Path(__file__).parent
    
    # Directories to clean
    dirs_to_clean = ['dist', 'build', '__pycache__']
    
    for dir_name in dirs_to_clean:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_path)
            print(f"[OK] Removed {dir_name}")
    
    # Clean .pyc files
    for pyc_file in current_dir.rglob("*.pyc"):
        pyc_file.unlink()
        print(f"[OK] Removed {pyc_file}")
    
    print("[OK] Clean completed!")

def main():
    """Main function"""
    print("Fishing Bot GUI - Clean and Rebuild")
    print("=" * 40)
    
    # Clean
    clean_build()
    
    # Rebuild
    print("\nRebuilding executable...")
    import subprocess
    
    try:
        result = subprocess.run([sys.executable, "build_executable.py"], 
                              check=True, capture_output=True, text=True)
        print("[OK] Rebuild completed successfully!")
        
        # Test the executable
        print("\nTesting executable...")
        test_result = subprocess.run([sys.executable, "test_executable.py"], 
                                   capture_output=True, text=True)
        if test_result.returncode == 0:
            print("[OK] Executable test passed!")
        else:
            print("[WARN] Executable test failed, but executable was built")
            print(f"Test output: {test_result.stdout}")
            if test_result.stderr:
                print(f"Test errors: {test_result.stderr}")
        
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Rebuild failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return 1
    
    print("\n[OK] Clean and rebuild completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
