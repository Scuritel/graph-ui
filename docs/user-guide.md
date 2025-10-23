# Function Graph Plotter - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Interface Overview](#interface-overview)
4. [Function Parameters](#function-parameters)
5. [Visual Customization](#visual-customization)
6. [Period Markers](#period-markers)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Tips and Best Practices](#tips-and-best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Technical Details](#technical-details)

---

## Introduction

The Function Graph Plotter is a desktop application for visualizing the mathematical function:

```
f(x) = a*sin(x*b + c) + tan(d*x)
```

This function combines sinusoidal oscillation with tangent components, creating rich periodic patterns. The application displays exactly **9 complete periods** of the function, centered around the origin (0, 0).

### Key Features

- ✅ Real-time parameter validation
- ✅ Customizable colors for graph line and axes
- ✅ Optional period boundary markers
- ✅ Responsive window resizing
- ✅ Automatic viewport calculation
- ✅ Asymptote detection and handling
- ✅ Origin marker at (0, 0)

---

## Getting Started

### Launching the Application

**Windows PowerShell:**
```powershell
.\run.ps1
```

**Manual Launch:**
```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "c:\Users\Scuritel\Documents\Work\graph-ui"
python -m src.main
```

### First Graph

1. The application opens with default parameters pre-filled:
   - a = 1.0
   - b = 1.0
   - c = 0.0
   - d = 0.1

2. Click **"Plot Graph"** to see the function visualization

3. The graph displays:
   - Blue function curve (default)
   - Black axes and grid (default)
   - Red dot at origin (0, 0)
   - 9 complete periods

---

## Interface Overview

The application window is divided into two main sections:

### Left Panel: Input Controls (300px fixed width)

**Function Parameters Section:**
- Four text input fields for a, b, c, d
- Real-time validation (button disabled if invalid)
- Error messages displayed in red below inputs

**Colors Section:**
- **Graph Line** color picker (blue square button)
- **Axes/Grid** color picker (black square button)

**Period Markers Section:**
- "Show Period Markers" checkbox
- Marker color picker (enabled when checkbox checked)
- Transparency slider (0.00 - 1.00)

**Action Button:**
- **"Plot Graph"** button at bottom

### Right Panel: Graph Canvas (expandable)

- Matplotlib graph visualization
- Resizes dynamically with window
- Placeholder text when no graph displayed

### Status Bar (bottom)

- Displays current function equation
- Example: `f(x) = 1.0*sin(1.0*x + 0.0) + tan(0.1*x)`

---

## Function Parameters

The function `f(x) = a*sin(x*b + c) + tan(d*x)` has four parameters:

### Parameter `a` - Sine Amplitude

**Default:** 1.0  
**Valid Range:** Any non-zero number  
**Effect:** Controls the height of the sine wave

- **Positive values:** Wave oscillates above/below center line
- **Negative values:** Wave is inverted (flipped vertically)
- **Large values (>10):** Tall waves, may dominate graph
- **Small values (<0.1):** Gentle oscillations

**Examples:**
- `a = 2.0`: Sine wave oscillates between -2 and +2
- `a = -1.5`: Inverted sine wave, amplitude 1.5
- `a = 0.5`: Small gentle waves

### Parameter `b` - Sine Frequency

**Default:** 1.0  
**Valid Range:** Any non-zero number  
**Effect:** Controls how quickly the sine wave oscillates

- **b > 1:** Faster oscillations (shorter period)
- **b < 1:** Slower oscillations (longer period)
- **b cannot be 0** (would create infinite period)

**Examples:**
- `b = 2.0`: Sine completes 2 cycles in the original period
- `b = 0.5`: Sine completes 1/2 cycle in the original period

**Warning:** Very small values (e.g., 0.001) create extremely long periods and may display poorly.

### Parameter `c` - Phase Shift

**Default:** 0.0  
**Valid Range:** Any number  
**Effect:** Shifts the sine wave horizontally

- **Positive values:** Shift left
- **Negative values:** Shift right
- Measured in radians

**Examples:**
- `c = π/2 ≈ 1.57`: Shifts sine to start at maximum
- `c = -π ≈ -3.14`: Shifts sine by half period

### Parameter `d` - Tangent Frequency

**Default:** 0.1  
**Valid Range:** Any non-zero number  
**Effect:** Controls the tangent component's oscillation rate

- **d > 0:** Positive tangent contribution
- **d < 0:** Negative tangent contribution
- **d cannot be 0** (would create infinite period)

**Important:** The tangent function has **vertical asymptotes** where `cos(d*x) = 0`. The application detects and clips these regions to prevent rendering issues.

**Examples:**
- `d = 0.1`: Gentle tangent component (fewer asymptotes)
- `d = 1.0`: Strong tangent influence (more asymptotes)

---

## Visual Customization

### Changing Graph Line Color

1. Click the **blue square button** next to "Graph Line:"
2. Select a color from the color picker dialog
3. The button updates to show the selected color
4. Click **"Plot Graph"** to apply the new color

**Tips:**
- High contrast colors (red, blue, green) work best
- Avoid colors too similar to the background (white)

### Changing Axes/Grid Color

1. Click the **black square button** next to "Axes/Grid:"
2. Select a color from the color picker dialog
3. Both axes and grid lines use this color
4. Click **"Plot Graph"** to apply

**Tips:**
- Gray (#808080) provides subtle grid lines
- Black (#000000) is the default for maximum contrast

### Color Formats

Colors are internally stored as hex values (#RRGGBB):
- Red: #FF0000
- Green: #00FF00
- Blue: #0000FF
- Gray: #808080
- Black: #000000

---

## Period Markers

Period markers are vertical lines that show where each period begins and ends, helping visualize the periodic nature of the function.

### Enabling Period Markers

1. Check the **"Show Period Markers"** checkbox
2. The marker color picker and transparency slider become enabled
3. Click **"Plot Graph"** to see the markers

### Customizing Period Markers

**Color:**
- Click the period marker color button (default gray #808080)
- Select any color from the picker
- Bright colors (red, yellow, blue) are most visible

**Transparency:**
- Use the slider to adjust alpha from 0.00 (invisible) to 1.00 (opaque)
- Default: 0.30 (30% opaque)
- Lower values: Subtle background lines
- Higher values: Prominent markers

**Recommended Settings:**
- For subtle hints: Gray (#808080) at 0.20 alpha
- For clear divisions: Red (#FF0000) at 0.50 alpha
- For emphasis: Blue (#0000FF) at 0.80 alpha

### How Period Markers Are Placed

The application calculates the fundamental period `T` of the combined function, then places markers at:

```
x = -4T, -3T, -2T, -T, 0, T, 2T, 3T, 4T
```

This creates 9 marked regions (the 9 periods displayed).

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Plot Graph (if parameters are valid) |
| **Return** | Plot Graph (same as Enter) |

**Usage:**
- After entering parameters, press Enter instead of clicking the button
- Works from any parameter input field
- Only triggers if all parameters are valid (button is enabled)

---

## Tips and Best Practices

### Parameter Selection

1. **Start with defaults** - The default values (1, 1, 0, 0.1) provide a good baseline
2. **Change one at a time** - Easier to understand each parameter's effect
3. **Use round numbers** - Values like 2, 0.5, π make periods easier to visualize

### Visualizing Different Patterns

**Pure Sine Wave (no tangent):**
```
a = 1.0, b = 1.0, c = 0.0, d = 0.1  (very small d)
```

**Pure Tangent (no sine):**
```
a = 0.01, b = 1.0, c = 0.0, d = 1.0  (very small a)
```

**Complex Interference:**
```
a = 1.0, b = 2.0, c = 0.0, d = 0.5
```

### Window Resizing

- The graph automatically redraws when you resize the window
- There's a 200ms delay to avoid excessive redrawing
- The 9-period display is maintained at all window sizes
- Minimum window size: 800x600 pixels

### Performance

- Graph rendering typically takes < 0.5 seconds
- 1000 points are evaluated for smooth curves
- Asymptote detection is automatic
- Y-axis clipping prevents extreme values from distorting the view

---

## Troubleshooting

### "Invalid Parameters" Error

**Problem:** The "Plot Graph" button is disabled

**Solutions:**
1. Check that all four fields have numeric values
2. Ensure `b` and `d` are not zero
3. Look for error messages in red below the inputs
4. Remove any non-numeric characters (letters, symbols)

### Graph Not Updating

**Problem:** Graph doesn't change after clicking "Plot Graph"

**Solutions:**
1. Verify parameters changed (status bar shows new equation)
2. Check if colors are very similar (try high contrast)
3. Resize the window to force a redraw

### Extreme Values Warning

**Problem:** Warning dialog appears when plotting

**Explanation:**
- `a > 1000`: Very large amplitude may be hard to see
- `b < 0.001`: Very small frequency creates huge periods

**Solutions:**
- Use more moderate values for better visualization
- Acknowledge the warning and proceed if intentional

### Vertical Lines in Graph

**Problem:** Unexpected vertical lines appear

**Explanation:** These are asymptotes of the tangent function

**Normal behavior:** The tangent component has vertical asymptotes where `cos(d*x) = 0`. The application clips extreme values but some vertical artifacts may still appear near asymptotes.

**To reduce:**
- Use smaller values of `d` (e.g., 0.1 instead of 1.0)
- Period markers (if enabled) will show as solid vertical lines - these are intentional

### Application Won't Start

**Problem:** Error message when running `.\run.ps1`

**Solutions:**
1. Ensure virtual environment exists: `.venv` folder present
2. Reinstall dependencies: `.\.venv\Scripts\pip install -r requirements.txt`
3. Check Python version: `python --version` (must be 3.11+)
4. Verify PYTHONPATH is set correctly

---

## Technical Details

### Mathematical Background

The function combines two periodic components:

1. **Sine Component:** `a*sin(x*b + c)`
   - Period: `T_sin = 2π/|b|`
   - Always bounded between `-|a|` and `+|a|`

2. **Tangent Component:** `tan(d*x)`
   - Period: `T_tan = π/|d|`
   - Unbounded (approaches ±∞ at asymptotes)

**Combined Period:**
The fundamental period `T` is the least common multiple (LCM) of `T_sin` and `T_tan`, calculated using continued fraction approximation.

### Viewport Calculation

The application automatically computes the viewing window:

- **X-axis:** Shows exactly 9 periods: `[-4.5T, 4.5T]`
- **Y-axis:** Auto-scales to fit the function values with 10% padding
- **Clipping:** Y-values are clipped to prevent asymptote artifacts

### Asymptote Handling

Asymptotes occur at: `x = (π/2 + nπ)/d` for integer `n`

The application:
1. Detects asymptote positions
2. Clips Y-values to a reasonable range
3. Optionally draws semi-transparent vertical lines

### Rendering Details

- **Backend:** Matplotlib with Qt5Agg
- **Resolution:** 100 DPI
- **Figure Size:** 8" × 6" (default)
- **Line Width:** 2 points for function curve
- **Grid Alpha:** 0.3 (30% opacity)

### Color System

Colors use hex format (#RRGGBB):
- 24-bit RGB color space
- 16.7 million possible colors
- Alpha channel (0.0-1.0) for transparency

---

## Advanced Usage

### Exploring Periodicity

To understand how `b` and `d` interact:

1. Set `b = 2.0, d = 1.0` → Period = 2π (integer ratio)
2. Set `b = 1.0, d = 0.5` → Period = 2π (different ratio)
3. Set `b = 1.5, d = 1.0` → Period ≈ 4π (fractional ratio)

### Creating Specific Patterns

**Beat Frequency Effect:**
```
a = 1.0, b = 1.0, c = 0.0, d = 0.9
```
Close but non-matching frequencies create slow "beats"

**High Frequency Interference:**
```
a = 1.0, b = 5.0, c = 0.0, d = 0.7
```
Creates complex rapid oscillations

**Phase Shifted Combination:**
```
a = 1.0, b = 1.0, c = 1.57, d = 1.0  (c ≈ π/2)
```
Sine starts at peak instead of zero crossing

---

## Appendix: Example Parameters

| Pattern | a | b | c | d | Description |
|---------|---|---|---|---|-------------|
| Default | 1.0 | 1.0 | 0.0 | 0.1 | Gentle sine with subtle tangent |
| Pure Sine | 1.0 | 1.0 | 0.0 | 0.01 | Nearly pure sinusoidal wave |
| Strong Tangent | 0.5 | 1.0 | 0.0 | 1.0 | Dominant tangent component |
| Fast Oscillation | 1.0 | 5.0 | 0.0 | 0.2 | Rapid sine oscillations |
| Slow Wave | 1.0 | 0.5 | 0.0 | 0.1 | Long gentle waves |
| Inverted | -1.0 | 1.0 | 0.0 | 0.1 | Flipped vertically |
| Phase Shift | 1.0 | 1.0 | 1.57 | 0.1 | Starts at peak (c ≈ π/2) |
| Complex | 2.0 | 2.5 | 0.5 | 0.7 | Rich interference pattern |

---

## Support

For technical issues or questions:
1. Check this user guide
2. Review the README.md file
3. Examine the implementation report: `specs/001-function-graph-plotter/IMPLEMENTATION_REPORT.md`

---

**Version:** 0.1.0  
**Last Updated:** October 23, 2025  
**Application:** Function Graph Plotter (MVP)
