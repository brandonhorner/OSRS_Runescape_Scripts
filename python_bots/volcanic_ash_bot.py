import time
import random
import pyautogui
from screen_interactor import ScreenInteractor
from pixel_monitor import PixelMonitor
import numpy as np
from image_monitor import ImageMonitor

def wait_for_mining_completion(si, ash_location, timeout=60):
    """Wait for mining to complete by monitoring teal pixels disappearing"""
    print("Waiting for mining to complete...")
    start_time = time.time()
    
    # Get the game screen region
    game_screen = si.get_scan_area("game_screen")
    center_x = game_screen[0] + game_screen[2] // 2
    center_y = game_screen[1] + game_screen[3] // 2
    search_radius = 100

    search_region = (center_x - search_radius, 
                    center_y - search_radius,
                    search_radius * 2,
                    search_radius * 2)

    while time.time() - start_time < timeout:
        # Check for any teal pixel in the region
        if not si.find_pixel("00FFFF", region=search_region, tolerance=0):
            print("No more ash pixels found - mining completed")
            return True
        time.sleep(0.5)
    
    print("Mining did not complete within timeout")
    return False

def mine_ash_pile(si):
    """Attempt to mine an ash pile"""
    print("Looking for ash pile...")
    
    # Find closest teal pixel (ash pile) with local search to find top-left
    ash_location = si.find_closest_pixel("00FFFF", tolerance=0, local_search_size=90)  # Teal color
    if not ash_location:
        print("No ash piles found")
        return False
    
    print(f"Found ash pile at {ash_location}")
    
    # Right-click with offset from top-left
    target_x = ash_location[0] + random.randint(5, 12)
    target_y = ash_location[1] + random.uniform(3, 10)
    pyautogui.moveTo(target_x, target_y)
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(button='right')
    print(f"Right-clicked at ({target_x}, {target_y})")
    
    # Wait for context menu
    time.sleep(random.uniform(0.3, 0.5))
    
    # Look for "Mine ash" option
    mine_ash_location = si.find_image_cv2('python_bots/images/mine_ash.png', threshold=0.9)
    if not mine_ash_location:
        print("Could not find 'Mine ash' option")
        # Move mouse away to clear right-click menu
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + random.uniform(40, 150), current_y + random.uniform(10, 50))
        time.sleep(random.uniform(0.2, 0.4))
        return False
    
    # Click with random offset
    target_x = mine_ash_location[0] + random.randint(-6, 12)
    target_y = mine_ash_location[1] + random.randint(-4, 4)
    pyautogui.moveTo(target_x, target_y)
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click()
    print(f"Clicked 'Mine ash' at ({target_x}, {target_y})")
    
    # Give character time to walk to the ash pile
    time.sleep(random.uniform(5, 10))
    
    # Wait for mining to complete by watching the ash pixels
    return wait_for_mining_completion(si, ash_location)

def test_mining_inactive(si):
    """Test function to check if mining inactive image can be found"""
    print("Testing mining inactive image detection...")
    
    # Try to find the image
    mining_inactive_location = si.find_image_cv2('python_bots/images/mining_inactive.png', threshold=0.99)
    mining_active_location = si.find_image_cv2('python_bots/images/mining_active.png', threshold=1)

    if mining_inactive_location:
        print(f"Found mining inactive image at {mining_inactive_location}")
        
        # Take a screenshot of the area around the found location
        x, y = mining_inactive_location
        region = (max(0, x-50), max(0, y-50), 100, 100)
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save('mining_inactive_test.png')
        print("Saved test screenshot to 'mining_inactive_test.png'")
        
        return True
    
    if mining_active_location:
        print(f"Found mining inactive image at {mining_active_location}")
        
        # Take a screenshot of the area around the found location
        x, y = mining_active_location
        region = (max(0, x-50), max(0, y-50), 100, 100)
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save('mining_active_test.png')
        print("Saved test screenshot to 'mining_active_test.png'")
        return True
    
    else:
        print("Could not find mining inactive image")
        return False

def main_loop(max_loops=150):
    # Create the screen interactor
    si = ScreenInteractor()
    print("Starting volcanic ash mining bot in 3 seconds...")
    time.sleep(3)
    
    try:
        completed_loops = 0
        while completed_loops < max_loops:
            print(f"\n--- Starting loop {completed_loops + 1} of {max_loops} ---")
            
            # Try to mine an ash pile
            if mine_ash_pile(si):
                completed_loops += 1
                print(f"Successfully mined ash pile {completed_loops}")
            else:
                print("Failed to mine ash pile, retrying...")
                time.sleep(random.uniform(1, 2))
                completed_loops += 1 # delete this when you stop failing so much lol
            
            # Small delay between attempts
            time.sleep(random.uniform(0.5, 1))
                
    except KeyboardInterrupt:
        print("Manual interruption detected. Exiting loop.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Volcanic ash mining bot finished.")

if __name__ == "__main__":
    main_loop(max_loops=150)  # Adjust as needed