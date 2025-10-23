"""
Axes rendering for the graph.

This module provides functions for rendering coordinate axes with
proper styling, arrow markers, and labels.
"""

from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch

from src.models.viewport import GraphViewport


def render_axes(ax: Axes, viewport: GraphViewport, axes_color: str) -> None:
    """
    Render X and Y axes with arrow markers and labels.

    Draws the coordinate axes through the origin with arrowheads at the ends
    and labels 'X' and 'Y' near the arrows.

    Args:
        ax: Matplotlib axes to render on
        viewport: Viewport defining the visible range
        axes_color: Hex color string for axes (e.g., "#000000")
    """
    # Hide all default spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Set tick colors
    ax.tick_params(axis="both", colors=axes_color, labelsize=8)

    # Calculate arrow positions
    x_min, x_max = viewport.x_min, viewport.x_max
    y_min, y_max = viewport.y_min, viewport.y_max

    # Arrow head properties
    arrow_style = "->"
    arrow_width = 1.5
    arrow_head_width = 8

    # Draw X-axis arrow (from left to right through origin)
    x_arrow = FancyArrowPatch(
        (x_min, 0),
        (x_max, 0),
        arrowstyle=arrow_style,
        color=axes_color,
        linewidth=arrow_width,
        mutation_scale=arrow_head_width,
        zorder=2,
    )
    ax.add_patch(x_arrow)

    # Draw Y-axis arrow (from bottom to top through origin)
    y_arrow = FancyArrowPatch(
        (0, y_min),
        (0, y_max),
        arrowstyle=arrow_style,
        color=axes_color,
        linewidth=arrow_width,
        mutation_scale=arrow_head_width,
        zorder=2,
    )
    ax.add_patch(y_arrow)

    # Add X label near the arrow tip
    x_label_offset = (x_max - x_min) * 0.02  # 2% offset from the edge
    y_label_offset = (y_max - y_min) * 0.02
    ax.text(
        x_max - x_label_offset,
        y_label_offset,
        "X",
        fontsize=12,
        color=axes_color,
        ha="right",
        va="bottom",
        weight="bold",
    )

    # Add Y label near the arrow tip
    ax.text(
        x_label_offset,
        y_max - y_label_offset,
        "Y",
        fontsize=12,
        color=axes_color,
        ha="left",
        va="top",
        weight="bold",
    )
