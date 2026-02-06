# Screen Area Recorder

A powerful tool for recording screen areas and generating multi-resolution coordinate code for your OSRS bots.

## Features

- **Interactive Overlay**: Draw areas directly on screen with click-and-drag
- **Multi-Resolution Support**: Convert coordinates between different screen resolutions
- **Code Generation**: Automatically generate Python code for your ScreenInteractor class
- **Export Functionality**: Save and load area definitions in JSON format
- **Visual Feedback**: Color-coded areas with real-time preview

## Why This Tool?

### The Resolution Problem
Converting from 1440p to 1080p using simple ratios can be problematic because:

1. **UI elements don't scale linearly** - buttons, menus, and game elements often have fixed pixel sizes
2. **Aspect ratio differences** - 2560x1440 vs 1920x1080 have different ratios  
3. **Game-specific scaling** - RuneLite and OSRS have their own scaling behaviors

### Better Approaches
This tool provides multiple solutions:

1. **Ratio-based conversion** - Uses screen ratios for proportional scaling
2. **Floor division method** - More precise coordinate calculations
3. **Multi-resolution export** - Generate coordinates for all target resolutions at once

## Installation

1. Ensure you have the required dependencies:
   ```bash
   pip install PyQt6 pyautogui opencv-python numpy
   ```

2. Make sure you're in the `python_bots` directory (the tool imports from `screen_interactor.py`)

3. Run the tool:
   ```bash
   python area_recorder.py
   ```

## Usage

### 1. Start Recording
- Click "Start Area Overlay" to begin drawing areas
- The main window will hide and the overlay will appear

### 2. Draw Areas
- **Left-click and drag** to draw rectangular areas
- **Right-click** to delete the last drawn area
- **Press 'S'** to save areas (creates a timestamped JSON file)
- **Press 'C'** to clear all areas
- **Press 'ESC'** to close the overlay

### 3. View Results
After closing the overlay, you'll see:
- **Recorded Areas**: List of all drawn areas with coordinates
- **Generated Code**: Python code ready to copy into your ScreenInteractor class
- **Multi-resolution support**: Choose target resolution for coordinate conversion

### 4. Export Options
- **Save Areas**: Save current areas to a JSON file
- **Load Areas**: Load previously saved areas from a JSON file
- **Export Areas**: Generate coordinates for all target resolutions
- **Copy Code**: Copy generated Python code to clipboard

## Generated Code Examples

### Basic Format
```python
def get_scan_area(self, label):
    screen_width, screen_height = pyautogui.size()
    
    areas = {
        "area_1": (screen_width // 2560 * 100, screen_height // 1440 * 200, 
                   screen_width // 2560 * 300, screen_height // 1440 * 400),
        "area_2": (screen_width // 2560 * 500, screen_height // 1440 * 600, 
                   screen_width // 2560 * 700, screen_height // 1440 * 800),
    }
    
    return areas.get(label, (0, 0, screen_width, screen_height))
```

### Floor Division Format
```python
def get_scan_area_floor(self, label):
    screen_width, screen_height = pyautogui.size()
    
    areas = {
        "area_1": (floor(screen_width * 0.0391), floor(screen_height * 0.1389), 
                   floor(screen_width * 0.1172), floor(screen_height * 0.2778)),
        "area_2": (floor(screen_width * 0.1953), floor(screen_height * 0.4167), 
                   floor(screen_width * 0.2734), floor(screen_height * 0.5556)),
    }
    
    return areas.get(label, (0, 0, screen_width, screen_height))
```

## Target Resolutions

The tool supports conversion to these common resolutions:
- **1920x1080** (1080p)
- **2560x1440** (1440p) 
- **3840x2160** (4K)
- **1366x768** (Laptop)
- **1600x900** (HD+)

## File Formats

### Saved Areas (.json)
```json
[
  {
    "name": "area_1",
    "x": 100,
    "y": 200,
    "width": 300,
    "height": 400,
    "screen_resolution": "2560x1440",
    "ratios": {
      "x_ratio": 0.0391,
      "y_ratio": 0.1389,
      "w_ratio": 0.1172,
      "h_ratio": 0.2778
    }
  }
]
```

### Exported Areas (.json)
```json
{
  "metadata": {
    "source_resolution": "2560x1440",
    "export_time": "2024-01-15T10:30:00",
    "total_areas": 1
  },
  "resolutions": {
    "1920x1080": [
      {
        "name": "area_1",
        "coordinates": [75, 150, 225, 300],
        "ratios": [0.0391, 0.1389, 0.1172, 0.2778]
      }
    ]
  }
}
```

## Best Practices

### 1. Test Multiple Resolutions
- Record areas on your primary resolution (e.g., 1440p)
- Test the generated code on target resolutions
- Adjust manually if UI elements don't align properly

### 2. Use Meaningful Names
- Instead of "area_1", use descriptive names like "bank_pane" or "chat_box"
- This makes your code more readable and maintainable

### 3. Validate Coordinates
- Always test generated coordinates on target resolutions
- Some UI elements may need manual adjustment due to non-linear scaling

### 4. Consider UI Variations
- RuneLite plugins can change UI layouts
- Game updates may affect element positioning
- Test thoroughly after any changes

## Troubleshooting

### Overlay Not Appearing
- Ensure you're running the tool as administrator (Windows)
- Check that no other applications are blocking the overlay
- Try minimizing other windows first

### Coordinates Not Accurate
- Verify the source resolution is correctly detected
- Test on the target resolution to validate scaling
- Consider manual adjustments for critical UI elements

### Import Errors
- Ensure you're in the `python_bots` directory
- Check that `screen_interactor.py` exists and is accessible
- Verify all required dependencies are installed

## Integration with Existing Code

This tool is designed to work seamlessly with your existing `ScreenInteractor` class:

1. **Record areas** using the tool
2. **Copy generated code** to your `screen_interactor.py`
3. **Test on target resolutions** to ensure accuracy
4. **Adjust manually** if needed for specific UI elements

## Advanced Usage

### Custom Target Resolutions
You can modify the `target_resolutions` list in the code to add your own target resolutions:

```python
self.target_resolutions = [
    (1920, 1080),   # 1080p
    (2560, 1440),   # 1440p
    (3840, 2160),   # 4K
    (1366, 768),    # Laptop
    (1600, 900),    # HD+
    (1280, 720),    # Your custom resolution
]
```

### Batch Processing
The tool can process multiple areas at once, making it efficient for complex UI layouts with many interactive elements.

## Contributing

Feel free to enhance this tool with additional features:
- Support for more coordinate formats
- Integration with other bot frameworks
- Advanced validation and testing features
- Custom export formats

## License

This tool is part of your OSRS bot collection and follows the same licensing terms.

