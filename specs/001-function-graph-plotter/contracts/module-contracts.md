# Module Contracts: Function Graph Plotter

**Feature**: 001-function-graph-plotter  
**Date**: 2025-10-23  
**Phase**: 1 (Design & Contracts)

This document defines the public interfaces (contracts) for each module in the function graph plotter application. These contracts serve as the API boundaries between modules and guide implementation.

## Module Overview

```
src/
├── models/          # Data structures (immutable contracts)
├── validation/      # Input validation
├── computation/     # Mathematical computation
├── rendering/       # Graph rendering
└── ui/              # User interface
```

---

## 1. validation.input

**Purpose**: Validate user parameter inputs in real-time

**File**: `src/validation/input.py`

### Public Interface

```python
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of validating a single parameter input."""
    is_valid: bool
    value: Optional[float]
    error_message: str

def validate_parameter(text: str) -> ValidationResult:
    """
    Validate a single parameter input string.
    
    Args:
        text: Raw text from input field
        
    Returns:
        ValidationResult with:
        - is_valid: True if text is valid numeric in range
        - value: Parsed float value if valid, None otherwise
        - error_message: Empty if valid, descriptive error otherwise
        
    Examples:
        >>> validate_parameter("1.5")
        ValidationResult(is_valid=True, value=1.5, error_message="")
        
        >>> validate_parameter("")
        ValidationResult(is_valid=False, value=None, error_message="Field cannot be empty")
        
        >>> validate_parameter("abc")
        ValidationResult(is_valid=False, value=None, error_message="Must be a numeric value")
        
        >>> validate_parameter("2000")
        ValidationResult(is_valid=False, value=None, error_message="Value must be between -1000 and 1000")
    """
    pass

def validate_all_parameters(
    a_text: str,
    b_text: str,
    c_text: str,
    d_text: str
) -> Tuple[bool, dict[str, ValidationResult]]:
    """
    Validate all four parameters at once.
    
    Args:
        a_text: Text from 'a' parameter field
        b_text: Text from 'b' parameter field
        c_text: Text from 'c' parameter field
        d_text: Text from 'd' parameter field
        
    Returns:
        (all_valid, results) where:
        - all_valid: True if all four parameters are valid
        - results: Dict mapping parameter name ('a', 'b', 'c', 'd') to ValidationResult
        
    Example:
        >>> all_valid, results = validate_all_parameters("1", "2", "0", "0.5")
        >>> all_valid
        True
        >>> results['a'].value
        1.0
    """
    pass
```

### Dependencies

- None (stdlib only)

### Contract Guarantees

- Empty strings return `is_valid=False`
- Non-numeric strings return `is_valid=False`
- Values outside `[-1000, 1000]` return `is_valid=False`
- Valid numeric strings in range return `is_valid=True` with parsed `float` value
- Error messages are user-friendly and actionable

---

## 2. computation.period

**Purpose**: Calculate the fundamental period of the combined function

**File**: `src/computation/period.py`

### Public Interface

```python
from typing import Optional
import numpy as np

def compute_fundamental_period(b: float, d: float) -> Optional[float]:
    """
    Compute the fundamental period of f(x) = a*sin(x*b + c) + tan(d*x).
    
    The period depends only on b and d (not on a or c):
    - Sine component has period 2π/|b| if b ≠ 0
    - Tangent component has period π/|d| if d ≠ 0
    - Combined period is LCM of component periods
    
    Args:
        b: Frequency multiplier for sine component
        d: Frequency multiplier for tangent component
        
    Returns:
        Fundamental period (float) or None if function is constant (b=0 and d=0)
        
    Examples:
        >>> compute_fundamental_period(1.0, 0.0)  # Pure sine
        6.283185307179586  # 2π
        
        >>> compute_fundamental_period(0.0, 1.0)  # Pure tangent
        3.141592653589793  # π
        
        >>> compute_fundamental_period(1.0, 1.0)  # Sine + tangent
        6.283185307179586  # 2π (LCM of 2π and π)
        
        >>> compute_fundamental_period(0.0, 0.0)  # Constant
        None
    """
    pass

def compute_display_range(fundamental_period: float, num_periods: int = 9) -> Tuple[float, float]:
    """
    Compute the X range to display a given number of periods symmetrically around origin.
    
    Args:
        fundamental_period: The fundamental period of the function
        num_periods: Number of periods to display (default 9 per spec)
        
    Returns:
        (x_min, x_max) tuple where x_min = -x_max (symmetric)
        
    Example:
        >>> compute_display_range(2*np.pi, num_periods=9)
        (-28.274333882308138, 28.274333882308138)  # ±4.5 * 2π
    """
    pass
```

### Dependencies

- `numpy`: For mathematical constants (`np.pi`) and `gcd` calculation

### Contract Guarantees

- Returns `None` if both `b=0` and `d=0` (constant function, no period)
- Returns positive float for all other cases
- Display range is always symmetric: `x_min = -x_max`
- Handles edge cases (b=0 XOR d=0) correctly

---

## 3. computation.function

**Purpose**: Evaluate the mathematical function and detect asymptotes

**File**: `src/computation/function.py`

### Public Interface

```python
import numpy as np
from src.models.parameters import FunctionParameters
from src.models.viewport import GraphViewport

def evaluate_function(
    x_array: np.ndarray,
    params: FunctionParameters
) -> np.ndarray:
    """
    Evaluate f(x) = a*sin(x*b + c) + tan(d*x) for an array of X values.
    
    Args:
        x_array: NumPy array of X coordinates
        params: Function parameters (a, b, c, d)
        
    Returns:
        NumPy array of Y values (same shape as x_array)
        
    Notes:
        - Uses vectorized NumPy operations for performance
        - Handles b=0 case: sine component becomes constant a*sin(c)
        - Handles d=0 case: tangent component is omitted
        - Asymptotes will produce inf/-inf values (caller should handle)
        
    Example:
        >>> params = FunctionParameters(a=1, b=1, c=0, d=0)
        >>> x = np.linspace(-np.pi, np.pi, 100)
        >>> y = evaluate_function(x, params)
        >>> y.shape
        (100,)
    """
    pass

def detect_asymptotes(
    x_min: float,
    x_max: float,
    d: float,
    tolerance: float = 1e-6
) -> list[float]:
    """
    Detect vertical asymptote positions in the range [x_min, x_max].
    
    Tangent has asymptotes where cos(d*x) = 0, i.e., x = (π/2 + n*π) / d
    
    Args:
        x_min: Minimum X coordinate
        x_max: Maximum X coordinate
        d: Frequency multiplier for tangent component
        tolerance: Tolerance for cos(d*x) near zero
        
    Returns:
        List of X coordinates where asymptotes occur (sorted)
        Empty list if d=0 (no tangent component)
        
    Example:
        >>> detect_asymptotes(-10, 10, d=1.0)
        [-7.853981633974483, -4.71238898038469, -1.5707963267948966,
         1.5707963267948966, 4.71238898038469, 7.853981633974483]
    """
    pass

def sample_function(
    params: FunctionParameters,
    x_min: float,
    x_max: float,
    points_per_period: int = 1000
) -> Tuple[np.ndarray, np.ndarray, list[float]]:
    """
    Sample the function over a range with adaptive sampling near asymptotes.
    
    Args:
        params: Function parameters
        x_min: Minimum X coordinate
        x_max: Maximum X coordinate
        points_per_period: Number of sample points per fundamental period
        
    Returns:
        (x_values, y_values, asymptote_positions) where:
        - x_values: NumPy array of sampled X coordinates
        - y_values: NumPy array of function values
        - asymptote_positions: List of asymptote X coordinates
        
    Notes:
        - Uses denser sampling near asymptotes for smooth curves
        - Total points ≈ points_per_period * num_periods
        - Y values may contain inf/-inf near asymptotes (caller clips)
    """
    pass
```

### Dependencies

- `numpy`: Vectorized math operations
- `src/models/parameters`: FunctionParameters dataclass

### Contract Guarantees

- Vectorized operations for performance (target: <2s for full graph)
- Handles all edge cases (b=0, d=0, both=0)
- Asymptote detection accurate within tolerance
- Sampling produces smooth curves (no visible artifacts)

---

## 4. computation.viewport

**Purpose**: Manage viewport transformation and auto-scaling

**File**: `src/computation/viewport.py`

### Public Interface

```python
import numpy as np
from src.models.viewport import GraphViewport

def create_viewport_for_function(
    fundamental_period: float,
    y_values: np.ndarray,
    width: int,
    height: int,
    y_padding_percent: float = 0.1
) -> GraphViewport:
    """
    Create a viewport that displays 9 periods with auto-scaled Y axis.
    
    Args:
        fundamental_period: Fundamental period of the function
        y_values: Array of Y values to fit (used for auto-scaling)
        width: Width of graph area in pixels
        height: Height of graph area in pixels
        y_padding_percent: Padding to add above/below Y range (default 10%)
        
    Returns:
        GraphViewport configured for 9 periods, symmetric X, auto-scaled Y
        
    Notes:
        - X range is always [-4.5T, 4.5T] for 9 periods
        - Y range auto-fits to min/max of y_values with padding
        - Handles inf/NaN in y_values by filtering to finite values
        
    Example:
        >>> y = np.array([...])  # Function values
        >>> viewport = create_viewport_for_function(
        ...     fundamental_period=2*np.pi,
        ...     y_values=y,
        ...     width=800,
        ...     height=600
        ... )
        >>> viewport.x_min
        -28.274333882308138  # -4.5 * 2π
    """
    pass

def update_viewport_for_resize(
    viewport: GraphViewport,
    new_width: int,
    new_height: int
) -> GraphViewport:
    """
    Create a new viewport with updated dimensions (for window resize).
    
    Args:
        viewport: Current viewport
        new_width: New width in pixels
        new_height: New height in pixels
        
    Returns:
        New GraphViewport with same X/Y ranges but new dimensions
        
    Notes:
        - Preserves X and Y ranges (caller may need to recalculate Y for new aspect ratio)
        - Creates immutable new viewport (does not modify original)
    """
    pass
```

### Dependencies

- `numpy`: Math operations, NaN/inf filtering
- `src/models/viewport`: GraphViewport dataclass

### Contract Guarantees

- Always creates symmetric X range: `x_min = -x_max`
- Always displays exactly 9 periods
- Y auto-scaling filters inf/NaN values
- Viewport is immutable (creates new instances)

---

## 5. rendering.graph

**Purpose**: Render the function graph using matplotlib

**File**: `src/rendering/graph.py`

### Public Interface

```python
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from src.models.parameters import FunctionParameters
from src.models.colors import ColorSettings
from src.models.viewport import GraphViewport

def render_graph(
    fig: Figure,
    ax: Axes,
    x_values: np.ndarray,
    y_values: np.ndarray,
    params: FunctionParameters,
    colors: ColorSettings,
    viewport: GraphViewport,
    asymptote_positions: list[float]
) -> None:
    """
    Render the complete graph including function curve, axes, markers, and labels.
    
    Args:
        fig: Matplotlib Figure object
        ax: Matplotlib Axes object
        x_values: Array of X coordinates
        y_values: Array of Y coordinates (may contain NaN for gaps)
        params: Function parameters (for title/label)
        colors: Color configuration
        viewport: Viewport for axis limits
        asymptote_positions: List of X coordinates for asymptote lines
        
    Returns:
        None (modifies fig and ax in-place)
        
    Side Effects:
        - Clears previous plot on ax
        - Draws function curve
        - Draws X and Y axes with arrows
        - Draws origin marker at O(0,0)
        - Draws asymptote lines (semi-transparent vertical, per clarification)
        - Draws period markers if enabled
        - Sets axis labels and title
        - Applies colors from ColorSettings
        
    Example:
        >>> fig, ax = plt.subplots(figsize=(8, 6))
        >>> render_graph(fig, ax, x, y, params, colors, viewport, asymptotes)
        >>> fig.canvas.draw()  # Update display
    """
    pass
```

### Dependencies

- `matplotlib`: Plotting library
- `numpy`: Array handling
- `src/models/*`: Data models
- `src/rendering/axes`: Axis rendering helper
- `src/rendering/markers`: Marker rendering helper

### Contract Guarantees

- Clears previous plot before rendering (no artifacts)
- Applies all colors from ColorSettings
- Renders asymptotes as semi-transparent vertical lines (per clarification)
- Renders period markers if enabled
- Marks origin O(0,0) visibly
- Handles NaN in y_values gracefully (breaks line)

---

## 6. rendering.axes

**Purpose**: Render X and Y axes with labels and arrows

**File**: `src/rendering/axes.py`

### Public Interface

```python
from matplotlib.axes import Axes
from src.models.colors import ColorSettings
from src.models.viewport import GraphViewport

def draw_axes(
    ax: Axes,
    viewport: GraphViewport,
    colors: ColorSettings
) -> None:
    """
    Draw X and Y axes with labels, tick marks, and directional arrows.
    
    Args:
        ax: Matplotlib Axes object
        viewport: Viewport for axis limits
        colors: Color configuration (uses axes_color)
        
    Returns:
        None (modifies ax in-place)
        
    Features:
        - Draws X and Y axes at y=0 and x=0 respectively
        - Adds arrow heads at positive ends
        - Labels: "X" near positive X axis, "Y" near positive Y axis
        - Tick marks at sensible intervals
        - Uses colors.axes_color
        
    Example:
        >>> draw_axes(ax, viewport, colors)
    """
    pass
```

### Dependencies

- `matplotlib.axes`: Axes object
- `src/models/colors`: ColorSettings
- `src/models/viewport`: GraphViewport

---

## 7. rendering.markers

**Purpose**: Render origin marker, period markers, and asymptote lines

**File**: `src/rendering/markers.py`

### Public Interface

```python
from matplotlib.axes import Axes
from src/models/colors import ColorSettings

def draw_origin_marker(ax: Axes, colors: ColorSettings) -> None:
    """
    Draw a visible marker at the origin O(0,0).
    
    Args:
        ax: Matplotlib Axes object
        colors: Color configuration
        
    Returns:
        None (modifies ax in-place)
        
    Implementation:
        - Circle or dot marker at (0, 0)
        - Contrasting color (e.g., red or colors.axes_color)
        - Labeled with "O" text annotation
    """
    pass

def draw_period_markers(
    ax: Axes,
    period: float,
    num_periods: int,
    colors: ColorSettings
) -> None:
    """
    Draw semi-transparent vertical lines at period boundaries.
    
    Args:
        ax: Matplotlib Axes object
        period: Fundamental period
        num_periods: Number of periods (9)
        colors: Color configuration (uses period_marker_color and alpha)
        
    Returns:
        None (modifies ax in-place)
        
    Implementation:
        - Vertical lines at x = n * period for n in [-4, -3, ..., 3, 4]
        - Color: colors.period_marker_color
        - Alpha: colors.period_marker_alpha
        - Only drawn if colors.period_markers_enabled is True
    """
    pass

def draw_asymptote_lines(
    ax: Axes,
    asymptote_positions: list[float],
    colors: ColorSettings
) -> None:
    """
    Draw semi-transparent vertical lines at asymptote positions.
    
    Args:
        ax: Matplotlib Axes object
        asymptote_positions: List of X coordinates where asymptotes occur
        colors: Color configuration
        
    Returns:
        None (modifies ax in-place)
        
    Implementation (per clarification):
        - Vertical dashed lines at each asymptote position
        - Color: Red or gray (semi-transparent)
        - Alpha: 0.3
        - Dashed line style '--'
    """
    pass
```

### Dependencies

- `matplotlib.axes`: Axes object
- `src/models/colors`: ColorSettings

---

## 8. ui.main_window

**Purpose**: Main application window with split panel layout

**File**: `src/ui/main_window.py` (using PyQt6)

### Public Interface

```python
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from src.ui.input_panel import InputPanel
from src.ui.graph_canvas import GraphCanvas

class MainWindow(QMainWindow):
    """Main application window with split layout: input panel (left) + graph (right)."""
    
    def __init__(self):
        """
        Initialize main window with:
        - Minimum size: 600x400 pixels (per clarification)
        - Layout: QHBoxLayout with InputPanel + GraphCanvas
        - Title: "Function Graph Plotter"
        """
        pass
    
    def on_start_clicked(self):
        """
        Handle "Start" button click from InputPanel.
        
        Workflow:
        1. Get validated parameters from InputPanel
        2. Compute function curve
        3. Update GraphCanvas with new curve
        """
        pass
    
    def on_resize_event(self, event):
        """
        Handle window resize event.
        
        Workflow:
        1. Get new dimensions
        2. Update viewport
        3. Redraw graph (must complete within 1 second per SC-003)
        """
        pass
```

### Dependencies

- `PyQt6.QtWidgets`: GUI components
- `src/ui.input_panel`: InputPanel widget
- `src/ui.graph_canvas`: GraphCanvas widget

---

## 9. ui.input_panel

**Purpose**: Left panel with parameter inputs, color pickers, and Start button

**File**: `src/ui/input_panel.py` (using PyQt6)

### Public Interface

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from src.models.parameters import FunctionParameters
from src.models.colors import ColorSettings

class InputPanel(QWidget):
    """
    Left panel with parameter inputs and controls.
    
    Layout (top to bottom):
    - Parameter input fields: a, b, c, d (QLineEdit with labels)
    - Color picker buttons: Graph Color, Axes Color
    - Period marker controls (optional): enable checkbox, color, alpha slider
    - Start button (bottom)
    """
    
    def __init__(self):
        """
        Initialize input panel with:
        - Pre-filled parameter fields (a=1, b=1, c=0, d=0 per clarification)
        - Default colors (blue graph, black axes per clarification)
        - Disabled Start button initially (enabled when all inputs valid)
        """
        pass
    
    def get_parameters(self) -> FunctionParameters:
        """
        Get current function parameters from input fields.
        
        Returns:
            FunctionParameters if all inputs valid, raises ValueError otherwise
        """
        pass
    
    def get_colors(self) -> ColorSettings:
        """Get current color settings from color pickers."""
        pass
    
    def on_parameter_changed(self):
        """
        Handle input field change event.
        
        Workflow:
        1. Validate changed parameter
        2. Update visual feedback (red border if invalid)
        3. Enable/disable Start button based on all validations
        """
        pass
    
    def is_start_enabled(self) -> bool:
        """Check if Start button should be enabled (all parameters valid)."""
        pass
```

### Dependencies

- `PyQt6.QtWidgets`: GUI components
- `src/validation.input`: Parameter validation
- `src/models.parameters`: FunctionParameters
- `src/models.colors`: ColorSettings

---

## 10. ui.graph_canvas

**Purpose**: Graph display area with matplotlib embedded in Qt

**File**: `src/ui/graph_canvas.py` (using PyQt6 + matplotlib)

### Public Interface

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from src.models.parameters import FunctionParameters
from src.models.colors import ColorSettings

class GraphCanvas(QWidget):
    """
    Graph display area using matplotlib embedded in PyQt6.
    
    Features:
    - Embeds matplotlib Figure in Qt widget
    - Handles high-DPI rendering
    - Provides update_graph() method for redrawing
    """
    
    def __init__(self):
        """
        Initialize graph canvas with:
        - Matplotlib Figure with DPI awareness
        - FigureCanvasQTAgg for Qt embedding
        - Empty initial plot
        """
        pass
    
    def update_graph(
        self,
        params: FunctionParameters,
        colors: ColorSettings
    ) -> None:
        """
        Update the graph with new parameters and colors.
        
        Args:
            params: Function parameters to plot
            colors: Color settings for rendering
            
        Workflow:
        1. Compute fundamental period
        2. Sample function
        3. Create viewport
        4. Render graph
        5. Refresh canvas (must complete within 2 seconds per SC-001)
        """
        pass
    
    def on_resize(self, width: int, height: int):
        """
        Handle resize event.
        
        Args:
            width: New width in pixels
            height: New height in pixels
            
        Workflow:
        1. Update viewport dimensions
        2. Redraw graph (must complete within 1 second per SC-003)
        """
        pass
```

### Dependencies

- `PyQt6.QtWidgets`: Qt widget base
- `matplotlib.backends.backend_qt5agg`: Matplotlib/Qt integration
- `matplotlib.figure`: Figure object
- `src/computation/*`: Function computation modules
- `src/rendering/*`: Graph rendering modules

---

## Contract Testing

Each module should have contract tests verifying:

1. **Input validation**: Correct handling of valid/invalid inputs
2. **Output format**: Return types match signatures
3. **Edge cases**: b=0, d=0, asymptotes, extreme values
4. **Performance**: Operations complete within specified time bounds
5. **Immutability**: Dataclasses don't mutate unexpectedly

Example contract test structure:

```python
# tests/contract/test_computation_period.py
def test_compute_fundamental_period_contract():
    """Test contract: returns Optional[float] for (float, float) input."""
    result = compute_fundamental_period(1.0, 0.0)
    assert isinstance(result, (float, type(None)))
    
def test_period_edge_cases_contract():
    """Test contract: handles edge cases as specified."""
    assert compute_fundamental_period(0.0, 0.0) is None  # Constant
    assert compute_fundamental_period(1.0, 0.0) == pytest.approx(2*np.pi)  # Pure sine
```

## Next Steps

1. Implement each module following these contracts
2. Write contract tests in `tests/contract/`
3. Write unit tests in `tests/unit/`
4. Proceed to Phase 2 (Tasks) with clear module boundaries
