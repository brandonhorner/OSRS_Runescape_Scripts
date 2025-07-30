import time
import pyautogui
import random
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor

def main_loop(max_loops=50):
    si = ScreenInteractor()
    
    # Step 1: Click the bank chest (teal = 00FFFF)
    try:
        bank_chest_click = si.pixel_click("00FFFF", region="v2", tolerance=10, 
                                          offset_range_x=(25, 60), offset_range_y=(10, 25))
        time.sleep(random.uniform(1, 1.5))
        print(f"Bank chest clicked at {bank_chest_click}.")
    except Exception as e:
        print(f"Bank chest not found.. maybe it's open :): {e}.")
    
    for loop in range(1, max_loops + 1):
        print(f"\n--- Starting loop {loop} of {max_loops} ---")
        
        # Step 2: Ensure bank is open
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)
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
            bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)

        # Step 3: (Commented out) Set quantity to 5 if not already set
        # TODO: Set quantity to 5 if not already set (wait for PNG from user)
        # Example: si.click_image_cv2_without_moving("python_bots/image_library/set_quantity_5.png", confidence=0.98)

        # Step 4: Withdraw giant seaweed
        print("Bank open. Withdrawing giant seaweed.")
        withdraw_seaweed_success = si.click_image_cv2_without_moving("python_bots/image_library/giant_seaweed.png",
                                                         confidence=0.98, offset_range=(0, 2))
        if withdraw_seaweed_success:
            print(f"Giant seaweed withdrawn at {withdraw_seaweed_success}.")
        else:
            print("Giant seaweed not found for withdrawal. Trying the loop again.")
            continue
        time.sleep(random.uniform(0.5, 1.0))

        # Step 5: Close the bank
        bank_close_click = si.click_image_cv2_without_moving("python_bots/image_library/bank_close.png",
                                                             region="v2", confidence=0.95, offset_range=(1, 4))
        if bank_close_click:
            print(f"Bank closed at {bank_close_click}.")
        else:
            print("Bank close button not found. Continuing...")

        # Step 6: Click the clay oven (pink = FF00FF)
        try:
            clay_oven_click = si.pixel_click("FF00FF", region="v2", tolerance=10, 
                                             offset_range_x=(25, 60), offset_range_y=(15, 25))
            print(f"Clay oven clicked at {clay_oven_click}.")
        except Exception as e:
            print(f"Clay oven not found or error: {e}. Skipping loop iteration.")
            continue
        time.sleep(random.uniform(3.2, 4.5))
        # Step 7: Press space to initiate cooking
        pyautogui.press("space")
        print("Spacebar pressed to start cooking.")

        # Step 8: Wait for cooking to finish (fixed 15 seconds)
        print("Waiting ~8.5 seconds for giant seaweed to cook...")
        time.sleep(random.uniform(8.4, 9.8))

        # Step 9: Click the bank chest again for deposit
        bank_close_button = si.find_image_cv2("python_bots/image_library/bank_close.png", threshold=0.95)
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

        print("Bank open. Depositing cooked soda ash.")
        # Step 10: Deposit all inventory (soda ash)
        deposit_success = si.click_image_cv2_without_moving("python_bots/image_library/deposit_all_inventory.png",
                                                           confidence=0.98, offset_range=(0, 2))
        if deposit_success:
            print(f"Inventory deposited at {deposit_success}.")
        else:
            print("Deposit all inventory button not found.")
        time.sleep(1)

        print(f"Loop {loop} complete.\n")

    print("Giant seaweed cooking bot main loop finished.")

if __name__ == "__main__":
    main_loop(max_loops=463)