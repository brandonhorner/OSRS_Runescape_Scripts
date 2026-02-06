# Anglerfish Fishing Bot GUI

A user-friendly graphical interface for the anglerfish fishing bot with logging capabilities and inventory-based execution control.

## Features

- **Compact GUI**: Easy-to-use interface with start/stop controls
- **Inventory Control**: Run the bot for a specific number of inventories instead of infinite loops
- **Real-time Logging**: Track login events, disconnections, and client restarts
- **Progress Tracking**: Visual progress bar and status updates
- **Activity Log**: Real-time log display with timestamps
- **Executable Support**: Can be built into a standalone executable

## Quick Start

### Option 1: Run with Python (Recommended)

1. **Activate the virtual environment** (if using one):
   ```bash
   # Windows
   python activate_venv.bat
   
   # Or PowerShell
   python activate_venv.ps1
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements_gui.txt
   ```

3. **Run the GUI**:
   ```bash
   python run_gui.py
   ```

### Option 2: Build and Run Executable

1. **Build the executable**:
   ```bash
   python build_executable.py
   ```

2. **Or use the batch file** (Windows):
   ```bash
   build_and_run.bat
   ```

3. **Run the executable**:
   - Navigate to the `dist` folder
   - Double-click `FishingBotGUI.exe`

## Usage

1. **Set Target Inventories**: Enter the number of inventories you want the bot to complete
2. **Click Start Bot**: The bot will begin fishing and banking
3. **Monitor Progress**: Watch the progress bar and activity log
4. **Stop Anytime**: Click "Stop Bot" to halt execution

## GUI Components

### Control Panel
- **Target Inventories**: Number of inventories to complete before stopping
- **Start/Stop Buttons**: Control bot execution

### Status Display
- **Bot Status**: Current state (Stopped/Running/Completed)
- **Current Inventories**: Number of inventories completed
- **Successful Trips**: Total successful fishing trips

### Activity Log
- **Real-time Logging**: Shows all bot activities with timestamps
- **Event Tracking**: Login events, disconnections, errors
- **Clear Log**: Button to clear the log display

### Progress Bar
- **Visual Progress**: Shows completion percentage
- **Progress Label**: Exact percentage display

## Logging Features

The GUI automatically logs:
- **Login Events**: When the bot successfully logs in
- **Disconnections**: When connection is lost
- **Client Restarts**: When the client needs to be restarted
- **Bot Activities**: All major bot operations
- **Errors**: Any errors that occur during execution

Logs are saved to:
- `../logs/fishing_bot_YYYYMMDD_HHMMSS.log`

## File Structure

```
fishing_bots/
├── fishing_bot_gui.py          # Main GUI application
├── fish_anglers.py             # Original bot logic
├── requirements_gui.txt        # GUI dependencies
├── build_executable.py         # Script to build executable
├── run_gui.py                  # Simple run script
├── build_and_run.bat           # Windows batch file
├── README_GUI.md               # This file
└── dist/                       # Executable output (after building)
    ├── FishingBotGUI.exe       # Standalone executable
    ├── image_library/          # Required images
    └── logs/                   # Log output directory
```

## Requirements

- Python 3.7+
- PyQt6 (modern GUI framework)
- pyautogui
- opencv-python
- numpy
- Pillow
- pyinstaller (for building executable)

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure virtual environment is activated
   - Install requirements: `pip install -r requirements_gui.txt`

2. **Images not found**:
   - Ensure `image_library` folder exists in parent directory
   - Check file paths in the bot code

3. **GUI doesn't start**:
   - Check Python version (3.7+ required)
   - Verify PyQt6 is installed: `python -c "import PyQt6"`

4. **Bot doesn't work**:
   - Make sure RuneLite is running
   - Check that you're in the correct location in-game
   - Verify image library contains required images

### Getting Help

- Check the activity log for error messages
- Review the log files in the `logs` directory
- Ensure all dependencies are properly installed

## Advanced Usage

### Customizing the Bot

The GUI uses the same bot logic as the original `fish_anglers.py`. You can modify:
- Fishing locations
- Banking behavior
- Image recognition settings
- Timing parameters

### Building Custom Executables

To create a custom executable with different settings:

1. Modify `fishing_bot_gui.py` as needed
2. Update `build_executable.py` if additional files are needed
3. Run `python build_executable.py`

## Safety Features

- **Inventory-based stopping**: Bot stops after completing target inventories
- **Manual stop**: Can be stopped at any time
- **Error handling**: Graceful error recovery
- **Logging**: Complete activity tracking for debugging
- **Progress tracking**: Visual feedback on completion status
