from screen_interactor import ScreenInteractor
import time

def test_bank_close_detection():
    si = ScreenInteractor()
    time.sleep(2)
    
    # Test all withdraw options
    withdraw_images = [
        "withdraw-13.png",
        "withdraw-14.png", 
        "withdraw-27.png",
        "withdraw-7.png",
        "withdraw-X.png",
        "withdraw-all.png"
    ]
    
    for image in withdraw_images:
        result = si.find_image_cv2(f"python_bots/image_library/{image}", threshold=0.85)
        if result:
            print(f"{image} found at: {result}")
        else:
            print(f"{image} NOT found on the screen.")

if __name__ == "__main__":
    test_bank_close_detection() 