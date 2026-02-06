#!/usr/bin/env python3
# fish_anglers.py
# Anglerfish fishing bot with state-based logic

import time
import random
import sys
import os
import pyautogui

# Add the parent directory to the path so we can import screen_interactor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor
from pixel_monitor import PixelMonitor

class AnglerfishBot:
    def __init__(self):
        self.si = ScreenInteractor()
        self.state = None
        self.loop_count = 0
        self.successful_trips = 0
        self.setup_completed = False  # Track whether setup has been run
        
    def setup(self):
        """Initial setup: zoom, face north, adjust camera angle, and assess current state."""
        print("Starting anglerfish bot setup...")
        
        # Step 1: Zoom setup - zoom out all the way then in a tiny bit
        print("Setting up zoom...")
        self.si.zoom_out(times=10)
        time.sleep(random.uniform(0.5, 1.0))
        
        # Step 2: Face north using compass
        print("Facing north...")
        compass_click = self.si.click_on_compass()
        if not compass_click:
            print("Failed to click compass. Continuing anyway...")
        time.sleep(random.uniform(1, 2))
        
        # Step 3: Press 'w' key for 1.5 seconds to aim camera up
        print("Adjusting camera to bird's eye view...")
        pyautogui.keyDown('w')
        time.sleep(1.5)
        pyautogui.keyUp('w')
        time.sleep(random.uniform(0.5, 1.0))
        
        # Step 4: Assess current state
        print("Assessing current state...")
        self.assess_state()
        
        # Mark setup as completed
        self.setup_completed = True
        
        print("Setup complete!")
        return True
    
    def assess_state(self):
        """Assess the current state and set appropriate flags."""
        print("Assessing current state...")
        
        # Check if inventory is full by looking for raw anglerfish in bag_last_slot
        print("Checking if inventory is full...")
        raw_angler_in_bag = self.si.ensure_bag_open_and_check_last_slot('image_library/raw_anglerfish.png')
        
        if raw_angler_in_bag:
            print("Inventory is full - setting state to NEED_BANK")
            self.state = "NEED_BANK"
            return
        
        # Check if we're at the fishing spot using closest image search
        print("Checking if fishing spot is visible (searching closest to character)...")
        fishing_spot_visible = self.si.find_closest_image_region('image_library/raw_anglerfish.png', region="game_screen",
            confidence=0.95, color_tolerance=30, shape_weight=0.7, color_weight=0.3
        )
        
        if fishing_spot_visible:
            print(f"Fishing spot visible at {fishing_spot_visible} - setting state to READY_TO_FISH")
            self.state = "READY_TO_FISH"
        else:
            print("Fishing spot not visible - setting state to WALK_TO_FISH")
            self.state = "WALK_TO_FISH"
            # Add delay between fishing spot checks when not found
            print("Waiting 3-5 seconds before next check...")
            time.sleep(random.uniform(3, 5))
    
    def handle_banking_state(self):
        """Handle the NEED_BANK state - deposit items and return to fishing."""
        print("Handling banking state...")
        
        # Step 1: Check if deposit option is already visible
        print("Checking if deposit option is already visible...")
        deposit_option_visible = self.si.find_image_cv2("image_library/deposit_bank_deposit_option.png", region="game_screen_center",
            threshold=0.90)
        
        if deposit_option_visible:
            print("Deposit option already visible - clicking directly...")
            # Click the deposit option directly
            deposit_click = self.si.click_image_cv2_without_moving("image_library/deposit_bank_deposit_option.png", region="game_screen_center",
                confidence=0.90, offset_range=(0, 3)
            )
            if not deposit_click:
                print("Failed to click deposit option directly.")
                return False
            print("Deposit option clicked successfully.")
        else:
            # Step 1a: Right-click deposit box (teal pixels) with confirmation
            print("Deposit option not visible - right-clicking deposit box with confirmation...")
            deposit_box_success = self.si.find_pixel_right_click_confirm(
                "00FFFF",  # Teal color for deposit box
                "image_library/deposit_bank_deposit_option.png",
                attempts=3,
                pixel_offset_range_x=(5, 15),
                pixel_offset_range_y=(5, 15)
            )
        
        # If we needed to right-click the deposit box, check if it succeeded
        if not deposit_option_visible and not deposit_box_success:
            print("Failed to interact with deposit box. Trying alternative search areas...")
            # Try alternative search areas
            for search_area in ["p1", "game_screen_center"]:
                print(f"Trying search area: {search_area}")
                deposit_box_success = self.si.find_pixel_right_click_confirm(
                    "00FFFF",
                    "image_library/deposit_bank_deposit_option.png",
                    attempts=2,
                    pixel_offset_range_x=(5, 15),
                    pixel_offset_range_y=(5, 15)
                )
                if deposit_box_success:
                    break
            
            if not deposit_box_success:
                print("Failed to interact with deposit box in all search areas.")
                return False
        
        print("Deposit box interaction successful.")
        time.sleep(random.uniform(1, 2))
        
        # Step 2: Wait for bank interface to appear and click deposit all inventory
        print("Waiting for bank interface and depositing all inventory...")
        bank_monitor = ImageMonitor(
            screen_interactor=self.si,
            image_path="image_library/deposit_all_inventory.png",
            region="game_screen_center",
            confidence=0.95,
            check_interval=2.0,
            wait_for="appear"
        )
        bank_monitor.start()
        
        if bank_monitor.wait_for_condition(timeout=25):
            print("Bank interface detected. Depositing all inventory...")
            bank_monitor.stop()
            
            # Click deposit all inventory in bank_deposit_box area
            deposit_all_click = self.si.click_image_cv2_without_moving(
                "image_library/deposit_all_inventory.png",
                region="bank_deposit_box",
                confidence=0.92,
                offset_range=(0, 3)
            )
            
            if deposit_all_click:
                print("Deposit all inventory clicked successfully.")
                time.sleep(random.uniform(1, 2))
                
                # Step 3: Right-click fish barrel with confirmation
                print("Right-clicking fish barrel with confirmation...")
                fish_barrel_success = self.si.find_image_right_click_confirm(
                    "image_library/fish_barrel.png",
                    "image_library/empty_open_fish_barrel_option.png",
                    region="bank_deposit_box",
                    confidence=0.90,
                    attempts=3,
                    offset_range_x=(2, 10),
                    offset_range_y=(2, 10)
                )
                
                if fish_barrel_success:
                    print("Fish barrel interaction successful.")
                    time.sleep(random.uniform(1, 2))
                    
                    # Step 4: Close bank interface
                    print("Closing bank interface...")
                    
                    # Debug: Check what's currently visible on screen
                    print("Debug: Checking what's currently visible...")
                    deposit_all_visible = self.si.find_image_cv2(
                        "image_library/deposit_all_inventory.png",
                        region="bank_deposit_box",
                        threshold=0.90
                    )
                    if deposit_all_visible:
                        print(f"  ✓ Deposit all button still visible at {deposit_all_visible}")
                    else:
                        print("  ✗ Deposit all button not visible")
                    
                    # Try multiple methods to close the bank interface
                    bank_closed = False
                    
                    # Method 1: Try CV3 in bank_pane area
                    print("Method 1: Trying CV3 in bank_pane area...")
                    bank_close_click = self.si.click_image_cv3_without_moving(
                        "image_library/bank_deposit_close.png",
                        region="bank_pane",
                        confidence=0.90,
                        offset_range=(0, 3),
                        color_tolerance=30,
                        shape_weight=0.9,
                        color_weight=0.1
                    )
                    
                    if bank_close_click:
                        print("Bank interface closed successfully with CV3 in bank_pane.")
                        bank_closed = True
                    else:
                        # Method 2: Try CV2 in bank_deposit_box area (where image test succeeded)
                        print("Method 2: Trying CV2 in bank_deposit_box area...")
                        bank_close_click = self.si.click_image_cv2_without_moving(
                            "image_library/bank_deposit_close.png",
                            region="bank_deposit_box",
                            confidence=0.90,
                            offset_range=(0, 3)
                        )
                        
                        if bank_close_click:
                            print("Bank interface closed successfully with CV2 in bank_deposit_box.")
                            bank_closed = True
                        else:
                            # Method 3: Try CV3 in bank_deposit_box area
                            print("Method 3: Trying CV3 in bank_deposit_box area...")
                            bank_close_click = self.si.click_image_cv3_without_moving(
                                "image_library/bank_deposit_close.png",
                                region="bank_deposit_box",
                                confidence=0.90,
                                offset_range=(0, 3),
                                color_tolerance=30,
                                shape_weight=0.7,
                                color_weight=0.3
                            )
                            
                            if bank_close_click:
                                print("Bank interface closed successfully with CV3 in bank_deposit_box.")
                                bank_closed = True
                    
                    if bank_closed:
                        time.sleep(random.uniform(1, 2))
                        
                        # Update state to walk to fishing spot
                        self.state = "WALK_TO_FISH"
                        print("State updated to WALK_TO_FISH")
                        return True
                    else:
                        print("Failed to close bank interface with all methods.")
                        return False
                else:
                    print("Failed to interact with fish barrel.")
                    return False
            else:
                print("Failed to click deposit all inventory.")
                return False
        else:
            print("Bank interface did not appear within timeout.")
            bank_monitor.stop()
            return False
    
    def handle_walking_state(self):
        """Handle the WALK_TO_FISH state - walk towards yellow tiles to reach fishing spot."""
        print("Handling walking state...")
        
        # Search for yellow pixels in game_screen_center and click them
        print("Searching for yellow tiles to walk towards...")
        game_center_region = self.si.get_scan_area("game_screen_center")
        
        try:
            yellow_tile_click = self.si.pixel_click(
                "FFFF00",  # Yellow color
                region=game_center_region,
                tolerance=5,
                offset_range_x=(10, 30),
                offset_range_y=(10, 30),
                button='left'
            )
        except ValueError as e:
            print(f"No yellow tiles found: {e}")
            print("This might mean we're already at the fishing spot or need to wait for tiles to appear.")
            print("Reassessing state to see if we can fish now...")
            
            # Check if we can see fishing spots now
            fishing_spot_visible = self.si.find_closest_image_region(
                'image_library/raw_anglerfish.png', 
                region="game_screen",
                color_tolerance=30,
                shape_weight=0.7,
                color_weight=0.3
            )
            
            if fishing_spot_visible:
                print("Fishing spot is now visible! Switching to READY_TO_FISH state.")
                self.state = "READY_TO_FISH"
                return True  # Return True to indicate state change
            else:
                print("Still no fishing spot visible. Waiting 15 seconds before retrying...")
                time.sleep(15)
                return False  # Return False to indicate we need to try again
        
        if yellow_tile_click:
            print(f"Yellow tile clicked at {yellow_tile_click}. Waiting for movement...")
            
            # Wait 10-12 seconds for movement
            wait_time = random.uniform(10, 12)
            print(f"Waiting {wait_time:.1f} seconds for movement...")
            time.sleep(wait_time)
            
            # Check inventory status after movement (in case we got an anglerfish while walking)
            print("Checking inventory status after movement...")
            raw_angler_in_bag = self.si.ensure_bag_open_and_check_last_slot('image_library/raw_anglerfish.png')
            
            if raw_angler_in_bag:
                print("Inventory is full after movement - switching to banking state")
                self.state = "NEED_BANK"
                return True
            
            # Reassess state after movement
            self.assess_state()
            return True
        else:
            print("No yellow tiles found to walk towards.")
            return False
    
    def handle_fishing_state(self):
        """Handle the READY_TO_FISH state - start fishing and monitor progress."""
        print("Handling fishing state...")
        
        # Step 0: Check inventory status before attempting to fish
        print("Checking inventory status before fishing...")
        raw_angler_in_bag = self.si.ensure_bag_open_and_check_last_slot('image_library/raw_anglerfish.png')
        
        if raw_angler_in_bag:
            print("Inventory is full - switching to banking state")
            self.state = "NEED_BANK"
            return True
        
        # Step 1: Find the closest fishing spot and right-click with confirmation
        print("Finding closest fishing spot and right-clicking with confirmation...")
        
        # First find the closest anglerfish spot
        closest_fishing_spot = self.si.find_closest_image_region(
            "image_library/raw_anglerfish.png",
            region="game_screen",
            confidence=0.95,
            color_tolerance=30,
            shape_weight=0.7,
            color_weight=0.3
        )
        
        if not closest_fishing_spot:
            print("No fishing spot found. Waiting 5-15 seconds before retry...")
            time.sleep(random.uniform(5, 15))
            return False
        
        print(f"Found closest fishing spot at {closest_fishing_spot}")
        
        # Create a small region around the found spot for the right-click confirmation
        spot_x, spot_y = closest_fishing_spot
        click_region = (spot_x - 50, spot_y - 50, 100, 100)
        
        fishing_spot_success = self.si.find_image_right_click_confirm(
            "image_library/raw_anglerfish.png",
            "image_library/bait_rod_fishing_spot_option.png",
            region=click_region,
            confidence=0.95,
            offset_range_x=(2, 5),
            offset_range_y=(2, 5)
        )
        
        if not fishing_spot_success:
            print("Failed to interact with fishing spot. Waiting 5-15 seconds before retry...")
            time.sleep(random.uniform(5, 15))
            return False
        
        print("Fishing spot interaction successful. Starting fishing...")
        time.sleep(random.uniform(1, 2))
        
        # Step 2: Monitor for green pixel (fishing started) in p1 area
        print("Monitoring for fishing to start (green pixel)...")
        activity_pane_region = self.si.get_scan_area("activity_pane")
        fishing_start_monitor = PixelMonitor(
            screen_interactor=self.si,
            color_hex="00FF00",  # Green color
            region=activity_pane_region,
            tolerance=5,
            check_interval=3.0,
            wait_for="appear"
        )
        fishing_start_monitor.start()
        
        if fishing_start_monitor.wait_for_condition(timeout=15):
            print("Fishing started (green pixel detected).")
            fishing_start_monitor.stop()
            
            # Step 3: Monitor for red pixel (fishing stopped) in p1 area
            print("Monitoring for fishing to stop (red pixel)...")
            fishing_stop_monitor = PixelMonitor(
                screen_interactor=self.si,
                color_hex="FF0000",  # Red color
                region=activity_pane_region,
                tolerance=5,
                check_interval=3.0,
                wait_for="appear"
            )
            fishing_stop_monitor.start()
            
            if fishing_stop_monitor.wait_for_condition(timeout=600):
                print("Fishing stopped (red pixel detected).")
                fishing_stop_monitor.stop()
                
                # Check if inventory is now full
                time.sleep(random.uniform(1, 2))
                self.assess_state()
                
                if self.state == "NEED_BANK":
                    print("Inventory is now full. Fishing cycle complete.")
                    # Note: successful_trips is now managed by the GUI thread to avoid double counting
                    return True
                else:
                    print("Inventory not full yet. Continuing fishing cycle...")
                    # Continue fishing cycle
                    return self.handle_fishing_state()
            else:
                print("Timeout waiting for fishing to stop. Checking for bait message...")
                fishing_stop_monitor.stop()
                
                # Check if we're out of bait
                bait_check = self.si.find_image_cv2("image_library/chat_you_don't_have_any_bait_left.png", 
                                                   region="chat_area", threshold=0.90)
                if bait_check:
                    print("No bait left detected in chat. Stopping bot.")
                    self.state = "NO_BAIT"
                    return False
                
                print("No bait message found. Waiting 5-15 seconds before retry...")
                time.sleep(random.uniform(5, 15))
                return False
        else:
            print("Timeout waiting for fishing to start. Checking for bait message...")
            fishing_start_monitor.stop()
            
            # Check if we're out of bait
            bait_check = self.si.find_image_cv2("image_library/chat_you_don't_have_any_bait_left.png", 
                                               region="chat_area", threshold=0.90)
            if bait_check:
                print("No bait left detected in chat. Stopping bot.")
                self.state = "NO_BAIT"
                return False
            
            print("No bait message found. Waiting 5-15 seconds before retry...")
            time.sleep(random.uniform(5, 15))
            return False
    
    
    def main_loop(self, max_loops=50000):
        """Main loop that handles the three states until max loops or manual interruption."""
        print(f"Starting Anglerfish Bot with max loops: {max_loops}")
        print("=" * 60)
        
        try:
            for loop in range(1, max_loops + 1):
                self.loop_count = loop
                print(f"\n--- Starting loop {loop} of {max_loops} ---")
                print(f"Current state: {self.state}")
                print(f"Successful trips completed: {self.successful_trips}")
                
                # Step 0: Always check login status before any other operations
                print("Checking login status...")
                # Only pass the setup callback if we've already completed initial setup
                callback = self.setup if self.setup_completed else None
                login_resolved = self.si.resolveLogin(post_login_callback=callback)
                if not login_resolved:
                    print("Login resolution failed. Waiting 10-15 seconds before retry...")
                    time.sleep(random.uniform(10, 15))
                    continue
                
                # Step 0.5: Run setup on first run if not completed yet
                if not self.setup_completed:
                    print("First run detected - running initial setup...")
                    self.setup()
                
                # Always check inventory status first, regardless of current state
                print("Checking inventory status...")
                raw_angler_in_bag = self.si.ensure_bag_open_and_check_last_slot('image_library/raw_anglerfish.png')
                
                if raw_angler_in_bag:
                    print("Inventory is full - switching to banking state")
                    self.state = "NEED_BANK"
                
                # Handle current state
                if self.state == "NEED_BANK":
                    print("Handling banking state...")
                    if self.handle_banking_state():
                        print("Banking completed successfully.")
                    else:
                        print("Banking failed. Retrying...")
                        continue
                
                elif self.state == "WALK_TO_FISH":
                    print("Handling walking state...")
                    if self.handle_walking_state():
                        print("Walking completed successfully.")
                    else:
                        print("Walking failed or no yellow tiles found. Retrying...")
                        continue
                
                elif self.state == "READY_TO_FISH":
                    print("Handling fishing state...")
                    if self.handle_fishing_state():
                        print("Fishing cycle completed successfully.")
                    else:
                        print("Fishing failed. Retrying...")
                        continue
                
                elif self.state == "NO_BAIT":
                    print("No bait left. Stopping bot.")
                    print("You don't have any bait left. Please re-up and try again.")
                    break
                
                else:
                    print(f"Unknown state: {self.state}. Reassessing...")
                    self.assess_state()
                    continue
                
                print(f"Loop {loop} complete.")
                
        except KeyboardInterrupt:
            print("Manual interruption detected. Exiting loop.")
        finally:
            print("Main loop finished.")
            print(f"Total successful trips: {self.successful_trips}")
            print(f"Total loops completed: {self.loop_count}")

def main():
    """Main function to run the anglerfish fishing bot."""
    print("Starting Anglerfish Fishing Bot...")
    print("Features:")
    print("- State-based logic for banking, walking, and fishing")
    print("- Right-click confirmation for reliable interactions")
    print("- Pixel monitoring for fishing progress")
    print("- Automatic inventory management")
    print("- Random offsets for human-like behavior")
    
    # Create bot instance
    bot = AnglerfishBot()
    
    # Run setup
    if not bot.setup():
        print("Setup failed. Exiting.")
        return
    
    # Run main loop
    bot.main_loop()

if __name__ == "__main__":
    main()
