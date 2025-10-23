"""
Viewport calculation for graph display.

This module computes the appropriate viewport dimensions to display
exactly 9 periods of the function, symmetric around the origin.
"""

from typing import Sequence

import numpy as np
import numpy.typing as npt

from src.computation.period import compute_fundamental_period
from src.models.parameters import FunctionParameters
from src.models.viewport import GraphViewport


def compute_viewport_for_nine_periods(params: FunctionParameters) -> GraphViewport:
    """
    Compute a viewport that displays exactly 9 periods of the function.

    The viewport is symmetric around the origin (0, 0) and shows 9 complete
    periods of the combined function f(x) = a*sin(x*b + c) + tan(d*x).

    Args:
        params: Function parameters

    Returns:
        GraphViewport symmetric around origin showing 9 periods
    """
    # Compute fundamental period
    period = compute_fundamental_period(params.b, params.d)

    # Total width for 9 periods
    total_width = 9 * period

    # Half width (symmetric around origin)
    half_width = total_width / 2

    # Compute appropriate height based on function amplitude
    # The sine component ranges from -a to +a
    # The tangent component can be very large near asymptotes, but we clip it
    # A reasonable height is based on the sine amplitude plus some margin

    sine_amplitude = abs(params.a)

    # For tangent, we consider the typical range between asymptotes
    # The maximum of tan varies, but we use a heuristic based on period
    # Typical range is about 5-10x the sine amplitude for visual clarity

    estimated_height = max(sine_amplitude * 10, 10.0)  # At least 10 units
    half_height = estimated_height / 2

    return GraphViewport.symmetric(half_width, half_height)


def compute_auto_viewport(
    x_min: float,
    x_max: float,
    y_values: Sequence[float] | npt.NDArray[np.float64],
    margin_factor: float = 0.1,
    use_percentiles: bool = True,
    symmetric: bool = True,
) -> GraphViewport:
    """
    Compute a viewport that fits the given data with optional margin.

    Uses percentile-based scaling by default to ignore outliers near
    asymptotes, focusing on the typical function behavior. Optionally
    enforces Y-axis symmetry to keep origin (0,0) centered.

    Args:
        x_min: Minimum x value
        x_max: Maximum x value
        y_values: Sequence of y values to fit (can be list or numpy array)
        margin_factor: Fraction of range to add as margin (default 0.1 = 10%)
        use_percentiles: If True, use 2nd and 98th percentiles instead of min/max
                        to ignore outliers (default True)
        symmetric: If True, make Y-axis symmetric around origin (default True)
                  This ensures (0,0) stays centered in the viewport

    Returns:
        GraphViewport that fits the data with margin

    Raises:
        ValueError: If y_values is empty
    """
    # Handle both lists and numpy arrays
    if len(y_values) == 0:
        raise ValueError("Cannot compute viewport for empty y_values")

    # Find y range using percentiles to ignore outliers near asymptotes
    if use_percentiles and len(y_values) > 10:
        # Use 2nd and 98th percentiles to exclude extreme outliers
        # This gives a much better view for functions with asymptotes
        y_min_data = float(np.percentile(y_values, 2))
        y_max_data = float(np.percentile(y_values, 98))
    else:
        # Fall back to min/max for small datasets or when disabled
        y_min_data = float(min(y_values))
        y_max_data = float(max(y_values))

    # Add margin
    y_range = y_max_data - y_min_data
    if y_range == 0:
        # All values are the same, use arbitrary margin
        y_range = 1.0

    y_margin = y_range * margin_factor
    y_min = y_min_data - y_margin
    y_max = y_max_data + y_margin

    # Make Y-axis symmetric around origin if requested
    # This ensures (0,0) stays centered in the graph
    if symmetric:
        y_abs_max = max(abs(y_min), abs(y_max))
        y_min = -y_abs_max
        y_max = y_abs_max

    return GraphViewport(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
