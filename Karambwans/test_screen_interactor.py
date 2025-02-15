# test_screen_interactor.py
import pytest
import pyautogui
import time
from screen_interactor import ScreenInteractor

# Create an instance of our class.
si = ScreenInteractor()

# def test_find_pixel_and_click_offset():
#     """
#     Test that:
#       1. A teal pixel (00FFFF) is found in the region (adjust region as needed).
#       2. The mouse is moved there, and after a 300 ms delay, a right click occurs at an offset.
#     """
#     # Define a region that is likely to contain your test content.
#     # For example: (x, y, width, height) – adjust as needed.
#     region = (1000, 450, 1500, 850)
#     target_color = "00FFFF"
#     found_pixel = si.find_pixel(target_color, region=region, tolerance=15)
#     assert found_pixel is not None, "Teal pixel not found in the defined region."
#     print(f"Found teal pixel at {found_pixel}. Moving mouse there.")
#     si.move_mouse_to(*found_pixel)
#     time.sleep(0.3)  # Wait for 300ms
#     click_position = si.click_with_offset(*found_pixel, offset_range_x=(-20, 20), offset_range_y=(-20, 20), button='right')
#     print(f"Right clicked at offset position {click_position}.")
#     # Verify that the offset is within our expected range.
#     assert abs(click_position[0] - found_pixel[0]) <= 20
#     assert abs(click_position[1] - found_pixel[1]) <= 20

# def test_find_and_click_image_randomly():
#     """
#     Test that:
#       1. The image 'raw_karambwan.png' is found on the screen.
#       2. A click is performed at a random location within the found image.
#     """
#     image_path = "C:\Git\OSRS_Runescape_Scripts\Karambwans\\raw_karambwan.png"  # Make sure this file is in your working directory.
#     print("Please ensure that 'raw_karambwan.png' is visible on your screen. Starting in 5 seconds...")
#     time.sleep(3)
#     # This is the bag area
#     region = (2225, 1025, 2528, 1391)
#     clicked_position = si.find_and_click_image_randomly(image_path, region=region, confidence=0.8)
#     assert clicked_position is not None, "Test image not found on the screen."
#     print(f"Clicked on test image at position {clicked_position}.")

def test_zoom_out():
    # Step 3: Zoom out and click on the pink fairy ring.
    print("Zooming out...")
    time.sleep(2)
    # full zoom out
    si.zoom_out(times=10)
    time.sleep(1)
    si.zoom_in(times=4)
    # time.sleep(2)
    # si.zoom_out(times=3)

# def test_click_without_moving():
#     """
#     Test that a click sent without moving the mouse does not change the mouse's current position.
#     """
#     current_position = pyautogui.position()
#     print(f"Current mouse position: {current_position}. Clicking without moving.")
#     clicked_position = si.click_without_moving(button='left')
#     assert clicked_position == current_position, "Mouse position changed after clicking without moving."
#     print(f"Clicked at {clicked_position} without moving the mouse.")


if __name__ == "__main__":
    # This allows you to run the tests by executing this file directly.
    time.sleep(3)
    import pytest
    pytest.main([__file__])
