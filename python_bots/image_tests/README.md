# Image Test Scripts

This directory contains various scripts for testing and comparing image detection methods.

## Available Test Scripts

### 1. `general_image_test_cv2.py` (Original CV2 Method)
- **Purpose**: Tests the original CV2 template matching method
- **Use Case**: General image detection, bank interface elements, non-food items
- **Features**: 
  - Traditional `cv2.TM_CCOEFF_NORMED` template matching
  - Fast detection
  - May confuse similar items with different colors
  - Confidence can fluctuate based on item position

### 2. `general_image_test_cv3.py` (Enhanced CV3 Method)
- **Purpose**: Tests the new CV3 color-aware detection methods
- **Use Case**: Food items, items where color matters, cooked vs raw discrimination
- **Features**:
  - Color-aware template matching
  - Configurable shape and color weights
  - Multi-layered validation
  - Prevents confusion between similar items with different colors
  - Stable confidence scoring

### 3. `compare_cv2_cv3.py` (Side-by-Side Comparison)
- **Purpose**: Compares CV2 and CV3 methods on the same image
- **Use Case**: Understanding differences between methods, choosing the right method
- **Features**:
  - Runs both CV2 and CV3 tests sequentially
  - Shows detection differences
  - Provides recommendations for when to use each method

### 4. `cv2_vs_cv3_comparison.py` (Advanced Comparison)
- **Purpose**: More detailed comparison with multiple test scenarios
- **Use Case**: In-depth analysis of detection differences
- **Features**:
  - Multiple confidence thresholds
  - Performance metrics
  - Detailed analysis output

## When to Use Each Method

### Use CV2 When:
- **Speed is priority** over accuracy
- **Bank interface elements** (close button, deposit button)
- **Non-food items** where color doesn't matter
- **General item finding** where false positives are acceptable

### Use CV3 When:
- **Accuracy is priority** over speed
- **Food items** (raw vs cooked discrimination)
- **Items where color matters** for identification
- **Preventing false positives** is critical
- **Stable confidence scoring** is needed

## CV3 Weight Recommendations

### Cooked vs Raw Discrimination (Recommended for Cooking Bot)
```
Shape Weight: 0.2 (low - avoids shape-based confusion)
Color Weight: 0.8 (high - prioritizes color differences)
Color Tolerance: 0-5 (very strict - nearly 1:1 color match)
```

### General Item Finding
```
Shape Weight: 0.5 (balanced)
Color Weight: 0.5 (balanced)
Color Tolerance: 30
```

### Shape-Based Detection
```
Shape Weight: 0.8 (high - prioritizes structural similarity)
Color Weight: 0.2 (low - ignores color differences)
Color Tolerance: 50
```

### Color-Based Detection
```
Shape Weight: 0.1 (very low - minimal shape consideration)
Color Weight: 0.9 (very high - prioritizes exact color matching)
Color Tolerance: 0-10 (strict - exact color matching)
```

### Ultra-Strict Color Matching
```
Shape Weight: 0.1 (very low)
Color Weight: 0.9 (very high)
Color Tolerance: 0-2 (nearly pixel-perfect color match)
```
Use case: Distinguishing between very similar items with slight color differences

## Usage Examples

### Test CV2 Method Only
```bash
python general_image_test_cv2.py
```

### Test CV3 Method Only
```bash
python general_image_test_cv3.py
```

### Compare Both Methods
```bash
python compare_cv2_cv3.py
```

### Advanced Comparison
```bash
python cv2_vs_cv3_comparison.py
```

## Input Parameters

All scripts accept similar parameters:
- **Image name**: Name of the image file (e.g., 'raw_karambwan.png')
- **Region**: Screen region to search in (e.g., 'p3', 'game_screen', 'bag')
- **Confidence**: Detection threshold (0.7-1.0)
- **Visual feedback**: Whether to show mouse movement

CV3 scripts also accept:
- **Shape weight**: Weight for structural similarity (0.0-1.0)
- **Color weight**: Weight for color similarity (0.0-1.0)
- **Color tolerance**: RGB color difference tolerance (0-100)

## Output Files

Each test generates:
- **Screenshot**: Captured search area
- **Annotated screenshot**: With detection results highlighted
- **Console output**: Detailed detection information and recommendations

## Troubleshooting

### CV3 Detection Fails
1. **Check weights**: Ensure shape_weight + color_weight = 1.0
2. **Adjust color tolerance**: 
   - 0-2: Ultra-strict (nearly pixel-perfect color match)
   - 5-10: Strict (exact color matching)
   - 20-30: Moderate (allows some color variation)
   - 50-100: Lenient (allows significant color variation)
3. **Use weight tuning**: Run with different weight combinations
4. **Check image quality**: Ensure template image is clear and representative

### CV2 Detection Fails
1. **Lower confidence**: Try 0.9 or 0.85
2. **Check region**: Ensure search area includes the target
3. **Verify image**: Ensure template image exists and is readable

## Performance Notes

- **CV2**: Faster, ~10-50ms per detection
- **CV3**: Slower, ~50-200ms per detection (due to additional validation)
- **Trade-off**: CV3 provides better accuracy at the cost of speed
- **Recommendation**: Use CV3 for critical operations, CV2 for routine tasks
