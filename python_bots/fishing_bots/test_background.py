#!/usr/bin/env python3
# test_background.py
# Test script to check background image loading

import os
import sys
from pathlib import Path

def test_background_paths():
    """Test all possible background image paths"""
    print("Testing background image paths...")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    # Test paths
    possible_paths = [
        "../image_library/UI_backgrounds/studio-gbli-1.png",  # Development path
        "image_library/UI_backgrounds/studio-gbli-1.png",     # Executable path
        os.path.join(current_dir, "..", "image_library", "UI_backgrounds", "studio-gbli-1.png"),
        os.path.join(current_dir, "image_library", "UI_backgrounds", "studio-gbli-1.png"),
        os.path.join(parent_dir, "image_library", "UI_backgrounds", "studio-gbli-1.png")
    ]
    
    found_paths = []
    for i, path in enumerate(possible_paths):
        exists = os.path.exists(path)
        print(f"{i+1}. {path}")
        print(f"   EXISTS: {exists}")
        if exists:
            found_paths.append(path)
            # Check if it's a file and get size
            if os.path.isfile(path):
                size = os.path.getsize(path)
                print(f"   SIZE: {size:,} bytes ({size/1024:.1f} KB)")
            else:
                print(f"   TYPE: Directory (not a file)")
        print()
    
    if found_paths:
        print(f"✅ Found {len(found_paths)} valid path(s):")
        for path in found_paths:
            print(f"   - {path}")
    else:
        print("❌ No valid background image paths found!")
        print("\nTrying to find UI_backgrounds directory...")
        
        # Search for UI_backgrounds directory
        search_dirs = [
            current_dir,
            parent_dir,
            os.path.join(current_dir, "image_library"),
            os.path.join(parent_dir, "image_library")
        ]
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                print(f"Searching in: {search_dir}")
                for root, dirs, files in os.walk(search_dir):
                    if "UI_backgrounds" in dirs:
                        ui_bg_path = os.path.join(root, "UI_backgrounds")
                        print(f"  Found UI_backgrounds at: {ui_bg_path}")
                        # List contents
                        try:
                            contents = os.listdir(ui_bg_path)
                            print(f"  Contents: {contents}")
                        except Exception as e:
                            print(f"  Error listing contents: {e}")
                    if "studio-gbli-1.png" in files:
                        full_path = os.path.join(root, "studio-gbli-1.png")
                        print(f"  Found studio-gbli-1.png at: {full_path}")
    
    return len(found_paths) > 0

def main():
    """Main function"""
    print("Background Image Path Test")
    print("=" * 50)
    
    success = test_background_paths()
    
    if success:
        print("\n✅ Background image should work!")
    else:
        print("\n❌ Background image will not work - check paths above")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
