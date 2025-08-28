# Hosidius Cooking Bot

A clean, focused cooking bot for Old School RuneScape that automates cooking at the Hosidius Kitchen with an intuitive Tkinter UI for food selection.

## Features

- **Clean Architecture**: Follows the same pattern as other bots in the project
- **User-Friendly UI**: Tkinter interface for selecting multiple food types and cooking order
- **Proper Setup**: Handles zoom, compass orientation, and bank configuration
- **Image Monitoring**: Uses `ImageMonitor` for reliable bank and cooking detection
- **Multiple Food Types**: Supports cooking various raw foods in sequence
- **Smart Food Processing**: Automatically moves to next food type when current one runs dry
- **Robust Error Handling**: Retries bank interactions up to 3 times before giving up

## Requirements

- Python 3.7+
- Required packages: `pyautogui`, `opencv-python`, `numpy`, `PIL`, `tkinter`
- Must be in the Hosidius Kitchen area
- Raw foods must be visible in your default bank view

## Setup Process

The bot automatically performs the following setup:

1. **Zoom Configuration**: Zooms in 10 times, then out 3 times for optimal visibility
2. **Orientation**: Faces north using the compass
3. **Bank Access**: Opens the bank if not already open
4. **Bank All Feature**: Activates the "bank all" quantity feature if inactive
5. **Disable Placeholders**: Turns off placeholders to prevent ghost items from interfering with detection
6. **Clear Inventory**: Deposits all existing inventory to start fresh

## UI Features

The bot provides a user-friendly interface with:

- **Available Foods List**: Shows all supported raw food types
- **Selected Foods List**: Displays your chosen cooking order
- **Add/Remove Buttons**: Use → and ← buttons or double-click to manage selections
- **Max Loops Input**: Set maximum cooking loops per food type
- **Start Button**: Begin cooking with selected foods

## Cooking Process

For each food type, the bot:

1. **Withdraws** raw food from the bank
2. **Closes** the bank
3. **Clicks** the clay oven (pink pixels)
4. **Waits** for movement to the oven
5. **Starts** cooking with spacebar
6. **Monitors** green "Cooking" text in activity_pane until it disappears (cooking complete)
7. **Returns** to bank to deposit cooked food
8. **Deposits all inventory** (cooked food, burnt food, etc.) using deposit all button
9. **Repeats** until all food is cooked or max loops reached
10. **Moves** to next food type when current one is depleted

## Configuration

### Food Selection

Use the UI to select which foods to cook and in what order:

1. Select a food from the "Available Raw Foods" list
2. Click the → button or double-click to add it to your cooking order
3. Use the ← button or double-click to remove foods from your selection
4. Foods are processed in the order they appear in the "Cooking Order" list

### Max Loops

Set the maximum number of cooking loops per food type using the "Max Loops" input field.

## Usage

1. Ensure you're in the Hosidius Kitchen area
2. Make sure raw foods are visible in your bank
3. Run the script: `python cooking_bot.py`
4. Use the UI to select foods and set max loops
5. Click "Start Cooking Bot" to begin

## Image Requirements

The bot requires the following images in the `image_library/` folder:

- `bank_close.png` - Bank close button
- `bank_all_quantity_is_inactive.png` - Inactive bank all feature
- `placeholders_active.png` - Active placeholders feature (to disable)
- `deposit_all_inventory.png` - Deposit all inventory button
- Raw food images (e.g., `raw_shark.png`, `raw_bass.png`, `raw_sea_turtle.png`)
- Cooked food images (e.g., `cooked_shark.png`, `cooked_bass.png`, `cooked_sea_turtle.png`)

## Error Handling

- **Bank Opening**: Retries up to 3 times with 10-second timeouts
- **Cooking Timeout**: 80-second timeout for food to cook
- **Setup Failures**: Exits gracefully if setup cannot be completed
- **Food Depletion**: Automatically moves to next food type when current one is exhausted

## Notes

- The bot uses the `v2` region for bank interactions
- Pixel detection is used for bank chest (teal) and clay oven (pink)
- All timing includes randomization for human-like behavior
- The bot automatically handles burnt food deposits if images exist
- The UI hides during bot operation and reappears when finished
- **Placeholders are disabled** to prevent ghost items (0.9998 confidence) from interfering with food detection when items run out of stock
- **Green text monitoring** detects cooking completion by monitoring the green "Cooking" text in the activity_pane, with a 3-7 second random delay after completion
