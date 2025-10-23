"""
Input validation module for the function graph plotter.

This package provides validation logic for user input parameters.
"""

from src.validation.input import (
    ValidationResult,
    validate_all_parameters,
    validate_parameter,
)

__all__ = [
    "ValidationResult",
    "validate_parameter",
    "validate_all_parameters",
]
