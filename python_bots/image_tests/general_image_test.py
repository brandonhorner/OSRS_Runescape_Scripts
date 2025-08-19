# general_image_test.py
import time
import pyautogui
import cv2
import numpy as np
import os
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_interactor import ScreenInteractor

# Set working directory to the folder containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory set to: {os.getcwd()}")

def general_image_test(image_path, region_name=None, confidence=0.95, show_visual=True):
    """General test to see exactly what the bot is seeing for any image search.
    
    Args:
        image_path: Path to the image file to test
        region_name: Name of the region to search in (e.g., "p3", "game_screen", "bag")
        confidence: Confidence threshold for image matching
        show_visual: Whether to show visual feedback (mouse movement, screenshots)
    """
    print(f"General Image Search Test")
    print("=" * 50)
    print(f"Image: {image_path}")
    print(f"Region: {region_name if region_name else 'Full screen'}")
    print(f"Confidence: {confidence}")
    
    # Create screen interactor
    si = ScreenInteractor()
    
    # Wait for user to get ready
    print("\nStarting in 3 seconds...")
    print("Please make sure the target image is visible on screen")
    time.sleep(3)
    
    # Get region coordinates
    if region_name:
        try:
            region = si.get_scan_area(region_name)
            print(f"Region '{region_name}' coordinates: {region}")
        except Exception as e:
            print(f"Error getting region '{region_name}': {e}")
            print("Falling back to full screen search")
            region = None
    else:
        region = None
        print("Searching full screen")
    
    # Take screenshot of search area
    if region:
        print(f"\nTaking screenshot of region {region}...")
        try:
            screenshot = pyautogui.screenshot(region=region)
            screenshot_filename = f"region_{region_name}_screenshot.png"
            screenshot.save(screenshot_filename)
            print(f"Screenshot saved as '{screenshot_filename}'")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return
    else:
        print("\nTaking full screen screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot_filename = "full_screen_screenshot.png"
        screenshot.save(screenshot_filename)
        print(f"Screenshot saved as '{screenshot_filename}'")
    
    # Check if image file exists
    import os
    if not os.path.exists(image_path):
        print(f"\n✗ ERROR: Image file not found: {image_path}")
        print("Please check the file path and try again")
        return
    
    print(f"\n✓ Image file found: {image_path}")
    
    # Load template image
    template = cv2.imread(image_path)
    if template is None:
        print(f"✗ ERROR: Failed to load image with cv2.imread")
        return
    
    print(f"Template size: {template.shape}")
    
    # Convert screenshot to CV2 format
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    print(f"Screenshot size: {screenshot_cv.shape}")
    
    # Test different confidence levels (highest to lowest)
    print(f"\nTesting image detection at different confidence levels...")
    
    best_match = None
    best_confidence = 0
    all_matches = []  # Collect all matches for later mouse movement
    
    for test_confidence in [1.0, 0.98, 0.95, 0.9, 0.85, 0.8, 0.7]:
        print(f"\n--- Confidence {test_confidence} ---")
        
        try:
            # Use CV2 template matching
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            print(f"Max match value: {max_val:.4f}")
            
            if max_val >= test_confidence:
                # Calculate center point
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                # Convert to screen coordinates if using region
                if region:
                    screen_x = region[0] + center_x
                    screen_y = region[1] + center_y
                else:
                    screen_x = center_x
                    screen_y = center_y
                
                print(f"  ✓ FOUND at screen coordinates: ({screen_x}, {screen_y})")
                print(f"  ✓ Relative to search area: ({center_x}, {center_y})")
                print(f"  ✓ Match location: {max_loc}")
                
                # Track best match
                if max_val > best_confidence:
                    best_confidence = max_val
                    best_match = (screen_x, screen_y, max_val)
                
                # Collect match info for later mouse movement
                match_info = {
                    'confidence': test_confidence,
                    'screen_coords': (screen_x, screen_y),
                    'relative_coords': (center_x, center_y),
                    'match_location': max_loc,
                    'match_value': max_val
                }
                all_matches.append(match_info)
                    
            else:
                print(f"  ✗ Below threshold")
                
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
    
    # Test the ScreenInteractor's find_image_cv2 method
    print(f"\n--- Testing ScreenInteractor.find_image_cv2() ---")
    try:
        si_result = si.find_image_cv2(image_path, region=region, threshold=confidence)
        if si_result:
            print(f"✓ ScreenInteractor found image at: {si_result}")
        else:
            print(f"✗ ScreenInteractor did not find image at confidence {confidence}")
    except Exception as e:
        print(f"✗ ScreenInteractor error: {e}")
    
    # Visual feedback - move mouse to all found locations after detection is complete
    if show_visual and all_matches:
        print(f"\n--- Visual Feedback - Moving Mouse to All Found Locations ---")
        print(f"Found {len(all_matches)} matches, moving mouse to each location...")
        
        for i, match in enumerate(all_matches):
            print(f"  {i+1}/{len(all_matches)}: Moving to confidence {match['confidence']:.2f} at {match['screen_coords']}")
            pyautogui.moveTo(match['screen_coords'][0], match['screen_coords'][1])
            time.sleep(0.5)  # Brief pause to show each location
        
        # Move mouse back to center
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)
        print("Mouse moved back to screen center")
    
    # Now add visual annotations to the screenshot (after all detection is complete)
    # Only draw the highest confidence match to avoid clutter
    if all_matches:
        print(f"\n--- Adding Visual Annotations to Screenshot ---")
        
        # Find the highest confidence match
        best_match_for_drawing = max(all_matches, key=lambda x: x['confidence'])
        
        # Get template dimensions for rectangle drawing
        h, w = template.shape[:2]
        max_loc = best_match_for_drawing['match_location']
        
        # Draw rectangle on screenshot for visualization (only the best match)
        cv2.rectangle(screenshot_cv, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
        cv2.putText(screenshot_cv, f"Best Match: Conf:{best_match_for_drawing['confidence']:.2f}", 
                   (max_loc[0], max_loc[1] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        print(f"  Added annotation for best match: confidence {best_match_for_drawing['confidence']:.2f} at {best_match_for_drawing['screen_coords']}")
    
    # Save annotated screenshot
    if best_match:
        annotated_filename = f"annotated_{os.path.basename(image_path).replace('.png', '')}.png"
        cv2.imwrite(annotated_filename, screenshot_cv)
        print(f"\nAnnotated screenshot saved as '{annotated_filename}'")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("Test Summary:")
    print(f"Image: {image_path}")
    print(f"Region: {region_name if region_name else 'Full screen'}")
    print(f"Total matches found: {len(all_matches)}")
    
    if all_matches:
        print(f"All matches (confidence level → coordinates):")
        for match in all_matches:
            print(f"  {match['confidence']:.2f} → ({match['screen_coords'][0]}, {match['screen_coords'][1]}) - value: {match['match_value']:.4f}")
        
        if best_match:
            print(f"\nBest match: {best_match[0]}, {best_match[1]} (confidence: {best_match[2]:.4f})")
    else:
        print("No matches found above any confidence threshold")
    
    print(f"\nFiles saved:")
    print(f"  - {screenshot_filename}")
    if best_match:
        print(f"  - {annotated_filename}")

def main():
    """Main function to run the general image test."""
    print("General Image Search Test")
    print("=" * 50)
    print("This script tests image detection for any image in any region.")
    print("It will show you exactly what the bot is seeing and where it finds matches.")
    
    # Get user input
    image_name = input("\nEnter image name (e.g., 'world_map.png'): ").strip()
    if not image_name:
        print("No image name provided. Exiting.")
        return
    
    # Automatically prepend image_library/ path
    image_path = f"image_library/{image_name}"
    print(f"Full image path: {image_path}")
    
    region_name = input("Enter region name (e.g., 'p3', 'game_screen', 'bag') or press Enter for full screen: ").strip()
    if not region_name:
        region_name = None
    
    confidence_input = input("Enter confidence threshold (0.7-1.0, default 0.95): ").strip()
    try:
        confidence = float(confidence_input) if confidence_input else 0.95
        if not (0.7 <= confidence <= 1.0):
            print("Confidence must be between 0.7 and 1.0. Using default 0.95.")
            confidence = 0.95
    except ValueError:
        print("Invalid confidence value. Using default 0.95.")
        confidence = 0.95
    
    show_visual = input("Show visual feedback (mouse movement)? (y/n, default y): ").strip().lower()
    show_visual = show_visual != 'n'
    
    # Run the test
    general_image_test(image_path, region_name, confidence, show_visual)

if __name__ == "__main__":
    main()
