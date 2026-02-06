#!/usr/bin/env python3
# test_gui.py
# Simple test script to verify the GUI can be imported and started

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import PyQt6
        print("✓ PyQt6 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        return False
    
    try:
        import pyautogui
        print("✓ pyautogui imported successfully")
    except ImportError as e:
        print(f"✗ pyautogui import failed: {e}")
        return False
    
    try:
        import cv2
        print("✓ opencv imported successfully")
    except ImportError as e:
        print(f"✗ opencv import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL imported successfully")
    except ImportError as e:
        print(f"✗ PIL import failed: {e}")
        return False
    
    return True

def test_gui_import():
    """Test that the GUI can be imported"""
    print("\nTesting GUI import...")
    
    try:
        from fishing_bot_gui import FishingBotGUI
        print("✓ FishingBotGUI imported successfully")
        return True
    except ImportError as e:
        print(f"✗ FishingBotGUI import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing GUI: {e}")
        return False

def test_bot_import():
    """Test that the bot can be imported"""
    print("\nTesting bot import...")
    
    try:
        from fish_anglers import AnglerfishBot
        print("✓ AnglerfishBot imported successfully")
        return True
    except ImportError as e:
        print(f"✗ AnglerfishBot import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing bot: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "fishing_bot_gui.py",
        "fish_anglers.py",
        "requirements_gui.txt",
        "build_executable.py",
        "run_gui.py"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    # Check for image library
    image_lib_path = "../image_library"
    if os.path.exists(image_lib_path):
        print(f"✓ {image_lib_path} exists")
    else:
        print(f"✗ {image_lib_path} missing")
        all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("Fishing Bot GUI - Test Script")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Bot Import", test_bot_import),
        ("GUI Import", test_gui_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            print(f"✓ {test_name} passed")
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'='*40}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! GUI should work correctly.")
        print("\nTo run the GUI:")
        print("  python run_gui.py")
        print("\nTo build executable:")
        print("  python build_executable.py")
    else:
        print("✗ Some tests failed. Please fix the issues before running the GUI.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements_gui.txt")

if __name__ == "__main__":
    main()
