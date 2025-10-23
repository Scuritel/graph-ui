"""
Performance profiling script for graph rendering.

Tests that graph render time is < 2 seconds as per SC-001.
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.computation import compute_viewport_for_nine_periods, evaluate_function
from src.models.colors import ColorSettings
from src.models.parameters import FunctionParameters
from src.rendering import render_complete_graph


def profile_render_time(params: FunctionParameters, iterations: int = 10) -> dict:
    """
    Profile graph rendering time.

    Args:
        params: Function parameters to test
        iterations: Number of iterations to average

    Returns:
        Dictionary with timing statistics
    """
    times = []

    for i in range(iterations):
        start = time.time()

        # Compute viewport
        viewport = compute_viewport_for_nine_periods(params)

        # Evaluate function
        curve = evaluate_function(
            params, x_min=viewport.x_min, x_max=viewport.x_max, num_points=1000
        )

        # Render graph
        colors = ColorSettings.default()
        _ = render_complete_graph(
            params=params,
            colors=colors,
            viewport=viewport,
            curve=curve,
            width=8.0,
            height=6.0,
            dpi=100,
        )

        end = time.time()
        elapsed = end - start
        times.append(elapsed)

        print(f"Iteration {i + 1}/{iterations}: {elapsed:.4f}s")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    return {"average": avg_time, "min": min_time, "max": max_time, "all_times": times}


def main():
    print("=" * 70)
    print("PERFORMANCE PROFILING: Graph Rendering")
    print("=" * 70)
    print()

    # Test scenarios
    scenarios = [
        ("Default parameters", FunctionParameters.default()),
        ("High frequency sine", FunctionParameters(a=1.0, b=10.0, c=0.0, d=0.1)),
        ("Complex function", FunctionParameters(a=2.0, b=2.5, c=0.5, d=0.7)),
        ("Large amplitude", FunctionParameters(a=100.0, b=1.0, c=0.0, d=0.1)),
    ]

    results = {}

    for name, params in scenarios:
        print(f"\nScenario: {name}")
        print(f"Parameters: a={params.a}, b={params.b}, c={params.c}, d={params.d}")
        print("-" * 70)

        stats = profile_render_time(params, iterations=10)
        results[name] = stats

        print("\nStatistics:")
        print(f"  Average: {stats['average']:.4f}s")
        print(f"  Min:     {stats['min']:.4f}s")
        print(f"  Max:     {stats['max']:.4f}s")

        # Check against SC-001 requirement (<2s)
        if stats["max"] < 2.0:
            print(f"  ✅ PASS: Max time {stats['max']:.4f}s < 2.0s (SC-001)")
        else:
            print(f"  ❌ FAIL: Max time {stats['max']:.4f}s >= 2.0s (SC-001)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_passed = True
    for name, stats in results.items():
        status = "✅ PASS" if stats["max"] < 2.0 else "❌ FAIL"
        print(
            f"{name:30s} Avg: {stats['average']:.4f}s Max: {stats['max']:.4f}s {status}"
        )
        if stats["max"] >= 2.0:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL SCENARIOS PASSED SC-001 (<2s render time)")
    else:
        print("❌ SOME SCENARIOS FAILED SC-001")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
