# gemstone_crab_bot.py
import time
import random
import signal
import os
from numpy import ma
import pyautogui
import sys

# Global flag for graceful shutdown
shutdown_requested = False
monitoring_active = False  # Track when pixel monitoring is active

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully only during pixel monitoring."""
    global shutdown_requested, monitoring_active
    if monitoring_active:
        print(f"\n⚠ Interrupt signal ({signum}) received during monitoring. Shutting down gracefully...")
        shutdown_requested = True
    else:
        # During normal operation, let Ctrl+C work normally
        print(f"\n⚠ Interrupt signal ({signum}) received. Exiting immediately...")
        os._exit(0)  # Force exit during non-monitoring phases

def setup_bot(si):
    """Initial setup: face north and zoom out completely."""
    print("Setting up bot...")
    
    # Step 1: Click compass to face north (using world map as reference)
    print("Facing north...")
    
    compass_click = si.click_on_compass(region="p3", confidence=0.90)
    
    if not compass_click:
        print("Warning: Could not click on compass")
    
    time.sleep(random.uniform(1, 2))
    
    # Step 2: Zoom out all the way
    print("Zooming out completely...")
    si.zoom_out(times=10)
    si.zoom_in(times=1)
    time.sleep(random.uniform(1, 2))
    
    print("Setup complete!")

def find_gemstone_crab(si):
    """Search for pink pixels (gemstone crab) in the game screen area."""
    print("Searching for gemstone crab (pink pixels)...")
    
    # Search for pink pixels (FF00FF) in the game screen area
    game_region = si.get_scan_area("game_screen")
    pink_pixel = si.find_pixel("FF00FF", region=game_region, tolerance=5)
    
    if pink_pixel:
        print(f"Found gemstone crab at {pink_pixel}")
        return pink_pixel
    else:
        print("No gemstone crab found")
        return None

def teleport_to_next_area(si):
    """Teleport to the next area using the teal cave."""
    print("Teleporting to next area...")
    
    # Step 1: Click on teal cave (transportation spot)
    game_region = si.get_scan_area("game_screen")
    teal_cave_click = si.pixel_click(
        "00FFFF",  # Teal color
        region=game_region, 
        tolerance=0, 
        offset_range_x=(10, 30), 
        offset_range_y=(10, 30)
    )
    
    if teal_cave_click:
        print(f"Teal cave clicked at {teal_cave_click}")
        
        # Wait for teleport
        wait_time = random.uniform(6, 8)
        print(f"Waiting {wait_time:.1f} seconds for teleport...")
        time.sleep(wait_time)
        
        # Step 2: Click on yellow game tile
        yellow_tile_click = si.pixel_click(
            "FFFF00",  # Yellow color
            region=game_region, 
            tolerance=0, 
            offset_range_x=(2, 10), 
            offset_range_y=(2, 10)
        )
        
        if yellow_tile_click:
            print(f"Yellow tile clicked at {yellow_tile_click}")
            
            # Wait for area to load
            wait_time = random.uniform(2.5, 4.5)
            print(f"Waiting {wait_time:.1f} seconds for area to load...")
            time.sleep(wait_time)
            
            return True
        else:
            print("Warning: Could not find yellow tile")
            return False
    else:
        print("Warning: Could not find teal cave")
        return False

def attack_gemstone_crab(si, crab_location):
    """Attempt to attack the gemstone crab with multiple retry attempts."""
    print(f"Attempting to attack gemstone crab at {crab_location}...")
    
    # Try up to 9 times to find the attack option
    for attempt in range(9):
        print(f"Attack attempt {attempt + 1}/9")
        
        # Re-find the crab location on each attempt to correct positioning errors
        current_crab_location = find_gemstone_crab(si)
        if not current_crab_location:
            print(f"No crab found on attempt {attempt + 1}, trying next attempt...")
            # Move mouse up and to the right by 150-300 pixels
            move_x = random.randint(150, 300)
            move_y = random.randint(-300, -150)  # Negative for up
            
            current_x, current_y = pyautogui.position()
            new_x = current_x + move_x
            new_y = current_y + move_y
            
            print(f"Moving mouse to ({new_x}, {new_y})")
            pyautogui.moveTo(new_x, new_y)
            time.sleep(random.uniform(0.2, 0.4))

        
        print(f"Re-found crab at {current_crab_location}")
        
        # Calculate click position with offset (down and right by 10-40 pixels)
        offset_x = random.randint(30, 60)
        offset_y = random.randint(30, 60)
        click_x = current_crab_location[0] + offset_x
        click_y = current_crab_location[1] + offset_y
        
        # Right click on the calculated position
        print(f"Right clicking at ({click_x}, {click_y})")
        pyautogui.moveTo(click_x, click_y)
        time.sleep(random.uniform(0.05, 0.1))
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.4, 0.5))
        
        # Look for attack option in the game screen area
        game_region = si.get_scan_area("game_screen_middle_horizontal")
        attack_option = si.find_image_cv2(
            'image_library/attack_gemstone_crab_option.png',
            region=game_region,
            threshold=0.90
        )
        
        if attack_option:
            print(f"Found attack option at {attack_option}")
            
            # Click the attack option with random offset within the image bounds
            # Image is 163x6, so we offset by x= -2 to 4 and y= 0 to 36
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-2, 4)
            target_x = attack_option[0] + offset_x
            target_y = attack_option[1] + offset_y
            
            print(f"Clicking attack option at ({target_x}, {target_y})")
            pyautogui.moveTo(target_x, target_y)
            time.sleep(random.uniform(0.05, 0.1))
            pyautogui.click()
            
            return True
        else:
            print(f"Attack option not found on attempt {attempt + 1}")
            
            if attempt < 2:  # Don't move on the last attempt
                # Move mouse up and to the right by 150-300 pixels
                move_x = random.randint(150, 300)
                move_y = random.randint(-300, -150)  # Negative for up
                
                current_x, current_y = pyautogui.position()
                new_x = current_x + move_x
                new_y = current_y + move_y
                
                print(f"Moving mouse to ({new_x}, {new_y})")
                pyautogui.moveTo(new_x, new_y)
                time.sleep(random.uniform(0.2, 0.4))

        time.sleep(random.uniform(0.5, 1))
    
    print("Failed to find attack option after 9 attempts")
    return False

def drink_strength_potion(si):
    """Drink a strength potion from the inventory."""
    print("Attempting to drink strength potion...")
    
    # Check if bag is closed and open it if needed
    p6_region = si.get_scan_area("p6")
    bag_closed = si.find_image_cv2(
        'image_library/bag_is_closed.png',
        region=p6_region,
        threshold=0.9
    )
    
    if bag_closed:
        print("Bag is closed - opening inventory...")
        bag_click = si.click_image_cv2(
            'image_library/bag_is_closed.png',
            region=p6_region,
            confidence=0.9
        )
        if bag_click:
            print("Inventory opened")
            time.sleep(random.uniform(0.2, 0.4))
        else:
            print("Warning: Failed to open inventory")
    else:
        print("Bag is already open")
    
    # Search for strength potions in order of preference (lowest dosage first)
    bag_region = si.get_scan_area("bag")
    potion_images = [
        'image_library/strength_pot-1.png',
        'image_library/strength_pot-2.png',
        'image_library/strength_pot-3.png',
        'image_library/strength_pot-4.png'
    ]
    
    for i, potion_image in enumerate(potion_images, 1):
        potion_click = si.click_image_cv2_without_moving(
            potion_image,
            region=bag_region,
            confidence=0.95,
            offset_range=(0, 3)
        )
        time.sleep(.05)
        
        if potion_click:
            print(f"Strength potion dose {i} found and consumed")
            return True
    
    print("No strength potion found in inventory")
    return False

def wait_for_crab_burrow(si):
    """Wait for the pink pixels (gemstone crab) to disappear, indicating it's defeated."""
    global shutdown_requested, monitoring_active
    print("Waiting for gemstone crab to be defeated (pink pixels to disappear)...")
    
    # Set monitoring flag to enable graceful Ctrl+C handling
    monitoring_active = True
    
    try:
        # Create pixel monitor to look for pink pixels (FF00FF) to disappear
        game_region = si.get_scan_area("game_screen")
        pixel_monitor = PixelMonitor(
            si, 
            color_hex="FF00FF",  # Pink color
            region=game_region, 
            tolerance=2, 
            check_interval=3.0, 
            wait_for="disappear"
        )
        pixel_monitor.start()
        
        try:
            # Wait for pink pixels to disappear for up to 20 minutes (1200 seconds)
            # Check for shutdown request every second
            timeout_seconds = 1200
            check_interval = 1.0
            
            for _ in range(int(timeout_seconds / check_interval)):
                if shutdown_requested:
                    print("⚠ Shutdown requested during crab wait - stopping monitor")
                    return False
                
                if pixel_monitor.wait_for_condition(timeout=check_interval):
                    print("Gemstone crab defeated - pink pixels disappeared")
                    return True
            
            print("Timeout reached waiting for crab to be defeated")
            return False
        finally:
            pixel_monitor.stop()
    finally:
        # Always reset monitoring flag when function exits
        monitoring_active = False

def main_loop(si, target_successes=45, max_attempts=None):
	"""Run until a target number of successful loops is reached.

	A successful loop is counted only when the crab is attacked and the pink
	pixels disappear (i.e., wait_for_crab_burrow returns True).

	Args:
		target_successes: Number of successful loops to complete
		max_attempts: Optional cap on total attempts to avoid infinite runs
	"""
	global shutdown_requested
	attempts = 0
	successes = 0
	print(f"Starting main loop aiming for {target_successes} successful runs...")

	while not shutdown_requested and successes < target_successes:
		# Respect optional max_attempts if provided
		if max_attempts is not None and attempts >= max_attempts:
			print("Reached maximum attempts limit; stopping.")
			break

		attempts += 1
		print(f"\n--- Attempt {attempts} | Successes {successes}/{target_successes} ---")

		# Search for gemstone crab
		crab_location = find_gemstone_crab(si)

		if not crab_location:
			# No crab found, try to teleport to next area
			print("No crab found, teleporting to next area...")
			if not teleport_to_next_area(si):
				print("Failed to teleport, retrying...")
				continue

			# Search again after teleport
			crab_location = find_gemstone_crab(si)
			if not crab_location:
				print("Still no crab found after teleport; counting as unsuccessful attempt.")
				continue

		# Attack the crab
		if attack_gemstone_crab(si, crab_location):
			print("Successfully initiated attack on gemstone crab")

			# Wait a moment for attack to register
			time.sleep(1)

			# Drink strength potion if needed and optionally re-initiate combat
			if drink_strength_potion(si):
				print("Strength potion consumed")
				print("Re-initiating combat after potion consumption...")
				if attack_gemstone_crab(si, crab_location):
					print("Combat re-initiated successfully")
				else:
					print("Warning: Failed to re-initiate combat")

			# Wait for crab to be defeated (pink pixels to disappear)
			if wait_for_crab_burrow(si):
				successes += 1
				print(f"Success! Completed {successes}/{target_successes} successful loops")
			else:
				if shutdown_requested:
					print("⚠ Attempt interrupted by shutdown request")
					break
				else:
					print("Attempt timed out waiting for crab to be defeated")
		else:
			print("Failed to attack gemstone crab; counting as unsuccessful attempt.")

		# Small delay between attempts
		time.sleep(random.uniform(1, 2))

	# Final summary
	if shutdown_requested:
		print("Stopped due to shutdown request")
	print(f"Summary: {successes} successes out of {attempts} attempts.")

def main():
    """Main function to run the gemstone crab bot."""
    global shutdown_requested
    
    print("Gemstone Crab Bot Starting...")
    print("Press Ctrl+C to stop the bot immediately (except during pixel monitoring)")
    
    # Create screen interactor
    si = ScreenInteractor()
    
    # Wait for user to get ready
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Setup phase
        setup_bot(si)
        
        # Main loop
        # Run until N successful loops are completed; cap attempts to avoid infinite runs
        main_loop(si, target_successes=78, max_attempts=300)
        
    except KeyboardInterrupt:
        print("\n⚠ Manual interruption detected. Exiting immediately...")
        # Let normal Ctrl+C behavior work
        raise
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Bot finished.")

if __name__ == "__main__":
    main()
