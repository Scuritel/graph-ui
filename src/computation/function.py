"""
Function evaluation for the mathematical expression.

This module evaluates f(x) = a*sin(x*b + c) + tan(d*x) using NumPy
for vectorized computation.
"""

import numpy as np
from numpy.typing import NDArray

from src.models.curve import FunctionCurve
from src.models.parameters import FunctionParameters


def evaluate_function(
    params: FunctionParameters, x_min: float, x_max: float, num_points: int = 1000
) -> FunctionCurve:
    """
    Evaluate f(x) = a*sin(x*b + c) + tan(d*x) over a specified range.

    Uses NumPy vectorized operations for efficient computation. Handles
    asymptotes of the tangent function by clipping extreme values.

    Args:
        params: Function parameters (a, b, c, d)
        x_min: Minimum x value
        x_max: Maximum x value
        num_points: Number of points to evaluate (default 1000)

    Returns:
        FunctionCurve containing x and y arrays

    Raises:
        ValueError: If x_min >= x_max or num_points < 2
    """
    if x_min >= x_max:
        raise ValueError(f"x_min ({x_min}) must be less than x_max ({x_max})")
    if num_points < 2:
        raise ValueError(f"num_points must be at least 2, got {num_points}")

    # Generate x values using linspace for evenly distributed points
    x_values = np.linspace(x_min, x_max, num_points)

    # Evaluate function components using vectorized NumPy operations
    # f(x) = a*sin(x*b + c) + tan(d*x)
    sine_component = params.a * np.sin(x_values * params.b + params.c)
    tan_component = np.tan(params.d * x_values)

    # Combine components
    y_values = sine_component + tan_component

    # Handle asymptotes by detecting discontinuities
    # When tangent jumps from +large to -large (or vice versa), insert NaN
    # This prevents matplotlib from drawing vertical lines
    if params.d != 0:
        # Find large jumps in consecutive y-values (indicates asymptote crossing)
        diff = np.abs(np.diff(y_values))
        # If the difference is huge (more than 2x the typical range), it's an asymptote
        threshold = max(abs(params.a) * 20, 50)  # Threshold for detecting jumps
        asymptote_indices = np.where(diff > threshold)[0]

        # Insert NaN at asymptote locations to break the line
        # Set both points around the discontinuity to NaN for symmetry
        for idx in asymptote_indices:
            y_values[idx] = np.nan
            y_values[idx + 1] = np.nan

    return FunctionCurve(x_values=x_values, y_values=y_values)


def find_asymptotes(
    params: FunctionParameters, x_min: float, x_max: float
) -> NDArray[np.float64]:
    """
    Find x-coordinates of asymptotes in the tangent component within a range.

    Asymptotes occur where d*x = π/2 + n*π for integer n
    (i.e., where cos(d*x) = 0)

    Args:
        params: Function parameters (uses d)
        x_min: Minimum x value
        x_max: Maximum x value

    Returns:
        NumPy array of x-coordinates where asymptotes occur
    """
    if params.d == 0:
        return np.array([])

    # Asymptotes of tan(d*x) occur at d*x = π/2 + n*π
    # Solving for x: x = (π/2 + n*π) / d = π(1/2 + n) / d

    # Find range of n values
    # x_min ≤ π(1/2 + n) / d ≤ x_max
    # Multiply by d/π: d*x_min/π ≤ 1/2 + n ≤ d*x_max/π
    # Subtract 1/2: d*x_min/π - 1/2 ≤ n ≤ d*x_max/π - 1/2

    d = params.d
    if d > 0:
        n_min = int(np.ceil(d * x_min / np.pi - 0.5))
        n_max = int(np.floor(d * x_max / np.pi - 0.5))
    else:  # d < 0
        # Reverse order because d is negative
        n_max = int(np.floor(d * x_min / np.pi - 0.5))
        n_min = int(np.ceil(d * x_max / np.pi - 0.5))

    # Generate asymptote positions
    n_values = np.arange(n_min, n_max + 1)
    asymptote_x = np.pi * (0.5 + n_values) / d

    # Filter to ensure they're actually within [x_min, x_max]
    filtered = asymptote_x[(asymptote_x >= x_min) & (asymptote_x <= x_max)]

    return filtered.astype(np.float64)
