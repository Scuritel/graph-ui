"""
Graph rendering using Matplotlib.

This module provides functions for setting up and rendering the complete
function graph with matplotlib.
"""

from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.models.colors import ColorSettings
from src.models.curve import FunctionCurve
from src.models.parameters import FunctionParameters
from src.models.viewport import GraphViewport


def setup_matplotlib_figure(
    width: float, height: float, dpi: int = 100
) -> Tuple[Figure, Axes]:
    """
    Create a matplotlib Figure and Axes with specified dimensions.

    Args:
        width: Figure width in inches
        height: Figure height in inches
        dpi: Dots per inch for high-DPI support (default 100)

    Returns:
        Tuple of (Figure, Axes) ready for plotting
    """
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_subplot(111)
    return fig, ax


def render_function_curve(ax: Axes, curve: FunctionCurve, graph_color: str) -> None:
    """
    Render the function curve on the given axes.

    Args:
        ax: Matplotlib axes to plot on
        curve: FunctionCurve containing x and y data
        graph_color: Hex color string for the curve (e.g., "#0000FF")
    """
    # Convert hex color to RGB tuple (matplotlib accepts both formats)
    ax.plot(
        curve.x_values, curve.y_values, color=graph_color, linewidth=2, label="f(x)"
    )


def render_complete_graph(
    params: FunctionParameters,
    colors: ColorSettings,
    viewport: GraphViewport,
    curve: FunctionCurve,
    width: float = 8.0,
    height: float = 6.0,
    dpi: int = 100,
) -> Figure:
    """
    Render a complete graph with all elements.

    Orchestrates the rendering of axes, origin marker, function curve,
    and asymptote lines into a single matplotlib Figure.

    Args:
        params: Function parameters
        colors: Color settings for graph elements
        viewport: Viewport defining visible range
        curve: Pre-computed function curve data
        width: Figure width in inches (default 8.0)
        height: Figure height in inches (default 6.0)
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Matplotlib Figure containing the complete graph
    """
    # Import rendering functions (avoid circular imports)
    from src.computation.period import compute_fundamental_period
    from src.rendering.axes import render_axes
    from src.rendering.markers import render_origin_marker, render_period_markers

    # Setup figure and axes
    fig, ax = setup_matplotlib_figure(width, height, dpi)

    # Set viewport limits
    ax.set_xlim(viewport.x_min, viewport.x_max)
    ax.set_ylim(viewport.y_min, viewport.y_max)

    # Render axes with grid
    render_axes(ax, viewport, colors.grid_color)

    # Render origin marker
    render_origin_marker(ax)

    # Render period markers if enabled
    if colors.period_markers_enabled:
        period = compute_fundamental_period(params.b, params.d)
        render_period_markers(
            ax=ax,
            period=period,
            num_periods=9,
            viewport=viewport,
            color=colors.period_marker_color,
            alpha=colors.period_marker_alpha,
        )

    # Render function curve
    render_function_curve(ax, curve, colors.function_color)

    # Add title and labels
    ax.set_title(
        f"f(x) = {params.a}*sin({params.b}*x + {params.c}) + tan({params.d}*x)",
        fontsize=10,
    )
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("f(x)", fontsize=10)

    # Enable grid
    ax.grid(True, alpha=0.3, color=colors.grid_color)

    # Tight layout to prevent label cutoff
    fig.tight_layout()

    return fig
