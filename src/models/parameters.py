"""
Data models for function parameters.

This module defines the FunctionParameters dataclass which holds the
coefficients for the mathematical function f(x) = a*sin(x*b + c) + tan(d*x).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionParameters:
    """
    Immutable parameters for the mathematical function f(x) = a*sin(x*b + c) + tan(d*x).

    Attributes:
        a: Amplitude of the sine component
        b: Frequency multiplier of the sine component
        c: Phase shift of the sine component
        d: Frequency multiplier of the tangent component
    """

    a: float
    b: float
    c: float
    d: float

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        # Validate types
        for field_name, field_value in [
            ("a", self.a),
            ("b", self.b),
            ("c", self.c),
            ("d", self.d),
        ]:
            if not isinstance(field_value, (int, float)):
                raise TypeError(
                    f"Parameter {field_name} must be numeric, got {type(field_value).__name__}"
                )

        # Validate b and d are non-zero (to avoid division by zero in period calculation)
        if self.b == 0:
            raise ValueError("Parameter b cannot be zero (would cause infinite period)")
        if self.d == 0:
            raise ValueError("Parameter d cannot be zero (would cause infinite period)")

    @staticmethod
    def default() -> "FunctionParameters":
        """
        Return default parameters as specified in requirements.

        Returns:
            FunctionParameters with a=1, b=1, c=0, d=0.1
            Note: d is set to 0.1 instead of 0 to avoid division by zero.
        """
        return FunctionParameters(a=1.0, b=1.0, c=0.0, d=0.1)
