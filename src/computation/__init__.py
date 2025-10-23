"""
Computation module for the function graph plotter.

This package contains mathematical computation functions for period
calculation, function evaluation, and viewport computation.
"""

from src.computation.function import evaluate_function, find_asymptotes
from src.computation.period import compute_fundamental_period
from src.computation.viewport import (
    compute_auto_viewport,
    compute_viewport_for_nine_periods,
)

__all__ = [
    "compute_fundamental_period",
    "evaluate_function",
    "find_asymptotes",
    "compute_viewport_for_nine_periods",
    "compute_auto_viewport",
]
