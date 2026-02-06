#!/usr/bin/env python3
# build_executable.py
# Script to build executable for the fishing bot GUI

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller with command line arguments"""
    print("Building Fishing Bot GUI executable...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    try:
        # Change to the fishing_bots directory
        os.chdir(current_dir)
        
        # PyInstaller command with all necessary arguments
        cmd = [
            "pyinstaller",
            "--onefile",  # Create a single executable file
            "--windowed",  # Don't show console window
            "--name=FishingBotGUI",
            f"--add-data={parent_dir / 'image_library'};image_library",  # Include image library
            f"--add-data={parent_dir / 'logs'};logs",  # Include logs directory
            f"--paths={parent_dir}",  # Add parent directory to Python path
            "--hidden-import=screen_interactor",
            "--hidden-import=image_monitor", 
            "--hidden-import=pixel_monitor",
            "--hidden-import=fish_anglers",
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=pyautogui",
            "--hidden-import=cv2",
            "--hidden-import=numpy",
            "--hidden-import=PIL",
            "--hidden-import=PIL.Image",
            "--hidden-import=PIL.ImageTk",
            "fishing_bot_gui.py"
        ]
        
        # Run PyInstaller
        print("Running PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Build successful!")
        print(f"Executable created in: {current_dir / 'dist' / 'FishingBotGUI.exe'}")
        
        # Verify the executable was created
        exe_path = current_dir / "dist" / "FishingBotGUI.exe"
        if exe_path.exists():
            print(f"[OK] Executable found at: {exe_path}")
            print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            print("[FAIL] Executable not found!")
            return False
        
        print("\nBuild complete! You can find the executable in the 'dist' folder.")
        print("The executable should now work without additional setup.")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"], check=True)
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False

if __name__ == "__main__":
    print("Fishing Bot GUI Builder")
    print("=" * 30)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("PyInstaller not found. Installing requirements...")
        if not install_requirements():
            print("Failed to install requirements. Please install manually:")
            print("pip install -r requirements_gui.txt")
            sys.exit(1)
    
    # Build the executable
    if build_executable():
        print("\n✅ Build completed successfully!")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)
