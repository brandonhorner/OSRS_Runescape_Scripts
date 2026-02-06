#!/usr/bin/env python3
# test_angler_bot.py
# Simple test script to verify the anglerfish bot can be imported and initialized

import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        print("  Importing screen_interactor...")
        from screen_interactor import ScreenInteractor
        print("    ✓ screen_interactor imported successfully")
        
        print("  Importing image_monitor...")
        from image_monitor import ImageMonitor
        print("    ✓ image_monitor imported successfully")
        
        print("  Importing pixel_monitor...")
        from pixel_monitor import PixelMonitor
        print("    ✓ pixel_monitor imported successfully")
        
        print("  Importing anglerfish bot...")
        from fish_anglers import AnglerfishBot
        print("    ✓ anglerfish bot imported successfully")
        
        print("\nAll imports successful!")
        return True
        
    except ImportError as e:
        print(f"    ✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"    ✗ Unexpected error: {e}")
        return False

def test_bot_initialization():
    """Test that the bot can be initialized without errors."""
    try:
        print("\nTesting bot initialization...")
        
        from fish_anglers import AnglerfishBot
        
        print("  Creating bot instance...")
        bot = AnglerfishBot()
        print("    ✓ Bot instance created successfully")
        
        print("  Checking bot attributes...")
        if hasattr(bot, 'si'):
            print("    ✓ ScreenInteractor instance exists")
        else:
            print("    ✗ ScreenInteractor instance missing")
            return False
            
        if hasattr(bot, 'state'):
            print("    ✓ State attribute exists")
        else:
            print("    ✗ State attribute missing")
            return False
            
        if hasattr(bot, 'loop_count'):
            print("    ✓ Loop count attribute exists")
        else:
            print("    ✗ Loop count attribute missing")
            return False
            
        if hasattr(bot, 'successful_trips'):
            print("    ✓ Successful trips attribute exists")
        else:
            print("    ✗ Successful trips attribute missing")
            return False
        
        print("\nBot initialization successful!")
        return True
        
    except Exception as e:
        print(f"    ✗ Bot initialization failed: {e}")
        return False

def test_method_existence():
    """Test that all required methods exist."""
    try:
        print("\nTesting method existence...")
        
        from fish_anglers import AnglerfishBot
        bot = AnglerfishBot()
        
        required_methods = [
            'setup',
            'assess_state',
            'handle_banking_state',
            'handle_walking_state',
            'handle_fishing_state',
            'find_image_right_click_confirm',
            'main_loop'
        ]
        
        for method_name in required_methods:
            if hasattr(bot, method_name):
                print(f"    ✓ Method '{method_name}' exists")
            else:
                print(f"    ✗ Method '{method_name}' missing")
                return False
        
        print("\nAll required methods exist!")
        return True
        
    except Exception as e:
        print(f"    ✗ Method existence test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Anglerfish Bot Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Bot Initialization Test", test_bot_initialization),
        ("Method Existence Test", test_method_existence)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  ✗ {test_name} FAILED")
    
    print(f"\n{'='*40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The anglerfish bot is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
