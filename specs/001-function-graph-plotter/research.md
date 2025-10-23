# Research: Function Graph Plotter

**Feature**: 001-function-graph-plotter  
**Date**: 2025-10-23  
**Phase**: 0 (Outline & Research)

This document captures the research and technology selection decisions for implementing the function graph plotter application in Python.

## Research Questions

### 1. GUI Framework Selection

**Question**: Which Python GUI framework best suits cross-platform desktop development with matplotlib integration?

**Options Evaluated**:
1. **Tkinter** (stdlib)
2. **PyQt6** / PySide6 (Qt bindings)
3. **wxPython** (wxWidgets bindings)
4. **Kivy** (modern, mobile-first)

**Decision**: **PyQt6** (primary choice) with **Tkinter** as fallback

**Rationale**:
- **PyQt6** provides superior matplotlib integration via `matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg`
- Native look and feel on all platforms (Windows, macOS, Linux)
- Excellent support for custom widgets, color pickers, and responsive layouts
- Strong community support and documentation
- Better high-DPI support (important for FR-017)
- Professional appearance suitable for mathematical/scientific applications

**Tkinter Fallback Rationale**:
- If licensing concerns arise (PyQt6 uses GPL/commercial license), Tkinter is stdlib (no dependencies)
- Tkinter also has matplotlib integration via `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`
- Simpler but less polished UI

**Alternatives Considered & Rejected**:
- **wxPython**: Less active development than Qt, more complex matplotlib integration
- **Kivy**: Overkill for desktop-only app, non-native look and feel, touchscreen-focused

**Implementation Impact**: 
- Use PyQt6 as primary, ensure code is modular enough to swap to Tkinter if needed
- Abstract UI framework behind interfaces in `src/ui/` modules

---

### 2. Mathematical Computation Strategy

**Question**: How should we compute the function `f(x) = a*sin(x*b + c) + tan(d*x)` efficiently and accurately?

**Decision**: **NumPy vectorized operations** with **mathematical edge case handling**

**Rationale**:
- NumPy's vectorized operations are 10-100x faster than Python loops for array math
- Native support for `numpy.sin()`, `numpy.tan()` with IEEE 754 floating point behavior
- Efficient handling of large arrays (thousands of sample points for smooth curves)
- Integrates seamlessly with matplotlib for plotting

**Edge Case Handling Strategy**:
1. **b=0 case**: Sine component becomes constant `a*sin(c)`, function reduces to `a*sin(c) + tan(d*x)`
2. **d=0 case**: Tangent component disappears, function becomes `a*sin(x*b + c)`
3. **Both b=0 and d=0**: Function becomes constant horizontal line `y = a*sin(c)`
4. **Asymptotes** (when `d != 0`): Tangent has vertical asymptotes at `x = π/(2d) + nπ/d` for integer n
   - Detect asymptotes by checking where `abs(cos(d*x))` is near zero
   - Clip Y values at viewport boundaries
   - Draw semi-transparent vertical lines at asymptote positions (per clarification)

**Sampling Strategy**:
- Sample 1000-2000 points per period for smooth curves (9 periods = 9000-18000 points)
- Adaptive sampling near asymptotes (denser sampling to avoid artifacts)

**Alternatives Considered & Rejected**:
- **SymPy symbolic math**: Overkill for numerical plotting, slower than NumPy
- **Pure Python loops**: Too slow for real-time rendering

**Implementation Impact**:
- Create `src/computation/function.py` with `evaluate_function(x_array, a, b, c, d)` using NumPy
- Create `src/computation/period.py` for fundamental period calculation

---

### 3. Period Calculation Algorithm

**Question**: How do we calculate the fundamental period of the combined function `f(x) = a*sin(x*b + c) + tan(d*x)`?

**Decision**: **Least Common Multiple (LCM) of component periods** with special case handling

**Rationale**:
- **Sine period**: `T_sin = 2π / |b|` when `b != 0`
- **Tangent period**: `T_tan = π / |d|` when `d != 0`
- **Fundamental period**: `T = LCM(T_sin, T_tan)` converted to LCM of rational multiples of π

**Algorithm**:
```python
def compute_fundamental_period(b, d):
    if b == 0 and d == 0:
        return None  # Constant function, no period
    elif b == 0:
        return π / abs(d)  # Only tangent component
    elif d == 0:
        return 2 * π / abs(b)  # Only sine component
    else:
        # LCM of 2π/|b| and π/|d|
        # Express as rational multiples of π: (2/|b|)π and (1/|d|)π
        # LCM(2/|b|, 1/|d|) = LCM(2*|d|, |b|) / (|b|*|d|) * π
        from math import gcd
        numerator = 2 * abs(d) * abs(b) // gcd(2 * abs(d), abs(b))
        denominator = abs(b) * abs(d)
        return (numerator / denominator) * π
```

**Special Cases**:
- **Irrational ratios**: When b and d create irrational period ratios, the function is *quasi-periodic* (not truly periodic). For display purposes, use the larger component period multiplied by a factor to show "apparent" periodicity.
- **Very small/large periods**: Clamp to reasonable display range (minimum period: 0.1, maximum: 1000)

**9 Periods Display Strategy**:
- Calculate fundamental period `T`
- Display range: `x ∈ [-4.5T, 4.5T]` (symmetrical around origin, 9 periods total)
- Adjust viewport when window resizes to maintain 9 periods

**Alternatives Considered & Rejected**:
- **Fixed period assumption**: Doesn't handle varying b, d parameters
- **Numerical period detection**: Too slow and inaccurate for real-time updates

**Implementation Impact**:
- Create `src/computation/period.py` with `compute_fundamental_period(b, d)`
- Use period in viewport calculation: `src/computation/viewport.py`

---

### 4. Viewport Scaling and Coordinate Transformation

**Question**: How should we map mathematical coordinates to screen pixels while maintaining symmetry and 9-period constraint?

**Decision**: **Affine transformation** with **automatic Y-axis scaling**

**Rationale**:
- **X-axis**: Fixed range based on 9 periods: `x ∈ [-4.5T, 4.5T]` where T = fundamental period
- **Y-axis**: Auto-scale to fit min/max function values in the visible X range (FR-009)
- **Symmetry**: Enforced by construction (xMin = -xMax)
- **Aspect ratio**: Allow non-uniform scaling (Y can scale independently to fit data)

**Transformation Math**:
```
Screen coordinates (sx, sy) ← Math coordinates (x, y):
  sx = (x - xMin) / (xMax - xMin) * width
  sy = height - (y - yMin) / (yMax - yMin) * height  # Flip Y for screen coords
```

**Auto-scaling Strategy**:
1. Sample function over X range
2. Find `yMin = min(f(x))`, `yMax = max(f(x))`
3. Add 10% padding: `yMin -= 0.1 * (yMax - yMin)`, `yMax += 0.1 * (yMax - yMin)`
4. Handle asymptotes: clip extreme values to reasonable bounds (e.g., ±10^6)

**Window Resize Handling**:
- On resize event, recompute transformation matrix
- Maintain X range (9 periods)
- Recompute Y scale to fit new aspect ratio
- Redraw graph (must complete within 1 second per SC-003)

**Alternatives Considered & Rejected**:
- **Fixed aspect ratio**: Wastes screen space, doesn't fit requirement
- **Manual Y-axis bounds**: Poor UX, doesn't auto-fit data

**Implementation Impact**:
- Create `src/computation/viewport.py` with `ViewportTransform` class
- Methods: `math_to_screen(x, y)`, `screen_to_math(sx, sy)`, `update_bounds(xMin, xMax, yMin, yMax, width, height)`

---

### 5. Input Validation Strategy

**Question**: How should we validate numeric parameter inputs in real-time while maintaining good UX?

**Decision**: **Real-time validation with visual feedback** and **disabled button state**

**Rationale** (per clarification in spec):
- User selected Option A: "Block submission: Disable the "Start" button until all fields contain valid numeric values"
- Real-time validation provides immediate feedback (better UX than error dialog)
- Visual indicators: red border or error message next to invalid fields
- "Start" button is grayed out and non-clickable until all fields valid

**Validation Rules**:
- **Numeric**: Must parse as Python `float`
- **Non-empty**: Fields cannot be blank (default values provided on launch)
- **Range** (optional): Could add reasonable limits (e.g., `-1000 <= a,b,c,d <= 1000`) to prevent overflow

**Implementation**:
```python
def validate_parameter(text: str) -> tuple[bool, float | None, str]:
    """
    Returns: (is_valid, parsed_value, error_message)
    """
    if not text.strip():
        return (False, None, "Field cannot be empty")
    try:
        value = float(text)
        if abs(value) > 1000:
            return (False, None, "Value must be between -1000 and 1000")
        return (True, value, "")
    except ValueError:
        return (False, None, "Must be a numeric value")
```

**UI Feedback**:
- Invalid field: red border, error message below field
- Valid field: normal border, no message
- "Start" button: enabled only when all 4 parameters valid

**Alternatives Considered & Rejected**:
- **Submission-time validation** (Option C): Poor UX, frustrating error dialogs
- **Auto-correction** (Option D): Confusing, user loses control

**Implementation Impact**:
- Create `src/validation/input.py` with `validate_parameter(text)` function
- Connect to UI input field change events: `textChanged.connect(on_parameter_changed)`
- Track validation state in UI controller

---

### 6. Asymptote Visualization Approach

**Question**: How should vertical asymptotes of the tangent function be visualized?

**Decision**: **Semi-transparent vertical lines + graph clipping** (Option C from clarification)

**Rationale** (per user clarification):
- User selected Option C: "Asymptote lines: Draw semi-transparent vertical lines at asymptote positions and clip the graph"
- Provides clear visual indication of discontinuities
- Clipping prevents graph from shooting to infinity and obscuring other data
- Semi-transparent lines don't obscure the main graph line

**Implementation Strategy**:
1. **Detect asymptotes**: Find x-values where `cos(d*x) ≈ 0` (within tolerance of 1e-6)
2. **Asymptote positions**: `x_asymptote = (π/2 + n*π) / d` for integer n in visible range
3. **Draw lines**: Use `matplotlib.pyplot.axvline(x_asymptote, color='red', alpha=0.3, linestyle='--')`
4. **Clip graph**: 
   - Sample function near asymptotes
   - Replace y-values exceeding viewport bounds with `NaN` (matplotlib will break line at NaN)
   - Alternatively, split curve into segments and draw separately

**Visual Specifications**:
- Line color: Red or gray (semi-transparent)
- Alpha: 0.3 (configurable by user in period marker settings)
- Line style: Dashed `--`
- Line width: 1-2 pixels

**Alternatives Considered** (from clarification question):
- **Option A (Clip only)**: Less informative, user doesn't see where asymptotes are
- **Option B (Visual discontinuity/gap)**: Harder to implement, less clear
- **Option D (Fade effect)**: Complex to implement, less standard

**Implementation Impact**:
- Add asymptote detection to `src/computation/function.py`
- Add asymptote rendering to `src/rendering/markers.py`
- Coordinate with period marker implementation (similar visual treatment)

---

### 7. Color Picker Implementation

**Question**: What's the best approach for cross-platform color picker widgets in PyQt6/Tkinter?

**Decision**: **QColorDialog (PyQt6)** or **tkinter.colorchooser (Tkinter)**

**PyQt6 Approach**:
```python
from PyQt6.QtWidgets import QColorDialog, QPushButton
from PyQt6.QtGui import QColor

# Color picker button
self.graph_color_button = QPushButton("Graph Color")
self.graph_color_button.clicked.connect(self.choose_graph_color)

def choose_graph_color(self):
    color = QColorDialog.getColor(initial=QColor("#0000FF"))  # Default blue
    if color.isValid():
        self.graph_color = color.name()  # Hex string like "#0000FF"
        self.update_color_button_preview(self.graph_color_button, color)
```

**Tkinter Fallback**:
```python
from tkinter import colorchooser

def choose_graph_color(self):
    color_tuple, color_hex = colorchooser.askcolor(
        initialcolor="#0000FF",
        title="Choose Graph Color"
    )
    if color_hex:
        self.graph_color = color_hex
```

**Default Colors** (per clarification):
- Graph line: Blue (`#0000FF`)
- Axes: Black (`#000000`)
- Period markers (optional): Gray (`#808080`) with alpha 0.3

**Implementation Impact**:
- Add color picker buttons to `src/ui/input_panel.py`
- Store selected colors in application state
- Pass colors to matplotlib rendering functions

---

### 8. High-DPI Display Support

**Question**: How do we ensure graphs render smoothly on high-DPI (Retina, 4K) displays?

**Decision**: **Matplotlib DPI-aware rendering** + **Qt scaling**

**Rationale**:
- Modern displays have 2x-4x pixel density
- Matplotlib supports DPI-aware figure creation
- PyQt6 has built-in high-DPI support

**Implementation**:
```python
import matplotlib
matplotlib.use('Qt5Agg')  # or 'TkAgg' for Tkinter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Enable high-DPI
from PyQt6.QtWidgets import QApplication
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# Create DPI-aware figure
dpi = 100  # Base DPI
fig = Figure(figsize=(8, 6), dpi=dpi)
canvas = FigureCanvasQTAgg(fig)
```

**Testing Strategy**:
- Test on 1x, 2x, and 4x DPI displays
- Verify text remains readable and lines are crisp
- Check rendering performance (should still meet 2s target)

**Alternatives Considered & Rejected**:
- **Fixed low DPI**: Blurry on modern displays
- **Manual bitmap scaling**: Complex, worse quality than native

**Implementation Impact**:
- Configure matplotlib backend with DPI awareness
- Set Qt high-DPI attributes in `src/main.py` before creating QApplication
- Test on various display densities

---

### 9. Testing Strategy

**Question**: What testing approach ensures compliance with constitution's 80% coverage target and all success criteria?

**Decision**: **Layered testing: Unit → Integration → Visual Regression**

**Unit Tests** (pytest):
- **Mathematical functions**: `test_function.py`
  - Test function evaluation for various (a,b,c,d) combinations
  - Test edge cases: b=0, d=0, both=0
  - Test asymptote detection
  - Test period calculation (including LCM logic)
- **Validation**: `test_validation.py`
  - Test numeric validation (valid, invalid, empty, extreme values)
  - Test error message generation
- **Viewport**: `test_viewport.py`
  - Test coordinate transformations
  - Test auto-scaling logic
  - Test symmetry constraints

**Integration Tests** (pytest + pytest-qt):
- **UI Interactions**: `test_ui_interactions.py`
  - Test parameter input changes
  - Test "Start" button enable/disable
  - Test color picker integration
- **Window Resize**: `test_window_resize.py`
  - Test resize handling
  - Verify 9-period constraint maintained
  - Verify performance (<1s)
- **Edge Cases**: `test_edge_cases.py`
  - Test all edge cases from spec (b=0, d=0, asymptotes, extreme values)
  - Verify no crashes or visual artifacts

**Visual Regression Tests** (pytest + matplotlib baseline):
- Use `matplotlib.testing.decorators.image_comparison`
- Compare rendered graphs against baseline images
- Test cases: default function, various parameters, edge cases
- Ensures rendering consistency across updates (SC-008)

**Performance Benchmarks** (pytest-benchmark):
- Benchmark graph rendering time (must be <2s)
- Benchmark window resize time (must be <1s)
- Run in CI to catch performance regressions

**Coverage Target**: 80%+ for `src/computation/`, `src/validation/`, `src/models/`

**Alternatives Considered & Rejected**:
- **Manual testing only**: Violates constitution, no regression protection
- **E2E tests only**: Slow, hard to debug, doesn't meet coverage target

**Implementation Impact**:
- Create `tests/unit/`, `tests/integration/`, `tests/visual/` directories
- Configure pytest in `pytest.ini`
- Add pytest-qt and pytest-benchmark to `requirements-dev.txt`
- Set up CI to run tests and check coverage

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Language** | Python 3.11+ | Specified by user, excellent scientific computing ecosystem |
| **GUI Framework** | PyQt6 (primary), Tkinter (fallback) | Best matplotlib integration, native look, high-DPI support |
| **Plotting** | Matplotlib | Industry standard for mathematical plotting, accurate rendering |
| **Computation** | NumPy | Fast vectorized operations, IEEE 754 math |
| **Testing** | pytest, pytest-qt, pytest-benchmark | Comprehensive testing, UI testing, performance benchmarks |
| **Linting** | flake8, black, mypy | Code quality, formatting, type safety |
| **Package Management** | pip + requirements.txt + virtual environment | Standard Python workflow |

## Dependencies

### Production (`requirements.txt`)
```
numpy>=1.24.0
matplotlib>=3.7.0
PyQt6>=6.5.0  # Or remove if using Tkinter
```

### Development (`requirements-dev.txt`)
```
pytest>=7.4.0
pytest-qt>=4.2.0
pytest-benchmark>=4.0.0
pytest-cov>=4.1.0
flake8>=6.0.0
black>=23.0.0
mypy>=1.5.0
```

## Next Steps

This research document resolves all "NEEDS CLARIFICATION" items from the Technical Context section of the plan. Proceed to:

1. **Phase 1**: Generate `data-model.md` (data structures)
2. **Phase 1**: Generate `contracts/` (internal module interfaces)
3. **Phase 1**: Generate `quickstart.md` (setup and run instructions)
4. **Phase 1**: Update agent context with Python stack information

All research questions have been answered with concrete decisions and implementation guidance.
