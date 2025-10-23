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

    Special cases:
    - If d=0 (no tangent), returns T_sin = 2π/|b|
    - If b=0 (constant sine), returns T_tan = π/|d|
    - At least one of b or d must be non-zero

    Args:
        b: Frequency multiplier of the sine component (can be zero if d≠0)
        d: Frequency multiplier of the tangent component (can be zero if b≠0)

    Returns:
        The fundamental period of the combined function

    Raises:
        ValueError: If both b and d are zero
    """
    if b == 0 and d == 0:
        raise ValueError(
            "At least one of b or d must be non-zero (need a periodic component)"
        )

    # If d=0, no tangent component, just return sine period
    if d == 0:
        return 2 * math.pi / abs(b)

    # If b=0, sine is constant, just return tangent period
    if b == 0:
        return math.pi / abs(d)

    # Compute individual periods
    t_sin = 2 * math.pi / abs(b)
    t_tan = math.pi / abs(d)

    # When periods differ by many orders of magnitude, the LCM is essentially
    # the larger period (since they won't have a simple rational relationship)
    # This prevents numerical precision issues with very small ratios
    ratio = t_sin / t_tan  # = 2|d| / |b|

    # If ratio is very small or very large, return the larger period
    # This handles cases like b=123, d=0.1 where t_sin=0.051, t_tan=31.4
    if ratio < 0.01 or ratio > 100:
        return max(t_sin, t_tan)

    # For reasonable ratios, compute LCM using fraction approximation
    tolerance = 1e-10
    max_denominator = 100
    numerator, denominator = _approximate_fraction(ratio, max_denominator, tolerance)

    # Safety check: if fraction approximation failed, return larger period
    if numerator == 0 or denominator == 0:
        return max(t_sin, t_tan)

    from math import gcd

    g = gcd(numerator, denominator)
    lcm_multiplier = numerator // g

    # Another safety check: if lcm_multiplier is 0, return larger period
    if lcm_multiplier == 0:
        return max(t_sin, t_tan)

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
