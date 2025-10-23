"""
Data models for function curves.

This module defines the FunctionCurve dataclass which holds the
computed data points for rendering a mathematical function.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class FunctionCurve:
    """
    Computed data points for a mathematical function curve.

    Stores arrays of x and y coordinates representing the function
    evaluated over a specific domain.

    Attributes:
        x_values: NumPy array of x-coordinates
        y_values: NumPy array of y-coordinates (f(x))
    """

    x_values: NDArray[np.float64]
    y_values: NDArray[np.float64]

    def __post_init__(self) -> None:
        """Validate curve data after initialization."""
        # Ensure both are NumPy arrays
        if not isinstance(self.x_values, np.ndarray):
            raise TypeError(
                f"x_values must be numpy.ndarray, got {type(self.x_values).__name__}"
            )
        if not isinstance(self.y_values, np.ndarray):
            raise TypeError(
                f"y_values must be numpy.ndarray, got {type(self.y_values).__name__}"
            )

        # Ensure arrays have same length
        if len(self.x_values) != len(self.y_values):
            raise ValueError(
                f"x_values and y_values must have same length, "
                f"got {len(self.x_values)} and {len(self.y_values)}"
            )

        # Ensure arrays are 1-dimensional
        if self.x_values.ndim != 1:
            raise ValueError(
                f"x_values must be 1-dimensional, got {self.x_values.ndim} dimensions"
            )
        if self.y_values.ndim != 1:
            raise ValueError(
                f"y_values must be 1-dimensional, got {self.y_values.ndim} dimensions"
            )

        # Ensure arrays contain floats
        if not np.issubdtype(self.x_values.dtype, np.floating):
            raise TypeError(f"x_values must contain floats, got {self.x_values.dtype}")
        if not np.issubdtype(self.y_values.dtype, np.floating):
            raise TypeError(f"y_values must contain floats, got {self.y_values.dtype}")

    def __len__(self) -> int:
        """Return the number of points in the curve."""
        return len(self.x_values)

    @property
    def is_empty(self) -> bool:
        """Check if the curve has no data points."""
        return len(self) == 0
