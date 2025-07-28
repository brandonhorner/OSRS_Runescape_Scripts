import time
import random
import pyautogui
from screen_interactor import ScreenInteractor

def test_mining_inactive(si):
    """Test function to check if mining inactive image can be found"""
    print("Testing mining inactive image detection...")
    
    # Try to find the image with different thresholds
    thresholds = [1, .99, .97, .95, .93]
    for threshold in thresholds:
        print(f"\nTrying threshold: {threshold}")
        mining_inactive_location = si.find_image_cv2('python_bots/image_library/mining_inactive.png', threshold=threshold)
        
        if mining_inactive_location:
            print(f"Found mining inactive image at {mining_inactive_location} with threshold {threshold}")
            
            # Take a screenshot of the area around the found location
            x, y = mining_inactive_location
            region = (max(0, x-50), max(0, y-50), 100, 100)
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(f'mining_inactive_test_{threshold}.png')
            print(f"Saved test screenshot to 'mining_inactive_test_{threshold}.png'")
            
            # Also take a screenshot of the entire game screen
            game_region = si.get_scan_area("game_screen")
            full_screenshot = pyautogui.screenshot(region=game_region)
            full_screenshot.save('mining_inactive_full_screen.png')
            print("Saved full game screen screenshot to 'mining_inactive_full_screen.png'")
            
            return True
        
        mining_active_location = si.find_image_cv2('python_bots/image_library/mining_active.png', threshold=threshold)
        if mining_active_location:
            print(f"Found mining active image at {mining_active_location} with threshold {threshold}")
            
            # Take a screenshot of the area around the found location
            x, y = mining_active_location
            region = (max(0, x-50), max(0, y-50), 100, 100)
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(f'mining_active_test_{threshold}.png')
            print(f"Saved test screenshot to 'mining_active_test_{threshold}.png'")
            
            # Also take a screenshot of the entire game screen
            game_region = si.get_scan_area("game_screen")
            full_screenshot = pyautogui.screenshot(region=game_region)
            full_screenshot.save('mining_active_full_screen.png')
            print("Saved full game screen screenshot to 'mining_active_full_screen.png'")
            
            return True

        else:
            print(f"Could not find mining inactive image with threshold {threshold}")
    
    return False

def main():
    # Create the screen interactor
    si = ScreenInteractor()
    print("Starting mining active/inactive image seconds...")
    
    # Run the test
    test_mining_inactive(si)
    
    print("\nTest complete. Check the saved screenshots to see what the bot is seeing.")

if __name__ == "__main__":
    main() 