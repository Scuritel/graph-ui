"""
Unit tests for computation modules.
"""

import math

import numpy as np
import pytest

from src.computation import (
    compute_fundamental_period,
    compute_viewport_for_nine_periods,
    evaluate_function,
    find_asymptotes,
)
from src.models.parameters import FunctionParameters


class TestComputeFundamentalPeriod:
    """Test cases for compute_fundamental_period function."""

    def test_basic_period_calculation(self) -> None:
        """Test period calculation with b=1, d=1."""
        # T_sin = 2π/1 = 2π, T_tan = π/1 = π
        # LCM(2π, π) = 2π
        period = compute_fundamental_period(b=1.0, d=1.0)
        assert abs(period - 2 * math.pi) < 0.01  # Allow small numerical error

    def test_period_with_b_equals_two(self) -> None:
        """Test period calculation with b=2, d=1."""
        # T_sin = 2π/2 = π, T_tan = π/1 = π
        # LCM(π, π) = π
        period = compute_fundamental_period(b=2.0, d=1.0)
        assert abs(period - math.pi) < 0.01

    def test_period_with_negative_b(self) -> None:
        """Test that negative b gives same period as positive."""
        period_pos = compute_fundamental_period(b=2.0, d=1.0)
        period_neg = compute_fundamental_period(b=-2.0, d=1.0)
        assert abs(period_pos - period_neg) < 0.01

    def test_period_with_zero_b_and_nonzero_d(self) -> None:
        """Test that b=0 with d≠0 returns tangent period."""
        # T_tan = π/1 = π (sine is constant)
        period = compute_fundamental_period(b=0.0, d=1.0)
        assert abs(period - math.pi) < 0.01

    def test_period_with_both_zero_raises(self) -> None:
        """Test that b=0 and d=0 raises ValueError."""
        with pytest.raises(ValueError, match="At least one of b or d must be non-zero"):
            compute_fundamental_period(b=0.0, d=0.0)

    def test_period_with_zero_d_returns_sine_period(self) -> None:
        """Test that d=0 returns just the sine period (no tangent)."""
        # T_sin = 2π/1 = 2π (no tangent component)
        period = compute_fundamental_period(b=1.0, d=0.0)
        assert abs(period - 2 * math.pi) < 0.01

    def test_period_with_zero_d_and_b_equals_two(self) -> None:
        """Test that d=0 with b=2 returns π."""
        # T_sin = 2π/2 = π (no tangent component)
        period = compute_fundamental_period(b=2.0, d=0.0)
        assert abs(period - math.pi) < 0.01


class TestEvaluateFunction:
    """Test cases for evaluate_function."""

    def test_basic_evaluation(self) -> None:
        """Test basic function evaluation."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        curve = evaluate_function(params, x_min=-math.pi, x_max=math.pi, num_points=100)

        assert len(curve) == 100
        assert len(curve.x_values) == 100
        assert len(curve.y_values) == 100

    def test_function_at_zero(self) -> None:
        """Test function value at x=0 with simple parameters."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        curve = evaluate_function(params, x_min=-0.01, x_max=0.01, num_points=3)

        # f(0) ≈ sin(0) + tan(0) = 0 + 0 = 0
        # Middle point should be close to zero
        assert abs(curve.y_values[1]) < 0.01

    def test_invalid_x_range(self) -> None:
        """Test that x_min >= x_max raises ValueError."""
        params = FunctionParameters.default()
        with pytest.raises(ValueError, match="x_min .* must be less than x_max"):
            evaluate_function(params, x_min=10.0, x_max=5.0)

    def test_invalid_num_points(self) -> None:
        """Test that num_points < 2 raises ValueError."""
        params = FunctionParameters.default()
        with pytest.raises(ValueError, match="num_points must be at least 2"):
            evaluate_function(params, x_min=0.0, x_max=10.0, num_points=1)

    def test_clipping_near_asymptotes(self) -> None:
        """Test that y-values are clipped to prevent extreme values."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        # Include a range near asymptote at π/2
        curve = evaluate_function(params, x_min=0.0, x_max=math.pi, num_points=1000)

        # All y values should be within reasonable bounds
        assert np.all(np.abs(curve.y_values) <= 1000)


class TestFindAsymptotes:
    """Test cases for find_asymptotes."""

    def test_find_asymptotes_d_equals_one(self) -> None:
        """Test finding asymptotes with d=1."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        asymptotes = find_asymptotes(params, x_min=-2 * math.pi, x_max=2 * math.pi)

        # Asymptotes at x = π/2 + nπ for d=1
        # In range [-2π, 2π], we expect: -3π/2, -π/2, π/2, 3π/2
        assert len(asymptotes) == 4
        expected = np.array(
            [-1.5 * math.pi, -0.5 * math.pi, 0.5 * math.pi, 1.5 * math.pi]
        )
        for asym, exp in zip(asymptotes, expected):
            assert abs(asym - exp) < 0.01

    def test_find_asymptotes_narrow_range(self) -> None:
        """Test finding asymptotes in a narrow range with no asymptotes."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        asymptotes = find_asymptotes(params, x_min=0.0, x_max=0.1)

        # No asymptotes in [0, 0.1]
        assert len(asymptotes) == 0


class TestComputeViewportForNinePeriods:
    """Test cases for compute_viewport_for_nine_periods."""

    def test_viewport_centered_at_origin(self) -> None:
        """Test that viewport is centered at origin."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        viewport = compute_viewport_for_nine_periods(params)

        assert abs(viewport.center_x) < 0.01
        assert abs(viewport.center_y) < 0.01

    def test_viewport_width_for_nine_periods(self) -> None:
        """Test that viewport width contains exactly 9 periods."""
        params = FunctionParameters(a=1.0, b=1.0, c=0.0, d=1.0)
        viewport = compute_viewport_for_nine_periods(params)

        period = compute_fundamental_period(params.b, params.d)
        expected_width = 9 * period

        assert abs(viewport.width - expected_width) < 0.01

    def test_viewport_symmetry(self) -> None:
        """Test that viewport is symmetric around origin."""
        params = FunctionParameters(a=2.0, b=1.5, c=0.5, d=0.5)
        viewport = compute_viewport_for_nine_periods(params)

        assert abs(viewport.x_min + viewport.x_max) < 0.01
        assert abs(viewport.y_min + viewport.y_max) < 0.01
