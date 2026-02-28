import time
import pyautogui
import random
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor
from pixel_monitor import PixelMonitor

def setup_mining(si):
    """Initial setup: Zoom out and open inventory"""
    print("Starting sandstone mining setup...")
    
    # Zoom out for better visibility of all mining targets
    print("Zooming out for better mining visibility...")
    si.zoom_out(times=5, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))
    
    # Zoom in slightly to get the right zoom level
    print("Zooming in slightly to get optimal zoom level...")
    si.zoom_in(times=2, delay_low=0.005, delay_high=0.01, scroll_amount=350)
    time.sleep(random.uniform(0.5, 1.0))
    
    # Open inventory with 'b' key
    print("Opening inventory...")
    pyautogui.press('b')
    time.sleep(random.uniform(0.5, 1.0))
    
    print("Sandstone mining setup complete.")
    return True

def mine_red_sandstone(si):
    """Mine RED sandstone node"""
    print("Mining RED sandstone...")
    
    # Locate & click the visible red rock within game_screen_middle_horizontal
    try:
        red_click = si.pixel_click_without_moving("FF0000", region="game_screen_middle_horizontal", tolerance=0, 
                                                 offset_range_x=(3, 15), offset_range_y=(3, 15))
        print(f"RED sandstone clicked at {red_click}.")
    except Exception as e:
        print(f"RED sandstone not found or error: {e}.")
        return False
    
    # Wait 1.5 seconds for walk to node
    print("Waiting 1 seconds for walk to RED node...")
    time.sleep(1)

    # Check inventory again before next mining attempt
    if check_inventory_full(si):
        print("Inventory full detected! Processing sandstone...")
        if process_inventory(si):
            print("Inventory processed successfully.")
            time.sleep(1.5)
        else:
            print("Failed to process inventory.")
    
    # pixel_monitor on bottom_of_char_zoom_8 for RED until RED disappears
    red_monitor = PixelMonitor(
        screen_interactor=si,
        color_hex="FF0000",  # RED color
        region="bottom_of_char_zoom_8",
        tolerance=1,
        check_interval=0.2,
        wait_for="disappear"
    )
    red_monitor.start()
    print("Waiting for RED sandstone to deplete...")
    if red_monitor.wait_for_condition(timeout=8):
        print("RED sandstone depleted.")
        red_monitor.stop()
        return True
    else:
        print("Timeout waiting for RED sandstone to deplete.")
        red_monitor.stop()
        return False

def mine_teal_sandstone_center(si):
    """Mine first TEAL node – center"""
    print("Mining TEAL sandstone (center)...")
    
    # Debug: Show the region being used
    region = si.get_scan_area("game_screen_middle_horizontal")
    print(f"Searching in region: {region}")
    
    # Find and click closest TEAL pixel with local search
    coords = si.find_closest_pixel_without_moving("00FFFF", tolerance=0, local_search_size=10, 
                                                 offset_range_x=(-10, 5), offset_range_y=(3, 15))
    if coords:
        print(f"TEAL center node clicked at {coords}.")
    else:
        print("TEAL center node not found.")
        return False
    
    # Wait 1.5 seconds for walk to node
    print("Waiting 1.5 seconds for walk to TEAL center node...")
    time.sleep(1.5)

    # Check inventory again before next mining attempt
    if check_inventory_full(si):
        print("Inventory full detected! Processing sandstone...")
        if process_inventory(si):
            print("Inventory processed successfully.")
            time.sleep(1.5)
        else:
            print("Failed to process inventory.")
    
    # pixel_monitor on bottom_of_char_zoom_8 for TEAL until TEAL disappears
    teal_monitor = PixelMonitor(
        screen_interactor=si,
        color_hex="00FFFF",  # TEAL color
        region="bottom_of_char_zoom_8",
        tolerance=1,
        check_interval=0.2,
        wait_for="disappear"
    )
    teal_monitor.start()
    print("Waiting for TEAL center node to deplete...")
    if teal_monitor.wait_for_condition(timeout=8):
        print("TEAL center node depleted.")
        teal_monitor.stop()
        return True
    else:
        print("Timeout waiting for TEAL center node to deplete.")
        teal_monitor.stop()
        return False

def mine_teal_sandstone_left(si):
    """Mine second TEAL node – left"""
    print("Mining TEAL sandstone (left)...")
    
    # Debug: Show the region being used
    region = si.get_scan_area("game_screen_middle_horizontal")
    print(f"Searching in region: {region}")
    
    # Find and click closest TEAL pixel with local search (should return left node now)
    coords = si.find_closest_pixel_without_moving("00FFFF", tolerance=0, local_search_size=15, 
                                                 offset_range_x=(-5, 0), offset_range_y=(-5, 5))
    if coords:
        print(f"TEAL left node clicked at {coords}.")
    else:
        print("TEAL left node not found.")
        return False
    
    # Wait 1.5 seconds for walk to node
    print("Waiting 1.5 seconds for walk to TEAL left node...")
    time.sleep(1.5)

    # Check inventory again before next mining attempt
    if check_inventory_full(si):
        print("Inventory full detected! Processing sandstone...")
        if process_inventory(si):
            print("Inventory processed successfully.")
            time.sleep(1.5)
        else:
            print("Failed to process inventory.")
        
    # pixel_monitor on left_of_char_zoom_8 for TEAL until TEAL disappears
    teal_monitor = PixelMonitor(
        screen_interactor=si,
        color_hex="00FFFF",  # TEAL color
        region="left_of_char_zoom_8",
        tolerance=1,
        check_interval=0.2,
        wait_for="disappear"
    )
    teal_monitor.start()
    print("Waiting for TEAL left node to deplete...")
    if teal_monitor.wait_for_condition(timeout=8):
        print("TEAL left node depleted.")
        teal_monitor.stop()
        return True
    else:
        print("Timeout waiting for TEAL left node to deplete.")
        teal_monitor.stop()
        return False

def process_inventory(si):
    """Process inventory when full"""
    print("Inventory full, processing sandstone...")
    
    # Click anywhere in game_screen_middle_horizontal (pink rock-crusher)
    try:
        crusher_click = si.pixel_click("FF00FF", region="game_screen_middle_horizontal", tolerance=0, 
                                       offset_range_x=(0, 8), offset_range_y=(0, 8))
        print(f"Rock crusher clicked at {crusher_click}.")
    except Exception as e:
        print(f"Rock crusher not found or error: {e}.")
        return False
    
    # Sleep 6–8 s (walk + crush)
    print("Waiting 6-8 seconds for walk + crush...")
    time.sleep(random.uniform(6, 8))
    
    # Return to the red mining node
    print("Returning to red mining node...")
    try:
        red_mining_click = si.pixel_click("FF0000", region="game_screen_middle_horizontal", tolerance=0, 
                                      offset_range_x=(5, 15), offset_range_y=(10, 15))
        print(f"red pixel square clicked at {red_mining_click}.")
    except Exception as e:
        print(f"red pixel square not found or error: {e}.")
        return False
    
    # Sleep 6–8 s for walk back
    print("Waiting 6-8 seconds for walk back...")
    time.sleep(random.uniform(6, 8))
    
    return True

def check_inventory_full(si):
    """Check if inventory is full by looking for inventory_full.png in chat area"""
    print("Checking inventory status...")
    inventory_full = si.find_image_cv2("python_bots/image_library/inventory_full.png",
                                       region="chat_area", threshold=0.85)
    if inventory_full:
        print(f"Inventory full detected at coordinates: {inventory_full}")
        return True
    else:
        print("Inventory not full - continuing with mining")
        return False

def main_loop(max_loops=500):
    si = ScreenInteractor()
    
    # Initial setup
    if not setup_mining(si):
        print("Setup failed. Exiting.")
        return
    
    loop_count = 0
    try:
        while loop_count < max_loops:
            loop_count += 1
            print(f"\n--- Starting mining loop {loop_count} ---")
            
            # 2.2 Mine RED sandstone
            if not mine_red_sandstone(si):
                print("Failed to mine RED sandstone. Continuing...")
                continue
            
            # 2.3 Mine first TEAL node – center
            if not mine_teal_sandstone_center(si):
                print("Failed to mine TEAL center node. Continuing...")
                continue
            
            # 2.4 Mine second TEAL node – left
            if not mine_teal_sandstone_left(si):
                print("Failed to mine TEAL left node. Continuing...")
                continue
            
            # 2.5 Return to RED & repeat
            print("Completed mining cycle. Returning to RED node...")
            
    except KeyboardInterrupt:
        print("Manual interruption detected. Exiting loop.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Sandstone mining bot finished.")

if __name__ == "__main__":
    main_loop(max_loops=500) 