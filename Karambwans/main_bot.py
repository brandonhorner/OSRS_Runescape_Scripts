# main_bot.py
import time
import random
import pyautogui
from screen_interactor import ScreenInteractor
from karambwan_bot import KarambwanBot
from chat_monitor import ChatMonitor

def main_loop(max_loops=50):
    # Create your interactor and bot objects.
    si = ScreenInteractor()

    # Step 0: Zoom out.
    print("Zooming out...")
    si.zoom_out(times=10)
    time.sleep(random.uniform(1.5, 2.5))

    # Zoom in
    print("Zoom in to reset camera.")
    si.zoom_in(times=1)
    time.sleep(random.uniform(1.5, 2.5))

    try:
        for loop in range(1, max_loops+1):
            print(f"\n--- Starting loop {loop} of {max_loops} ---")
            
            # For each loop, create a new ChatMonitor instance.
            chat_region = si.get_scan_area("chat")
            chat_monitor = ChatMonitor(chat_region=chat_region)
            chat_monitor.start()

            # Zoom in
            print("Zoom in to reset camera.")
            si.zoom_in(times=1)
            time.sleep(random.uniform(1.5, 2.5))

            # Step 1: Click on the fishing spot using the raw karambwan image.
            fishing_spot_image = 'Karambwans/raw_karambwan.png'
            # Use the "center" area for the top-middle of the screen.
            center_region = si.get_scan_area("center")
            fishing_spot_click = si.click_image_without_moving(fishing_spot_image, region=center_region, confidence=0.8, offset_range=(0, 3))
            print(f"Fishing spot (raw karambwan) clicked at {fishing_spot_click}.")

            # Step 2: Wait for the chat to indicate that inventory is full.
            print("Waiting for chat message that indicates inventory is full...")
            if chat_monitor.wait_for_message(timeout=600):
                print("Chat message detected: cannot catch more karambwans.")
            else:
                print("Timeout reached without detecting the chat message.")

            # Stop the current chat monitor for this round.
            chat_monitor.stop()

            # Use the "v2" area (middle vertical third) to search for pink pixels.
            v2_region = si.get_scan_area("v2")
            pink_click = si.pixel_click("FF00FF", region=v2_region, tolerance=5, 
                                         offset_range_x=(30, 30), offset_range_y=(30, 30), button='left')
            print(f"Pink fairy ring clicked at {pink_click}.")

            # Step 4: Wait for teleport to complete.
            time.sleep(random.uniform(8, 10))

            # Zoom out
            print("Zooming out...")
            si.zoom_out(times=1)
            time.sleep(random.uniform(3, 4))

            # Step 5: Click on the yellow tile in the bank approach.
            # Use the "p1" area for the top-left of the screen.
            p1_region = si.get_scan_area("p1")
            yellow_click = si.pixel_click("FFFF00", region=p1_region, tolerance=5,
                                         offset_range_x=(10, 30), offset_range_y=(10, 30), button='left')
            print(f"Yellow tile clicked at {yellow_click}.")

            time.sleep(random.uniform(12, 15))

            # Step 6: Click on the bank booth (highlighted by teal pixels) in p1.
            bank_booth_click = si.pixel_click("00FFFF", region=p1_region, tolerance=5,
                                               offset_range_x=(5, 10), offset_range_y=(5, 10), button='left')
            print(f"Bank booth clicked at {bank_booth_click}.")

            time.sleep(random.uniform(13, 15))

            # Step 7: Deposit items by clicking on the fish barrel and raw karambwans in the bag.
            bag_region = si.get_scan_area("bag")
            fish_barrel_click = si.click_image_without_moving('Karambwans/fish_barrel.png', region=bag_region, confidence=0.8, offset_range=(0, 3))
            print(f"Fish barrel clicked at {fish_barrel_click}.")
            time.sleep(random.uniform(0.2, 0.5))
            raw_karambwan_click = si.click_image_without_moving('Karambwans/raw_karambwan.png', region=bag_region, confidence=0.88, offset_range=(0, 3))
            print(f"Raw karambwan clicked at {raw_karambwan_click}.")
            time.sleep(random.uniform(0.2, 0.5))

            # Step 8: Close the bank interface by clicking a yellow tile in the "p6" area.
            p6_region = si.get_scan_area("p6")
            close_bank_click = si.pixel_click("FFFF00", region=p6_region, tolerance=5,
                                               offset_range_x=(10, 30), offset_range_y=(10, 30), button='left')
            print(f"Bank interface closed by clicking yellow tile at {close_bank_click}.")
            time.sleep(random.uniform(12, 15))

            # Step 9: Click on the pink fairy ring in p6 to teleport back to the fishing spot.
            pink_return_click = si.pixel_click("FF00FF", region=p6_region, tolerance=5,
                                                offset_range_x=(15, 30), offset_range_y=(15, 30), button='left')
            print(f"Pink fairy ring clicked for return at {pink_return_click}.")
            time.sleep(random.uniform(13, 15))

            print(f"Loop {loop} complete.")
            
    except KeyboardInterrupt:
        print("Manual interruption detected. Exiting loop.")
    finally:
        print("Main loop finished.")

if __name__ == "__main__":
    main_loop()
