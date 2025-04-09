import pyautogui
import time
import random
from PIL import Image, ImageChops  # if needed for additional processing
import cv2
import numpy as np

class ScreenInteractor:
    def __init__(self):
        pass

    def get_scan_area(self, label):
        screen_width, screen_height = pyautogui.size()
        # todo: Offset these in the x direction if menu is open (check if combat tab (active or not) is on screen)
        areas = {
            "game_screen": (0, 90, screen_width - 280, screen_height - 245),
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
            "chat": (0, screen_height - 200, 500, screen_height - 72),
            "activity_pane": (0, 22, 150, 250)
        }
        return areas.get(label, (0, 0, screen_width, screen_height))
        
    def resolve_region(self, region):
        """If region is a string, look it up using get_scan_area; otherwise return it directly."""
        if isinstance(region, str):
            return self.get_scan_area(region)
        return region

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

    def pixel_click(self, color, region, tolerance=10, offset_range_x=(10, 30), offset_range_y=(10, 30), button='left'):
        region = self.resolve_region(region)
        found_pixel = self.find_pixel(color, region=region, tolerance=tolerance)
        if not found_pixel:
            raise ValueError(f"{color} pixel not found in region {region}.")
        offset_x = random.randint(*offset_range_x)
        offset_y = random.randint(*offset_range_y)
        target_x = found_pixel[0] + offset_x
        target_y = found_pixel[1] + offset_y
        original = pyautogui.position()
        pyautogui.moveTo(target_x, target_y)
        time.sleep(random.uniform(0.05, 0.1))
        self.click_without_moving(button=button)
        pyautogui.moveTo(original)
        return (target_x, target_y)

    def find_image_cv2(self, image_path, region=None, threshold=0.98):
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        # Load the template image and convert to BGR
        target = cv2.imread(image_path)
        if target is None:
            print(f"Failed to load image: {image_path}")
            return None

        if region:
            screenshot = pyautogui.screenshot(region=region)
            region_offset = (region[0], region[1])
        else:
            screenshot = pyautogui.screenshot()
            region_offset = (0, 0)
            
        # Convert screenshot to BGR format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Ensure both images are in the same format
        if target.shape[2] != screenshot_cv.shape[2]:
            if target.shape[2] == 4:  # If template has alpha channel
                target = cv2.cvtColor(target, cv2.COLOR_BGRA2BGR)
            elif screenshot_cv.shape[2] == 4:
                screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGRA2BGR)
        
        result = cv2.matchTemplate(screenshot_cv, target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            target_h, target_w = target.shape[:2]
            top_left = max_loc
            center = (top_left[0] + target_w // 2, top_left[1] + target_h // 2)
            center = (center[0] + region_offset[0], center[1] + region_offset[1])
            return center
        else:
            return None

    def find_all_images_cv2(self, image_path, region=None, threshold=0.98):
        """Find all instances of an image in the specified region that match above the threshold.
        Returns a list of center coordinates for each match."""
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        # Load the template image and convert to BGR
        target = cv2.imread(image_path)
        if target is None:
            print(f"Failed to load image: {image_path}")
            return []

        if region:
            screenshot = pyautogui.screenshot(region=region)
            region_offset = (region[0], region[1])
        else:
            screenshot = pyautogui.screenshot()
            region_offset = (0, 0)
            
        # Convert screenshot to BGR format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Ensure both images are in the same format
        if target.shape[2] != screenshot_cv.shape[2]:
            if target.shape[2] == 4:  # If template has alpha channel
                target = cv2.cvtColor(target, cv2.COLOR_BGRA2BGR)
            elif screenshot_cv.shape[2] == 4:
                screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGRA2BGR)
        
        # Get template dimensions
        target_h, target_w = target.shape[:2]
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_cv, target, cv2.TM_CCOEFF_NORMED)
        
        # Find all locations where the match is above threshold
        locations = np.where(result >= threshold)
        matches = []
        
        # Convert locations to center coordinates
        for pt in zip(*locations[::-1]):
            center = (pt[0] + target_w // 2, pt[1] + target_h // 2)
            # Add region offset to get screen coordinates
            center = (center[0] + region_offset[0], center[1] + region_offset[1])
            matches.append(center)
        
        return matches

    def click_image_cv2_without_moving(self, image_path, region=None, confidence=0.8, offset_range=(-10, 10)):
        center = self.find_image_cv2(image_path, region=region, threshold=confidence)
        if center is None:
            print(f"Image not found: {image_path}")
            return None
        offset_x = random.randint(*offset_range)
        offset_y = random.randint(*offset_range)
        target = (center[0] + offset_x, center[1] + offset_y)
        original = pyautogui.position()
        pyautogui.moveTo(target)
        time.sleep(random.uniform(0.05, 0.1))
        self.click_without_moving(button='left')
        pyautogui.moveTo(original)
        return target

    def click_image_cv2(self, image_path, region=None, confidence=0.8, offset_range_x=(-7, 7), offset_range_y=(-7, 7), sleep_after=None, click_type='left'):
        """Click on an image with separate x and y offset ranges and optional sleep after clicking.
        
        Args:
            image_path: Path to the image file to find and click
            region: Region to search in (can be string label or tuple)
            confidence: Confidence threshold for image matching
            offset_range_x: Tuple of (min, max) for random x offset from center
            offset_range_y: Tuple of (min, max) for random y offset from center
            sleep_after: If provided, sleep for random time between (min, max) after clicking
            click_type: Type of click to perform ('left', 'right', or 'double')
        
        Returns:
            Tuple of (x, y) click coordinates or None if image not found
        """
        center = self.find_image_cv2(image_path, region=region, threshold=confidence)
        if center is None:
            print(f"Image not found: {image_path}")
            return None
            
        offset_x = random.randint(*offset_range_x)
        offset_y = random.randint(*offset_range_y)
        target = (center[0] + offset_x, center[1] + offset_y)
        pyautogui.moveTo(target)
        time.sleep(random.uniform(0.05, 0.1))
        
        if click_type == 'right':
            pyautogui.click(button='right')
        elif click_type == 'double':
            pyautogui.click()
            # Human-like delay between double clicks (typically 100-200ms)
            time.sleep(random.uniform(0.1, 0.2))
            pyautogui.click()
        else:  # default to left click
            pyautogui.click()
        
        if sleep_after is not None:
            time.sleep(random.uniform(*sleep_after))
            
        return target
    
    def move_mouse_to(self, x, y):
        pyautogui.moveTo(x, y)

    def click_without_moving(self, button='left'):
        current_x, current_y = pyautogui.position()
        pyautogui.mouseDown(x=current_x, y=current_y, button=button)
        pyautogui.mouseUp(x=current_x, y=current_y, button=button)
        return (current_x, current_y)

    def check_region_color(self, region, expected_color_hex, tolerance=10, samples=3):
        # Ensure region is a tuple of ints
        region = tuple(int(x) for x in region)
        expected_color = tuple(int(expected_color_hex[i:i+2], 16) for i in (0, 2, 4))
        screenshot = pyautogui.screenshot(region=region).convert("RGB")
        width, height = screenshot.size
        center = (width // 2, height // 2)
        center_color = screenshot.getpixel(center)
        print(f"Checking region color, center pixel: {center_color}, expected: {expected_color}")
        if center_color[0] < 20 and center_color[1] < 20 and center_color[2] < 20:
            for _ in range(samples):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                sample_color = screenshot.getpixel((x, y))
                print(f"Sampled color at ({x},{y}): {sample_color}")
                if all(abs(sample_color[i] - expected_color[i]) <= tolerance for i in range(3)):
                    return True
            return False
        else:
            return all(abs(center_color[i] - expected_color[i]) <= tolerance for i in range(3))


    def click_image_without_moving(self, image_path, region=None, confidence=0.8, offset_range=(-10, 10),
                                   expected_color=None, color_tolerance=10, color_samples=3):
        try:
            location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        except Exception:
            return None
        if not location:
            return None

        if expected_color is not None:
            if not self.check_region_color(location, expected_color, tolerance=color_tolerance, samples=color_samples):
                return None

        left, top, width, height = location
        x_target = random.randint(left, left + width - 1) + random.randint(*offset_range)
        y_target = random.randint(top, top + height - 1) + random.randint(*offset_range)
        original = pyautogui.position()
        pyautogui.moveTo(x_target, y_target)
        time.sleep(random.uniform(0.05, 0.1))
        self.click_without_moving(button='left')
        pyautogui.moveTo(original)
        return (x_target, y_target)

    def zoom_out(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=-400):
        screen_width, screen_height = pyautogui.size()
        x, y = screen_width // 6, screen_height // 6
        original = pyautogui.position()
        pyautogui.moveTo(x, y)
        for _ in range(times):
            pyautogui.scroll(scroll_amount)
            time.sleep(random.uniform(delay_low, delay_high))
        pyautogui.moveTo(original)

    def zoom_in(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=400):
        screen_width, screen_height = pyautogui.size()
        x, y = screen_width // 6, screen_height // 6
        original = pyautogui.position()
        pyautogui.moveTo(x, y)
        for _ in range(times):
            pyautogui.scroll(scroll_amount)
            time.sleep(random.uniform(delay_low, delay_high))
        pyautogui.moveTo(original)
