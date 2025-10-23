"""
Period calculation for mathematical functions.

This module computes the fundamental period of the combined function
f(x) = a*sin(x*b + c) + tan(d*x) using LCM-based approach.
"""

import math


def compute_fundamental_period(b: float, d: float) -> float:
    """
    Compute the fundamental period of f(x) = a*sin(x*b + c) + tan(d*x).

    The sine component has period T_sin = 2π/|b|
    The tangent component has period T_tan = π/|d|
    The combined function has period LCM(T_sin, T_tan)

    Args:
        b: Frequency multiplier of the sine component (must be non-zero)
        d: Frequency multiplier of the tangent component (must be non-zero)

    Returns:
        The fundamental period of the combined function

    Raises:
        ValueError: If b or d is zero
    """
    if b == 0:
        raise ValueError("Parameter b cannot be zero (would cause infinite period)")
    if d == 0:
        raise ValueError("Parameter d cannot be zero (would cause infinite period)")

    # Compute individual periods
    t_sin = 2 * math.pi / abs(b)
    t_tan = math.pi / abs(d)

    # The LCM of two numbers a and b is: LCM(a,b) = a * b / GCD(a,b)
    # For periods that are multiples of π, we can work with the coefficients

    # t_sin = 2π/|b|, t_tan = π/|d|
    # Express as: t_sin = π * (2/|b|), t_tan = π * (1/|d|)

    # LCM(t_sin, t_tan) = π * LCM(2/|b|, 1/|d|)
    # For fractions: LCM(a/b, c/d) = LCM(a,c) / GCD(b,d)

    # So: LCM(2/|b|, 1/|d|) = LCM(2, 1) / GCD(|b|, |d|) = 2 / GCD(|b|, |d|)

    # Therefore: period = π * 2 / GCD(|b|, |d|)

    # But this only works if b and d are integers or have simple rational ratios
    # For general case, we need numeric LCM approximation

    # Use a simpler approach: find smallest k such that k * t_tan is close to a multiple of t_sin
    # This is equivalent to finding LCM

    # Compute ratio
    ratio = t_sin / t_tan  # = 2|d| / |b|

    # Approximate as fraction
    tolerance = 1e-10
    max_denominator = 100
    numerator, denominator = _approximate_fraction(ratio, max_denominator, tolerance)

    # LCM formula: LCM(t_sin, t_tan) = t_sin * denominator / gcd(numerator, denominator)
    # But since ratio = numerator/denominator, we have:
    # t_sin = ratio * t_tan = (numerator/denominator) * t_tan
    # So LCM = t_tan * numerator
    # Actually, let's think more carefully:
    # If ratio = numerator/denominator (simplified), then:
    # t_sin / t_tan = numerator / denominator
    # Therefore: t_sin = t_tan * numerator / denominator
    #
    # LCM(t_sin, t_tan) is the smallest T such that T is a multiple of both
    # T = m * t_sin = n * t_tan for some integers m, n
    # From T = m * t_sin = m * t_tan * numerator / denominator
    # And T = n * t_tan
    # So: m * numerator / denominator = n
    # Therefore: m * numerator = n * denominator
    # Smallest m is: m = denominator / gcd(numerator, denominator)
    # And smallest n is: n = numerator / gcd(numerator, denominator)

    from math import gcd

    g = gcd(numerator, denominator)
    lcm_multiplier = numerator // g

    period = t_tan * lcm_multiplier

    return period


def _approximate_fraction(
    value: float, max_denominator: int, tolerance: float
) -> tuple[int, int]:
    """
    Approximate a floating point value as a fraction using continued fractions.

    Args:
        value: The floating point value to approximate
        max_denominator: Maximum allowed denominator
        tolerance: Acceptable error tolerance

    Returns:
        Tuple of (numerator, denominator) for the best rational approximation
    """
    # Handle edge cases
    if value == 0:
        return (0, 1)

    # Start with continued fraction algorithm
    sign = 1 if value >= 0 else -1
    value = abs(value)

    # Initial approximations (corrected initialization)
    h1, h2 = 1, 0  # Numerators
    k1, k2 = 0, 1  # Denominators

    b = value
    while True:
        a = int(b)

        # Compute next convergent
        h = a * h1 + h2
        k = a * k1 + k2

        # Check if we've exceeded max denominator or achieved tolerance
        if k > max_denominator:
            break

        # Check if we've achieved sufficient accuracy
        if k > 0 and abs(value - h / k) < tolerance:
            return (sign * h, k)

        # Check if value is exactly an integer (b == a exactly)
        remainder = b - a
        if abs(remainder) < 1e-10:
            # Value is very close to an integer, use current convergent
            return (sign * h, k)

        # Prepare for next iteration
        h2, h1 = h1, h
        k2, k1 = k1, k

        # Compute next term
        b = 1 / remainder

        # Safety check for infinite loops
        if abs(b) > 1e6:
            break

    # Return last valid convergent
    return (sign * h1, k1)
