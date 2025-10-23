"""
Viewport calculation for graph display.

This module computes the appropriate viewport dimensions to display
exactly 9 periods of the function, symmetric around the origin.
"""

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
    x_min: float, x_max: float, y_values: list[float], margin_factor: float = 0.1
) -> GraphViewport:
    """
    Compute a viewport that fits the given data with optional margin.

    Args:
        x_min: Minimum x value
        x_max: Maximum x value
        y_values: List of y values to fit
        margin_factor: Fraction of range to add as margin (default 0.1 = 10%)

    Returns:
        GraphViewport that fits the data with margin

    Raises:
        ValueError: If y_values is empty
    """
    if not y_values:
        raise ValueError("Cannot compute viewport for empty y_values")

    # Find y range
    y_min_data = min(y_values)
    y_max_data = max(y_values)

    # Add margin
    y_range = y_max_data - y_min_data
    if y_range == 0:
        # All values are the same, use arbitrary margin
        y_range = 1.0

    y_margin = y_range * margin_factor
    y_min = y_min_data - y_margin
    y_max = y_max_data + y_margin

    return GraphViewport(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
