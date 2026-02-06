#!/usr/bin/env python3
# run_gui.py
# Simple script to run the fishing bot GUI

import sys
import os
import subprocess

def main():
    """Run the fishing bot GUI"""
    print("Starting Fishing Bot GUI...")
    
    # Check if we're in the right directory
    if not os.path.exists("fishing_bot_gui.py"):
        print("Error: fishing_bot_gui.py not found in current directory")
        print("Please run this script from the fishing_bots directory")
        return
    
    # Check if virtual environment is activated
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment detected ✓")
    else:
        print("Warning: Virtual environment not detected")
        print("Consider running: python activate_venv.bat")
    
    # Install requirements if needed
    try:
        import tkinter
        import pyautogui
        import cv2
        print("Required packages found ✓")
    except ImportError as e:
        print(f"Missing package: {e}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"])
    
    # Run the GUI
    try:
        from fishing_bot_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure all dependencies are installed and the image_library exists")

if __name__ == "__main__":
    main()
