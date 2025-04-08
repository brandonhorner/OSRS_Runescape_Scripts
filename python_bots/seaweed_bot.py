import time
import random
import pyautogui
import cv2
import numpy as np
from screen_interactor import ScreenInteractor
from pixel_monitor import PixelMonitor
from image_monitor import ImageMonitor

def create_seaweed_spore_purple_pixel_monitor(si):
    """Helper function to create a new PixelMonitor instance"""
    return PixelMonitor(
        screen_interactor=si,
        color_hex="AA00FF",  # Purple color
        region="game_screen",  # Middle vertical third of screen
        tolerance=15,
        check_interval=0.1,
        wait_for="appear"
    )

def main_loop(max_loops=50):
    # Create the screen interactor
    si = ScreenInteractor()
    print("Starting seaweed spore bot in 3 seconds...")
    time.sleep(3)
    
    try:
        for loop in range(1, max_loops+1):
            print(f"\n--- Starting loop {loop} of {max_loops} ---")
            
            # Create a new monitor instance for each loop
            seaweed_spore_purple_pixel_monitor = create_seaweed_spore_purple_pixel_monitor(si)
            
            print("Waiting for seaweed spore to appear (purple text)...")
            seaweed_spore_purple_pixel_monitor.start()
            
            # Wait for up to 10 minutes for a spore to appear
            if seaweed_spore_purple_pixel_monitor.wait_for_condition(timeout=600):
                # Process multiple spores if available
                spores_processed = 0
                max_spores_to_process = 4  # Process up to 4 spores (original + 3 more scans)
                
                while spores_processed < max_spores_to_process:
                    print(f"Seaweed spore detected! (Spore #{spores_processed + 1})")
                    
                    # Get the location where the purple pixel was found
                    spore_location = seaweed_spore_purple_pixel_monitor.get_found_location()
                    
                    if not spore_location:
                        print("No spore location detected, breaking loop")
                        break
                    
                    print(f"Spore found at {spore_location}")
                    
                    # Single attempt to click the spore
                    # Right-click with offset (100px right, 10px down)
                    target_x = spore_location[0] + random.uniform(97, 103)
                    target_y = spore_location[1] + random.uniform(7, 13)
                    
                    # Move to target and right-click
                    pyautogui.moveTo(target_x, target_y)
                    time.sleep(random.uniform(0.1, 0.2))
                    pyautogui.click(button='right')
                    print(f"Right-clicked at position: ({target_x}, {target_y})")
                    
                    # Wait longer for the context menu to appear
                    time.sleep(random.uniform(0.3, 0.5))
                    
                    # Try to find and click the menu option
                    spore_clicked = False
                    try:
                        # Take a screenshot of the entire screen
                        menu_screenshot = pyautogui.screenshot()
                        
                        # Convert the screenshot to CV2 format
                        menu_cv = cv2.cvtColor(np.array(menu_screenshot), cv2.COLOR_RGB2BGR)
                        
                        # Load and match the "Take seaweed spore" template
                        template = cv2.imread('python_bots/images/take_seaweed_spore.png')
                        if template is None:
                            raise ValueError("Could not load take_seaweed_spore.png template")
                        
                        # Perform template matching
                        result = cv2.matchTemplate(menu_cv, template, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        
                        # If we found a good match
                        if max_val > 0.8:  # Adjust threshold as needed
                            # Get center of the template
                            template_h, template_w = template.shape[:2]
                            click_x = max_loc[0] + template_w // 2
                            click_y = max_loc[1] + template_h // 2
                            
                            # Add small random offset
                            click_x += random.randint(-3, 3)
                            click_y += random.randint(-2, 2)
                            
                            # Click on the option
                            pyautogui.moveTo(click_x, click_y)
                            time.sleep(random.uniform(.05, .09))
                            pyautogui.click()
                            print(f"Clicked 'Take seaweed spore' at ({click_x}, {click_y})")
                            
                            time.sleep(random.uniform(7, 8))

                            # Mark as successfully clicked
                            spore_clicked = True
                        else:
                            print("Menu option not found.")
                    except Exception as e:
                        print(f"Error detecting menu option: {e}")
                    
                    # Increment the counter regardless of success
                    spores_processed += 1
                    
                    # If we've processed all spores we want to check, break out
                    if spores_processed >= max_spores_to_process:
                        break
                    
                    # Look for another spore only if we successfully clicked this one
                    if spore_clicked:
                        print(f"Looking for additional spores ({spores_processed}/{max_spores_to_process-1})...")
                        
                        # Stop the current monitor completely
                        seaweed_spore_purple_pixel_monitor.stop()
                        
                        # Create a fresh monitor instance for the next spore
                        seaweed_spore_purple_pixel_monitor = create_seaweed_spore_purple_pixel_monitor(si)
                        
                        # Start looking for another spore
                        seaweed_spore_purple_pixel_monitor.start()
                        
                        timeout = random.uniform(7, 10)
                        
                        # Wait a shorter time for additional spores (30 seconds)
                        if not seaweed_spore_purple_pixel_monitor.wait_for_condition(timeout):
                            print("No more spores detected. Moving on.")
                            seaweed_spore_purple_pixel_monitor.stop()
                            break
                    else:
                        # If we failed to click this spore, don't look for more
                        print("Failed to click spore. Not looking for additional spores.")
                        break
                
                # Return to the red box position (after processing all spores)
                try:
                    red_box_click = si.pixel_click(
                        "FF0000",  # Red color
                        region="game_screen",  # Middle vertical third
                        tolerance=10,
                        offset_range_x=(-80, 80),
                        offset_range_y=(-80, 80)
                    )
                    print(f"Returning to red box at {red_box_click}")
                    time.sleep(random.uniform(7, 8))
                    print(f"Returned to red box.")
                    
                except ValueError as e:
                    print(f"Error finding red box: {e}. Continuing...")
                
                # Make sure the current monitor is stopped before the next loop
                if seaweed_spore_purple_pixel_monitor:
                    seaweed_spore_purple_pixel_monitor.stop()
            else:
                print("No seaweed spore detected within timeout period")
                seaweed_spore_purple_pixel_monitor.stop()
            
            print(f"Loop {loop} complete.")
            
    except KeyboardInterrupt:
        print("Manual interruption detected. Exiting loop.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Seaweed bot main loop finished.")

if __name__ == "__main__":
    main_loop(max_loops=1000)  # Adjust as needed 