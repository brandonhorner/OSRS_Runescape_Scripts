import cv2
import numpy as np
import pyautogui
import time
import os
from screen_interactor import ScreenInteractor

class ImageDetectionTest:
    def __init__(self, template_path="Karambwans/take_seaweed_spore.png"):
        self.si = ScreenInteractor()
        self.template_path = template_path
        
        # Ensure the template exists
        if not os.path.exists(template_path):
            print(f"ERROR: Template image not found at: {template_path}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Files in directory: {os.listdir('Karambwans/' if os.path.exists('Karambwans/') else '.')}")
            return
            
        # Load the template for testing
        self.template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if self.template is None:
            print(f"ERROR: Could not load template image: {template_path}")
            return
            
        print(f"Template loaded successfully: {template_path}")
        print(f"Template dimensions: {self.template.shape}")
    
    def test_full_screen_detection(self, thresholds=[0.9, 0.8, 0.7, 0.6]):
        """Test detection across the full screen with different threshold values."""
        print("\n--- Testing Full Screen Detection ---")
        screenshot = pyautogui.screenshot()
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        for threshold in thresholds:
            start_time = time.time()
            result = cv2.matchTemplate(screenshot_np, self.template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            end_time = time.time()
            
            print(f"\nThreshold: {threshold}")
            print(f"Max match value: {max_val:.4f}")
            print(f"Match location (if above threshold): {max_loc if max_val >= threshold else 'No match'}")
            print(f"Detection time: {(end_time - start_time)*1000:.2f}ms")
            
            if max_val >= threshold:
                h, w = self.template.shape[:2]
                # Create a copy for visualization
                vis_img = screenshot_np.copy()
                # Draw rectangle
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv2.rectangle(vis_img, top_left, bottom_right, (0, 255, 0), 2)
                
                # Save the visualization for inspection
                output_path = f"match_threshold_{threshold:.1f}.png"
                cv2.imwrite(output_path, vis_img)
                print(f"Visualization saved to: {output_path}")
    
    def test_screen_interactor_detection(self, thresholds=[0.9, 0.8, 0.7, 0.6]):
        """Test detection using the ScreenInteractor class."""
        print("\n--- Testing ScreenInteractor Detection ---")
        
        for threshold in thresholds:
            print(f"\nTesting with threshold: {threshold}")
            start_time = time.time()
            location = self.si.find_image_cv2(self.template_path, region=None, threshold=threshold)
            end_time = time.time()
            
            print(f"Detection time: {(end_time - start_time)*1000:.2f}ms")
            if location:
                print(f"Image found at: {location}")
                # Take a screenshot with highlight
                screenshot = pyautogui.screenshot()
                screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                # Draw circle at center position
                cv2.circle(screenshot_np, location, 10, (0, 255, 0), 2)
                # Draw circle at where it would click with offset
                offset_x = np.random.randint(-8, 9)
                offset_y = np.random.randint(-2, 3)
                click_loc = (location[0] + offset_x, location[1] + offset_y)
                cv2.circle(screenshot_np, click_loc, 5, (0, 0, 255), -1)
                
                # Save the visualization
                output_path = f"si_match_threshold_{threshold:.1f}.png"
                cv2.imwrite(output_path, screenshot_np)
                print(f"Visualization saved to: {output_path}")
            else:
                print("Image not found with this threshold")
    
    def interactive_test(self):
        """Interactive test where you can position your cursor and test detection."""
        print("\n--- Interactive Test ---")
        print("Position your cursor over where you expect the 'Take seaweed spore' option to be.")
        print("You have 5 seconds to position your cursor...")
        time.sleep(5)
        
        # Get cursor position
        x, y = pyautogui.position()
        print(f"Testing detection around cursor position: ({x}, {y})")
        
        # Define a region around the cursor
        region_size = 200
        region = (x - region_size//2, y - region_size//2, region_size, region_size)
        
        # Test detection in this region
        for threshold in [0.9, 0.8, 0.7, 0.6]:
            print(f"\nTesting with threshold: {threshold}")
            location = self.si.find_image_cv2(self.template_path, region=region, threshold=threshold)
            
            if location:
                print(f"Image found at: {location}")
                # Take a screenshot with highlight
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                # Adjust location relative to region
                rel_x = location[0] - region[0]
                rel_y = location[1] - region[1]
                # Draw circle at center position
                cv2.circle(screenshot_np, (rel_x, rel_y), 10, (0, 255, 0), 2)
                
                # Save the visualization
                output_path = f"interactive_match_threshold_{threshold:.1f}.png"
                cv2.imwrite(output_path, screenshot_np)
                print(f"Visualization saved to: {output_path}")
            else:
                print("Image not found with this threshold")

def main():
    test = ImageDetectionTest()
    
    # Test 1: Full screen detection
    test.test_full_screen_detection()
    
    # Test 2: ScreenInteractor detection
    test.test_screen_interactor_detection()
    
    # Test 3: Interactive test
    test.interactive_test()
    
    print("\nAll tests completed. Check the output images for visualization.")

if __name__ == "__main__":
    main() 