# Anglerfish Fishing Bot

A state-based fishing bot for Old School RuneScape that automatically fishes anglerfish using advanced image recognition and right-click confirmation systems.

## Features

- **State-Based Logic**: Automatically manages three states: banking, walking to fishing spot, and fishing
- **CV3 Image Detection**: Uses enhanced color-aware image recognition for reliable item detection
- **Right-Click Confirmation**: Ensures accurate interactions by confirming right-click menu options
- **Pixel Monitoring**: Tracks fishing progress using green/red pixel detection
- **Random Offsets**: All clicks include random offsets for human-like behavior
- **Automatic Inventory Management**: Detects when inventory is full and banks automatically

## Requirements

- Python 3.7+
- Required packages (install via `pip install -r requirements.txt`):
  - `pyautogui`
  - `opencv-python` (cv2)
  - `numpy`
  - `PIL` (Pillow)

## Setup

1. **Activate Virtual Environment**:
   ```bash
   cd python_bots
   # On Windows:
   activate_venv.bat
   # On Unix/Mac:
   source activate_venv.sh
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the Bot**:
   ```bash
   cd fishing_bots
   python test_angler_bot.py
   ```

## Usage

### Basic Usage

```python
from fish_anglers import AnglerfishBot

# Create bot instance
bot = AnglerfishBot()

# Run setup (zoom, face north, adjust camera)
if bot.setup():
    # Start main loop
    bot.main_loop(max_loops=50)
```

### Command Line

```bash
cd python_bots/fishing_bots
python fish_anglers.py
```

## How It Works

### 1. Setup Phase
- Zooms out completely then in slightly
- Faces north using compass
- Presses 'w' key for 1.5 seconds to achieve bird's eye view
- Assesses current state automatically

### 2. State Management
The bot operates in three distinct states:

#### **NEED_BANK State**
- Triggered when inventory is full (raw anglerfish detected in last slot)
- Right-clicks deposit box with confirmation
- Deposits all inventory items
- Interacts with fish barrel to store fish
- Closes bank interface
- Transitions to WALK_TO_FISH state

#### **WALK_TO_FISH State**
- Triggered when not at fishing spot
- Searches for yellow pixels (walking tiles) in game center
- Clicks yellow tiles to move towards fishing spot
- Waits 10-12 seconds for movement
- Reassesses state after movement

#### **READY_TO_FISH State**
- Triggered when fishing spot is visible
- Right-clicks fishing spot with confirmation
- Selects "Bait" option from right-click menu
- Monitors for green pixel (fishing started)
- Monitors for red pixel (fishing stopped)
- Continues fishing cycle until inventory is full

### 3. Image Recognition
- Uses CV3 enhanced detection with color-aware validation
- Searches in specific screen regions (bag_last_slot, game_screen_center, etc.)
- Includes color tolerance and shape/color weight balancing
- Provides detailed logging of detection attempts

### 4. Right-Click Confirmation
- Finds target image using CV3
- Right-clicks with random offset
- Searches for confirmation image in right-click menu
- Clicks confirmation option if found
- Includes fallback error handling and menu cleanup

## Configuration

### Screen Areas
The bot uses predefined screen areas from `screen_interactor.py`:
- `bag_last_slot`: Last inventory slot for detecting full inventory
- `game_screen_center`: Center game area for fishing spot detection
- `bank_deposit_box`: Bank interface area for banking operations
- `activity_pane`: Activity panel for fishing progress monitoring

### Image Files
Required images in `image_library/`:
- `raw_anglerfish.png`: Anglerfish fishing spot and inventory item
- `bait_rod_fishing_spot_option.png`: Right-click menu option
- `deposit_bank_deposit_option.png`: Bank deposit option
- `deposit_all_inventory.png`: Deposit all button
- `fish_barrel.png`: Fish barrel in bank
- `empty_open_fish_barrel_option.png`: Fish barrel interaction option
- `bank_close.png`: Bank close button

### CV3 Parameters
- `color_tolerance`: 30 (RGB color variation allowance)
- `shape_weight`: 0.7 (emphasis on structural similarity)
- `color_weight`: 0.3 (emphasis on color similarity)
- `threshold`: 0.95 (confidence threshold)

## Troubleshooting

### Common Issues

1. **Image Not Found Errors**:
   - Ensure all required images exist in `image_library/`
   - Check that images are clear and representative
   - Verify screen resolution matches expected areas

2. **Fishing Spot Detection Fails**:
   - Ensure camera is properly positioned (bird's eye view)
   - Check that fishing spot is visible in game center
   - Verify `raw_anglerfish.png` image quality

3. **Banking Issues**:
   - Ensure deposit box is visible and accessible
   - Check that bank interface appears correctly
   - Verify all banking images are accurate

4. **State Stuck**:
   - Check console output for error messages
   - Verify screen areas are correctly defined
   - Ensure game window is active and visible

### Debug Mode

Enable detailed logging by running:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Safety Features

- **Random Delays**: Human-like timing between actions
- **Random Offsets**: Varied click positions to avoid detection
- **Error Handling**: Graceful failure handling and retry logic
- **State Validation**: Continuous state assessment and correction
- **Manual Interruption**: Ctrl+C support for emergency stops

## Performance

- **Typical Fishing Cycle**: 2-3 minutes per inventory
- **Banking Time**: 10-15 seconds per banking operation
- **Walking Time**: 10-12 seconds per movement
- **Detection Accuracy**: >95% with CV3 enhanced recognition

## Contributing

When modifying the bot:
1. Test changes with `test_angler_bot.py`
2. Update documentation for any new features
3. Maintain consistent error handling patterns
4. Follow existing code style and structure

## License

This bot is for educational purposes. Use responsibly and in accordance with game terms of service.
