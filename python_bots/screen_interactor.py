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
        # Note: Some areas need both X and width adjustment, others only X adjustment
        # Use the width_adjustment_areas dictionary below to control this behavior
        runelite_top_margin = floor(screen_height // 62)
        runelite_right_margin = floor(screen_width // 82)
        windows_bottom_margin = floor(screen_height // 62)
        
        runelite_right_menu_area = (screen_width - runelite_right_margin, runelite_top_margin, runelite_right_margin, (screen_height // 2))
        
        # Cache menu status to avoid multiple checks in the same execution
        if not hasattr(self, '_menu_cache_time') or time.time() - self._menu_cache_time > 5:
            self._cached_menu_offset = None
            self._menu_cache_time = time.time()

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
            "game_screen_center": (floor(screen_width * 0.2637), floor(screen_height * 0.0167), floor(screen_width * 0.6016), floor(screen_height * 0.9493)),
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
            "bag_last_slot": (floor(screen_width * 0.9492), floor(screen_height * 0.8986), floor(screen_width * 0.0187), floor(screen_height * 0.0319)),            
            "chat": (floor(screen_width // 320), screen_height - floor(screen_height// 5.69), (screen_width // 4), floor(screen_height // 8.47)),
            "bank_pane": ((screen_width // 3), floor(screen_height // 8.08), floor(screen_width // 5.30), floor(screen_height // 1.62)),
            "bank_pane_with_menus": ((screen_width // 3) - floor(screen_width // 37), floor(screen_height // 18.04), floor(screen_width // 4.03), floor(screen_height // 1.38)),
            "bank_deposit_box": (floor(screen_width * 0.3219), floor(screen_height * 0.2757), floor(screen_width * 0.2164), floor(screen_height * 0.2812)),
            "activity_pane": (floor(screen_width * 0.0023), floor(screen_height * 0.0340), floor(screen_width * 0.0844), floor(screen_height * 0.1514)),                
            "chat_area": (floor(screen_width // 320), screen_height - floor(screen_height// 5.69), (screen_width // 4), floor(screen_height // 8.47)),
            "runelite_right_menu": (screen_width - runelite_right_margin, runelite_top_margin, runelite_right_margin, (screen_height // 2)),
            "game_screen_middle_horizontal": (0, 292, 2525, 950),
            "bottom_of_char_zoom_8": (1245, 743, 1285, 779),
            "left_of_char_zoom_8": (1183, 689, 1228, 723)
        }
        
        # Get the base area
        base_area = areas.get(label, (0, 0, screen_width, screen_height))
        
        # Apply dynamic adjustments for right-side areas that need menu offset
        # Define which areas need width adjustment vs X-only adjustment
        width_adjustment_areas = {
            "game_screen_center": True,  # Adjust width only
            "bag": False,                 # Adjust X only
            "bank_pane": False,           # Adjust X only
            "bank_pane_with_menus": False, # Adjust X only
            "bag_last_slot": False,         # Adjust X only
            "bank_deposit_box": False         # Adjust X only
        }
        
        if label in width_adjustment_areas:
            # Check if RuneLite menu is open (use cached result if available)
            if hasattr(self, '_cached_menu_offset') and self._cached_menu_offset is not None:
                menu_offset = self._cached_menu_offset
            else:
                menu_offset = 0
                menu_found = None
                try:
                    # Use existing find_image_cv2 function to check for menu (silently)
                    menu_found = self.find_image_cv2_silent(
                        'image_library/runelite_menu_is_open.png',
                        region=runelite_right_menu_area,
                        threshold=0.98
                    )
                    if menu_found:
                        if label in ["bank_pane", "bank_pane_with_menus", "bank_deposit_box"]:
                            menu_offset = -floor(screen_width // 21)
                        else:
                            menu_offset = -floor(screen_width // 10.6)
                        print(f"RuneLite menu OPEN - applying {menu_offset} offset to {label} search area")
                    # Cache the result
                    self._cached_menu_offset = menu_offset
                except Exception as e:
                    print(f"RuneLite menu check failed - treating as CLOSED (no offset)")
                    menu_offset = 0
                    self._cached_menu_offset = menu_offset
            
            # Apply offset based on area type
            if menu_offset != 0:
                needs_width_adjustment = width_adjustment_areas.get(label, False)
                
                if needs_width_adjustment:
                    # Adjust width only to maintain proper area size (keep same X position)
                    adjusted_area = (base_area[0], base_area[1], base_area[2] + menu_offset, base_area[3])
                    print(f"Applied width adjustment for {label}: W={base_area[2]}->{base_area[2] + menu_offset}")
                else:
                    # Adjust X coordinate only (applies to menu items)
                    adjusted_area = (base_area[0] + menu_offset, base_area[1], base_area[2], base_area[3])
                    print(f"Applied X-only adjustment for {label}: X={base_area[0]}->{base_area[0] + menu_offset}")
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
                                      pixel_offset_range_x=(5, 20), pixel_offset_range_y=(5, 20),
                                      region=None):
        # FUNCTION 1 - find_pixel_right_click_confirm
        """
        Find a pixel of specified color, right-click on it, and confirm the right-click menu 
        appears by finding a specific image. Uses CV2 for finding the confirmation image 
        (better for UI elements like menu options). This provides more reliable interaction than 
        just assuming a left-click worked.
        
        Args:
            pixel_color: Hex color string to search for (e.g., "00FFFF" for teal)
            confirm_image_path: Path to image that should appear in right-click menu
            attempts: Number of attempts to find and right-click the pixel (default: 5)
            pixel_offset_range_x: Tuple of (min, max) for random x offset from found pixel (default: (5, 20))
            pixel_offset_range_y: Tuple of (min, max) for random y offset from found pixel (default: (5, 20))
            region: Optional (x, y, w, h) to limit pixel search to that area (e.g. get_scan_area label).
        
        Returns:
            True if successful (pixel found, right-clicked, and confirmation image found and clicked)
            False if failed after all attempts
        """
        print(f"find_pixel_right_click_confirm: Searching for {pixel_color} pixel with {confirm_image_path} confirmation")
        
        for attempt in range(1, attempts + 1):
            print(f"  Attempt {attempt}/{attempts}")
            
            # Step 1: Find the pixel (optionally within region)
            found_pixel = self.find_pixel(pixel_color, region=region, tolerance=5)
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
            
            # Move to target and right-click (minimal delay: move and click together)
            pyautogui.moveTo(target_x, target_y)
            time.sleep(random.uniform(0.01, 0.02))
            pyautogui.click(button='right')
            
            # Step 3: Search for confirmation image in area around mouse - FUNCTION 1
            # Search area: x direction ±300, y direction ±(screen_height/2) centered on mouse
            screen_width, screen_height = pyautogui.size()
            
            # Calculate search region bounds - centered on mouse position
            left = max(0, target_x - 300)
            right = min(screen_width, target_x + 300)
            y_search_height = screen_height // 2  # Half screen height for comprehensive menu search
            top = max(0, target_y - y_search_height)
            bottom = min(screen_height, target_y + y_search_height)
            
            # Ensure valid region dimensions
            width = right - left
            height = bottom - top
            
            if width <= 0 or height <= 0:
                print(f"    Invalid search region calculated: left={left}, right={right}, top={top}, bottom={bottom}")
                print(f"    Adjusting to valid region...")
                # Fallback to a smaller, guaranteed valid region
                left = max(0, target_x - 100)
                right = min(screen_width, target_x + 100)
                y_search_height = screen_height // 4  # Quarter screen height as fallback
                top = max(0, target_y - y_search_height)
                bottom = min(screen_height, target_y + y_search_height)
                width = right - left
                height = bottom - top
            
            search_region = (left, top, width, height)
            
            print(f"    Searching for confirmation image in region: {search_region}")
            
            # Look for the confirmation image using CV2 for better menu option detection
            # Try with adaptive confidence - start high and lower each attempt
            confirm_location = None
            start_confidence = 0.90
            confidence_step = 0.02
            
            for confirm_attempt in range(6):
                current_confidence = start_confidence - (confirm_attempt * confidence_step)
                current_confidence = max(0.70, current_confidence)  # Don't go below 0.70
                
                try:
                    confirm_location = self.find_image_cv2(
                        confirm_image_path, 
                        region=search_region, 
                        threshold=current_confidence
                    )
                    if confirm_location:
                        break  # Found it, exit the retry loop
                    # Wait a bit before retrying
                    time.sleep(0.1)
                except Exception as e:
                    print(f"    Error searching for confirmation image (attempt {confirm_attempt + 1}): {e}")
                    time.sleep(0.1)
            
            if confirm_location:
                print(f"    Confirmation image found at {confirm_location} (attempt {confirm_attempt + 1}, confidence: {current_confidence:.2f})")
                
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
                print(f"    Confirmation image not found after 6 attempts on attempt {attempt}")
                
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

    def find_pixel_right_click_confirm_new(self, pixel_color, confirm_image_path, attempts=10, 
                                      pixel_offset_range_x=(5, 20), pixel_offset_range_y=(5, 20)):
        # FUNCTION 2 - find_pixel_right_click_confirm_new
        """
        Find a pixel of specified color, right-click on it, and confirm the right-click menu 
        appears by finding a specific image. Uses CV2 for finding the confirmation image 
        (better for UI elements like menu options). This provides more reliable interaction than 
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
            
            # Move to target and right-click (minimal delay: move and click together)
            pyautogui.moveTo(target_x, target_y)
            time.sleep(random.uniform(0.01, 0.02))
            pyautogui.click(button='right')
            
            # Step 3: Search for confirmation image in area around mouse - FUNCTION 2
            # Search area: x direction ±300, y direction ±(screen_height/2) centered on mouse
            screen_width, screen_height = pyautogui.size()
            
            # Calculate search region bounds - centered on mouse position
            left = max(0, target_x - 300)
            right = min(screen_width, target_x + 300)
            y_search_height = screen_height // 2  # Half screen height for comprehensive menu search
            top = max(0, target_y - y_search_height)
            bottom = min(screen_height, target_y + y_search_height)
            
            # Ensure valid region dimensions
            width = right - left
            height = bottom - top
            
            if width <= 0 or height <= 0:
                print(f"    Invalid search region calculated: left={left}, right={right}, top={top}, bottom={bottom}")
                print(f"    Adjusting to valid region...")
                # Fallback to a smaller, guaranteed valid region
                left = max(0, target_x - 100)
                right = min(screen_width, target_x + 100)
                y_search_height = screen_height // 4  # Quarter screen height as fallback
                top = max(0, target_y - y_search_height)
                bottom = min(screen_height, target_y + y_search_height)
                width = right - left
                height = bottom - top
            
            search_region = (left, top, width, height)
            
            print(f"    Searching for confirmation image in region: {search_region}")
            
            # Look for the confirmation image using CV2 for better menu option detection
            # Try with adaptive confidence - start high and lower each attempt
            confirm_location = None
            start_confidence = 0.90
            confidence_step = 0.02
            
            for confirm_attempt in range(6):
                current_confidence = start_confidence - (confirm_attempt * confidence_step)
                current_confidence = max(0.70, current_confidence)  # Don't go below 0.70
                
                try:
                    confirm_location = self.find_image_cv2(
                        confirm_image_path, 
                        region=search_region, 
                        threshold=current_confidence
                    )
                    if confirm_location:
                        break  # Found it, exit the retry loop
                    # Wait a bit before retrying
                    time.sleep(0.1)
                except Exception as e:
                    print(f"    Error searching for confirmation image (attempt {confirm_attempt + 1}): {e}")
                    time.sleep(0.1)
            
            if confirm_location:
                print(f"    Confirmation image found at {confirm_location} (attempt {confirm_attempt + 1}, confidence: {current_confidence:.2f})")
                
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
                print(f"    Confirmation image not found after 6 attempts on attempt {attempt}")
                
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
            print(f"CV2: ✓ Found {os.path.basename(image_path)} at {center} (Score: {max_val:.3f})")
            return center
        else:
            print(f"CV2: ✗ No match found for {os.path.basename(image_path)} (Best score: {max_val:.3f} < {threshold})")
            return None

    def find_image_cv2_silent(self, image_path, region=None, threshold=0.98):
        """Silent version of find_image_cv2 that doesn't output anything - for internal checks."""
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        # Load the template image and convert to BGR
        target = cv2.imread(image_path)
        if target is None:
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
    
    def click_image_cv2_without_moving_xy(self, image_path, region=None, confidence=0.95, 
                                         offset_range_x=(0, 3), offset_range_y=(0, 3)):
        """Click on an image with separate x and y offset ranges, without moving mouse after."""
        center = self.find_image_cv2(image_path, region=region, threshold=confidence)
        if center is None:
            print(f"Image not found: {image_path}")
            return None
        offset_x = random.randint(*offset_range_x)
        offset_y = random.randint(*offset_range_y)
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

    def find_image_right_click_confirm(self, image_path, confirm_image_path, region=None, 
                                      confidence=0.95, attempts=5, offset_range_x=(2, 10), 
                                      offset_range_y=(2, 10)):
        # FUNCTION 3 - find_image_right_click_confirm
        """
        Find an image, right-click on it, and confirm the right-click menu appears by finding a specific image.
        Uses CV3 for finding the main image (enhanced color-aware detection) and CV2 for finding the 
        confirmation image (better for UI elements like menu options).
        
        Args:
            image_path: Path to image to find and right-click
            confirm_image_path: Path to image that should appear in right-click menu
            region: Region to search in
            confidence: Confidence threshold for image matching
            attempts: Number of attempts
            offset_range_x: Tuple of (min, max) for random x offset
            offset_range_y: Tuple of (min, max) for random y offset
        
        Returns:
            True if successful, False otherwise
        """
        print(f"find_image_right_click_confirm: Searching for {image_path} with {confirm_image_path} confirmation")
        
        for attempt in range(1, attempts + 1):
            print(f"  Attempt {attempt}/{attempts}")
            
            # Step 1: Find the image using CV3 for enhanced color-aware detection
            found_image = self.find_image_cv3(
                image_path, 
                region=region, 
                threshold=confidence,
                color_tolerance=30,  # Allow some color variation
                shape_weight=0.7,    # Balanced approach
                color_weight=0.3
            )
            if not found_image:
                print(f"    Image {image_path} not found on attempt {attempt}")
                continue
            
            print(f"    Found {image_path} at {found_image}")
            
            # Step 2: Calculate offset position and right-click
            offset_x = random.randint(*offset_range_x)
            offset_y = random.randint(*offset_range_y)
            target_x = found_image[0] + offset_x
            target_y = found_image[1] + offset_y
            
            # Ensure target coordinates are within screen bounds
            screen_width, screen_height = pyautogui.size()
            target_x = max(0, min(target_x, screen_width - 1))
            target_y = max(0, min(target_y, screen_height - 1))
            
            # Store original mouse position
            original_pos = pyautogui.position()
            
            # Move to target and right-click (minimal delay: move and click together)
            pyautogui.moveTo(target_x, target_y)
            time.sleep(random.uniform(0.01, 0.02))
            pyautogui.click(button='right')
            
            # Step 3: Search for confirmation image in area around mouse - FUNCTION 3
            # Search area: x direction ±300, y direction ±(screen_height/2) centered on mouse
            left = max(0, target_x - 300)
            right = min(screen_width, target_x + 300)
            y_search_height = screen_height // 2  # Half screen height for comprehensive menu search
            top = max(0, target_y - y_search_height)
            bottom = min(screen_height, target_y + y_search_height)
            
            # Ensure valid region dimensions
            width = right - left
            height = bottom - top
            
            if width <= 0 or height <= 0:
                print(f"    Invalid search region calculated: left={left}, right={right}, top={top}, bottom={bottom}")
                print(f"    Adjusting to valid region...")
                # Fallback to a smaller, guaranteed valid region
                left = max(0, target_x - 100)
                right = min(screen_width, target_x + 100)
                y_search_height = screen_height // 4  # Quarter screen height as fallback
                top = max(0, target_y - y_search_height)
                bottom = min(screen_height, target_y + y_search_height)
                width = right - left
                height = bottom - top
            
            search_region = (left, top, width, height)
            
            print(f"    Searching for confirmation image in region: {search_region}")
            # Sleep randomly for .2 to .4 seconds
            time.sleep(random.uniform(0.4, 0.7))

            # Look for the confirmation image using CV2 for better menu option detection
            # Try with adaptive confidence - start high and lower each attempt
            confirm_location = None
            start_confidence = 0.90
            confidence_step = 0.02
            
            for confirm_attempt in range(6):
                current_confidence = start_confidence - (confirm_attempt * confidence_step)
                current_confidence = max(0.70, current_confidence)  # Don't go below 0.70
                
                try:
                    confirm_location = self.find_image_cv2(
                        confirm_image_path, 
                        region=search_region, 
                        threshold=current_confidence
                    )
                    if confirm_location:
                        break  # Found it, exit the retry loop
                    # Wait a bit before retrying
                    time.sleep(0.1)
                except Exception as e:
                    print(f"    Error searching for confirmation image (attempt {confirm_attempt + 1}): {e}")
                    time.sleep(0.1)
            
            if confirm_location:
                print(f"    Confirmation image found at {confirm_location} (attempt {confirm_attempt + 1}, confidence: {current_confidence:.2f})")
                
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
                print(f"    Confirmation image not found after 6 attempts on attempt {attempt}")
                
                # Step 5: Reset mouse position to close any open right-click menus
                # Move up and to the right to close menus
                reset_x = target_x + random.randint(200, 500)
                reset_y = target_y + random.randint(-500, -200)
                
                # Ensure we stay within screen bounds
                reset_x = max(0, min(reset_x, screen_width - 1))
                reset_y = max(0, min(reset_y, screen_height - 1))
                
                print(f"    Resetting mouse to ({reset_x}, {reset_y}) to close menus")
                pyautogui.moveTo(reset_x, reset_y)
                time.sleep(random.uniform(0.1, 0.2))
                
                # Return mouse to original position
                pyautogui.moveTo(original_pos)
        
        # If we get here, all attempts failed
        print(f"  Failed to find and confirm {image_path} after {attempts} attempts")
        return False

    def zoom_out(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=-400):
        """Zoom out safely on low-res/edge-case displays without tripping PyAutoGUI failsafe."""
        screen_width, screen_height = pyautogui.size()
        # Keep well inside screen bounds to avoid corner-triggered failsafe.
        safe_x = max(50, min(screen_width - 50, screen_width // 6))
        safe_y = max(50, min(screen_height - 50, screen_height // 6))
        original = pyautogui.position()

        # Save and temporarily disable failsafe during controlled bot movement.
        prev_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(safe_x, safe_y)
            for _ in range(times):
                pyautogui.scroll(scroll_amount)
                time.sleep(random.uniform(delay_low, delay_high))
            # Return near original, still clamped safely.
            return_x = max(50, min(screen_width - 50, int(original[0])))
            return_y = max(50, min(screen_height - 50, int(original[1])))
            pyautogui.moveTo(return_x, return_y)
        finally:
            pyautogui.FAILSAFE = prev_failsafe

    def zoom_in(self, times=3, delay_low=0.005, delay_high=0.01, scroll_amount=400):
        """Zoom in safely on low-res/edge-case displays without tripping PyAutoGUI failsafe."""
        screen_width, screen_height = pyautogui.size()
        safe_x = max(50, min(screen_width - 50, screen_width // 6))
        safe_y = max(50, min(screen_height - 50, screen_height // 6))
        original = pyautogui.position()

        prev_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(safe_x, safe_y)
            for _ in range(times):
                pyautogui.scroll(scroll_amount)
                time.sleep(random.uniform(delay_low, delay_high))
            return_x = max(50, min(screen_width - 50, int(original[0])))
            return_y = max(50, min(screen_height - 50, int(original[1])))
            pyautogui.moveTo(return_x, return_y)
        finally:
            pyautogui.FAILSAFE = prev_failsafe

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
            world_map_click = self.click_image_cv2_without_moving_xy(
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
                
                                # If this candidate meets BOTH the composite threshold AND the color threshold, return it
                if composite_score >= threshold and color_passed:
                    center = (x + target_w // 2, y + target_h // 2)
                    # Convert numpy integers to regular integers to clean up logs
                    center = (int(center[0] + region_offset[0]), int(center[1] + region_offset[1]))
                    print(f"CV3: ✓ Found {os.path.basename(image_path)} at {center} (Score: {composite_score:.3f})")
                    return center
        
        # If we get here, no valid match was found
        print(f"CV3: ✗ No valid match found for {os.path.basename(image_path)} above threshold {threshold}")
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

    def find_closest_image_region(self, image_path, region=None, confidence=0.95, 
                                 max_radius=1440, color_tolerance=30,
                                 shape_weight=0.7, color_weight=0.3,
                                 shape_threshold=None, color_threshold=None):
        """
        Find the closest image to the screen center (character) by expanding search radius outward,
        but only search within the specified region boundaries.
        Returns the coordinates of the closest matching image center.
        
        Args:
            image_path: Path to the template image to find
            region: Region to search in (if None, searches entire screen)
            confidence: Confidence threshold for image matching
            max_radius: Maximum radius to search from center (default: 1440 for 2560x1440 screen)
            color_tolerance: RGB color difference tolerance for CV3 validation
            shape_weight: Weight for structural similarity (0.0-1.0) for CV3
            color_weight: Weight for color similarity (0.0-1.0) for CV3
            shape_threshold: Minimum shape similarity threshold for CV3 (if None, uses confidence)
            color_threshold: Minimum color similarity threshold for CV3 (if None, uses confidence)
        
        Returns:
            Tuple of (x, y) coordinates of the closest matching image center, or None if none found
        """
        # Get screen dimensions first (needed for bounds checking)
        screen_width, screen_height = pyautogui.size()
        
        # Always use screen center for distance calculations (character position)
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        if region:
            # Get region boundaries for constraining search
            region_x, region_y, region_width, region_height = region
            # Limit max_radius to the region size
            max_radius = min(max_radius, max(region_width, region_height) // 2)
        
        # Start with a small radius and expand
        for radius in range(50, max_radius, 50):
            # Calculate search area centered on screen center (character)
            left = max(0, center_x - radius)
            right = min(screen_width, center_x + radius)
            top = max(0, center_y - radius)
            bottom = min(screen_height, center_y + radius)
            
            # If we have a specific region, constrain the search to that region
            if region:
                left = max(left, region_x)
                right = min(right, region_x + region_width)
                top = max(top, region_y)
                bottom = min(bottom, region_y + region_height)
            
            # Create region tuple for this search area
            search_region = (left, top, right - left, bottom - top)
            
            # Use CV3 for enhanced color-aware detection
            try:
                found_image = self.find_image_cv3(
                    image_path,
                    region=search_region,
                    threshold=confidence,
                    color_tolerance=color_tolerance,
                    shape_weight=shape_weight,
                    color_weight=color_weight,
                    shape_threshold=shape_threshold,
                    color_threshold=color_threshold
                )
                
                if found_image:
                    print(f"Found {os.path.basename(image_path)} at radius {radius} - closest to character")
                    return found_image
                    
            except Exception as e:
                print(f"Error searching at radius {radius}: {e}")
                continue
        
        print(f"No {os.path.basename(image_path)} found within max radius {max_radius}")
        return None

    def find_closest_image_cv2_region(self, image_path, region=None, confidence=0.95, 
                                     max_radius=1440):
        """
        Find the closest image to the screen center (character) using CV2 (faster but less accurate).
        Expands search radius outward from screen center, but only searches within the specified region.
        
        Args:
            image_path: Path to the template image to find
            region: Region to search in (if None, searches entire screen)
            confidence: Confidence threshold for image matching
            max_radius: Maximum radius to search from center (default: 1440 for 2560x1440 screen)
        
        Returns:
            Tuple of (x, y) coordinates of the closest matching image center, or None if none found
        """
        # Get screen dimensions first (needed for bounds checking)
        screen_width, screen_height = pyautogui.size()
        
        # Always use screen center for distance calculations (character position)
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Resolve the region if it's given as a label
        region = self.resolve_region(region) if region is not None else None
        
        if region:
            # Get region boundaries for constraining search
            region_x, region_y, region_width, region_height = region
            # Limit max_radius to the region size
            max_radius = min(max_radius, max(region_width, region_height) // 2)
        
        # Start with a small radius and expand
        for radius in range(50, max_radius, 50):
            # Calculate search area centered on screen center (character)
            left = max(0, center_x - radius)
            right = min(screen_width, center_x + radius)
            top = max(0, center_y - radius)
            bottom = min(screen_height, center_y + radius)
            
            # If we have a specific region, constrain the search to that region
            if region:
                left = max(left, region_x)
                right = min(right, region_x + region_width)
                top = max(top, region_y)
                bottom = min(bottom, region_y + region_height)
            
            # Create region tuple for this search area
            search_region = (left, top, right - left, bottom - top)
            
            # Use CV2 for faster detection
            try:
                found_image = self.find_image_cv2(
                    image_path,
                    region=search_region,
                    threshold=confidence
                )
                
                if found_image:
                    print(f"Found {os.path.basename(image_path)} at radius {radius} - closest to character")
                    return found_image
                    
            except Exception as e:
                print(f"Error searching at radius {radius}: {e}")
                continue
        
        print(f"No {os.path.basename(image_path)} found within max radius {max_radius}")
        return None

    def activate_game_window(self):
        """
        Find the RuneLite/game window and bring it to the foreground so key inputs are received.
        Returns True if a window was found and activated, False otherwise.
        """
        # First try via Win32 APIs if available
        try:
            import win32gui
            import win32con

            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "runelite" in window_title.lower() or "runescape" in window_title.lower():
                        windows.append((hwnd, window_title))
                return True

            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)

            if windows:
                hwnd, title = windows[0]
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
                return True
        except ImportError:
            # Fall through to pyautogui-click fallback
            pass
        except Exception as e:
            print(f"Error activating game window via Win32: {e}")

        # Fallback: click near the RuneLite window title bar (top toolbar) to bring it to foreground
        try:
            screen_width, _ = pyautogui.size()
            # Title bar is usually at very top of the screen, just below OS chrome
            x = screen_width // 2
            y = 15  # small y so we stay on the toolbar, not in the game area
            print(f"Fallback activate: clicking top toolbar at ({x}, {y})")
            original = pyautogui.position()
            pyautogui.moveTo(x, y)
            time.sleep(0.1)
            pyautogui.click()
            pyautogui.moveTo(original)
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error activating game window via click fallback: {e}")
            return False

    def close_runelite_client(self):
        """
        Close the RuneLite client window.
        
        Returns:
            True if RuneLite was closed successfully, False otherwise
        """
        print("Attempting to close RuneLite client...")
        
        try:
            import win32gui
            import win32con
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "runelite" in window_title.lower() or "runescape" in window_title.lower():
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                print(f"Found RuneLite windows: {windows}")
                # Close all RuneLite windows
                for hwnd, title in windows:
                    print(f"Closing window: {title}")
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                
                # Wait a moment for windows to close
                time.sleep(3)
                print("RuneLite client closed successfully")
                return True
            else:
                print("No RuneLite windows found")
                return False
                
        except ImportError:
            print("win32gui not available. Trying alternative method...")
            return self.try_alternative_runelite_close()
        except Exception as e:
            print(f"Error closing RuneLite client: {e}")
            return self.try_alternative_runelite_close()
    
    def try_alternative_runelite_close(self):
        """Alternative method to close RuneLite using taskkill."""
        print("Trying to close RuneLite via taskkill...")
        
        try:
            import subprocess
            
            # Try to kill RuneLite processes
            result = subprocess.run(
                ["taskkill", "/f", "/im", "RuneLite.exe"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("RuneLite closed successfully via taskkill")
                time.sleep(2)
                return True
            else:
                print(f"taskkill failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error with taskkill: {e}")
            return False

    def handle_servers_updated_restart(self, post_login_callback=None):
        """
        Handle the special case when game servers are being updated.
        This requires waiting 3 minutes, closing RuneLite, and restarting via Jagex Launcher.
        
        Returns:
            True if restart process completed successfully, False otherwise
        """
        print("=" * 60)
        print("HANDLING GAME SERVERS BEING UPDATED")
        print("=" * 60)
        
        # Step 1: Wait 3 minutes
        print("Waiting 3 minutes for servers to update...")
        wait_seconds = 3 * 60  # 3 minutes
        
        # Show progress every 30 seconds
        for remaining in range(wait_seconds, 0, -30):
            minutes_left = remaining // 60
            seconds_left = remaining % 60
            print(f"Waiting... {minutes_left:02d}:{seconds_left:02d} remaining")
            time.sleep(30)
        
        print("Wait period completed. Proceeding with client restart...")
        
        # Step 2: Close RuneLite client
        print("Closing RuneLite client...")
        runelite_closed = self.close_runelite_client()
        if not runelite_closed:
            print("Warning: Could not close RuneLite client, proceeding anyway...")
        
        # Step 3: Try to find and activate Jagex Launcher
        launcher_found = self.find_jagex_launcher_window()
        if not launcher_found:
            print("Failed to find/activate Jagex Launcher")
            return False
        
        # Step 4: Click play button in launcher
        play_clicked = self.click_launcher_play_button()
        if not play_clicked:
            print("Failed to click play button in launcher")
            return False
        
        # Step 5: Monitor for login screen and complete login
        login_completed = self.monitor_for_login_screen_after_restart(post_login_callback=post_login_callback)
        
        if login_completed:
            print("=" * 60)
            print("SERVERS UPDATE RESTART COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            return True
        else:
            print("=" * 60)
            print("SERVERS UPDATE RESTART FAILED")
            print("=" * 60)
            return False
    
    def find_jagex_launcher_window(self):
        """Try to find and activate the Jagex Launcher window."""
        print("Attempting to find Jagex Launcher window...")
        
        try:
            # Try to find the launcher using Windows API
            import win32gui
            import win32con
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "jagex" in window_title.lower() or "launcher" in window_title.lower():
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                print(f"Found Jagex Launcher windows: {windows}")
                # Use the first found window
                hwnd, title = windows[0]
                print(f"Activating window: {title}")
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(2)
                return True
            else:
                print("No Jagex Launcher window found")
                return False
                
        except ImportError:
            print("win32gui not available. Trying alternative method...")
            return self.try_alternative_launcher_activation()
        except Exception as e:
            print(f"Error finding Jagex Launcher window: {e}")
            return self.try_alternative_launcher_activation()
    
    def try_alternative_launcher_activation(self):
        """Alternative method to activate Jagex Launcher using subprocess."""
        print("Trying to launch Jagex Launcher via subprocess...")
        
        import subprocess
        
        # Common Jagex Launcher paths
        possible_paths = [
            r"C:\Users\%USERNAME%\AppData\Local\Jagex Launcher\JagexLauncher.exe",
            r"C:\Program Files\Jagex Launcher\JagexLauncher.exe",
            r"C:\Program Files (x86)\Jagex Launcher\JagexLauncher.exe",
            r"C:\Users\%USERNAME%\AppData\Roaming\Jagex Launcher\JagexLauncher.exe"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                print(f"Found Jagex Launcher at: {expanded_path}")
                try:
                    # Launch the launcher
                    subprocess.Popen([expanded_path])
                    print("Jagex Launcher launched successfully")
                    time.sleep(5)  # Wait for launcher to load
                    return True
                except Exception as e:
                    print(f"Error launching Jagex Launcher: {e}")
                    continue
        
        print("Could not find or launch Jagex Launcher")
        return False
    
    def click_launcher_play_button(self):
        """Click the play button in Jagex Launcher."""
        print("Looking for Jagex Launcher play button...")
        
        # Try to find the play button in the launcher
        play_button_found = self.find_image_cv2(
            "image_library/jagex_launcher_play_button.png",
            region=None,  # Search entire screen since launcher might be anywhere
            threshold=0.90
        )
        
        if play_button_found:
            print(f"Found play button at {play_button_found}. Clicking...")
            click_result = self.click_image_cv2_without_moving(
                "image_library/jagex_launcher_play_button.png",
                region=None,
                confidence=0.90,
                offset_range=(0, 3)
            )
            
            if click_result:
                print("Play button clicked successfully")
                time.sleep(5)  # Wait for game to start loading
                return True
            else:
                print("Failed to click play button")
                return False
        else:
            print("Play button not found in Jagex Launcher")
            return False
    
    def monitor_for_login_screen_after_restart(self, timeout=120, post_login_callback=None):
        """Monitor for login screen after launcher restart."""
        print("Monitoring for login screen after launcher restart...")
        
        p2_region = self.get_scan_area("p2")
        
        # Import ImageMonitor here to avoid circular imports
        from image_monitor import ImageMonitor
        
        # Create image monitor for login_play_now.png
        login_monitor = ImageMonitor(
            self,
            "image_library/login_play_now.png",
            region=p2_region,
            confidence=0.90,
            wait_for="appear"
        )
        
        print(f"Waiting up to {timeout} seconds for login screen...")
        login_monitor.start()  # Start the monitoring thread
        login_found = login_monitor.wait_for_condition(timeout=timeout)
        login_monitor.stop()  # Clean up the thread
        
        if login_found:
            print("Login screen detected! Proceeding with login process...")
            # Use the existing resolveLogin logic but skip the initial error checks
            # since we're already past the launcher restart
            return self.complete_login_after_restart(post_login_callback)
        else:
            print("Login screen not detected within timeout period")
            return False
    
    def complete_login_after_restart(self, post_login_callback=None):
        """Complete the login process after launcher restart."""
        print("Completing login process after restart...")
        
        # Track whether we actually perform a login action
        login_action_performed = False
        
        p2_region = self.get_scan_area("p2")
        
        # Check for login_play_now.png and click it
        play_now_found = self.find_image_cv2(
            "image_library/login_play_now.png",
            region=p2_region,
            threshold=0.90
        )
        
        if play_now_found:
            print("Play Now button found. Clicking it...")
            login_action_performed = True  # Mark that we're performing a login action
            play_now_click = self.click_image_cv2_without_moving(
                "image_library/login_play_now.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if play_now_click:
                print("Play Now button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for next screen
            else:
                print("Failed to click Play Now button.")
                return False
        else:
            print("Play Now button not found.")
            return False
        
        # Wait and click "Click here to play" button
        print("Waiting for 'Click here to play' button...")
        start_time = time.time()
        while time.time() - start_time < 60:
            click_here_found = self.find_image_cv2(
                "image_library/login_click_here_to_play.png",
                region=p2_region,
                threshold=0.90
            )
            if click_here_found:
                print("Click here to play button found. Clicking it...")
                click_here_click = self.click_image_cv2_without_moving(
                    "image_library/login_click_here_to_play.png",
                    region=p2_region,
                    confidence=0.90,
                    offset_range=(0, 3)
                )
                if click_here_click:
                    print("Click here to play button clicked successfully.")
                    print("Login process completed after restart. Waiting for game to load...")
                    time.sleep(random.uniform(5, 10))  # Wait for game to load
                    # Call post-login callback if provided and we actually performed a login action
                    if post_login_callback and login_action_performed:
                        print("Running post-login setup...")
                        post_login_callback()
                    return True
                else:
                    print("Failed to click Click here to play button.")
                    return False
            time.sleep(2)
        else:
            print("Click here to play button not found within 60 seconds.")
            return False

    def check_internet_connectivity(self, timeout_minutes=5):
        """
        Check internet connectivity by pinging Google.
        
        Args:
            timeout_minutes: Maximum time to wait for internet connectivity (default: 5 minutes)
            
        Returns:
            bool: True if internet is available, False if timeout reached
        """
        import subprocess
        import time
        
        print(f"Checking internet connectivity (will try for up to {timeout_minutes} minutes)...")
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        
        while time.time() - start_time < timeout_seconds:
            try:
                # Ping Google DNS (8.8.8.8) with 1 packet, 1 second timeout
                result = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", "8.8.8.8"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    print("✅ Internet connectivity restored!")
                    return True
                else:
                    print("❌ Internet still down, retrying in 10 seconds...")
                    time.sleep(10)
                    
            except subprocess.TimeoutExpired:
                print("❌ Ping timeout, retrying in 10 seconds...")
                time.sleep(10)
            except Exception as e:
                print(f"❌ Ping error: {e}, retrying in 10 seconds...")
                time.sleep(10)
        
        print(f"⚠️ Internet connectivity check timed out after {timeout_minutes} minutes")
        return False

    def handle_account_logged_in_error(self, post_login_callback=None):
        """
        Handle the "Account logged in" error by checking internet connectivity
        and restarting the launcher/client if needed.
        
        Returns:
            bool: True if login process was completed successfully, False otherwise
        """
        print("Handling 'Account logged in' error (internet connectivity issue)...")
        
        # Step 1: Check internet connectivity for up to 5 minutes
        internet_available = self.check_internet_connectivity(timeout_minutes=5)
        
        # Step 2: Restart launcher and client regardless of internet status
        print("Restarting launcher and client for fresh session...")
        
        # Close RuneLite client
        runelite_closed = self.close_runelite_client()
        if runelite_closed:
            print("RuneLite client closed successfully")
        else:
            print("Warning: Could not close RuneLite client, proceeding anyway...")
        
        # Close and reopen Jagex Launcher
        print("Closing Jagex Launcher...")
        try:
            import win32gui
            import win32con
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "jagex" in window_title.lower() or "launcher" in window_title.lower():
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                for hwnd, title in windows:
                    print(f"Closing window: {title}")
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                time.sleep(3)
                print("Jagex Launcher closed successfully")
            else:
                print("No Jagex Launcher windows found")
        except Exception as e:
            print(f"Error closing Jagex Launcher: {e}")
        
        # Wait a moment before reopening
        time.sleep(2)
        
        # Find and activate Jagex Launcher
        launcher_found = self.find_jagex_launcher_window()
        if not launcher_found:
            print("Failed to find/activate Jagex Launcher")
            return False
        
        # Click play button
        play_clicked = self.click_launcher_play_button()
        if not play_clicked:
            print("Failed to click play button")
            return False
        
        # Monitor for login screen and complete login
        login_completed = self.monitor_for_login_screen_after_restart(
            timeout=120, 
            post_login_callback=post_login_callback
        )
        
        if login_completed:
            print("=" * 60)
            print("ACCOUNT LOGGED IN ERROR RESOLVED SUCCESSFULLY!")
            print("=" * 60)
            return True
        else:
            print("Failed to complete login after restart")
            return False

    def ensure_bag_open_and_check_last_slot(self, image_path, confidence=0.95, color_tolerance=30, shape_weight=0.7, color_weight=0.3):
        """
        Ensure the bag is open and check if the last slot contains the specified image.
        
        Args:
            image_path: Path to the image to look for in the last slot
            confidence: Confidence threshold for image matching (default: 0.95)
            color_tolerance: Color tolerance for CV3 matching (default: 30)
            shape_weight: Shape weight for CV3 matching (default: 0.7)
            color_weight: Color weight for CV3 matching (default: 0.3)
            
        Returns:
            bool: True if the image is found in the last slot (bag is full), False otherwise
        """
        print(f"Ensuring bag is open and checking last slot for {image_path}...")
        
        # First, check if bag is closed and open it if necessary
        bag_closed_region = self.get_scan_area("bag_closed")
        bag_closed_found = self.find_image_cv2(
            "image_library/bag_is_closed.png",
            region=bag_closed_region,
            threshold=0.90
        )
        
        if bag_closed_found:
            print("Bag is closed. Opening bag...")
            bag_opened = self.click_image_cv2_without_moving(
                "image_library/bag_is_closed.png",
                region=bag_closed_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if bag_opened:
                print("Bag opened successfully.")
                time.sleep(random.uniform(0.5, 1.0))  # Wait for bag to open
            else:
                print("Failed to open bag.")
                return False
        else:
            print("Bag is already open.")
        
        # Now check the last slot for the specified image
        bag_last_slot_region = self.get_scan_area("bag_last_slot")
        image_found = self.find_image_cv3(
            image_path,
            region=bag_last_slot_region,
            color_tolerance=color_tolerance,
            shape_weight=shape_weight,
            color_weight=color_weight
        )
        
        if image_found:
            print(f"Found {image_path} in last slot - bag is full.")
            return True
        else:
            print(f"Did not find {image_path} in last slot - bag has space.")
            return False

    def resolveLogin(self, post_login_callback=None):
        """
        Automatically resolve login issues and reconnect to the game.
        Handles various error scenarios and performs the complete login process.
        Checks for errors and login screen prompts simultaneously.
        
        Returns:
            True if login process was completed successfully, False otherwise
        """
        print("Checking for login issues and attempting to resolve...")
        
        # Track whether we actually perform a login action
        login_action_performed = False
        
        # Get the p2 region for error detection and login interactions
        p2_region = self.get_scan_area("p2")
        
        # Step 1: Check for all error scenarios and login prompts simultaneously
        print("Checking for errors and login screen prompts...")
        
        # Check for "Failed to login" error
        failed_login_error = self.find_image_cv2(
            "image_library/error_failed_to_login.png",
            region=p2_region,
            threshold=0.90
        )
        
        # Check for "Account logged in" error (internet connectivity issue)
        account_logged_in_error = self.find_image_cv2(
            "image_library/error_account_logged_in.png",
            region=p2_region,
            threshold=0.90
        )
        
        # Check for "Disconnected from server" error
        disconnected_error = self.find_image_cv2(
            "image_library/error_you_were_disconnected_from_the_server.png",
            region=p2_region,
            threshold=0.90
        )
        
        # Check for "Game servers being updated" error
        servers_updated_error = self.find_image_cv2(
            "image_library/error_game_servers_being_updated.png",
            region=p2_region,
            threshold=0.90
        )
        
        # Check for login screen prompts
        play_now_found = self.find_image_cv2(
            "image_library/login_play_now.png",
            region=p2_region,
            threshold=0.90
        )
        
        click_here_found = self.find_image_cv2(
            "image_library/login_click_here_to_play.png",
            region=p2_region,
            threshold=0.90
        )
        
        # Handle error scenarios
        if failed_login_error:
            print("Found 'Failed to login' error. Clicking try again button...")
            try_again_click = self.click_image_cv2_without_moving(
                "image_library/error_failed_to_login_try_again_button.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if try_again_click:
                print("Try again button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for error to clear
            else:
                print("Failed to click try again button.")
        
        if disconnected_error:
            print("Found 'Disconnected from server' error. Clicking OK button...")
            ok_button_click = self.click_image_cv2_without_moving(
                "image_library/error_you_were_disconnected_from_the_server_ok_button.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if ok_button_click:
                print("OK button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for error to clear
            else:
                print("Failed to click OK button.")
        
        if account_logged_in_error:
            print("Found 'Account logged in' error. This indicates an internet connectivity issue.")
            print("Attempting to dismiss error and initiating connectivity check and restart process...")
            
            # Try to find and click an OK button, but if not found, proceed anyway
            ok_button_click = self.click_image_cv2_without_moving(
                "image_library/error_account_logged_in_ok_button.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            
            if ok_button_click:
                print("OK button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for error to clear
            else:
                print("No OK button found for account logged in error, proceeding with restart process...")
                # Try pressing Escape key to dismiss the error dialog
                import pyautogui
                pyautogui.press('escape')
                time.sleep(random.uniform(1, 2))
            
            # Handle the account logged in error (internet connectivity issue)
            return self.handle_account_logged_in_error(post_login_callback)
        
        if servers_updated_error:
            print("Found 'Game servers being updated' error. This requires a 3-minute wait and launcher restart.")
            print("Clicking OK button and initiating restart process...")
            ok_button_click = self.click_image_cv2_without_moving(
                "image_library/error_game_servers_being_updated_ok_button.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if ok_button_click:
                print("OK button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for error to clear
                
                # Handle the special case of servers being updated
                return self.handle_servers_updated_restart(post_login_callback)
            else:
                print("Failed to click OK button.")
                return False
        
        # Check if we need to perform login process
        any_error_found = failed_login_error or account_logged_in_error or disconnected_error or servers_updated_error
        any_login_prompt_found = play_now_found or click_here_found
        
        if not any_error_found and not any_login_prompt_found:
            # No errors or login prompts detected - we're already logged in
            print("No login errors or prompts detected. Bot is already logged in and ready.")
            # Don't call setup callback since we didn't actually log in
            return True
        
        # Step 2: Handle "Play Now" button if found or if we had errors
        if play_now_found:
            print("Play Now button found. Clicking it...")
            login_action_performed = True  # Mark that we're performing a login action
            play_now_click = self.click_image_cv2_without_moving(
                "image_library/login_play_now.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if play_now_click:
                print("Play Now button clicked successfully.")
                time.sleep(random.uniform(2, 4))  # Wait for next screen
            else:
                print("Failed to click Play Now button.")
                return False
        elif any_error_found:
            # If we had errors but no Play Now button, wait for it to appear
            print("Waiting up to 20 seconds for Play Now button to appear after error resolution...")
            start_time = time.time()
            while time.time() - start_time < 20:
                play_now_found = self.find_image_cv2(
                    "image_library/login_play_now.png",
                    region=p2_region,
                    threshold=0.90
                )
                if play_now_found:
                    print("Play Now button found. Clicking it...")
                    play_now_click = self.click_image_cv2_without_moving(
                        "image_library/login_play_now.png",
                        region=p2_region,
                        confidence=0.90,
                        offset_range=(0, 3)
                    )
                    if play_now_click:
                        print("Play Now button clicked successfully.")
                        time.sleep(random.uniform(2, 4))  # Wait for next screen
                        break
                    else:
                        print("Failed to click Play Now button.")
                        return False
                time.sleep(1)
            else:
                print("Play Now button not found after waiting for errors. Login resolution failed.")
                return False
        
        # Step 3: Handle "Click here to play" button
        if click_here_found:
            print("Click here to play button found. Clicking it...")
            click_here_click = self.click_image_cv2_without_moving(
                "image_library/login_click_here_to_play.png",
                region=p2_region,
                confidence=0.90,
                offset_range=(0, 3)
            )
            if click_here_click:
                print("Click here to play button clicked successfully.")
                print("Login process completed. Waiting for game to load...")
                time.sleep(random.uniform(5, 10))  # Wait for game to load
                # Call post-login callback if provided and we actually performed a login action
                if post_login_callback and login_action_performed:
                    print("Running post-login setup...")
                    post_login_callback()
                return True
            else:
                print("Failed to click Click here to play button.")
                return False
        else:
            # Wait for "Click here to play" button to appear
            print("Waiting for 'Click here to play' button...")
            start_time = time.time()
            while time.time() - start_time < 60:
                click_here_found = self.find_image_cv2(
                    "image_library/login_click_here_to_play.png",
                    region=p2_region,
                    threshold=0.90
                )
                if click_here_found:
                    print("Click here to play button found. Clicking it...")
                    click_here_click = self.click_image_cv2_without_moving(
                        "image_library/login_click_here_to_play.png",
                        region=p2_region,
                        confidence=0.90,
                        offset_range=(0, 3)
                    )
                    if click_here_click:
                        print("Click here to play button clicked successfully.")
                        print("Login process completed. Waiting for game to load...")
                        time.sleep(random.uniform(5, 10))  # Wait for game to load
                        # Call post-login callback if provided and we actually performed a login action
                        if post_login_callback and login_action_performed:
                            print("Running post-login setup...")
                            post_login_callback()
                        return True
                    else:
                        print("Failed to click Click here to play button.")
                        return False
                time.sleep(2)
            else:
                print("Click here to play button not found within 60 seconds.")
                return False
