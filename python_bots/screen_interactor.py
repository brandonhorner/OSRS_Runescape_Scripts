import pyautogui
import time
import random
from PIL import Image, ImageChops  # if needed for additional processing
import cv2
import numpy as np
from math import floor  # Add this import
import os

class ScreenInteractor:
    def __init__(self):
        # Set working directory to python_bots folder (parent of this script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"ScreenInteractor working directory set to: {os.getcwd()}")

    def get_scan_area(self, label):
        screen_width, screen_height = pyautogui.size()
        # todo: Offset these in the x direction if menu is open (check if combat tab (active or not) is on screen)
        runelite_top_margin = floor(screen_height // 62)
        runelite_right_margin = floor(screen_width // 82)
        windows_bottom_margin = floor(screen_height // 62)
        
        runelite_right_menu_area = (screen_width - runelite_right_margin, runelite_top_margin, runelite_right_margin, (screen_height // 2))

        # when adding areas.. calculate them like this:                            y1____________
        # find the top left corner of the area, that will be the x1, y1           x1|        |   |
        # then find the width of the area, that will be w = x2 - x1                 |---w----h---|
        # then find the height of the area, that will be h = y2 - y1                |________|___|  
        # now say your area is starts at 1/3 of the screen's width, you'd want to say screen_width // 3 versus 2560/3,
        # you should also express your width and height in terms of screen_width and screen_height
        # Example: center below, we want to start at 1/3 of the screen's width, and go to 2/3 of the screen's width, it should extend to the height of the screen
        # so we'd say x1:screen_width // 3, y1:runelite_top_margin, width:screen_width // 3, height:screen_height - runelite_top_margin - windows_bottom_margin)
        # use the floor function when you're dividing by numbers with decimals, so the coordinate is a flat integer.
        areas = {
            "game_screen": (0, 90, screen_width - floor(screen_width // 6.7), screen_height - floor(screen_height // 4)),
            "center": (screen_width // 3, runelite_top_margin, screen_width // 3, screen_height - runelite_top_margin - windows_bottom_margin),
            "p1": (0, runelite_top_margin, screen_width // 3, screen_height // 2),
            "p2": (screen_width // 3, runelite_top_margin, screen_width // 3, screen_height // 2),
            "p3": (2 * screen_width // 3, runelite_top_margin, (screen_width // 3) - runelite_right_margin, screen_height // 2),
            "p4": (0, (screen_height // 2) - 1, screen_width // 3, (screen_height // 2) - windows_bottom_margin),
            "p5": (screen_width // 3, (screen_height // 2) - 1, screen_width // 3, (screen_height // 2) - windows_bottom_margin),
            "p6": (2 * screen_width // 3, (screen_height // 2) - 1, (screen_width // 3) - runelite_right_margin, (screen_height // 2) - windows_bottom_margin),
            "h1": (0, windows_bottom_margin, screen_width - runelite_right_margin, screen_height // 2),
            "h2": (0, (screen_height // 2) - 1, screen_width - runelite_right_margin, (screen_height // 2) - windows_bottom_margin),
            "v1": (0, runelite_top_margin, screen_width // 3, screen_height - runelite_top_margin - windows_bottom_margin),
            "v2": (screen_width // 3 - runelite_right_margin, runelite_top_margin, screen_width // 3, screen_height - runelite_top_margin - windows_bottom_margin),
            "v3": (2 * screen_width // 3 - runelite_right_margin, runelite_top_margin, (screen_width // 3) - runelite_right_margin, screen_height - runelite_top_margin - windows_bottom_margin),
            "bag": (screen_width - 306, screen_height - floor(screen_height // 3.34), floor(screen_width // 10.9), floor(screen_height // 4.27)),
            "chat": (floor(screen_width // 320), screen_height - floor(screen_height// 5.69), (screen_width // 4), floor(screen_height // 8.47)),
            "bank_pane": ((screen_width // 3), floor(screen_height // 8.08), floor(screen_width // 5.30), floor(screen_height // 1.62)),
            "bank_pane_with_menus": ((screen_width // 3) - floor(screen_width // 37), floor(screen_height // 18.04), floor(screen_width // 4.03), floor(screen_height // 1.38)),
            "activity_pane": (0, 22, 150, 250),
            "chat_area": (floor(screen_width // 320), screen_height - floor(screen_height// 5.69), (screen_width // 4), floor(screen_height // 8.47)),
            "runelite_right_menu": (screen_width - runelite_right_margin, runelite_top_margin, runelite_right_margin, (screen_height // 2)),
            "game_screen_middle_horizontal": (0, 292, 2525, 950),
            "bottom_of_char_zoom_8": (1245, 743, 1285, 779),
            "left_of_char_zoom_8": (1183, 689, 1228, 723)
        }
        
        # Get the base area
        base_area = areas.get(label, (0, 0, screen_width, screen_height))
        
        # Apply dynamic adjustments for right-side areas that need menu offset
        if label in ["bag", "bank_pane", "bank_pane_with_menus"]:  # Add other right-side areas here as needed
            # Check if RuneLite menu is open
            menu_offset = 0
            
            menu_found = None
            for attempt in range(3):
                try:
                    # Use existing find_image_cv2 function to check for menu
                    menu_found = self.find_image_cv2(
                        'image_library/runelite_menu_is_open.png',
                        region=runelite_right_menu_area,
                        threshold=0.98
                    )
                    if menu_found:
                        if label == "bank_pane" or label == "bank_pane_with_menus":
                            menu_offset = -floor(screen_width // 21)
                        else:
                            menu_offset = -floor(screen_width // 10.6)
                        print(f"RuneLite menu OPEN - applying {menu_offset} offset to {label} search area")
                        break
                except Exception as e:
                    print(f"RuneLite menu check failed on attempt {attempt+1}/3 - treating as CLOSED (no offset)")
                    menu_offset = 0
            
            # Apply offset to X coordinate
            if menu_offset != 0:
                adjusted_area = (base_area[0] + menu_offset, base_area[1], base_area[2], base_area[3])
                return adjusted_area
        return base_area
    
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

    def find_pixel_right_click_confirm(self, pixel_color, confirm_image_path, attempts=10, 
                                     pixel_offset_range_x=(5, 20), pixel_offset_range_y=(5, 20)):
        """
        Find a pixel of specified color, right-click on it, and confirm the right-click menu 
        appears by finding a specific image. This provides more reliable interaction than 
        just assuming a left-click worked.
        
        Args:
            pixel_color: Hex color string to search for (e.g., "00FFFF" for teal)
            confirm_image_path: Path to image that should appear in right-click menu
            attempts: Number of attempts to find and right-click the pixel (default: 5)
            pixel_offset_range_x: Tuple of (min, max) for random x offset from found pixel (default: (5, 20))
            pixel_offset_range_y: Tuple of (min, max) for random y offset from found pixel (default: (5, 20))
        
        Returns:
            True if successful (pixel found, right-clicked, and confirmation image found and clicked)
            False if failed after all attempts
        """
        print(f"find_pixel_right_click_confirm: Searching for {pixel_color} pixel with {confirm_image_path} confirmation")
        
        for attempt in range(1, attempts + 1):
            print(f"  Attempt {attempt}/{attempts}")
            
            # Step 1: Find the pixel
            found_pixel = self.find_pixel(pixel_color, tolerance=5)
            if not found_pixel:
                print(f"    Pixel {pixel_color} not found on attempt {attempt}")
                continue
            
            print(f"    Found {pixel_color} pixel at {found_pixel}")
            
            # Step 2: Calculate offset position and right-click
            offset_x = random.randint(*pixel_offset_range_x)
            offset_y = random.randint(*pixel_offset_range_y)
            target_x = found_pixel[0] + offset_x
            target_y = found_pixel[1] + offset_y
            
            # Ensure target coordinates are within screen bounds
            screen_width, screen_height = pyautogui.size()
            target_x = max(0, min(target_x, screen_width - 1))
            target_y = max(0, min(target_y, screen_height - 1))
            
            # Store original mouse position
            original_pos = pyautogui.position()
            
            # Move to target and right-click
            pyautogui.moveTo(target_x, target_y)
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.click(button='right')
            
            # Step 3: Search for confirmation image in area below and around mouse
            # Search area: x direction ±300, y direction 0 to +300 below mouse
            screen_width, screen_height = pyautogui.size()
            
            # Calculate search region bounds
            left = max(0, target_x - 300)
            right = min(screen_width, target_x + 300)
            top = target_y
            bottom = min(screen_height, target_y + 300)
            
            # Ensure valid region dimensions
            width = right - left
            height = bottom - top
            
            if width <= 0 or height <= 0:
                print(f"    Invalid search region calculated: left={left}, right={right}, top={top}, bottom={bottom}")
                print(f"    Adjusting to valid region...")
                # Fallback to a smaller, guaranteed valid region
                left = max(0, target_x - 100)
                right = min(screen_width, target_x + 100)
                top = target_y
                bottom = min(screen_height, target_y + 200)
                width = right - left
                height = bottom - top
            
            search_region = (left, top, width, height)
            
            print(f"    Searching for confirmation image in region: {search_region}")
            
            # Look for the confirmation image
            try:
                confirm_location = self.find_image_cv2(
                    confirm_image_path, 
                    region=search_region, 
                    threshold=0.95
                )
            except Exception as e:
                print(f"    Error searching for confirmation image: {e}")
                confirm_location = None
            
            if confirm_location:
                print(f"    Confirmation image found at {confirm_location}")
                
                # Step 4: Left-click on the confirmation image with small offset
                click_offset_x = random.randint(-10, 10)
                click_offset_y = random.randint(-4, 4)
                click_x = confirm_location[0] + click_offset_x
                click_y = confirm_location[1] + click_offset_y
                
                # Click on the confirmation option
                pyautogui.moveTo(click_x, click_y)
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.click()
                
                # Return mouse to original position
                pyautogui.moveTo(original_pos)
                
                print(f"    Successfully clicked confirmation image at ({click_x}, {click_y})")
                return True
                
            else:
                print(f"    Confirmation image not found on attempt {attempt}")
                
                # Step 5: Reset mouse position to close any open right-click menus
                # Move up and to the right to close menus
                reset_x = target_x + random.randint(200, 500)
                reset_y = target_y + random.randint(-500, -200)
                
                # Ensure we stay within screen bounds
                screen_width, screen_height = pyautogui.size()
                reset_x = max(0, min(reset_x, screen_width - 1))
                reset_y = max(0, min(reset_y, screen_height - 1))
                
                print(f"    Resetting mouse to ({reset_x}, {reset_y}) to close menus")
                pyautogui.moveTo(reset_x, reset_y)
                time.sleep(random.uniform(0.1, 0.2))
                
                # Return mouse to original position
                pyautogui.moveTo(original_pos)
        
        # If we get here, all attempts failed
        print(f"  Failed to find and confirm {pixel_color} pixel after {attempts} attempts")
        return False

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

    def click_image_cv2_without_moving(self, image_path, region=None, confidence=0.95, offset_range=(0, 3)):
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

    def click_image_cv2(self, image_path, region=None, confidence=0.95, offset_range_x=(-7, 7), offset_range_y=(-7, 7), sleep_after=None, click_type='left'):
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


    def click_image_without_moving(self, image_path, region=None, confidence=0.95, offset_range=(-10, 10),
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

    def find_closest_pixel(self, color_hex, tolerance=1, max_radius=1440, local_search_size=90):
        """Find the closest pixel of the specified color to the center of the screen by expanding search radius.
        Optionally performs a local search around the found pixel to find the top-left most pixel.
        
        Args:
            color_hex: The hex color to search for (e.g. "00FFFF" for teal)
            tolerance: Color matching tolerance
            max_radius: Maximum radius to search from center (default: 1440 for 2560x1440 screen)
            local_search_size: Size of the local search area around the found pixel (default: 90x90)
        
        Returns:
            Tuple of (x, y) coordinates of the closest matching pixel, or None if none found
        """
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        target_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        
        # Start with a small radius and expand
        for radius in range(50, max_radius, 50):
            # Calculate search area
            left = max(0, center_x - radius)
            right = min(screen_width, center_x + radius)
            top = max(0, center_y - radius)
            bottom = min(screen_height, center_y + radius)
            
            # Take screenshot of the current search area
            screenshot = pyautogui.screenshot(region=(int(left), int(top), int(right - left), int(bottom - top)))
            
            # Convert to numpy array for faster processing
            pixels = np.array(screenshot)
            
            # Find all pixels that match the target color within tolerance
            matches = np.where(
                (np.abs(pixels[:, :, 0] - target_color[0]) <= tolerance) &
                (np.abs(pixels[:, :, 1] - target_color[1]) <= tolerance) &
                (np.abs(pixels[:, :, 2] - target_color[2]) <= tolerance)
            )
            
            if len(matches[0]) > 0:
                # Calculate distances to center for all matches
                distances = np.sqrt(
                    (matches[0] + top - center_y) ** 2 +
                    (matches[1] + left - center_x) ** 2
                )
                
                # Find the closest match
                closest_idx = np.argmin(distances)
                closest_y = matches[0][closest_idx] + top
                closest_x = matches[1][closest_idx] + left
                
                # If local_search_size is specified, perform a local search
                if local_search_size > 0:
                    # Calculate local search area
                    local_left = max(0, closest_x - local_search_size // 2)
                    local_right = min(screen_width, closest_x + local_search_size // 2)
                    local_top = max(0, closest_y - local_search_size // 2)
                    local_bottom = min(screen_height, closest_y + local_search_size // 2)
                    
                    # Take screenshot of local area
                    local_screenshot = pyautogui.screenshot(region=(
                        int(local_left), 
                        int(local_top),
                        int(local_right - local_left),
                        int(local_bottom - local_top)
                    ))
                    
                    # Convert to numpy array
                    local_pixels = np.array(local_screenshot)
                    
                    # Find all matching pixels in local area
                    local_matches = np.where(
                        (np.abs(local_pixels[:, :, 0] - target_color[0]) <= tolerance) &
                        (np.abs(local_pixels[:, :, 1] - target_color[1]) <= tolerance) &
                        (np.abs(local_pixels[:, :, 2] - target_color[2]) <= tolerance)
                    )
                    
                    if len(local_matches[0]) > 0:
                        # Find the top-left most pixel in the local area
                        top_left_idx = np.argmin(local_matches[0] + local_matches[1])
                        return (int(local_matches[1][top_left_idx] + local_left), 
                               int(local_matches[0][top_left_idx] + local_top))
                
                return (int(closest_x), int(closest_y))
        
        return None

    def find_closest_pixel_without_moving(self, color_hex, tolerance=1, max_radius=1440, local_search_size=90, offset_range_x=(0, 20), offset_range_y=(0, 20)):
        """Find the closest pixel of the specified color to the center of the screen and click it without moving mouse back.
        
        Args:
            color_hex: The hex color to search for (e.g. "00FFFF" for teal)
            tolerance: Color matching tolerance
            max_radius: Maximum radius to search from center (default: 1440 for 2560x1440 screen)
            local_search_size: Size of the local search area around the found pixel (default: 90x90)
            offset_range_x: Tuple of (min, max) for random x offset from found pixel
            offset_range_y: Tuple of (min, max) for random y offset from found pixel
        
        Returns:
            Tuple of (x, y) coordinates where it clicked, or None if none found
        """
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        target_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        
        # Start with a small radius and expand
        for radius in range(50, max_radius, 50):
            # Calculate search area
            left = max(0, center_x - radius)
            right = min(screen_width, center_x + radius)
            top = max(0, center_y - radius)
            bottom = min(screen_height, center_y + radius)
            
            # Take screenshot of the current search area
            screenshot = pyautogui.screenshot(region=(int(left), int(top), int(right - left), int(bottom - top)))
            
            # Convert to numpy array for faster processing
            pixels = np.array(screenshot)
            
            # Find all pixels that match the target color within tolerance
            matches = np.where(
                (np.abs(pixels[:, :, 0] - target_color[0]) <= tolerance) &
                (np.abs(pixels[:, :, 1] - target_color[1]) <= tolerance) &
                (np.abs(pixels[:, :, 2] - target_color[2]) <= tolerance)
            )
            
            if len(matches[0]) > 0:
                # Calculate distances to center for all matches
                distances = np.sqrt(
                    (matches[0] + top - center_y) ** 2 +
                    (matches[1] + left - center_x) ** 2
                )
                
                # Find the closest match
                closest_idx = np.argmin(distances)
                closest_y = matches[0][closest_idx] + top
                closest_x = matches[1][closest_idx] + left
                
                # If local_search_size is specified, perform a local search
                if local_search_size > 0:
                    # Calculate local search area
                    local_left = max(0, closest_x - local_search_size // 2)
                    local_right = min(screen_width, closest_x + local_search_size // 2)
                    local_top = max(0, closest_y - local_search_size // 2)
                    local_bottom = min(screen_height, closest_y + local_search_size // 2)
                    
                    # Take screenshot of local area
                    local_screenshot = pyautogui.screenshot(region=(
                        int(local_left), 
                        int(local_top),
                        int(local_right - local_left),
                        int(local_bottom - local_top)
                    ))
                    
                    # Convert to numpy array
                    local_pixels = np.array(local_screenshot)
                    
                    # Find all matching pixels in local area
                    local_matches = np.where(
                        (np.abs(local_pixels[:, :, 0] - target_color[0]) <= tolerance) &
                        (np.abs(local_pixels[:, :, 1] - target_color[1]) <= tolerance) &
                        (np.abs(local_pixels[:, :, 2] - target_color[2]) <= tolerance)
                    )
                    
                    if len(local_matches[0]) > 0:
                        # Find the top-left most pixel in the local area
                        top_left_idx = np.argmin(local_matches[0] + local_matches[1])
                        closest_x = int(local_matches[1][top_left_idx] + local_left)
                        closest_y = int(local_matches[0][top_left_idx] + local_top)
                
                # Add random offset and click
                offset_x = random.randint(*offset_range_x)
                offset_y = random.randint(*offset_range_y)
                click_x = closest_x + offset_x
                click_y = closest_y + offset_y
                
                # Click without moving mouse back
                pyautogui.moveTo(click_x, click_y)
                time.sleep(random.uniform(0.05, 0.1))
                self.click_without_moving(button='left')
                
                return (click_x, click_y)
        
        return None

    def pixel_click_without_moving(self, color, region, tolerance=10, offset_range_x=(10, 30), offset_range_y=(10, 30), button='left'):
        """Click on a pixel color without moving the mouse back to original position."""
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
        return (target_x, target_y)

    def click_on_compass(self, region="p3", confidence=0.90):
        """Click on the compass by finding the world map and applying an offset.
        
        This function finds the world map icon and clicks with a calculated offset
        to land on the compass, which is more reliable than trying to find the
        compass directly due to rotation variations.
        
        Args:
            region: Region to search in (default: "p3" for top-right area)
            confidence: Confidence threshold for world map detection (default: 0.90)
            
        Returns:
            Tuple of (x, y) coordinates where the compass was clicked, or None if failed
        """
        try:
            # Get the search region
            search_region = self.get_scan_area(region)
            
            # Find world map and click with offset to land on compass
            # World map at (2262, 204), compass at (2079, 51)
            # Offset: -183 (left), -153 (up)
            world_map_click = self.click_image_cv2(
                'image_library/world_map.png', 
                region=search_region, 
                confidence=confidence,
                offset_range_x=(-185, -181),  # -183 ± 2
                offset_range_y=(-155, -151)   # -153 ± 2
            )
            
            if world_map_click:
                print(f"World map found and compass clicked at {world_map_click}")
                return world_map_click
            else:
                print(f"Warning: Could not find world map in region {region}")
                return None
                
        except Exception as e:
            print(f"Error clicking on compass: {e}")
            return None

    def find_image_cv3(self, image_path, region=None, threshold=0.98, color_tolerance=30, 
                       shape_weight=0.7, color_weight=0.3, shape_threshold=None, color_threshold=None):
        """
        Enhanced image finding with color-aware template matching and multiple validation techniques.
        This method finds all structural matches and continues searching until a color-validated match is found.
        
        Args:
            image_path: Path to the template image
            region: Region to search in
            threshold: Overall confidence threshold
            color_tolerance: RGB color difference tolerance for validation
            shape_weight: Weight for structural similarity (0.0-1.0)
            color_weight: Weight for color similarity (0.0-1.0)
            shape_threshold: Minimum shape similarity threshold (if None, uses threshold)
            color_threshold: Minimum color similarity threshold (if None, uses threshold)
        
        Returns:
            Center coordinates if found, None otherwise
        """
        # Use provided thresholds or fall back to main threshold
        if shape_threshold is None:
            shape_threshold = threshold
        if color_threshold is None:
            color_threshold = threshold
            
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        # Load the template image
        target = cv2.imread(image_path)
        if target is None:
            print(f"Failed to load image: {image_path}")
            return None

        # Debug: Show template dimensions
        target_h, target_w = target.shape[:2]
        
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
        
        target_h, target_w = target.shape[:2]
        
        # Find all structural matches above a lower threshold for candidates
        result_structural = cv2.matchTemplate(screenshot_cv, target, cv2.TM_CCOEFF_NORMED)
        # Use a high candidate threshold to only consider good structural matches
        # This prevents checking thousands of low-quality candidates
        candidate_threshold = 0.9  # High threshold to only consider good structural matches
        locations = np.where(result_structural >= candidate_threshold)
        
        # Sort candidates by structural score (highest first)
        candidates = []
        for pt in zip(*locations[::-1]):
            x, y = pt
            structural_score = result_structural[y, x]
            candidates.append((x, y, structural_score))
        
        # Sort by structural score descending
        candidates.sort(key=lambda x: x[2], reverse=True)
        
        print(f"CV3: Found {len(candidates)} structural candidates above threshold {candidate_threshold}")
        
        # Test each candidate with color validation
        for x, y, structural_score in candidates:
            # Extract the region around this candidate
            if (x + target_w <= screenshot_cv.shape[1] and 
                y + target_h <= screenshot_cv.shape[0]):
                
                matched_region = screenshot_cv[y:y + target_h, x:x + target_w]
                
                # Calculate color similarity using mean squared error
                color_diff = cv2.absdiff(target, matched_region)
                color_mse = np.mean(color_diff ** 2)
                max_possible_mse = 255 ** 2  # Maximum possible difference
                color_similarity = 1.0 - (color_mse / max_possible_mse)
                
                # Additional validation: Check if the matched region has similar color distribution
                target_mean_color = np.mean(target, axis=(0, 1))
                matched_mean_color = np.mean(matched_region, axis=(0, 1))
                color_distance = np.linalg.norm(target_mean_color - matched_mean_color)
                max_color_distance = np.sqrt(3 * 255**2)  # Maximum possible color distance
                color_distribution_score = 1.0 - (color_distance / max_color_distance)
                
                # STRICT COLOR TOLERANCE VALIDATION
                # Check if any pixel exceeds the color tolerance threshold
                color_tolerance_passed = True
                if color_tolerance < 255:  # Only apply if tolerance is set
                    # Calculate per-pixel color differences
                    pixel_diff = np.abs(target.astype(np.int16) - matched_region.astype(np.int16))
                    max_pixel_diff = np.max(pixel_diff, axis=(0, 1))  # Max difference per channel
                    
                    # Check if any channel exceeds tolerance
                    if np.any(max_pixel_diff > color_tolerance):
                        color_tolerance_passed = False
                        # Penalize the color scores if tolerance is exceeded
                        color_similarity *= 0.3
                        color_distribution_score *= 0.3
                
                # Calculate weighted composite score
                composite_score = (shape_weight * structural_score + 
                                  color_weight * (color_similarity * 0.5 + color_distribution_score * 0.5))
                
                # STRICT COLOR THRESHOLD VALIDATION
                # The color similarity must meet a minimum threshold regardless of composite score
                color_passed = color_similarity >= color_threshold and color_tolerance_passed
                
                # Show only near matches with essential info
                if structural_score >= 0.8 or color_similarity >= 0.8:  # Only show good candidates
                    screen_x = int(x + region_offset[0])
                    screen_y = int(y + region_offset[1])
                    print(f"CV3: Candidate at ({screen_x},{screen_y}) - S:{structural_score:.3f}, C:{color_similarity:.3f}, Score:{composite_score:.3f}")
                
                # If this candidate meets BOTH the composite threshold AND the color threshold, return it
                if composite_score >= threshold and color_passed:
                    center = (x + target_w // 2, y + target_h // 2)
                    # Convert numpy integers to regular integers to clean up logs
                    center = (int(center[0] + region_offset[0]), int(center[1] + region_offset[1]))
                    print(f"CV3: Found valid match at {center} (Score: {composite_score:.3f})")
                    return center
        
        # If we get here, no valid match was found
        print(f"CV3: No valid match found above threshold {threshold}")
        return None

    def find_all_images_cv3(self, image_path, region=None, threshold=0.98, color_tolerance=30, 
                           shape_weight=0.7, color_weight=0.3):
        """
        Enhanced image finding that returns all matches with color-aware validation.
        """
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        # Load the template image
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
        
        target_h, target_w = target.shape[:2]
        matches = []
        
        # Use structural matching to find candidate locations
        result_structural = cv2.matchTemplate(screenshot_cv, target, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result_structural >= threshold * 0.8)  # Lower threshold for candidates
        
        for pt in zip(*locations[::-1]):
            x, y = pt
            
            # Extract the region around this candidate
            if (x + target_w <= screenshot_cv.shape[1] and 
                y + target_h <= screenshot_cv.shape[0]):
                
                matched_region = screenshot_cv[y:y + target_h, x:x + target_w]
                
                # Calculate color similarity
                color_diff = cv2.absdiff(target, matched_region)
                color_mse = np.mean(color_diff ** 2)
                max_possible_mse = 255 ** 2
                color_similarity = 1.0 - (color_mse / max_possible_mse)
                
                # Calculate mean color distance
                target_mean_color = np.mean(target, axis=(0, 1))
                matched_mean_color = np.mean(matched_region, axis=(0, 1))
                color_distance = np.linalg.norm(target_mean_color - matched_mean_color)
                max_color_distance = np.sqrt(3 * 255**2)
                color_distribution_score = 1.0 - (color_distance / max_color_distance)
                
                # STRICT COLOR TOLERANCE VALIDATION
                # Check if any pixel exceeds the color tolerance threshold
                color_tolerance_passed = True
                if color_tolerance < 255:  # Only apply if tolerance is set
                    # Calculate per-pixel color differences
                    pixel_diff = np.abs(target.astype(np.int16) - matched_region.astype(np.int16))
                    max_pixel_diff = np.max(pixel_diff, axis=(0, 1))  # Max difference per channel
                    
                    # Check if any channel exceeds tolerance
                    if np.any(max_pixel_diff > color_tolerance):
                        color_tolerance_passed = False
                        # Penalize the color scores if tolerance is exceeded
                        color_similarity *= 0.3
                        color_distribution_score *= 0.3
                
                # Calculate composite score
                structural_score = result_structural[y, x]
                composite_score = (shape_weight * structural_score + 
                                  color_weight * (color_similarity * 0.5 + color_distribution_score * 0.5))
                
                if composite_score >= threshold:
                    center = (x + target_w // 2, y + target_h // 2)
                    center = (center[0] + region_offset[0], center[1] + region_offset[1])
                    matches.append(center)
        
        return matches

    def click_image_cv3_without_moving(self, image_path, region=None, confidence=0.95, 
                                     offset_range=(0, 3), color_tolerance=30,
                                     shape_weight=0.7, color_weight=0.3,
                                     shape_threshold=None, color_threshold=None):
        """
        Enhanced click method using CV3 image finding with color-aware validation.
        """
        center = self.find_image_cv3(image_path, region=region, threshold=confidence,
                                   color_tolerance=color_tolerance, shape_weight=shape_weight,
                                   color_weight=color_weight, shape_threshold=shape_threshold,
                                   color_threshold=color_threshold)
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

    def click_image_cv3(self, image_path, region=None, confidence=0.95, 
                       offset_range_x=(-7, 7), offset_range_y=(-7, 7), 
                       sleep_after=None, click_type='left', color_tolerance=30,
                       shape_weight=0.7, color_weight=0.3,
                       shape_threshold=None, color_threshold=None):
        """
        Enhanced click method using CV3 image finding with color-aware validation.
        """
        center = self.find_image_cv3(image_path, region=region, threshold=confidence,
                                   color_tolerance=color_tolerance, shape_weight=shape_weight,
                                   color_weight=color_weight, shape_threshold=shape_threshold,
                                   color_threshold=color_threshold)
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

    def get_cv3_weight_recommendations(self):
        """
        Get recommendations for CV3 weight configurations based on use case.
        
        Returns:
            Dictionary of recommended configurations for different scenarios
        """
        return {
            "cooked_vs_raw_discrimination": {
                "description": "Strictly distinguish between cooked and raw items",
                "shape_weight": 0.2,
                "color_weight": 0.8,
                "threshold": 0.95,
                "use_case": "When you need to avoid false positives between similar items with different colors"
            },
            "general_item_finding": {
                "description": "Balanced approach for general item detection",
                "shape_weight": 0.7,
                "color_weight": 0.3,
                "threshold": 0.95,
                "use_case": "Standard item detection with some color validation"
            },
            "color_critical": {
                "description": "When color is the primary identifier",
                "shape_weight": 0.1,
                "color_weight": 0.9,
                "threshold": 0.95,
                "use_case": "For items where color is more important than shape (e.g., different potion types)"
            },
            "shape_critical": {
                "description": "When shape is the primary identifier",
                "shape_weight": 0.9,
                "color_weight": 0.1,
                "threshold": 0.95,
                "use_case": "For items where shape is more important than color (e.g., different tool types)"
            },
            "ultra_strict": {
                "description": "Maximum precision with minimal false positives",
                "shape_weight": 0.1,
                "color_weight": 0.9,
                "threshold": 0.98,
                "use_case": "When you absolutely cannot afford false positives"
            }
        }

    def tune_cv3_weights(self, image_path, region=None, target_threshold=0.95):
        """
        Automatically tune CV3 weights for a specific image and region.
        
        Args:
            image_path: Path to the template image
            region: Region to search in
            target_threshold: Target confidence threshold
            
        Returns:
            Dictionary with recommended weights and performance metrics
        """
        print(f"Tuning CV3 weights for: {image_path}")
        print(f"Region: {region}")
        print(f"Target threshold: {target_threshold}")
        print("=" * 50)
        
        # Test different weight combinations with improved CV3 logic
        weight_combinations = [
            (0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6), (0.5, 0.5),
            (0.6, 0.4), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1)
        ]
        
        results = []
        
        for shape_w, color_w in weight_combinations:
            print(f"\nTesting weights - Shape: {shape_w:.1f}, Color: {color_w:.1f}")
            
            # Test with improved CV3 logic using separate shape and color thresholds
            start_time = time.time()
            result = self.find_image_cv3(
                image_path, region=region, threshold=target_threshold,
                shape_weight=shape_w, color_weight=color_w,
                shape_threshold=0.95,  # High shape threshold for accuracy
                color_threshold=0.95   # High color threshold for validation
            )
            test_time = time.time() - start_time
            
            if result:
                print(f"  ✓ Found at: {result}")
                success = True
            else:
                print(f"  ✗ Not found")
                success = False
            
            results.append({
                "shape_weight": shape_w,
                "color_weight": color_w,
                "success": success,
                "time": test_time,
                "result": result
            })
        
        # Analyze results
        successful_combinations = [r for r in results if r["success"]]
        failed_combinations = [r for r in results if not r["success"]]
        
        print(f"\n{'='*50}")
        print("TUNING RESULTS")
        print(f"{'='*50}")
        
        if successful_combinations:
            print(f"✓ Successful combinations: {len(successful_combinations)}")
            fastest_success = min(successful_combinations, key=lambda x: x["time"])
            print(f"  Fastest successful: Shape {fastest_success['shape_weight']:.1f}, "
                  f"Color {fastest_success['color_weight']:.1f} ({fastest_success['time']:.3f}s)")
            
            # Recommend balanced approach if multiple successful
            if len(successful_combinations) > 1:
                balanced = [r for r in successful_combinations if abs(r["shape_weight"] - r["color_weight"]) <= 0.2]
                if balanced:
                    recommended = balanced[0]
                    print(f"  Recommended balanced: Shape {recommended['shape_weight']:.1f}, "
                          f"Color {recommended['color_weight']:.1f}")
                else:
                    recommended = successful_combinations[0]
                    print(f"  Recommended: Shape {recommended['shape_weight']:.1f}, "
                          f"Color {recommended['color_weight']:.1f}")
            else:
                recommended = successful_combinations[0]
                print(f"  Only successful: Shape {recommended['shape_weight']:.1f}, "
                      f"Color {recommended['color_weight']:.1f}")
        else:
            print("✗ No successful combinations found")
            print("  Try lowering the threshold or using different weights")
        
        if failed_combinations:
            print(f"\n✗ Failed combinations: {len(failed_combinations)}")
            # Show a few examples
            for r in failed_combinations[:3]:
                print(f"  Shape {r['shape_weight']:.1f}, Color {r['color_weight']:.1f}")
        
        return {
            "successful_combinations": successful_combinations,
            "failed_combinations": failed_combinations,
            "recommended_weights": recommended if successful_combinations else None
        }
