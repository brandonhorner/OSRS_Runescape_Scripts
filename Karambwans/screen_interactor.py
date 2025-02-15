# screen_interactor.py
import pyautogui
import time
import random

class ScreenInteractor:
    def __init__(self):
        pass

    def find_pixel(self, color_hex, region=None, tolerance=10):
        screenshot = pyautogui.screenshot(region=region)
        target_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        width, height = screenshot.size
        for x in range(width):
            for y in range(height):
                current_color = screenshot.getpixel((x, y))
                if all(abs(a - b) <= tolerance for a, b in zip(current_color, target_color)):
                    if region:
                        region_x, region_y, _, _ = region
                        return (region_x + x, region_y + y)
                    return (x, y)
        return None

    def move_mouse_to(self, x, y):
        pyautogui.moveTo(x, y)


    def click_without_moving(self, button='left'):
        current_x, current_y = pyautogui.position()
        pyautogui.mouseDown(x=current_x, y=current_y, button=button)
        pyautogui.mouseUp(x=current_x, y=current_y, button=button)
        return (current_x, current_y)
    

    def click_image_without_moving(self, image_path, region=None, confidence=0.8, offset_range=(-10, 10)):
        """
        Generic method to click an image without moving the cursor visibly.
        Finds the image on the screen, determines a random coordinate within its bounding box
        (with an additional random offset), temporarily moves the mouse there, performs a click,
        and restores the original mouse position.
        Returns the (x, y) coordinates where the click was performed.
        """
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if not location:
            raise ValueError(f"Image '{image_path}' not found on screen.")
        left, top, width, height = location
        x_target = random.randint(left, left + width - 1) + random.randint(*offset_range)
        y_target = random.randint(top, top + height - 1) + random.randint(*offset_range)
        original = pyautogui.position()
        pyautogui.moveTo(x_target, y_target)
        self.click_without_moving(button='left')
        pyautogui.moveTo(original)
        return (x_target, y_target)

    def zoom_out(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=-400):
        screen_width, screen_height = pyautogui.size()
        x, y = screen_width // 2, screen_height // 2
        original = pyautogui.position()
        pyautogui.moveTo(x, y)
        for _ in range(times):
            pyautogui.scroll(scroll_amount)
            time.sleep(random.uniform(delay_low, delay_high))
        pyautogui.moveTo(original)

    def zoom_in(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=400):
        screen_width, screen_height = pyautogui.size()
        x, y = screen_width // 2, screen_height // 2
        original = pyautogui.position()
        pyautogui.moveTo(x, y)
        for _ in range(times):
            pyautogui.scroll(scroll_amount)
            time.sleep(random.uniform(delay_low, delay_high))
        pyautogui.moveTo(original)

    def get_scan_area(self, label):
        """
        Returns a region tuple (x, y, width, height) based on the label.
        Labels (examples):
          - p1, p2, ..., p6: Screen panels (e.g. left-to-right, top-bottom)
          - h1, h2: Horizontal top and bottom halves.
          - v1, v2, v3: Vertical slices.
          - bag, chat: Specific regions.
        Adjust the values as needed for your resolution.
        """
        screen_width, screen_height = pyautogui.size()
        areas = {
            # center should be smilar to p2 and p4, but skinnier. So it's the middle 5th of a 5 panels
            "center": (screen_width // 3, 0, screen_width // 4, screen_height - 50),
            "p1": (0, 0, screen_width // 3, screen_height // 2),
            "p2": (screen_width // 3, 0, screen_width // 3, screen_height // 2),
            "p3": (2 * screen_width // 3, 0, screen_width - 2 * (screen_width // 3), screen_height // 2),
            "p4": (0, screen_height // 2, screen_width // 3, screen_height - screen_height // 2),
            "p5": (screen_width // 3, screen_height // 2, screen_width // 3, screen_height - screen_height // 2),
            "p6": (2 * screen_width // 3, screen_height // 2, screen_width - 2 * (screen_width // 3), screen_height - screen_height // 2),
            "h1": (0, 0, screen_width, screen_height // 2),
            "h2": (0, screen_height // 2, screen_width, screen_height - screen_height // 2),
            "v1": (0, 0, screen_width // 3, screen_height),
            "v2": (screen_width // 3, 0, screen_width // 3, screen_height),
            "v3": (2 * screen_width // 3, 0, screen_width - 2 * (screen_width // 3), screen_height),
            "bag": (screen_width - 243, screen_height - 345, 183, 260),
            "chat": (0, screen_height - 200, 500, 200)
        }
        return areas.get(label, (0, 0, screen_width, screen_height))

    def pixel_click(self, color, region, tolerance=10, offset_range_x=(10, 30), offset_range_y=(10, 30), button='left'):
        """
        Finds a pixel matching the given hex color in the specified region,
        applies a random offset, temporarily moves the mouse there, clicks without moving the visible cursor,
        and then restores the original position.
        Returns the (x, y) coordinates where the click was performed.
        """
        found_pixel = self.find_pixel(color, region=region, tolerance=tolerance)
        if not found_pixel:
            raise ValueError(f"{color} pixel not found in region {region}.")
        offset_x = random.randint(*offset_range_x)
        offset_y = random.randint(*offset_range_y)
        target_x = found_pixel[0] + offset_x
        target_y = found_pixel[1] + offset_y
        original = pyautogui.position()
        pyautogui.moveTo(target_x, target_y)
        self.click_without_moving(button=button)
        pyautogui.moveTo(original)
        return (target_x, target_y)
