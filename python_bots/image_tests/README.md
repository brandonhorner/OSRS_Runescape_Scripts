# Image Testing Tools

This folder contains tools for testing and debugging image detection in the OSRS bots.

## general_image_test.py

A comprehensive tool for testing image detection across different confidence levels and regions.

### Usage

```bash
cd python_bots/image_tests
python general_image_test.py
```

### What It Does

1. **Takes Screenshots**: Captures the specified screen region or full screen
2. **Tests Multiple Confidence Levels**: From 1.0 (exact match) down to 0.7
3. **Visual Feedback**: Moves mouse to all found locations
4. **Saves Results**: Creates annotated screenshots showing detection results
5. **Comprehensive Testing**: Tests both raw CV2 and ScreenInteractor methods

### Input Parameters

- **Image Name**: Just the filename (e.g., `world_map.png`) - automatically prepends `image_library/`
- **Region**: Screen region name (e.g., `p3`, `game_screen`, `bag`) or press Enter for full screen
- **Confidence**: Threshold for testing (0.7-1.0, default 0.95)
- **Visual Feedback**: Whether to move mouse to found locations (y/n, default y)

### Output Files

- **Screenshots**: `region_[name]_screenshot.png` or `full_screen_screenshot.png`
- **Annotated**: `annotated_[image_name].png` with green rectangles around matches

### Use Cases

- **Debug Image Detection**: See exactly what the bot is finding
- **Test New Images**: Verify new image templates work correctly
- **Troubleshoot Failures**: Understand why certain images aren't being detected
- **Optimize Confidence**: Find the right confidence threshold for your images

### Example

```bash
Enter image name (e.g., 'world_map.png'): runelite_menu_is_open.png
Full image path: image_library/runelite_menu_is_open.png
Enter region name (e.g., 'p3', 'game_screen', 'bag') or press Enter for full screen: p6
Enter confidence threshold (0.7-1.0, default 0.95): 0.9
Show visual feedback (mouse movement)? (y/n, default y): y
```

This will test the `runelite_menu_is_open.png` image in the `p6` region with 0.9 confidence and show visual feedback.
