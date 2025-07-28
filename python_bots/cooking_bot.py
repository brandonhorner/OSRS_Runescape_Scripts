import time
import pyautogui
import random
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor  # <--- Our new class

def main_loop(max_loops=50):
    si = ScreenInteractor()
        # Step 1: Click the bank chest (teal = 00FFFF).

    try:
        bank_chest_click = si.pixel_click("00FFFF", region="v2", tolerance=10, 
                                            offset_range_x=(25, 60), offset_range_y=(10, 25))
        time.sleep(random.uniform(1, 1.5))
        print(f"Bank chest clicked at {bank_chest_click}.")
    except Exception as e:
        print(f"Bank chest not found.. maybe it's open :): {e}.")
    

    for loop in range(1, max_loops + 1):
        print(f"\n--- Starting loop {loop} of {max_loops} ---")
        
        # Step 2: Withdraw raw karambwans from the bank
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)
        # while we don't see bank close, repeat the step to click the bank
        iteration = 0
        while not bank_close_button and iteration < 20:
            print("Raw karambwans not found in bank. Re-clicking bank chest.")
            try:
                bank_chest_click = si.pixel_click("00FFFF", region="v2", tolerance=10, 
                                                  offset_range_x=(25, 60), offset_range_y=(10, 25))
                print(f"Bank chest clicked at {bank_chest_click}.")
                iteration += 1
            except Exception as e:
                print(f"Bank chest not found or error: {e}. Trying again.")
            time.sleep(random.uniform(1, 1.5))
            bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)

        # bank is now open, withdraw karambwans
        print("Bank open. Withdrawing raw karambwans.")
        withdraw_karambwan_success = si.click_image_cv2_without_moving("python_bots/image_library/raw_karambwan.png",
                                                         confidence=0.98, offset_range=(0, 2))

        if withdraw_karambwan_success:
            print(f"Raw karambwans withdrawn at {withdraw_karambwan_success}.")
        else:
            print("Raw karambwans not found for withdrawal. Trying the loop again.")
            continue

        # sleep between 0.5 and 1.0 seconds
        time.sleep(random.uniform(0.5, 1.0))
        
        # Step 3: Close the bank
        bank_close_click = si.click_image_cv2_without_moving("python_bots/image_library/bank_close.png",
                                                             region="v2", confidence=0.95, offset_range=(1, 4))
        if bank_close_click:
            print(f"Bank closed at {bank_close_click}.")
        else:
            print("Bank close button not found. Continuing...")

        # Step 4: Click the clay oven (pink = FF00FF).
        try:
            clay_oven_click = si.pixel_click("FF00FF", region="v2", tolerance=10, 
                                             offset_range_x=(25, 60), offset_range_y=(15, 25))
            print(f"Clay oven clicked at {clay_oven_click}.")
        except Exception as e:
            print(f"Clay oven not found or error: {e}. Skipping loop iteration.")
            continue
        
        # Step 5: Wait for movement
        time.sleep(random.uniform(3, 4))
        
        # Step 6: Press space to initiate cooking
        pyautogui.press("space")
        print("Spacebar pressed to start cooking.")
        
        # Step 7: Short delay to avoid race conditions
        time.sleep(3)

        # Step 8: Wait for raw karambwans to DISAPPEAR from the bag region
        # i.e., they've all been cooked
        while True:
            # Create the monitor to wait for "raw_karambwan.png" to DISAPPEAR in "bag"
            monitor = ImageMonitor(
                screen_interactor=si,
                image_path="python_bots/image_library/raw_karambwan.png",
                #region="bag",
                confidence=0.98,
                check_interval=1.0,
                wait_for="disappear"
            )
            monitor.start()
            print("Waiting up to 64s for raw karambwans to disappear from bag (fully cooked).")
            if monitor.wait_for_condition(timeout=64):
                # Condition met: The raw karambwan image is gone
                print("Raw karambwans have disappeared (fully cooked).")
                monitor.stop()
                break
            else:
                # Timed out. Check if we still have raw karambwans in the bag
                monitor.stop()
                raw_still_exists = si.find_image_cv2("python_bots/image_library/raw_karambwan.png",
                                                     threshold=0.98)
                if raw_still_exists:
                    print("Timeout, but raw karambwans still remain. Re-clicking oven & pressing space.")
                    try:
                        # Step 6 repeated
                        oven_click_again = si.pixel_click("FF00FF", region="v2", tolerance=10,
                                                          offset_range_x=(25, 60), offset_range_y=(15, 25))
                        print(f"Oven re-clicked at {oven_click_again}.")
                    except Exception as e:
                        print(f"Oven not found on re-click attempt: {e}")
                        break
                    time.sleep(random.uniform(1, 1.5))
                    pyautogui.press("space")
                    print("Spacebar pressed again for leftover karambwans.")
                    # Then we loop again, waiting for them to disappear
                else:
                    print("Timeout, but apparently no raw karambwans found. Moving on.")
                    break 
        
        # Step 9: Click the bank chest again for deposit
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)
        # while we don't see bank close, repeat the step to click the bank
        iteration = 0
        while not bank_close_button and iteration < 20:
            print("Bank not open yet. Clicking bank chest.")
            try:
                bank_chest_click = si.pixel_click("00FFFF", region="v2", tolerance=10, 
                                                  offset_range_x=(25, 60), offset_range_y=(15, 25))
                print(f"Bank chest clicked at {bank_chest_click}.")
                iteration += 1
            except Exception as e:
                print(f"Bank chest not found or error: {e}. Trying again.")

            time.sleep(random.uniform(2.8, 3.4))
            bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)

        # bank is now open, withdraw karambwans
        print("Bank open. Depositing cooked/burnt karambwans.")
        
        # Step 11: Deposit burnt and cooked karambwans
        bag_region = si.get_scan_area("bag")
        burnt_click = si.click_image_cv2_without_moving("python_bots/image_library/burnt_karambwan.png",
                                                        region=bag_region, confidence=0.98, offset_range=(0, 2))
        if burnt_click:
            print(f"Burnt karambwan clicked at {burnt_click} for deposit.")
            time.sleep(random.uniform(0.1, 0.3))
        else:
            print("No burnt karambwan found in inventory for deposit.")

        cooked_click = si.click_image_cv2_without_moving("python_bots/image_library/cooked_karambwan.png",
                                                         region=bag_region, confidence=0.98, offset_range=(0, 2))
        if cooked_click:
            print(f"Cooked karambwan clicked at {cooked_click} for deposit.")
            time.sleep(random.uniform(0.1, 0.3))
        else:
            print("No cooked karambwan found in inventory for deposit.")
        
        print(f"Loop {loop} complete.\n")
    
    print("Cooking bot main loop finished.")

if __name__ == "__main__":
    main_loop(max_loops=354)
