import time
import random
import pyautogui
from screen_interactor import ScreenInteractor
from pixel_monitor import PixelMonitor
import numpy as np
from image_monitor import ImageMonitor

def create_bank_chest_monitor(si):
    """Helper function to create a new PixelMonitor instance for the teal bank chest"""
    return PixelMonitor(
        screen_interactor=si,
        color_hex="00FFFF",  # Teal color
        region="game_screen",
        tolerance=1,
        check_interval=0.2,
        wait_for="appear"
    )

def create_bank_close_monitor(si):
    """Helper function to create a new ImageMonitor instance for the bank close button"""
    return ImageMonitor(
        screen_interactor=si,
        image_path='python_bots/images/bank_close.png',
        region="game_screen",
        confidence=0.9,
        check_interval=0.2,
        wait_for="appear"
    )

def wait_for_bank_open(si, timeout=8):
    """Wait for bank interface to open by looking for bank_close.png"""
    bank_close_monitor = create_bank_close_monitor(si)
    bank_close_monitor.start()
    try:
        if bank_close_monitor.wait_for_condition(timeout=timeout):
            return True
    finally:
        bank_close_monitor.stop()
    return False

def move_mouse_away_from_bank():
    """Move mouse away from bank interface to avoid blocking items"""
    current_x, current_y = pyautogui.position()
    # Move at least 200 pixels to the right
    target_x = current_x + random.uniform(200, 300)
    # Add some vertical randomness too
    target_y = current_y + random.uniform(-100, 100)
    pyautogui.moveTo(target_x, target_y)
    time.sleep(random.uniform(0.2, 0.4))

def setup_bank(si):
    """Initial setup: Open bank and withdraw items"""
    print("Starting setup...")
    
    # First check if bank is already open
    bank_close_location = si.find_image_cv2('python_bots/images/bank_close.png', threshold=0.9)
    if bank_close_location:
        print("Bank is already open")
        # Move mouse away from bank interface
        move_mouse_away_from_bank()
    else:
        # Step 1: Open bank chest
        bank_opened = False
        attempts = 0
        max_attempts = 3
        
        while not bank_opened and attempts < max_attempts:
            attempts += 1
            print(f"Attempt {attempts} to open bank chest...")
            
            # Create a new monitor instance for each attempt
            bank_chest_monitor = create_bank_chest_monitor(si)
            
            # Find and right-click teal bank chest
            bank_chest_monitor.start()
            if bank_chest_monitor.wait_for_condition(timeout=5):
                chest_location = bank_chest_monitor.get_found_location()
                if chest_location:
                    # Right-click with random offset
                    target_x = chest_location[0] + random.uniform(10, 25)
                    target_y = chest_location[1] + random.uniform(10, 25)
                    pyautogui.moveTo(target_x, target_y)
                    time.sleep(random.uniform(0.2, 0.4))
                    pyautogui.click(button='right')
                    print(f"Right-clicked bank chest at ({target_x}, {target_y})")
                    
                    # Wait for context menu and click "Use bank"
                    time.sleep(random.uniform(0.3, 0.5))
                    use_bank_location = si.find_image_cv2('python_bots/images/use_bank.png', threshold=0.9)
                    if use_bank_location:
                        pyautogui.moveTo(use_bank_location[0], use_bank_location[1])
                        time.sleep(random.uniform(0.2, 0.4))
                        pyautogui.click()
                        print("Clicked 'Use bank'")
                        
                        # Wait for bank interface with proper monitoring
                        if wait_for_bank_open(si):
                            # Move mouse away from bank interface
                            move_mouse_away_from_bank()
                            bank_opened = True
                            print("Bank interface opened successfully")
                            break
            
            bank_chest_monitor.stop()
            if not bank_opened:
                print("Failed to open bank, retrying...")
                time.sleep(random.uniform(1, 2))
        
        if not bank_opened:
            print("Failed to open bank after multiple attempts. Stopping script.")
            return False
    
    # Check for required items
    print("Checking for required items...")
    
    # Check for volcanic ash and harralander potion (unf)
    ash_location = si.find_image_cv2('python_bots/images/volcanic_ash.png', threshold=0.98)
    potion_location = si.find_image_cv2('python_bots/images/harralander_potion_unf.png', threshold=0.99)
    
    if not ash_location or not potion_location:
        print("Required items not found in bank. Stopping script.")
        return False
    
    # Withdraw harralander potion (unf)
    print("Withdrawing harralander potion (unf)...")
    pyautogui.moveTo(potion_location[0], potion_location[1])
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(button='right')
    time.sleep(random.uniform(0.3, 1))
    
    # Try to find and click "Withdraw-27" first
    withdraw_27_location = si.find_image_cv2('python_bots/images/withdraw-27.png', threshold=0.98)
    if withdraw_27_location:
        pyautogui.moveTo(withdraw_27_location[0], withdraw_27_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Clicked 'Withdraw-27'")
    else:
        # Try withdraw-x option
        withdraw_x_location = si.find_image_cv2('python_bots/images/withdraw-x.png', threshold=0.9)
        if withdraw_x_location:
            pyautogui.moveTo(withdraw_x_location[0], withdraw_x_location[1])
            time.sleep(random.uniform(1, 1.4))
            pyautogui.click()
            time.sleep(random.uniform(1, 1.5))
            pyautogui.write('2')
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.write('7')
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.press('enter')
            print("Entered withdraw amount: 27")
        else:
            print("Could not find withdraw options. Stopping script.")
            return False
    
    # Check and set X quantity if needed
    if not si.find_image_cv2('python_bots/images/bank_x_quantity_is_active.png', threshold=0.95):
        x_quantity_location = si.find_image_cv2('python_bots/images/bank_x_quantity_is_NOT_active.png', threshold=0.95)
        if x_quantity_location:
            pyautogui.moveTo(x_quantity_location[0], x_quantity_location[1])
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.click()
            print("Set X quantity option")
        else:
            print("Could not find X quantity option. Stopping script.")
            return False
    
    # Withdraw volcanic ash
    print("Withdrawing volcanic ash...")
    ash_withdrawn = False
    max_attempts = 3
    attempts = 0
    
    while not ash_withdrawn and attempts < max_attempts:
        attempts += 1
        print(f"Attempt {attempts} to withdraw volcanic ash...")
        
        pyautogui.moveTo(ash_location[0], ash_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        time.sleep(random.uniform(0.5, 0.8))
        
        # Check if ash is in inventory
        ash_bag_location = si.find_image_cv2('python_bots/images/volcanic_ash.png', region="bag", threshold=0.98)
        if ash_bag_location:
            print("Volcanic ash successfully withdrawn")
            ash_withdrawn = True
        else:
            print("Volcanic ash not found in inventory, retrying...")
            time.sleep(random.uniform(0.5, 1))
    
    if not ash_withdrawn:
        print("Failed to withdraw volcanic ash after multiple attempts. Stopping script.")
        return False

    # Close bank
    print("Closing bank...")
    bank_close_location = si.find_image_cv2('python_bots/images/bank_close.png', threshold=0.9)
    if bank_close_location:
        pyautogui.moveTo(bank_close_location[0], bank_close_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Bank closed")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Check if bag interface is present
        bag_is_closed_location = si.find_image_cv2('python_bots/images/bag_is_closed.png', threshold=0.98)
        if bag_is_closed_location:
            print("Closed bag icon still present, clicking bag to open...")
            pyautogui.moveTo(bag_is_closed_location[0], bag_is_closed_location[1])
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.click()
            time.sleep(random.uniform(0.5, 1.5))
    
    return True

def make_potions(si):
    """Make a full inventory of ultra compost potions"""
    print("Making ultra compost potions...")
    time.sleep(random.uniform(.5, 1))
    
    # Click volcanic ash
    ash_bag_location = si.find_image_cv2('python_bots/images/volcanic_ash.png', region="bag", threshold=0.99)
    if ash_bag_location:
        pyautogui.moveTo(ash_bag_location[0], ash_bag_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Clicked volcanic ash in inventory")
    
    # Click harralander potion (unf)
    potion_bag_location = si.find_image_cv2('python_bots/images/harralander_potion_unf.png', region="bag", threshold=0.99)
    if potion_bag_location:
        pyautogui.moveTo(potion_bag_location[0], potion_bag_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Clicked harralander potion (unf) in inventory")
    
    # Press spacebar and wait for combination
    time.sleep(random.uniform(1.2, 2.0))
    pyautogui.press('space')
    time.sleep(random.uniform(29, 32))  # Wait for all 27 potions to be made
    
    return True

def bank_items(si):
    """Bank all items and check if we can continue"""
    print("Banking items...")
    
    # First check if bank is already open
    bank_close_location = si.find_image_cv2('python_bots/images/bank_close.png', threshold=0.9)
    if bank_close_location:
        print("Bank is already open")
        # Move mouse away from bank interface
        move_mouse_away_from_bank()
    else:
        # Create a new monitor instance for banking
        bank_chest_monitor = create_bank_chest_monitor(si)
        bank_chest_monitor.start()
        
        if bank_chest_monitor.wait_for_condition(timeout=5):
            chest_location = bank_chest_monitor.get_found_location()
            if chest_location:
                # Right-click bank chest
                target_x = chest_location[0] + random.uniform(10, 25)
                target_y = chest_location[1] + random.uniform(10, 25)
                pyautogui.moveTo(target_x, target_y)
                time.sleep(random.uniform(0.2, 0.4))
                pyautogui.click(button='right')
                time.sleep(random.uniform(0.3, 0.5))
                
                # Click "Use bank"
                use_bank_location = si.find_image_cv2('python_bots/images/use_bank.png', threshold=0.9)
                if use_bank_location:
                    pyautogui.moveTo(use_bank_location[0], use_bank_location[1])
                    time.sleep(random.uniform(0.2, 0.4))
                    pyautogui.click()
                    
                    # Wait for bank interface with proper monitoring
                    if not wait_for_bank_open(si):
                        print("Failed to open bank interface")
                        bank_chest_monitor.stop()
                        return False
                    
                    # Move mouse away from bank interface
                    move_mouse_away_from_bank()
        
        bank_chest_monitor.stop()
    
    # Deposit all
    deposit_all_location = si.find_image_cv2('python_bots/images/deposit_all_inventory.png', threshold=0.9)
    if deposit_all_location:
        pyautogui.moveTo(deposit_all_location[0], deposit_all_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Deposited all items")
        
        # Check if we can continue (items still available)
        ash_location = si.find_image_cv2('python_bots/images/volcanic_ash.png', threshold=0.98)
        potion_location = si.find_image_cv2('python_bots/images/harralander_potion_unf.png', threshold=0.99)
        
        if not ash_location or not potion_location:
            print("Out of materials. Stopping script.")
            return False
        
        # Withdraw new materials
        print("Withdrawing new materials...")
        pyautogui.moveTo(ash_location[0], ash_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.moveTo(potion_location[0], potion_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        
        # Close bank
        bank_close_location = si.find_image_cv2('python_bots/images/bank_close.png', threshold=0.9)
        if bank_close_location:
            pyautogui.moveTo(bank_close_location[0], bank_close_location[1])
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.click()
            print("Bank closed")
            return True
    
    return False

def main_loop(max_loops=100):
    # Create the screen interactor
    si = ScreenInteractor()
    print("Starting ultra compost potion bot in 3 seconds...")
    time.sleep(3)
    
    try:
        # Initial setup
        if not setup_bank(si):
            return
        
        completed_inventories = 1
        can_continue = True
        
        while can_continue:
            print(f"\n--- Starting inventory {completed_inventories} ---")
            
            # Make potions
            if not make_potions(si):
                break
            
            # Bank items and check if we can continue
            can_continue = bank_items(si)
            
            if can_continue:
                print(f"Completed {completed_inventories} inventories")
                completed_inventories += 1
                
    except KeyboardInterrupt:
        print("Manual interruption detected. Exiting loop.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Ultra compost potion bot finished.")

if __name__ == "__main__":
    main_loop(max_loops=100)  # Adjust as needed 