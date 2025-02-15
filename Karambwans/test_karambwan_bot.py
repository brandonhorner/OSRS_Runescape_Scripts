# test_karambwan_bot.py
import pytest
import time
import random
from karambwan_bot import KarambwanBot
from screen_interactor import ScreenInteractor

# Create an instance of our ScreenInteractor and our bot.
si = ScreenInteractor()
bot = KarambwanBot(si)

# def test_perform_fishing_spot_interaction():
#     """
#     Test that:
#       1. The bot can locate a teal pixel in the given region (p2 area).
#       2. It moves the mouse there, waits a short period, and then right-clicks at an offset.
#     """
#     # Define the region for the fishing spot (p2 area, top-middle of your screen)
#     # Adjust these values to match your screen setup.
#     region = (900, 25, 600, 775)
#     click_pos = bot.perform_fishing_spot_interaction(pixel_region=region)
#     print(f"Test: Right-click performed at {click_pos}.")
#     # We can’t assert an exact value, but we can check that a tuple (x,y) was returned.
#     assert isinstance(click_pos, tuple) and len(click_pos) == 2

# def test_select_fishing_option():
#     """
#     Test that:
#       1. The bot finds the "Fish Fishing spot" option via image search.
#       2. It clicks at a random location inside the found image.
#     """
#     # Provide the path to your fishing option image.
#     # Ensure that 'fish_option.png' is visible on the screen.
#     image_path = "Karambwans\\fish_option.png"
#     # Optionally define a region where this image is expected.
#     region = (900, 25, 600, 775)
#     print("Please ensure that 'fish_option.png' is visible in the defined region. Starting in 3 seconds...")
#     time.sleep(3)
#     click_pos = bot.select_fishing_option(image_path, region=region, confidence=0.8)
#     print(f"Test: Fishing option clicked at {click_pos}.")
#     assert isinstance(click_pos, tuple) and len(click_pos) == 2



def test_click_karambwan():
    """
    Test the alternative click function that uses click_without_moving to click on the karambwan image.
    Ensure that the karambwan image (e.g. 'raw_karambwan.png') is visible in the specified region.
    """
    image_path = r"Karambwans\raw_karambwan.png"
    # Define the region where the image is expected.
    region = (900, 25, 600, 775)
    click_pos = bot.click_karambwan(image_path, region=region, confidence=0.8, offset_range=(-10, 10))
    print(f"Click performed at {click_pos}.")
    assert isinstance(click_pos, tuple) and len(click_pos) == 2



if __name__ == "__main__":
    import pytest
    time.sleep(3)
    pytest.main([__file__])
