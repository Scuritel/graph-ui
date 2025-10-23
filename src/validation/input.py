"""
Input validation for function parameters.

This module provides validation logic for user input when entering
function parameters.
"""

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """
    Result of validating a parameter input.

    Attributes:
        is_valid: True if the input is valid
        value: The parsed numeric value (None if invalid)
        error_message: Human-readable error message (None if valid)
    """

    is_valid: bool
    value: Optional[float]
    error_message: Optional[str]

    @staticmethod
    def success(value: float) -> "ValidationResult":
        """Create a successful validation result."""
        return ValidationResult(is_valid=True, value=value, error_message=None)

    @staticmethod
    def error(message: str) -> "ValidationResult":
        """Create a failed validation result."""
        return ValidationResult(is_valid=False, value=None, error_message=message)


def validate_parameter(
    input_str: str, param_name: str, allow_zero: bool = True
) -> ValidationResult:
    """
    Validate a single parameter input string.

    Args:
        input_str: The user input string to validate
        param_name: Name of the parameter (for error messages)
        allow_zero: Whether zero is a valid value (False for b and d)

    Returns:
        ValidationResult indicating success or failure with error message
    """
    # Check for empty input
    if not input_str or input_str.strip() == "":
        return ValidationResult.error(f"{param_name} cannot be empty")

    # Try to parse as float
    try:
        value = float(input_str.strip())
    except ValueError:
        return ValidationResult.error(f"{param_name} must be a valid number")

    # Check for special float values
    if not (-1e308 <= value <= 1e308):
        return ValidationResult.error(f"{param_name} is out of valid range")

    # Check for NaN or infinity
    if math.isnan(value):
        return ValidationResult.error(f"{param_name} cannot be NaN")
    if math.isinf(value):
        return ValidationResult.error(f"{param_name} cannot be infinite")

    # Check zero constraint
    if not allow_zero and value == 0:
        return ValidationResult.error(
            f"{param_name} cannot be zero (would cause infinite period)"
        )

    return ValidationResult.success(value)


def validate_all_parameters(
    a_str: str, b_str: str, c_str: str, d_str: str
) -> tuple[bool, dict[str, Optional[str]]]:
    """
    Validate all four function parameters.

    Args:
        a_str: Input string for parameter a
        b_str: Input string for parameter b
        c_str: Input string for parameter c
        d_str: Input string for parameter d

    Returns:
        Tuple of (all_valid, error_messages_dict)
        - all_valid: True if all parameters are valid
        - error_messages_dict: Dictionary mapping parameter names to error messages
          (None for valid parameters)
    """
    result_a = validate_parameter(a_str, "a", allow_zero=True)
    result_b = validate_parameter(b_str, "b", allow_zero=False)
    result_c = validate_parameter(c_str, "c", allow_zero=True)
    result_d = validate_parameter(d_str, "d", allow_zero=False)

    all_valid = all(
        [result_a.is_valid, result_b.is_valid, result_c.is_valid, result_d.is_valid]
    )

    error_messages = {
        "a": result_a.error_message,
        "b": result_b.error_message,
        "c": result_c.error_message,
        "d": result_d.error_message,
    }

    return all_valid, error_messages
