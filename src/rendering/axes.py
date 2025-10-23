"""
Axes rendering for the graph.

This module provides functions for rendering coordinate axes with
proper styling and labels.
"""

from matplotlib.axes import Axes

from src.models.viewport import GraphViewport


def render_axes(ax: Axes, viewport: GraphViewport, axes_color: str) -> None:
    """
    Render X and Y axes with labels and styling.

    Draws the coordinate axes, sets viewport limits, and configures
    tick marks and labels.

    Args:
        ax: Matplotlib axes to render on
        viewport: Viewport defining the visible range
        axes_color: Hex color string for axes (e.g., "#000000")
    """
    # Set spine colors (the box around the plot)
    for spine in ax.spines.values():
        spine.set_color(axes_color)
        spine.set_linewidth(1)

    # Set tick colors
    ax.tick_params(axis="both", colors=axes_color, labelsize=8)

    # Move left and bottom spines to zero (create axis arrows through origin)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")

    # Hide top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add arrow-like appearance by setting linewidth
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
