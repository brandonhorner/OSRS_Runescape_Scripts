"""
Gem mining bot for OSRS (low-visibility / Pi path only).
Starts at bank deposit box. Trip to gem nodes via intermediate tiles (yellow → red → pink),
zoom in, mine until full (inventory full = chat message). Return to bank via red/yellow tiles,
deposit, repeat.

Requires bot_config.json from running setup_config.py first (resolution).
"""
import sys
import time
import random

import pyautogui
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor
from bot_config import require_config, get_os, OS_WINDOWS, OS_LINUX


# Image library paths
DEPOSIT_OPTION_IMAGE = "image_library/deposit_bank_deposit_option.png"
DEPOSIT_ALL_IMAGE = "image_library/deposit_all_inventory.png"
BANK_CLOSE_IMAGE = "image_library/bank_deposit_close.png"
MINE_GEM_ROCKS_OPTION_IMAGE = "image_library/mine_gem_rocks_option.png"
MINING_INACTIVE_IMAGE = "image_library/mining_inactive.png"
INVENTORY_FULL_IMAGE = "image_library/inventory_full.png"

# Hex colors for tiles and nodes (find_pixel / pixel_click_without_moving / find_pixel_right_click_confirm)
PIXEL_COLOR_YELLOW = "FFFF00"   # yellow walk tile
PIXEL_COLOR_RED = "FF0000"     # red walk tile
PIXEL_COLOR_PINK = "FF00FF"    # pink gem node
PIXEL_COLOR_TEAL = "00FFFF"    # teal bank deposit box

MAX_CONSECUTIVE_PINK_FAILURES = 3  # exit mining loop after this many failures to find/click a node


def setup_gem_mining(si):
    """Initial setup: zoom out, brief 'w' to align camera above character, compass, inventory.
    Pi/low-visibility: user must focus the game window before starting (no Win32 activate).
    """
    print("Starting gem mining setup...")
    print("Ensure game window is focused (Pi/low-visibility mode).")
    time.sleep(0.5)

    print("Zooming out for better visibility...")
    si.zoom_out(times=5, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))

    print("Holding 'w' briefly to align camera above character...")
    pyautogui.keyDown("w")
    time.sleep(random.uniform(1.5, 2.0))
    pyautogui.keyUp("w")
    time.sleep(random.uniform(0.2, 0.4))

    print("Clicking compass to correct north...")
    compass_clicked = si.click_on_compass(region="p3", confidence=0.90)
    if not compass_clicked:
        print("Warning: Could not click compass. Continuing anyway.")
    else:
        time.sleep(random.uniform(0.3, 0.6))

    print("Opening inventory...")
    pyautogui.press("b")
    time.sleep(random.uniform(0.5, 1.0))

    print("Gem mining setup complete.")
    return True


def click_tile_by_color_center_then_screen(si, color_hex, tolerance=10):
    """Try to find and left-click the tile by color in game_screen_center first, then game_screen. Returns True if clicked."""
    for region_name in ("game_screen_center", "game_screen"):
        try:
            si.pixel_click_without_moving(color_hex, region_name, tolerance=tolerance, button="left")
            return True
        except ValueError:
            continue
    return False


def click_tile_by_color_p5_then_screen(si, color_hex, tolerance=10):
    """Try to find and left-click the tile by color in p5 first, then game_screen_center, then game_screen. Returns True if clicked."""
    for region_name in ("p5", "game_screen_center", "game_screen"):
        try:
            si.pixel_click_without_moving(color_hex, region_name, tolerance=tolerance, button="left")
            return True
        except ValueError:
            continue
    return False


def _run_to_mining_pi(si):
    """
    Low-visibility path: yellow tile → 7-9s → red tile → interact with first pink node → wait 3-5s.
    Tiles and pink use find_pixel / pixel_click_without_moving / find_pixel_right_click_confirm (color-based).
    """
    if not click_tile_by_color_center_then_screen(si, PIXEL_COLOR_YELLOW):
        print("Yellow tile not found (game_screen_center or game_screen).")
        return False
    print("Clicked yellow tile.")

    wait = random.uniform(5.5, 7.0)
    print(f"Waiting {wait:.1f}s...")
    time.sleep(wait)

    if not click_tile_by_color_center_then_screen(si, PIXEL_COLOR_RED):
        print("Red tile not found (game_screen_center or game_screen).")
        return False
    print("Clicked red tile.")

    wait = random.uniform(7.0, 9.0)
    print(f"Waiting {wait:.1f}s...")
    time.sleep(wait)

    # First pink: bottom-up search (16 horizontal slices) with find_pixel_right_click_confirm
    print("Looking for pink node on game_screen (bottom-up slices)...")
    game_screen = si.get_scan_area("game_screen")
    x, y, w, h = game_screen
    slice_h = max(1, h // 16)
    found = False
    for i in range(15, -1, -1):
        slice_region = (x, y + i * slice_h, w, slice_h)
        if si.find_pixel_right_click_confirm(
                PIXEL_COLOR_PINK, MINE_GEM_ROCKS_OPTION_IMAGE,
                region=slice_region, attempts=2):
            found = True
            break
    if not found:
        print("No pink node found on game_screen.")
        return False
    print("Found pink node, right-clicked and selected mine.")

    # Zoom in: Windows uses less zoom; Linux/Pi uses small scroll amount and slower delay
    if get_os() == OS_WINDOWS:
        print("Zooming in (Windows)...")
        si.zoom_in(times=2, delay_low=0.005, delay_high=0.01, scroll_amount=400)
    else:
        print("Zooming in (Linux/Pi)...")
        si.zoom_in(times=8, delay_low=0.2, delay_high=0.3, scroll_amount=1)
    time.sleep(random.uniform(0.4, 0.8))

    wait = random.uniform(3.5, 5.0)
    print(f"Waiting {wait:.1f}s before monitoring for NOT mining...")
    time.sleep(wait)

    return True


def run_to_mining_via_pink_node(si):
    """Use intermediate tiles (yellow → red → pink), zoom in, short wait. Ready for mining loop."""
    return _run_to_mining_pi(si)


def is_inventory_full_message_in_chat(si):
    """
    Return True if the inventory-full message appears in the search area (p4).
    """
    loc = si.find_image_cv2(INVENTORY_FULL_IMAGE, region="chat_area", threshold=0.85)
    return loc is not None


def is_last_inventory_slot_filled(si):
    """
    Alternative: True if the last inventory slot appears to contain an item (not blank).
    Uses bag_last_slot region and a simple heuristic. Prefer is_inventory_full_message_in_chat.
    """
    region = si.get_scan_area("bag_last_slot")
    try:
        screenshot = pyautogui.screenshot(region=region)
    except Exception:
        return False
    pixels = list(screenshot.getdata())
    if not pixels:
        return False
    r_avg = sum(p[0] for p in pixels) / len(pixels)
    g_avg = sum(p[1] for p in pixels) / len(pixels)
    b_avg = sum(p[2] for p in pixels) / len(pixels)
    brightness = (r_avg + g_avg + b_avg) / 3
    if brightness > 85:
        return True
    if r_avg > 100 or g_avg > 100 or b_avg > 100:
        return True
    return False


def mine_until_inventory_full(si):
    """
    Caller has already run to mining and zoomed in. Right-click closest pink node, left-click
    mine_gem_rocks_option. ImageMonitor for mining_inactive.png in p1 (NOT mining). Then find
    next closest pink and repeat until inventory full message appears in chat.
    Exits after MAX_CONSECUTIVE_PINK_FAILURES failures (no pink found or click failed).
    """
    consecutive_failures = 0

    while True:
        if is_inventory_full_message_in_chat(si):
            print("Inventory full (chat message) - stopping mining.")
            break

        if consecutive_failures >= MAX_CONSECUTIVE_PINK_FAILURES:
            print(f"No pink node found or click failed {MAX_CONSECUTIVE_PINK_FAILURES} times - leaving mining area.")
            break

        # Right-click closest pink node (find_pixel_right_click_confirm)
        pink_region = _region_around_center(800)
        if not si.find_pixel_right_click_confirm(
                PIXEL_COLOR_PINK, MINE_GEM_ROCKS_OPTION_IMAGE,
                region=pink_region, attempts=PINK_NODE_RESEARCH_ATTEMPTS):
            consecutive_failures += 1
            print(f"Failed to find/click pink node ({consecutive_failures}/{MAX_CONSECUTIVE_PINK_FAILURES}) - waiting 1s and retrying...")
            time.sleep(1.0)
            continue

        consecutive_failures = 0  # reset on success

        time.sleep(random.uniform(3.0, 5.0))

        print("Mining started - waiting for mining_inactive (NOT mining) in p1...")
        inactive_monitor = ImageMonitor(
            screen_interactor=si,
            image_path=MINING_INACTIVE_IMAGE,
            region="p1",
            confidence=0.94,
            check_interval=1.0,
            wait_for="appear",
        )
        inactive_monitor.start()
        if inactive_monitor.wait_for_condition(timeout=60):
            inactive_monitor.stop()
            print("Mining inactive detected.")
        else:
            inactive_monitor.stop()
            print("Timeout waiting for mining_inactive - continuing to next node.")

        # Check inventory full before going to next node so we don't try to mine when full
        if is_inventory_full_message_in_chat(si):
            print("Inventory full (chat message) - stopping mining.")
            break

        print("Looking for next closest pink node...")
        si.maybe_afk()
        time.sleep(random.uniform(0.3, 0.7))

    return True


def return_to_bank_and_deposit(si):
    """
    Zoom out. Return trip: look for red tile, yellow tile, and bank (teal) in p5 first.
    Walk to red (wait), walk to yellow (wait). From yellow, right-click teal in p5 and confirm; retry teal a few times if we fail.
    If still no bank, walk to fallback red and retry teal a few times. After success, wait ~4.5s for pane.
    ImageMonitor for deposit all inventory button, click it, close bank.
    """
    print("Zooming out...")
    si.zoom_out(times=5, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))

    # Return trip: red and yellow tiles in p5 first, then game_screen_center, then game_screen
    print("Walking to red tile (p5 then game_screen_center then game_screen)...")
    if not click_tile_by_color_p5_then_screen(si, PIXEL_COLOR_RED):
        print("Red tile not found on return.")
        return False
    print("Clicked red tile.")
    wait = random.uniform(7.8, 8.4)
    print(f"Waiting {wait:.1f}s to reach yellow tile area...")
    time.sleep(wait)

    print("Walking to yellow tile (p5 then game_screen_center then game_screen)...")
    if not click_tile_by_color_p5_then_screen(si, PIXEL_COLOR_YELLOW):
        print("Yellow tile not found on return.")
        return False
    print("Clicked yellow tile.")
    wait = random.uniform(5.8, 6.4)
    print(f"Waiting {wait:.1f}s at yellow tile...")
    time.sleep(wait)

    # Bank (teal) in p5; retry finding teal a few times before moving to fallback red
    bank_region = si.get_scan_area("p5")
    max_teal_rounds = 3
    success = False
    for round_num in range(1, max_teal_rounds + 1):
        print(f"Interacting with bank deposit box in p5 (teal round {round_num}/{max_teal_rounds})...")
        success = si.find_pixel_right_click_confirm(PIXEL_COLOR_TEAL, DEPOSIT_OPTION_IMAGE, attempts=5, region=bank_region)
        if success:
            break
        if round_num < max_teal_rounds:
            time.sleep(random.uniform(0.5, 1.0))

    if not success:
        print("Could not interact with deposit box from yellow tile. Moving to fallback red tile...")

        print("Walking to fallback red tile (p5 then game_screen_center then game_screen)...")
        if not click_tile_by_color_p5_then_screen(si, PIXEL_COLOR_RED):
            print("Fallback red tile not found on return.")
            return False
        print("Clicked fallback red tile.")
        wait = random.uniform(5.8, 6.4)
        print(f"Waiting {wait:.1f}s at fallback red tile (near bank)...")
        time.sleep(wait)

        for round_num in range(1, max_teal_rounds + 1):
            print(f"Interacting with bank deposit box in p5 from fallback red (teal round {round_num}/{max_teal_rounds})...")
            success = si.find_pixel_right_click_confirm(PIXEL_COLOR_TEAL, DEPOSIT_OPTION_IMAGE, attempts=5, region=bank_region)
            if success:
                break
            if round_num < max_teal_rounds:
                time.sleep(random.uniform(0.5, 1.0))

        if not success:
            print("Failed to open deposit box menu from both yellow and fallback red tiles.")
            return False

    print("Deposit box interaction succeeded.")

    wait = random.uniform(4.5, 5.0)
    print(f"Waiting {wait:.1f}s for character to open bank deposit pane...")
    time.sleep(wait)

    # Wait for deposit all inventory button to appear, then click it
    print("Waiting for deposit all inventory button...")
    bank_monitor = ImageMonitor(
        screen_interactor=si,
        image_path=DEPOSIT_ALL_IMAGE,
        region="bank_deposit_box",
        confidence=0.92,
        check_interval=1.5,
        wait_for="appear",
    )
    bank_monitor.start()
    if not bank_monitor.wait_for_condition(timeout=20):
        print("Bank interface did not appear.")
        bank_monitor.stop()
        return False
    bank_monitor.stop()

    time.sleep(1.5)

    # Search same region as ImageMonitor (game_screen_center) so we find the button we just detected
    deposit_click = si.click_image_cv2_without_moving(
        DEPOSIT_ALL_IMAGE,
        region="bank_deposit_box",
        confidence=0.88,
        offset_range=(0, 5),
    )
    if not deposit_click:
        time.sleep(2.0)
        deposit_click = si.click_image_cv2_without_moving(
            DEPOSIT_ALL_IMAGE,
            region="bank_deposit_box",
            confidence=0.85,
            offset_range=(0, 5),
        )
    if not deposit_click:
        print("Failed to click deposit all inventory.")
        return False
    time.sleep(1.0)

    # Close bank (deposit box close button) - search same region as deposit UI first
    close_click = si.click_image_cv2_without_moving(
        BANK_CLOSE_IMAGE,
        region="bank_deposit_box",
        confidence=0.88,
        offset_range=(0, 5),
    )
    if not close_click:
        time.sleep(1.0)
        close_click = si.click_image_cv2_without_moving(
            BANK_CLOSE_IMAGE,
            region="bank_deposit_box",
            confidence=0.85,
            offset_range=(0, 5),
        )
    if not close_click:
        close_click = si.click_image_cv2_without_moving(
            BANK_CLOSE_IMAGE,
            region="bank_deposit_box",
            confidence=0.85,
            offset_range=(0, 5),
        )
    if close_click:
        print("Bank closed.")
    else:
        print("Warning: Bank close button not found. Attempting to continue...")
    si.maybe_afk()
    return True


def _offset_ranges_for_pixel_relative_to_center(pixel_x, pixel_y, screen_w, screen_h):
    """
    Return (offset_x_range, offset_y_range) from the found pixel so we click toward the
    node. Small offsets so we still hit the node when zoomed out (nodes appear smaller).
    """
    cx, cy = screen_w // 2, screen_h // 2
    left_of_center = pixel_x < cx
    right_of_center = pixel_x > cx
    below_center = pixel_y > cy
    above_center = pixel_y < cy

    if below_center and left_of_center:
        return ((-7, -2), (2, 7))    # down-left
    if below_center and right_of_center:
        return ((2, 7), (2, 7))      # down-right
    if above_center and left_of_center:
        return ((-7, -2), (-7, -2))  # up-left
    if above_center and right_of_center:
        return ((2, 7), (-7, -2))    # up-right
    if right_of_center:
        return ((2, 7), (-2, 2))     # right of us
    if left_of_center:
        return ((-7, -2), (-2, 2))   # left of us
    if below_center:
        return ((-2, 2), (2, 7))     # below
    return ((-2, 2), (-7, -2))      # above


def _right_click_pixel_with_directional_converge(si, pixel_xy, confirm_image_path, max_attempts=5):
    """
    For a pixel that is the *closest* to the character (e.g. from find_closest_pixel).
    5 steps: 4 right-clicks with directional offset (converging toward pixel), then 1 with
    opposite-direction nudge + up/down. Then find and left-click confirm image.
    """
    x, y = pixel_xy
    screen_w, screen_h = pyautogui.size()
    orig = pyautogui.position()

    (ox_lo, ox_hi), (oy_lo, oy_hi) = _offset_ranges_for_pixel_relative_to_center(x, y, screen_w, screen_h)

    for attempt in range(max_attempts):
        scale = 1.0 - (attempt / max(1, max_attempts - 1))
        if scale > 0:
            offset_x = int(round(random.uniform(ox_lo, ox_hi) * scale))
            offset_y = int(round(random.uniform(oy_lo, oy_hi) * scale))
        else:
            mid_x = (ox_lo + ox_hi) / 2
            mid_y = (oy_lo + oy_hi) / 2
            opposite_x = random.randint(1, 3) if mid_x < 0 else random.randint(-3, -1)
            opposite_y = random.randint(1, 3) if mid_y < 0 else random.randint(-3, -1)
            offset_x = opposite_x
            offset_y = opposite_y + random.randint(-1, 1)
        target_x = max(0, min(x + offset_x, screen_w - 1))
        target_y = max(0, min(y + offset_y, screen_h - 1))

        pyautogui.moveTo(target_x, target_y)
        time.sleep(random.uniform(0.01, 0.02))
        pyautogui.click(button="right")

        left = max(0, target_x - 300)
        right = min(screen_w, target_x + 300)
        top = max(0, target_y - screen_h // 2)
        bottom = min(screen_h, target_y + screen_h // 2)
        search_region = (left, top, right - left, bottom - top)
        time.sleep(random.uniform(0.15, 0.3))

        for conf_attempt in range(4):
            conf = max(0.72, 0.90 - conf_attempt * 0.03)
            try:
                loc = si.find_image_cv2(confirm_image_path, region=search_region, threshold=conf)
                if loc:
                    cx = loc[0] + random.randint(-6, 6)
                    cy = loc[1] + random.randint(-3, 3)
                    pyautogui.moveTo(cx, cy)
                    time.sleep(0.04)
                    pyautogui.click()
                    pyautogui.moveTo(orig)
                    return True
            except Exception:
                pass
            time.sleep(0.05)

        reset_x = max(0, min(target_x + random.randint(180, 350), screen_w - 1))
        reset_y = max(0, min(target_y + random.randint(-350, -180), screen_h - 1))
        pyautogui.moveTo(reset_x, reset_y)
        time.sleep(0.06)
    pyautogui.moveTo(orig)
    return False


PINK_NODE_RESEARCH_ATTEMPTS = 7  # max attempts for find_pixel_right_click_confirm on pink node


def _region_around_center(size=800):
    """Region centered on screen (same effective area as find_closest_pixel max_radius)."""
    screen_w, screen_h = pyautogui.size()
    cx, cy = screen_w // 2, screen_h // 2
    half = size // 2
    left = max(0, cx - half)
    top = max(0, cy - half)
    w = min(size, screen_w - left)
    h = min(size, screen_h - top)
    return (left, top, w, h)


def test_yellow_tile(si, iterations=5):
    """
    Test finding and clicking the yellow tile (pixel_click_without_moving, game_screen_center then game_screen).
    Run: python mining_gem_shilo.py test-yellow [N]
    """
    print("Testing yellow tile (color-based: game_screen_center then game_screen).")
    print("Ensure game window is focused and yellow tile is visible.")
    for i in range(iterations):
        print(f"\n--- Attempt {i + 1}/{iterations} ---")
        ok = click_tile_by_color_center_then_screen(si, PIXEL_COLOR_YELLOW)
        if not ok:
            print("  Yellow tile NOT found in game_screen_center or game_screen.")
            if i < iterations - 1:
                time.sleep(2.0)
            continue
        print("  Found and clicked yellow tile.")
        if i < iterations - 1:
            time.sleep(2.0)
    print("\nTest done.")


def test_pink_mining_loop(si, iterations=5):
    """
    Run find_pixel_right_click_confirm for pink N times (game_screen region).
    Run: python mining_gem_shilo.py test-pink [N]
    """
    game_screen = si.get_scan_area("game_screen")
    print(f"Test: pink mining loop ({iterations} iterations), region=game_screen. Using find_pixel_right_click_confirm.")
    for i in range(iterations):
        ok = si.find_pixel_right_click_confirm(
            PIXEL_COLOR_PINK, MINE_GEM_ROCKS_OPTION_IMAGE,
            region=game_screen, attempts=5)
        print(f"  {i + 1}/{iterations} Result: {ok}")
        if i < iterations - 1:
            time.sleep(2.0)
    print("Test done.")


def main_loop(max_runs=10):
    """Run until we have max_runs successful deposits (each deposit = one full mining run + bank)."""
    require_config()
    si = ScreenInteractor()
    print("Starting gem mining bot (low-visibility / Pi path) in 3 seconds...")
    time.sleep(3)
    if not setup_gem_mining(si):
        print("Setup failed. Exiting.")
        return

    completed_deposits = 0
    failed_runs = 0
    max_failed_runs = 20

    while completed_deposits < max_runs:
        print(f"\n--- Run (target: {completed_deposits + 1}/{max_runs} successful deposits) ---")

        if not run_to_mining_via_pink_node(si):
            print("Failed to run to mining (pink node). Retrying...")
            failed_runs += 1
            if failed_runs >= max_failed_runs:
                print(f"Aborting: failed to start a run {failed_runs} times in a row.")
                break
            continue

        mine_until_inventory_full(si)

        if not return_to_bank_and_deposit(si):
            print("Failed to bank. Retrying...")
            continue

        completed_deposits += 1
        failed_runs = 0  # reset failure counter after a successful full run
        print(f"Successful deposit {completed_deposits}/{max_runs}.")
        time.sleep(random.uniform(1.0, 2.0))

    print(f"Gem mining bot finished. Completed {completed_deposits} deposits.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test-yellow":
        require_config()
        si = ScreenInteractor()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        test_yellow_tile(si, iterations=n)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test-pink":
        require_config()
        si = ScreenInteractor()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        test_pink_mining_loop(si, iterations=n)
        sys.exit(0)
    main_loop(max_runs=50)
