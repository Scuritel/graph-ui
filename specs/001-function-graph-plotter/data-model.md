# Data Model: Function Graph Plotter

**Feature**: 001-function-graph-plotter  
**Date**: 2025-10-23  
**Phase**: 1 (Design & Contracts)

This document defines the core data structures used throughout the function graph plotter application.

## Overview

The application uses four primary data models (as specified in the Key Entities section of the spec):

1. **FunctionParameters**: User-provided function coefficients
2. **ColorSettings**: User-selected color preferences
3. **GraphViewport**: Current display state and coordinate system
4. **FunctionCurve**: Computed mathematical curve data

All models are implemented as Python `@dataclass` for immutability, type safety, and easy serialization.

---

## 1. FunctionParameters

Represents the four coefficients in the function `f(x) = a*sin(x*b + c) + tan(d*x)`.

### Definition

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FunctionParameters:
    """
    Immutable parameters for the mathematical function.
    
    Function: f(x) = a*sin(x*b + c) + tan(d*x)
    
    Attributes:
        a: Amplitude scalar for sine component
        b: Frequency multiplier for sine component (can be 0)
        c: Phase shift for sine component (in radians)
        d: Frequency multiplier for tangent component (can be 0)
    """
    a: float = 1.0
    b: float = 1.0
    c: float = 0.0
    d: float = 0.0
    
    def __post_init__(self):
        """Validate parameter ranges."""
        for param_name in ['a', 'b', 'c', 'd']:
            value = getattr(self, param_name)
            if not isinstance(value, (int, float)):
                raise TypeError(f"{param_name} must be numeric")
            if abs(value) > 1000:
                raise ValueError(f"{param_name} must be between -1000 and 1000")
```

### Usage

```python
# Default parameters (pre-filled on app launch per clarification)
default_params = FunctionParameters()  # a=1, b=1, c=0, d=0

# Custom parameters
params = FunctionParameters(a=2.5, b=0.5, c=1.0, d=0.1)

# Immutable - creates new instance on change
new_params = FunctionParameters(
    a=params.a,
    b=params.b,
    c=params.c,
    d=0.0  # Changed value
)
```

### Validation Rules

- All parameters MUST be numeric (`float` or `int`)
- All parameters MUST be in range `[-1000, 1000]` to prevent overflow
- `b` and `d` CAN be zero (handled as edge cases)
- Dataclass is `frozen=True` for immutability (prevents accidental modification)

### Edge Cases

| Case | Behavior |
|------|----------|
| `b = 0` | Sine component becomes constant `a*sin(c)` |
| `d = 0` | Tangent component disappears, pure sine wave |
| `b = 0, d = 0` | Function becomes horizontal line `y = a*sin(c)` |

---

## 2. ColorSettings

Represents user-selected colors for graph elements.

### Definition

```python
from dataclasses import dataclass

@dataclass
class ColorSettings:
    """
    Color configuration for graph rendering.
    
    Attributes:
        graph_color: Hex color string for the function curve (default: blue)
        axes_color: Hex color string for X and Y axes (default: black)
        period_marker_color: Hex color string for period markers (optional, default: gray)
        period_marker_alpha: Transparency for period markers, range [0.0, 1.0] (default: 0.3)
        period_markers_enabled: Whether to show period markers (default: False)
    """
    graph_color: str = "#0000FF"  # Blue (per clarification)
    axes_color: str = "#000000"   # Black (per clarification)
    period_marker_color: str = "#808080"  # Gray
    period_marker_alpha: float = 0.3
    period_markers_enabled: bool = False
    
    def __post_init__(self):
        """Validate color formats and alpha range."""
        # Validate hex color format
        for color_attr in ['graph_color', 'axes_color', 'period_marker_color']:
            color = getattr(self, color_attr)
            if not isinstance(color, str) or not color.startswith('#') or len(color) != 7:
                raise ValueError(f"{color_attr} must be a hex color string like #RRGGBB")
        
        # Validate alpha range
        if not (0.0 <= self.period_marker_alpha <= 1.0):
            raise ValueError("period_marker_alpha must be between 0.0 and 1.0")
    
    def to_rgb_tuple(self, color_hex: str) -> tuple[float, float, float]:
        """
        Convert hex color to matplotlib RGB tuple (0.0-1.0 range).
        
        Args:
            color_hex: Hex color string like "#RRGGBB"
            
        Returns:
            (r, g, b) tuple with values in [0.0, 1.0]
        """
        hex_clean = color_hex.lstrip('#')
        r = int(hex_clean[0:2], 16) / 255.0
        g = int(hex_clean[2:4], 16) / 255.0
        b = int(hex_clean[4:6], 16) / 255.0
        return (r, g, b)
```

### Usage

```python
# Default colors (blue graph, black axes per clarification)
colors = ColorSettings()

# Custom colors
colors = ColorSettings(
    graph_color="#FF0000",  # Red graph
    axes_color="#333333",   # Dark gray axes
    period_markers_enabled=True,
    period_marker_alpha=0.5
)

# Convert to matplotlib format
rgb = colors.to_rgb_tuple(colors.graph_color)  # (1.0, 0.0, 0.0) for red
```

### Validation Rules

- Color strings MUST be in hex format `#RRGGBB`
- `period_marker_alpha` MUST be in range `[0.0, 1.0]`
- RGB conversion uses 0.0-1.0 range (matplotlib convention)

---

## 3. GraphViewport

Represents the current display state and coordinate transformation.

### Definition

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class GraphViewport:
    """
    Viewport state for coordinate transformation and display bounds.
    
    Attributes:
        x_min: Minimum X coordinate in mathematical space (always negative)
        x_max: Maximum X coordinate in mathematical space (always positive)
        y_min: Minimum Y coordinate in mathematical space (auto-scaled)
        y_max: Maximum Y coordinate in mathematical space (auto-scaled)
        width: Width of graph area in pixels
        height: Height of graph area in pixels
        number_of_periods: Constant 9 (always display 9 periods per spec)
    """
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    width: int
    height: int
    number_of_periods: int = 9
    
    def __post_init__(self):
        """Validate viewport constraints."""
        # Ensure symmetry around origin (per spec FR-008)
        if not np.isclose(self.x_min, -self.x_max, rtol=1e-9):
            raise ValueError(f"Viewport must be symmetric: x_min={self.x_min}, x_max={self.x_max}")
        
        # Ensure positive dimensions
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Viewport width and height must be positive")
        
        # Ensure number of periods is exactly 9
        if self.number_of_periods != 9:
            raise ValueError("number_of_periods must be exactly 9 per specification")
    
    def math_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """
        Transform mathematical coordinates to screen pixel coordinates.
        
        Args:
            x: Mathematical X coordinate
            y: Mathematical Y coordinate
            
        Returns:
            (screen_x, screen_y) tuple in pixel coordinates
        """
        # Linear transformation
        screen_x = (x - self.x_min) / (self.x_max - self.x_min) * self.width
        # Flip Y axis for screen coordinates (Y increases downward on screen)
        screen_y = self.height - (y - self.y_min) / (self.y_max - self.y_min) * self.height
        return (screen_x, screen_y)
    
    def screen_to_math(self, screen_x: float, screen_y: float) -> tuple[float, float]:
        """
        Transform screen pixel coordinates to mathematical coordinates.
        
        Args:
            screen_x: Screen X coordinate in pixels
            screen_y: Screen Y coordinate in pixels
            
        Returns:
            (x, y) tuple in mathematical coordinates
        """
        x = self.x_min + (screen_x / self.width) * (self.x_max - self.x_min)
        # Unflip Y axis
        y = self.y_max - (screen_y / self.height) * (self.y_max - self.y_min)
        return (x, y)
    
    @staticmethod
    def create_for_function(
        fundamental_period: float,
        y_min: float,
        y_max: float,
        width: int,
        height: int
    ) -> 'GraphViewport':
        """
        Factory method to create a viewport for displaying 9 periods.
        
        Args:
            fundamental_period: The fundamental period of the function
            y_min: Minimum Y value to display (auto-scaled)
            y_max: Maximum Y value to display (auto-scaled)
            width: Width of graph area in pixels
            height: Height of graph area in pixels
            
        Returns:
            GraphViewport configured for 9 periods centered at origin
        """
        # 9 periods centered at origin: [-4.5T, 4.5T]
        half_range = 4.5 * fundamental_period
        return GraphViewport(
            x_min=-half_range,
            x_max=half_range,
            y_min=y_min,
            y_max=y_max,
            width=width,
            height=height,
            number_of_periods=9
        )
```

### Usage

```python
# Create viewport for a function with period T=2π
period = 2 * np.pi
viewport = GraphViewport.create_for_function(
    fundamental_period=period,
    y_min=-2.5,
    y_max=2.5,
    width=800,
    height=600
)

# Transform coordinates
screen_x, screen_y = viewport.math_to_screen(0.0, 0.0)  # Origin
math_x, math_y = viewport.screen_to_math(400, 300)  # Center of screen
```

### Invariants

- **Symmetry**: `x_min = -x_max` (enforced in `__post_init__`)
- **9 Periods**: X range always spans exactly 9 fundamental periods
- **Auto-scale Y**: Y range auto-fits function values with 10% padding
- **Positive dimensions**: `width > 0` and `height > 0`

---

## 4. FunctionCurve

Represents the computed mathematical curve as a set of sampled points.

### Definition

```python
from dataclasses import dataclass
import numpy as np
from typing import Optional

@dataclass
class FunctionCurve:
    """
    Computed function curve as sampled (x, y) points.
    
    Attributes:
        x_values: NumPy array of X coordinates (sampled points)
        y_values: NumPy array of Y coordinates (function values at x_values)
        fundamental_period: The fundamental period of the function
        asymptote_positions: List of X coordinates where vertical asymptotes occur
        has_asymptotes: Whether the function has vertical asymptotes
    """
    x_values: np.ndarray
    y_values: np.ndarray
    fundamental_period: float
    asymptote_positions: list[float]
    has_asymptotes: bool
    
    def __post_init__(self):
        """Validate curve data."""
        if len(self.x_values) != len(self.y_values):
            raise ValueError("x_values and y_values must have the same length")
        
        if len(self.x_values) == 0:
            raise ValueError("Curve must have at least one point")
        
        if self.fundamental_period <= 0:
            raise ValueError("Fundamental period must be positive")
    
    @property
    def num_points(self) -> int:
        """Number of sampled points in the curve."""
        return len(self.x_values)
    
    @property
    def y_min(self) -> float:
        """Minimum Y value in the curve (excluding NaN/inf)."""
        finite_y = self.y_values[np.isfinite(self.y_values)]
        return float(np.min(finite_y)) if len(finite_y) > 0 else 0.0
    
    @property
    def y_max(self) -> float:
        """Maximum Y value in the curve (excluding NaN/inf)."""
        finite_y = self.y_values[np.isfinite(self.y_values)]
        return float(np.max(finite_y)) if len(finite_y) > 0 else 0.0
    
    def clip_to_viewport(self, y_min: float, y_max: float) -> 'FunctionCurve':
        """
        Clip Y values to viewport bounds, replacing out-of-bounds with NaN.
        
        This is used for handling asymptotes (per clarification: clip graph at viewport).
        
        Args:
            y_min: Minimum Y bound
            y_max: Maximum Y bound
            
        Returns:
            New FunctionCurve with clipped Y values
        """
        clipped_y = np.copy(self.y_values)
        clipped_y[clipped_y < y_min] = np.nan
        clipped_y[clipped_y > y_max] = np.nan
        
        return FunctionCurve(
            x_values=self.x_values,
            y_values=clipped_y,
            fundamental_period=self.fundamental_period,
            asymptote_positions=self.asymptote_positions,
            has_asymptotes=self.has_asymptotes
        )
```

### Usage

```python
# Compute curve (typically done by computation module)
x = np.linspace(-10, 10, 2000)
y = a * np.sin(x * b + c) + np.tan(d * x)

curve = FunctionCurve(
    x_values=x,
    y_values=y,
    fundamental_period=2 * np.pi,
    asymptote_positions=[np.pi/2, 3*np.pi/2],
    has_asymptotes=True
)

# Get bounds for auto-scaling
y_min, y_max = curve.y_min, curve.y_max

# Clip for rendering
clipped_curve = curve.clip_to_viewport(y_min=-10, y_max=10)
```

### Sampling Strategy

- **Points per period**: 1000-2000 points for smooth curves
- **Total points for 9 periods**: 9000-18000 points
- **Adaptive sampling**: Denser near asymptotes to avoid artifacts
- **NaN handling**: Use `np.nan` to break lines at discontinuities (matplotlib handles gracefully)

---

## Data Flow

```
User Input (UI)
    ↓
FunctionParameters (a, b, c, d)
    ↓
computation.period.compute_fundamental_period()
    ↓
fundamental_period
    ↓
computation.function.evaluate_function()
    ↓
FunctionCurve (x_values, y_values, asymptotes)
    ↓
GraphViewport.create_for_function() + auto-scale Y
    ↓
GraphViewport (x_min, x_max, y_min, y_max, width, height)
    ↓
rendering.graph.render() + ColorSettings
    ↓
Matplotlib Figure → UI Canvas
```

## Module Mapping

| Data Model | Primary Module | Usage |
|------------|----------------|-------|
| `FunctionParameters` | `src/models/parameters.py` | UI input, computation input |
| `ColorSettings` | `src/models/colors.py` | UI color pickers, rendering |
| `GraphViewport` | `src/models/viewport.py` | Coordinate transformation, rendering |
| `FunctionCurve` | Returned by `src/computation/function.py` | Rendering input |

## Type Hints

All data models use full type hints for IDE support and `mypy` type checking:

```python
from typing import Optional, Union
import numpy as np
import numpy.typing as npt

# Example type aliases
FloatArray = npt.NDArray[np.float64]
ColorHex = str  # Hex color string like "#RRGGBB"
```

## Immutability

- `FunctionParameters`: Immutable (`frozen=True` dataclass)
- `ColorSettings`: Mutable (user can change colors)
- `GraphViewport`: Immutable (create new viewport on resize)
- `FunctionCurve`: Immutable (create new curve on parameter change)

Immutability prevents accidental state corruption and makes reasoning about data flow easier.

## Next Steps

With data models defined:

1. Generate module contracts in `contracts/` directory
2. Implement data classes in `src/models/`
3. Write unit tests in `tests/unit/test_models.py`
4. Proceed to implementation phase with clear type contracts
