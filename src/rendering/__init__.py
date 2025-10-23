"""
Rendering module for the function graph plotter.

This package contains matplotlib-based rendering functions for
graphs, axes, and markers.
"""

from src.rendering.axes import render_axes
from src.rendering.graph import (
    render_complete_graph,
    render_function_curve,
    setup_matplotlib_figure,
)
from src.rendering.markers import (
    render_asymptote_lines,
    render_origin_marker,
    render_period_markers,
)

__all__ = [
    "setup_matplotlib_figure",
    "render_function_curve",
    "render_complete_graph",
    "render_axes",
    "render_origin_marker",
    "render_asymptote_lines",
    "render_period_markers",
]
