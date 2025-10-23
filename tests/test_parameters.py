"""
Unit tests for FunctionParameters data model.
"""

import pytest

from src.models.parameters import FunctionParameters


class TestFunctionParameters:
    """Test cases for FunctionParameters dataclass."""

    def test_create_valid_parameters(self) -> None:
        """Test creating parameters with valid values."""
        params = FunctionParameters(a=2.0, b=3.0, c=1.0, d=0.5)
        assert params.a == 2.0
        assert params.b == 3.0
        assert params.c == 1.0
        assert params.d == 0.5

    def test_immutability(self) -> None:
        """Test that parameters are immutable (frozen dataclass)."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        with pytest.raises(AttributeError):
            params.a = 5.0  # type: ignore

    def test_default_parameters(self) -> None:
        """Test default parameter factory method."""
        params = FunctionParameters.default()
        assert params.a == 1.0
        assert params.b == 1.0
        assert params.c == 0.0
        assert params.d == 0.0  # Pure sine wave (no tangent component)

    def test_b_can_be_zero_with_nonzero_d(self) -> None:
        """Test that b=0 is allowed when d≠0 (constant sine + tangent)."""
        params = FunctionParameters(a=1.0, b=0.0, c=1.0, d=1.0)
        assert params.b == 0.0  # Should not raise

    def test_both_b_and_d_zero_raises(self) -> None:
        """Test that b=0 and d=0 raises ValueError."""
        with pytest.raises(ValueError, match="At least one of b or d must be non-zero"):
            FunctionParameters(a=1.0, b=0.0, c=0.0, d=0.0)

    def test_both_a_and_d_zero_raises(self) -> None:
        """Test that a=0 and d=0 raises ValueError (constant zero function)."""
        with pytest.raises(ValueError, match="At least one of a or d must be non-zero"):
            FunctionParameters(a=0.0, b=1.0, c=0.0, d=0.0)

    def test_d_can_be_zero(self) -> None:
        """Test that d=0 is allowed (pure sine wave with a≠0)."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=0.0)
        assert params.d == 0.0  # Should not raise

    def test_a_can_be_zero(self) -> None:
        """Test that a=0 is allowed (pure tangent function)."""
        params = FunctionParameters(a=0.0, b=1.0, c=0.0, d=1.0)
        assert params.a == 0.0  # Should not raise

    def test_negative_values_allowed(self) -> None:
        """Test that negative values are allowed."""
        params = FunctionParameters(a=-2.0, b=-1.0, c=-3.0, d=-0.5)
        assert params.a == -2.0
        assert params.b == -1.0
        assert params.c == -3.0
        assert params.d == -0.5

    def test_integer_values_converted_to_float(self) -> None:
        """Test that integer values are accepted and work correctly."""
        params = FunctionParameters(a=1, b=2, c=3, d=4)
        assert params.a == 1
        assert params.b == 2
        assert params.c == 3
        assert params.d == 4

    def test_type_validation_on_a(self) -> None:
        """Test that non-numeric type for 'a' raises TypeError."""
        with pytest.raises(TypeError, match="Parameter a must be numeric"):
            FunctionParameters(a="not a number", b=1.0, c=0.0, d=1.0)  # type: ignore

    def test_type_validation_on_b(self) -> None:
        """Test that non-numeric type for 'b' raises TypeError."""
        with pytest.raises(TypeError, match="Parameter b must be numeric"):
            FunctionParameters(a=1.0, b="invalid", c=0.0, d=1.0)  # type: ignore
