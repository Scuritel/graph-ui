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

        # Validate at least one of b or d is non-zero (need a periodic component)
        # AND at least one of a or d is non-zero (need a non-trivial function)
        # Note: c can always be zero
        # - b=0, d≠0: Pure tangent (or constant + tangent if a≠0)
        # - b≠0, d=0: Pure sine (requires a≠0)
        # - b≠0, d≠0: Combined sine + tangent
        # - b=0, d=0: Invalid (no period defined)
        # - a=0, d=0: Invalid (constant zero function)
        if self.b == 0 and self.d == 0:
            raise ValueError(
                "At least one of b or d must be non-zero (need a periodic component)"
            )
        if self.a == 0 and self.d == 0:
            raise ValueError(
                "At least one of a or d must be non-zero (need a non-trivial function)"
            )

    @staticmethod
    def default() -> "FunctionParameters":
        """
        Return default parameters for a pure sine wave.

        Returns:
            FunctionParameters with a=1, b=1, c=0, d=0 (pure sine wave)
        """
        return FunctionParameters(a=1.0, b=1.0, c=0.0, d=0.0)
