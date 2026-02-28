"""Quick test: wait 3s then check if bank close button is visible on screen."""
import time
from screen_interactor import ScreenInteractor

BANK_CLOSE_IMAGE = "image_library/bank_deposit_close.png"

def main():
    si = ScreenInteractor()
    print("Open the bank deposit interface now. Checking in 3 seconds...")
    time.sleep(3)
    # Use silent version to avoid console Unicode issues with find_image_cv2's checkmark
    loc = si.find_image_cv2_silent(BANK_CLOSE_IMAGE, region=None, threshold=0.85)
    if loc:
        print("YES - Found bank close button at", loc)
    else:
        print("NO - Bank close button not found on screen (tried threshold 0.85)")

if __name__ == "__main__":
    main()
