import time
import pyautogui
import random
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor

def setup_bank(si):
    """Initial setup: Open bank and withdraw items with proper quantity setup"""
    print("Starting setup...")
    
    # Zoom out for better visibility
    print("Zooming out...")
    si.zoom_out(times=3, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))
    
    # First check if bank is already open
    bank_close_location = si.find_image_cv2('python_bots/image_library/bank_close.png', threshold=0.9)
    if bank_close_location:
        print("Bank is already open")
    else:
        # Step 1: Open bank chest using teal pixels
        try:
            bank_chest_click = si.pixel_click("00FFFF", region="center", tolerance=10, 
                                              offset_range_x=(0, 4), offset_range_y=(0, 4))
            time.sleep(random.uniform(1, 1.5))
            print(f"Bank chest clicked at {bank_chest_click}.")
        except Exception as e:
            print(f"Bank chest not found: {e}")
            return False
        
        # Wait for bank to open
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.90)
        iteration = 0
        while not bank_close_button and iteration < 20:
            print("Bank not open. Re-clicking bank chest.")
            try:
                bank_chest_click = si.pixel_click("00FFFF", region="v2", tolerance=10, 
                                                  offset_range_x=(25, 60), offset_range_y=(10, 25))
                print(f"Bank chest clicked at {bank_chest_click}.")
                iteration += 1
            except Exception as e:
                print(f"Bank chest not found or error: {e}. Trying again.")
            time.sleep(random.uniform(1, 1.5))
            bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.90)

    # deposit all inventory (can comment this out if you're double dipping)
    deposit_success = si.click_image_cv2_without_moving("python_bots/image_library/deposit_all_inventory.png",
                                                           confidence=0.90, offset_range=(0, 2))
    if deposit_success:
        print(f"Inventory deposited at {deposit_success}.")
    else:
        print("Deposit all inventory button not found.")
    time.sleep(1)

    # Check for required items
    print("Checking for required items...")
    
    # Check for bucket of sand and soda ash
    sand_location = si.find_image_cv2('python_bots/image_library/bucket_of_sand.png', threshold=0.90)
    soda_ash_location = si.find_image_cv2('python_bots/image_library/soda_ash.png', threshold=0.90)
    
    if not sand_location or not soda_ash_location:
        print("Required items not found in bank. Stopping script.")
        return False
    
    # Check and set X quantity if needed
    x_quantity_not_active = si.find_image_cv2('python_bots/image_library/bank_x_quantity_is_NOT_active.png', threshold=0.90)
    if x_quantity_not_active:
        pyautogui.moveTo(x_quantity_not_active[0], x_quantity_not_active[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Set X quantity option")
    else:
        print("X quantity is already active or could not find X quantity option.")
    
    # Withdraw bucket of sand with quantity 14
    print("Withdrawing bucket of sand...")
    pyautogui.moveTo(sand_location[0], sand_location[1])

    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.click(button='right')
    time.sleep(random.uniform(0.4, 1.2))
    
    # Try to find and click "Withdraw-14" first
    withdraw_14_location = si.find_image_cv2('python_bots/image_library/withdraw-14.png', threshold=0.93)
    if withdraw_14_location:
        pyautogui.moveTo(withdraw_14_location[0], withdraw_14_location[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Clicked 'Withdraw-14'")
    else:
        print("Could not find withdraw-14 option. Trying withdraw-X option.")
        # Try withdraw-x option
        withdraw_x_location = si.find_image_cv2('python_bots/image_library/withdraw-X.png', threshold=0.85)
        if withdraw_x_location:
            pyautogui.moveTo(withdraw_x_location[0], withdraw_x_location[1])
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.click()
            time.sleep(random.uniform(0.5, 0.7))
            pyautogui.write('1')
            time.sleep(random.uniform(0.2, 0.3))
            pyautogui.write('4')
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.press('enter')
            print("Entered withdraw amount: 14")
        else:
            print("Could not find withdraw options. Stopping script.")
            return False
    
    # Withdraw soda ash
    print("Withdrawing soda ash.")
    withdraw_soda_success = si.click_image_cv2_without_moving("python_bots/image_library/soda_ash.png",
                                                        confidence=.90, offset_range=(0, 2))
    if withdraw_soda_success:
        print(f"Soda ash withdrawn at {withdraw_soda_success}.")
    else:
        print("Soda ash not found for withdrawal. Trying the loop again.")
    time.sleep(random.uniform(0.3, 1.1))
    
    # Close bank
    print("Closing bank...")
    bank_close_click = si.click_image_cv2_without_moving("python_bots/image_library/bank_close.png",
                                                         region="v2", confidence=0.95, offset_range=(1, 4))
    if bank_close_click:
        print(f"Bank closed at {bank_close_click}.")
    else:
        print("Bank close button not found. Continuing...")
    
    return True

def main_loop(max_loops=50):
    si = ScreenInteractor()
    
    # Initial setup - withdraw the 3 main items once
    if not setup_bank(si):
        print("Setup failed. Exiting.")
        return
    
    for loop in range(1, max_loops + 1):
        print(f"\n--- Starting loop {loop} of {max_loops} ---")
        
        # Step 1: Click the furnace (pink = FF00FF)
        try:
            furnace_click = si.pixel_click("FF00FF", region="v2", tolerance=10, 
                                           offset_range_x=(0, 8), offset_range_y=(0, 8))
            print(f"Furnace clicked at {furnace_click}.")
        except Exception as e:
            print(f"Furnace not found or error: {e}. Skipping loop iteration.")
            continue
        print("Waiting 7-9 seconds for walk to furnace...")
        time.sleep(random.uniform(5.5, 6.5))  # Wait for walk to furnace

        # Step 2: Press space to initiate glass blowing
        pyautogui.press("space")
        print("Spacebar pressed to start glass blowing.")

        # Step 3: Wait for glass blowing to finish
        print("Waiting 17-21 seconds for molten glass to be made...")
        time.sleep(random.uniform(17, 25))

        # Step 4: Click the bank chest for deposit
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.90)
        iteration = 0
        while not bank_close_button and iteration < 20:
            print("Bank not open yet. Clicking bank chest.")
            try:
                bank_chest_click = si.pixel_click("00FFFF", region="center", tolerance=0, 
                                                  offset_range_x=(0, 8), offset_range_y=(0, 8))
                print(f"Bank chest clicked at {bank_chest_click}.")
                iteration += 1
            except Exception as e:
                print(f"Bank chest not found or error: {e}. Trying again.")

            print("Waiting 6-8 seconds for return walk to bank...")
            time.sleep(random.uniform(5, 6.5))  # Wait for return walk to bank
            bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.90)
            time.sleep(random.uniform(1.5, 2.5))
        
        if (loop % 12 == 0):
            delay = random.triangular(1.5, 45.5, 1.5)
            print(f"Waiting {delay} extra seconds... for more human...")
            time.sleep(delay)
        
        print("Bank open. Depositing molten glass and buckets.")
        
        # Step 5: Deposit all inventory
        deposit_success = si.click_image_cv2_without_moving("python_bots/image_library/deposit_all_inventory.png",
                                                           confidence=0.90, offset_range=(0, 2))
        if deposit_success:
            print(f"Inventory deposited at {deposit_success}.")
        else:
            print("Deposit all inventory button not found.")
        time.sleep(1)

        # Step 6: Withdraw bucket of sand
        print("Withdrawing bucket of sand.")
        withdraw_sand_success = si.click_image_cv2_without_moving("python_bots/image_library/bucket_of_sand.png",
                                                         confidence=.90, offset_range=(0, 2))
        if withdraw_sand_success:
            print(f"Bucket of sand withdrawn at {withdraw_sand_success}.")
        else:
            print("Bucket of sand not found for withdrawal. Trying the loop again.")
            continue
        time.sleep(random.uniform(0.3, 0.7))

        # Step 7: Withdraw soda ash
        print("Withdrawing soda ash.")
        withdraw_soda_success = si.click_image_cv2_without_moving("python_bots/image_library/soda_ash.png",
                                                         confidence=.90, offset_range=(0, 2))
        if withdraw_soda_success:
            print(f"Soda ash withdrawn at {withdraw_soda_success}.")
        else:
            print("Soda ash not found for withdrawal. Trying the loop again.")
            continue
        time.sleep(random.uniform(0.3, 0.7))

        # Step 8: Close the bank
        bank_close_click = si.click_image_cv2_without_moving("python_bots/image_library/bank_close.png",
                                                             region="v2", confidence=0.95, offset_range=(1, 4))
        # if bank_close_click:
        #     print(f"Bank closed at {bank_close_click}.")
        # else:
        #     print("Bank close button not found. Continuing...")

        print(f"Loop {loop} complete.\n")
    
    print("Molten glass blowing bot main loop finished.")

if __name__ == "__main__":
    main_loop(max_loops=237) 