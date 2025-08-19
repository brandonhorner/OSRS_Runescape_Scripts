# Gemstone Crab Bot

A Python bot for hunting gemstone crabs in Old School RuneScape (OSRS).

## Overview

This bot automates the process of hunting gemstone crabs by:
1. **Setup**: Facing north and zooming out
2. **Search**: Looking for pink pixels (gemstone crabs) in the game screen
3. **Teleport**: Moving to new areas when no crabs are found
4. **Combat**: Attacking crabs and managing strength potions
5. **Monitoring**: Waiting for crabs to be defeated

## Features

- **Smart Navigation**: Uses teal caves and yellow tiles for area transitions
- **Combat Management**: Automatically drinks strength potions when needed
- **Pixel Detection**: Reliable crab detection using color matching
- **Interrupt Handling**: Graceful Ctrl+C shutdown during pixel monitoring
- **Progress Tracking**: Counts successful vs. total attempts

## Requirements

- Python 3.7+
- RuneLite client
- OSRS game running
- Required Python packages (see setup below)

## Setup

### 1. Install Python Dependencies

```bash
# Navigate to the python_bots directory
cd python_bots

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install required packages
pip install pyautogui opencv-python numpy pillow
```

### 2. Image Library

Ensure the `image_library/` folder contains all required images:
- `world_map.png` - For compass navigation
- `attack_gemstone_crab_option.png` - Attack option detection
- `bag_is_closed.png` - Inventory state detection
- `strength_pot-1.png` through `strength_pot-4.png` - Potion detection

### 3. Game Setup

1. **Position**: Place your character in the gemstone crab hunting area
2. **Inventory**: Ensure you have strength potions available
3. **Equipment**: Equip appropriate combat gear
4. **RuneLite**: Make sure the side menu is in your preferred state

## Usage

### Basic Run

```bash
# Navigate to the gemstone_crab_bot directory
cd python_bots/gemstone_crab_bot

# Run the bot
python gemstone_crab_bot.py
```

### Configuration

The bot can be configured by modifying these parameters in `main()`:

```python
# Run until 78 successful loops (default)
main_loop(si, target_successes=78, max_attempts=300)

# Customize for your needs
main_loop(si, target_successes=50, max_attempts=200)
```

### Interrupting the Bot

- **Ctrl+C**: Ctrl+ C in the console immediately stops the bot
- **During Monitoring**: Ctrl+C triggers graceful shutdown
- **Emergency Stop**: Close the terminal/console

## How It Works

### 1. Setup Phase
- Finds world map and clicks compass to face north
- Zooms out completely for maximum visibility

### 2. Main Loop
- **Search**: Scans for pink pixels (gemstone crabs)
- **Teleport**: If no crab found, moves to next area
- **Attack**: Right-clicks crab, verifies attack option, initiates combat
- **Potion**: Drinks strength potion if needed
- **Wait**: Monitors for crab defeat (pink pixels disappear)

### 3. Area Navigation
- **Teal Cave**: Transportation spot to new area
- **Yellow Tile**: Game tile that loads the new area
- **Wait Times**: 6-8 seconds for teleport, 2.5-4.5 seconds for area load

### 4. Combat System
- **9 Attempts**: Multiple tries to find and attack crab
- **Position Correction**: Re-finds crab location on each attempt
- **Potion Management**: Automatically opens inventory and drinks potions

## Troubleshooting

### Common Issues

1. **"Could not find world map"**
   - Ensure you're in the correct area
   - Check if `world_map.png` exists in image_library

2. **"No strength potion found"**
   - Verify potion images are in image_library
   - Check if inventory is open/closed correctly

3. **"Failed to attack gemstone crab"**
   - Crab may have moved or been killed
   - Check if attack option image is correct

### Debug Tools

Use the `general_image_test.py` in the `image_tests/` folder to test image detection:

```bash
cd python_bots/image_tests
python general_image_test.py
```

## Safety Notes

- **Use at your own risk** - Botting may violate game terms of service
- **Monitor regularly** - Check bot behavior and stop if issues arise
- **Test first** - Run with low target_successes initially
- **Backup saves** - Ensure your character is in a safe location

## File Structure

```
gemstone_crab_bot/
├── gemstone_crab_bot.py    # Main bot script
├── README.md               # This file
└── requirements.txt        # Python dependencies (if needed)
```

## Dependencies

- `screen_interactor.py` - Screen interaction utilities
- `pixel_monitor.py` - Pixel color monitoring
- `image_library/` - Game image templates

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all image files are present
3. Test image detection with `general_image_test.py`
4. Check console output for error messages

## Version History

- **v1.0**: Initial bot with basic crab hunting functionality
- **v1.1**: Added potion management and improved combat
- **v1.2**: Enhanced interrupt handling and progress tracking
- **v1.3**: Reorganized into dedicated folder with documentation
