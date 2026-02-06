#!/usr/bin/env python3
# test_executable.py
# Test script to verify the executable works

import os
import sys
import subprocess
from pathlib import Path

def test_executable():
    """Test if the executable runs without errors"""
    current_dir = Path(__file__).parent
    exe_path = current_dir / "dist" / "FishingBotGUI.exe"
    
    if not exe_path.exists():
        print("[FAIL] Executable not found!")
        print(f"Expected location: {exe_path}")
        return False
    
    print(f"[OK] Executable found at: {exe_path}")
    print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    print("\nTesting executable startup...")
    print("This will start the GUI briefly to test for import errors.")
    print("Close the GUI window to complete the test.")
    
    try:
        # Run the executable with a timeout
        result = subprocess.run([str(exe_path)], 
                              timeout=10,  # 10 second timeout
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("[OK] Executable started successfully!")
            return True
        else:
            print(f"[FAIL] Executable failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[OK] Executable started successfully (timeout reached - GUI is running)")
        return True
    except Exception as e:
        print(f"[FAIL] Error running executable: {e}")
        return False

def main():
    """Main test function"""
    print("Fishing Bot GUI - Executable Test")
    print("=" * 40)
    
    if test_executable():
        print("\n[OK] All tests passed! The executable should work correctly.")
    else:
        print("\n[FAIL] Tests failed! Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
