"""
Gem mining bot for OSRS.
Starts at bank deposit box (image 1). Trip to gem nodes: right-click a pink node in p1 or p2
(random), wait 18-30s to run there, zoom in, then mine until full (inventory full = chat message; monitor mining_inactive in p1).
Returns to bank via red/yellow tiles, deposits, repeat.

Supports two modes via config (mining_gem_config.json):
- Normal: full visibility (e.g. 117 HD), direct pink click + long run, camera angle in setup.
- Low visibility (Pi / no 117 HD): first-run prompt; setup skips camera angle; run to mining
  uses intermediate tiles (yellow p1/p2 → 7-9s → red p1/p2 → 6-7s → pink → zoom → 3-5s).
"""
import json
import os
import time
import random
from datetime import datetime

import pyautogui
from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor

DEBUG_SCREENSHOTS_DIR = "debug_screenshots"
CONFIG_FILENAME = "mining_gem_config.json"
CONFIG_KEY_LOW_VISIBILITY = "low_visibility"


# Image library paths
DEPOSIT_OPTION_IMAGE = "image_library/deposit_bank_deposit_option.png"
DEPOSIT_ALL_IMAGE = "image_library/deposit_all_inventory.png"
BANK_CLOSE_IMAGE = "image_library/bank_deposit_close.png"
MINE_GEM_ROCKS_OPTION_IMAGE = "image_library/mine_gem_rocks_option.png"
MINING_INACTIVE_IMAGE = "image_library/mining_inactive.png"
INVENTORY_FULL_IMAGE = "image_library/inventory_full.png"

# Colors for overlay markers and nodes
COLOR_YELLOW = "FFFF00"
COLOR_RED = "FF0000"
COLOR_TEAL = "00FFFF"  # bank deposit box
COLOR_PINK = "FF00FF"  # gem mining nodes (exact match, tolerance=0)

MAX_CONSECUTIVE_PINK_FAILURES = 20  # exit mining loop after this many failures to find/click a node
AFK_CHANCE = 0.05  # 5% chance to idle at various steps (tiles, bank steps, mining)
AFK_MIN = 3.0
AFK_MAX = 90.0  # 1.5 min
# Bell curve centered near 25th percentile of [AFK_MIN, AFK_MAX] so most AFKs are short
_AFK_MEAN = AFK_MIN + 0.25 * (AFK_MAX - AFK_MIN)  # ~24.75s
_AFK_SIGMA = 20.0  # spread; result is clipped to [AFK_MIN, AFK_MAX]


def _config_path():
    """Path to config file (same directory as this script)."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILENAME)


def load_config():
    """Load config dict. Returns {} if file missing or invalid."""
    path = _config_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(config):
    """Overwrite config file with given dict."""
    path = _config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_low_visibility_config():
    """
    Return low_visibility flag. If config doesn't exist or key missing, prompt once
    ('Running on low visibility / Pi (no 117 HD)? [y/N]:'), save config, and return.
    """
    config = load_config()
    if CONFIG_KEY_LOW_VISIBILITY in config:
        return config[CONFIG_KEY_LOW_VISIBILITY]
    try:
        answer = input("Running on low visibility / Pi (no 117 HD)? [y/N]: ").strip().lower()
    except EOFError:
        answer = "n"
    low = answer in ("y", "yes")
    config[CONFIG_KEY_LOW_VISIBILITY] = low
    save_config(config)
    print(f"Saved config: {CONFIG_FILENAME} -> low_visibility = {low}")
    return low


def _random_afk_duration():
    """Return a single AFK duration (3s to 1.5min) from a normal distribution leaning toward the short end (25th percentile)."""
    t = random.gauss(_AFK_MEAN, _AFK_SIGMA)
    return max(AFK_MIN, min(AFK_MAX, t))


def _maybe_afk():
    """5% chance to idle 3s–1.5min (bell curve, leaning short) to simulate multitasking."""
    if random.random() < AFK_CHANCE:
        extra = _random_afk_duration()
        print(f"Simulating multitasking - idling for {extra:.1f}s...")
        time.sleep(extra)


def save_debug_screenshot(reason="failure"):
    """Take a screenshot and save to debug_screenshots/ with timestamp and reason."""
    os.makedirs(DEBUG_SCREENSHOTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_reason = "".join(c if c.isalnum() or c in "-_" else "_" for c in reason)
    filename = f"{stamp}_{safe_reason}.png"
    path = os.path.join(DEBUG_SCREENSHOTS_DIR, filename)
    try:
        im = pyautogui.screenshot()
        im.save(path)
        print(f"Debug screenshot saved: {path}")
    except Exception as e:
        print(f"Could not save debug screenshot: {e}")


def setup_gem_mining(si, low_visibility=False):
    """Initial setup: activate game window, zoom out; if not low_visibility, camera up (w) then down (s); compass, inventory."""
    print("Starting gem mining setup...")
    if low_visibility:
        print("Low visibility mode: skipping camera angle (w/s).")

    print("Activating game window...")
    if si.activate_game_window():
        time.sleep(0.5)
    else:
        print("Warning: Could not activate game window. Key inputs may go to the wrong app.")

    print("Zooming out for better visibility...")
    si.zoom_out(times=5, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))

    if not low_visibility:
        print("Holding 'w' to put camera up...")
        pyautogui.keyDown("w")
        time.sleep(random.uniform(1.5, 2.0))
        pyautogui.keyUp("w")
        time.sleep(random.uniform(0.2, 0.4))

        print("Holding 's' 0.7-0.9s to bring camera down a bit...")
        pyautogui.keyDown("s")
        time.sleep(random.uniform(0.7, 0.9))
        pyautogui.keyUp("s")
        time.sleep(random.uniform(0.3, 0.5))

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


def click_tile_randomly(si, color_hex, region, tolerance=5, offset_range=(-18, 18)):
    """Find a pixel of color in region and left-click randomly around that tile.

    Uses a wider offset so we don't always land on the exact same tile – movement looks less robotic.
    """
    region_resolved = si.resolve_region(region)
    found = si.find_pixel(color_hex, region=region_resolved, tolerance=tolerance)
    if not found:
        return None
    ox = random.randint(offset_range[0], offset_range[1])
    oy = random.randint(offset_range[0], offset_range[1])
    x = max(0, min(found[0] + ox, pyautogui.size()[0] - 1))
    y = max(0, min(found[1] + oy, pyautogui.size()[1] - 1))
    pyautogui.moveTo(x, y)
    time.sleep(random.uniform(0.05, 0.12))
    pyautogui.click()
    return (x, y)


def _run_to_mining_pi(si):
    """
    Low-visibility path: yellow tile (p1 or p2) → 7-9s → red tile (p1 or p2) → 6-7s →
    interact with first pink node → zoom in → wait 3-5s. Then ready for mining loop.
    """
    for region_label in ["p1", "p2"]:
        click = click_tile_randomly(si, COLOR_YELLOW, region_label)
        if click:
            print(f"Clicked yellow tile in {region_label}.")
            break
    else:
        print("Yellow tile not found in p1 or p2.")
        return False

    wait = random.uniform(7.0, 9.0)
    print(f"Waiting {wait:.1f}s...")
    time.sleep(wait)
    _maybe_afk()

    for region_label in ["p1", "p2"]:
        click = click_tile_randomly(si, COLOR_RED, region_label)
        if click:
            print(f"Clicked red tile in {region_label}.")
            break
    else:
        print("Red tile not found in p1 or p2.")
        return False

    wait = random.uniform(6.0, 7.0)
    print(f"Waiting {wait:.1f}s...")
    time.sleep(wait)
    _maybe_afk()

    regions = ["p1", "p2"]
    random.shuffle(regions)
    clicked_mine = False
    for region_label in regions:
        print(f"Looking for pink node in {region_label}...")
        region = si.get_scan_area(region_label)
        found = si.find_pixel(COLOR_PINK, region=region, tolerance=0)
        if found:
            print(f"Found pink node in {region_label}, right-clicking and selecting mine...")
            if _right_click_at_and_confirm(si, found, MINE_GEM_ROCKS_OPTION_IMAGE):
                clicked_mine = True
                break
    if not clicked_mine:
        print("No pink node found in p1 or p2, or failed to click mine option.")
        return False

    print("Zooming in a little...")
    si.zoom_in(times=2, delay_low=0.005, delay_high=0.01, scroll_amount=350)
    time.sleep(random.uniform(0.4, 0.8))

    wait = random.uniform(3.0, 5.0)
    print(f"Waiting {wait:.1f}s before monitoring for NOT mining...")
    time.sleep(wait)

    return True


def run_to_mining_via_pink_node(si, low_visibility=False):
    """
    If low_visibility: use intermediate tiles (yellow → red → pink) then zoom and short wait.
    Else: right-click a pink gem node in p1 or p2, wait 18-30s (camera adjust during run),
    zoom in. Ready for mining loop.
    """
    if low_visibility:
        return _run_to_mining_pi(si)

    regions = ["p1", "p2"]
    random.shuffle(regions)
    clicked_mine = False
    for region_label in regions:
        print(f"Looking for pink node in {region_label}...")
        region = si.get_scan_area(region_label)
        found = si.find_pixel(COLOR_PINK, region=region, tolerance=0)
        if found:
            print(f"Found pink node in {region_label}, right-clicking and selecting mine...")
            if _right_click_at_and_confirm(si, found, MINE_GEM_ROCKS_OPTION_IMAGE):
                clicked_mine = True
                break
    if not clicked_mine:
        print("No pink node found in p1 or p2, or failed to click mine option.")
        return False

    total_wait = random.uniform(18, 30)
    print(f"Running to mining area; adjusting camera during the {total_wait:.1f}s run...")
    start = time.time()

    print("Holding 'w' to tip camera up for easier node clicking...")
    pyautogui.keyDown("w")
    time.sleep(random.uniform(1.5, 2.0))
    pyautogui.keyUp("w")
    time.sleep(random.uniform(0.2, 0.4))

    print("Zooming in a little...")
    si.zoom_in(times=2, delay_low=0.005, delay_high=0.01, scroll_amount=350)
    time.sleep(random.uniform(0.4, 0.8))

    elapsed = time.time() - start
    remaining = max(0.0, total_wait - elapsed)
    if remaining > 0:
        time.sleep(remaining)

    return True


def is_inventory_full_message_in_chat(si):
    """
    Return True if the inventory-full message appears in the chat area (e.g. from inventory_full.png).
    Same idea as check_inventory_full in mining-sandstone-quarry.py.
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

        # Right-click closest pink node (uses directional offset converge; pixel is truly closest to us)
        if not _right_click_closest_pink_and_confirm(si, MINE_GEM_ROCKS_OPTION_IMAGE):
            consecutive_failures += 1
            print(f"Failed to find/click pink node ({consecutive_failures}/{MAX_CONSECUTIVE_PINK_FAILURES}) - waiting 1s and retrying...")
            time.sleep(1.0)
            continue

        consecutive_failures = 0  # reset on success

        time.sleep(random.uniform(3.0, 5.0))  # wait after clicking mine gem rocks (between nodes) before monitoring for NOT mining

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

        # Small random chance to idle like we're multitasking
        if random.random() < 0.05:
            extra_wait = _random_afk_duration()
            print(f"Simulating multitasking - idling for {extra_wait:.1f}s before next node...")
            time.sleep(extra_wait)

        time.sleep(random.uniform(0.3, 0.7))

    return True


def return_to_bank_and_deposit(si):
    """
    Zoom out, walk to red tile (wait 7-9s), walk to yellow tile (wait 5-7s).
    From yellow tile, first try to right-click bank deposit box in p6 and confirm deposit option.
    If that fails (teal box not loaded / off-screen), walk to the fallback red tile and then try to
    right-click the bank deposit box in p5 instead. After success, wait ~4.5s for pane to open.
    ImageMonitor for deposit all inventory button, then left-click it, then bank close, then camera down.
    """
    print("Zooming out...")
    si.zoom_out(times=5, delay_low=0.005, delay_high=0.01, scroll_amount=-400)
    time.sleep(random.uniform(0.5, 1.0))

    print("Walking to red square (p5)...")
    click = click_tile_randomly(si, COLOR_RED, "p5")
    if not click:
        print("Red square (p5) not found on return.")
        save_debug_screenshot("bank_red_tile_not_found")
        return False
    wait = random.uniform(7.8, 8.4)  # tighter range, closer to min; +0.4s so we don't interact too soon
    print(f"Waiting {wait:.1f}s to reach yellow tile area...")
    time.sleep(wait)
    _maybe_afk()

    print("Walking to yellow square (p5)...")
    click = click_tile_randomly(si, COLOR_YELLOW, "p5")
    if not click:
        print("Yellow square (p5) not found on return.")
        save_debug_screenshot("bank_yellow_tile_not_found")
        return False
    wait = random.uniform(5.8, 6.4)  # tighter range, closer to min
    print(f"Waiting {wait:.1f}s at yellow tile...")
    time.sleep(wait)
    _maybe_afk()

    # From yellow tile: try up to 3 times to interact with bank deposit box in p6
    print("Interacting with bank deposit box (p6) from yellow tile (up to 3 tries)...")
    success = si.find_pixel_right_click_confirm(COLOR_TEAL, DEPOSIT_OPTION_IMAGE, attempts=3, region=si.get_scan_area("p6"))
    if not success:
        print("Could not interact with deposit box from yellow tile (p6). Moving to fallback red tile...")

        print("Walking to fallback red square (p5)...")
        click = click_tile_randomly(si, COLOR_RED, "p5")
        if not click:
            print("Fallback red square (p5) not found on return.")
            save_debug_screenshot("bank_fallback_red_not_found")
            return False
        wait = random.uniform(5.8, 6.4)
        print(f"Waiting {wait:.1f}s at fallback red tile (near bank)...")
        time.sleep(wait)
        _maybe_afk()

        print("Interacting with bank deposit box (p5) from fallback red tile (up to 3 tries)...")
        success = si.find_pixel_right_click_confirm(COLOR_TEAL, DEPOSIT_OPTION_IMAGE, attempts=3, region=si.get_scan_area("p5"))
        if not success:
            print("Failed to open deposit box menu from both yellow and fallback red tiles.")
            save_debug_screenshot("bank_deposit_box_failed")
            return False

    print("Deposit box interaction succeeded.")
    _maybe_afk()

    # Fixed-ish wait before we look for the pane (character runs a short distance)
    wait = random.uniform(4.5, 5.0)
    print(f"Waiting {wait:.1f}s for character to open bank deposit pane...")
    time.sleep(wait)

    # Wait for deposit all inventory button to appear, then click it
    print("Waiting for deposit all inventory button...")
    bank_monitor = ImageMonitor(
        screen_interactor=si,
        image_path=DEPOSIT_ALL_IMAGE,
        region="game_screen_center",
        confidence=0.92,
        check_interval=1.5,
        wait_for="appear",
    )
    bank_monitor.start()
    if not bank_monitor.wait_for_condition(timeout=20):
        print("Bank interface did not appear.")
        bank_monitor.stop()
        save_debug_screenshot("bank_interface_not_appeared")
        return False
    bank_monitor.stop()

    time.sleep(1.5)  # troubleshoot: pause after monitor found button so UI is settled

    # Search same region as ImageMonitor (game_screen_center) so we find the button we just detected
    deposit_click = si.click_image_cv2_without_moving(
        DEPOSIT_ALL_IMAGE,
        region="game_screen_center",
        confidence=0.88,
        offset_range=(0, 5),
    )
    if not deposit_click:
        time.sleep(2.0)  # troubleshoot: pause before retry so you can see the screen
        deposit_click = si.click_image_cv2_without_moving(
            DEPOSIT_ALL_IMAGE,
            region="bank_deposit_box",
            confidence=0.85,
            offset_range=(0, 5),
        )
    if not deposit_click:
        print("Failed to click deposit all inventory.")
        save_debug_screenshot("bank_deposit_all_failed")
        return False
    time.sleep(1.0)  # troubleshoot: pause after click before closing bank
    _maybe_afk()

    # Close bank (deposit box close button) - search same region as deposit UI first
    close_click = si.click_image_cv2_without_moving(
        BANK_CLOSE_IMAGE,
        region="game_screen_center",
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
            region="bank_pane",
            confidence=0.85,
            offset_range=(0, 5),
        )
    if close_click:
        print("Bank closed.")
    else:
        print("Warning: Bank close button not found. Continuing.")
    _maybe_afk()

    print("Pointing camera back down (hold s 0.7-0.9s)...")
    pyautogui.keyDown("s")
    time.sleep(random.uniform(0.7, 0.9))
    pyautogui.keyUp("s")
    time.sleep(random.uniform(0.2, 0.4))

    return True


def _offset_ranges_for_pixel_relative_to_center(pixel_x, pixel_y, screen_w, screen_h):
    """
    Return (offset_x_range, offset_y_range) from the found pixel so we click toward the
    node. Reduced overall offsets. Node down-left of us -> offset further down-left; etc.
    """
    cx, cy = screen_w // 2, screen_h // 2
    left_of_center = pixel_x < cx
    right_of_center = pixel_x > cx
    below_center = pixel_y > cy
    above_center = pixel_y < cy

    if below_center and left_of_center:
        return ((-14, -5), (5, 14))   # down-left
    if below_center and right_of_center:
        return ((5, 14), (5, 14))     # down-right
    if above_center and left_of_center:
        return ((-14, -5), (-14, -5)) # up-left
    if above_center and right_of_center:
        return ((5, 14), (-14, -5))   # up-right
    if right_of_center:
        return ((5, 14), (-4, 4))     # right of us
    if left_of_center:
        return ((-14, -5), (-4, 4))   # left of us
    if below_center:
        return ((-4, 4), (5, 14))     # below
    return ((-4, 4), (-14, -5))       # above


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
            opposite_x = random.randint(2, 6) if mid_x < 0 else random.randint(-6, -2)
            opposite_y = random.randint(2, 6) if mid_y < 0 else random.randint(-6, -2)
            offset_x = opposite_x
            offset_y = opposite_y + random.randint(-3, 3)
        target_x = max(0, min(x + offset_x, screen_w - 1))
        target_y = max(0, min(y + offset_y, screen_h - 1))

        pyautogui.moveTo(target_x, target_y)
        time.sleep(random.uniform(0.08, 0.15))
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


def _right_click_closest_pink_and_confirm(si, confirm_image_path):
    """
    Find the closest pink pixel to the character (exact color match), then right-click with
    directional converge (only valid when pixel is truly closest to us, e.g. while at mining nodes).
    """
    coords = si.find_closest_pixel(
        COLOR_PINK,
        tolerance=0,  # exact match so we don't click gray/other pixels
        max_radius=800,
        local_search_size=15,
    )
    if not coords:
        return False
    return _right_click_pixel_with_directional_converge(si, coords, confirm_image_path)


def _right_click_at_and_confirm(si, pixel_xy, confirm_image_path, max_attempts=15):
    """
    Simple right-click at a pixel (e.g. from region scan p1/p2). No directional offset—
    scan order is top-left to bottom-right so the first pixel found may not be 'toward' us.
    Just try small random offsets around the pixel until confirm menu appears.
    """
    x, y = pixel_xy
    screen_w, screen_h = pyautogui.size()
    orig = pyautogui.position()
    offset_range = 4  # small random offset 1–4 px down/right for more accurate initial node click

    for attempt in range(max_attempts):
        # For the first trip to mining, the gem rock is visually down/right of the found pixel.
        # Always bias the click slightly down and to the right of the located pixel.
        offset_x = random.randint(1, offset_range)
        offset_y = random.randint(1, offset_range)
        target_x = max(0, min(x + offset_x, screen_w - 1))
        target_y = max(0, min(y + offset_y, screen_h - 1))

        pyautogui.moveTo(target_x, target_y)
        time.sleep(random.uniform(0.08, 0.15))
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
                    cx = loc[0] + random.randint(-2, 2)
                    cy = loc[1] + random.randint(-1, 1)
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


def main_loop(max_runs=10):
    """Run until we have max_runs successful deposits (each deposit = one full mining run + bank)."""
    si = ScreenInteractor()
    low_visibility = get_low_visibility_config()
    if low_visibility:
        print("Using low visibility / Pi path (intermediate tiles to mining).")
    print("Starting gem mining bot in 3 seconds...")
    time.sleep(3)
    if not setup_gem_mining(si, low_visibility=low_visibility):
        print("Setup failed. Exiting.")
        save_debug_screenshot("setup_failed")
        return

    completed_deposits = 0
    failed_runs = 0
    max_failed_runs = 20

    while completed_deposits < max_runs:
        print(f"\n--- Run (target: {completed_deposits + 1}/{max_runs} successful deposits) ---")

        if not run_to_mining_via_pink_node(si, low_visibility=low_visibility):
            print("Failed to run to mining (pink node in p1/p2). Retrying...")
            save_debug_screenshot("run_to_mining_failed")
            failed_runs += 1
            if failed_runs >= max_failed_runs:
                print(f"Aborting: failed to start a run {failed_runs} times in a row.")
                save_debug_screenshot("abort_max_failed_runs")
                break
            continue

        mine_until_inventory_full(si)

        if not return_to_bank_and_deposit(si):
            print("Failed to bank. Retrying...")
            save_debug_screenshot("bank_failed")
            continue

        completed_deposits += 1
        failed_runs = 0  # reset failure counter after a successful full run
        print(f"Successful deposit {completed_deposits}/{max_runs}.")
        time.sleep(random.uniform(1.0, 2.0))

    print(f"Gem mining bot finished. Completed {completed_deposits} deposits.")


if __name__ == "__main__":
    main_loop(max_runs=50)
