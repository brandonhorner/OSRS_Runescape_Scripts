from screen_interactor import ScreenInteractor
import time

def test_inventory_full_detection():
    si = ScreenInteractor()
    time.sleep(2)
    
    print("Testing inventory full detection...")
    print("Make sure you have a full inventory of sandstone to test this.")
    
    # Test the inventory full detection
    inventory_full = si.find_image_cv2("python_bots/image_library/inventory_full_sandstone.png", 
                                       region="chat_area", threshold=0.85)
    if inventory_full:
        print(f"inventory_full_sandstone.png found at: {inventory_full}")
    else:
        print("inventory_full_sandstone.png NOT found on the screen.")
        print("Make sure your inventory is full of sandstone and the image file exists.")

if __name__ == "__main__":
    test_inventory_full_detection() 