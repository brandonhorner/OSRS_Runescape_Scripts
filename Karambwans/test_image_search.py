import pyautogui
import cv2
import numpy as np
import time

def find_image_on_screen(image_path):
    """Find the center coordinates of the image on the screen using OpenCV."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # Set a threshold for the match
    threshold = 0.8
    if max_val > threshold:
        img_width, img_height = img.shape[1], img.shape[0]
        top_left = max_loc
        center = (top_left[0] + img_width // 2, top_left[1] + img_height // 2)
        return center
    else:
        return None

def click_image(image_path):
    """Click the image on the screen without moving the cursor."""
    position = find_image_on_screen(image_path)
    if position:
        x, y = position
        pyautogui.click(x=x, y=y)
    else:
        print(f"Image not found: {image_path}")

def main():
    # Paths to the images
    raw_karambwan_img_path = 'C:/Git/OSRS_Runescape_Scripts/Karambwans/raw_karambwan.png'
    cooked_karambwan_path = 'C:/Git/OSRS_Runescape_Scripts/Karambwans/cooked_karambwan.png'
    burnt_karambwan_path = 'C:/Git/OSRS_Runescape_Scripts/Karambwans/burnt_karambwan.png'

    # Wait for 2 seconds
    time.sleep(2)

    # Click the third image
    click_image(burnt_karambwan_path)

    # Click the first image
    click_image(raw_karambwan_img_path)

    # Click the second image
    click_image(cooked_karambwan_path)

if __name__ == "__main__":
    main()