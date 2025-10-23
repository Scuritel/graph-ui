"""
Marker rendering for special points and lines.

This module provides functions for rendering origin markers,
period markers, and asymptote lines.
"""

import numpy as np
from matplotlib.axes import Axes
from numpy.typing import NDArray

from src.models.viewport import GraphViewport


def render_origin_marker(ax: Axes, marker_size: int = 8) -> None:
    """
    Render a marker at the origin (0, 0).

    Args:
        ax: Matplotlib axes to render on
        marker_size: Size of the marker in points (default 8)
    """
    ax.plot(
        0,
        0,
        "ko",
        markersize=marker_size,
        markerfacecolor="red",
        markeredgecolor="black",
        markeredgewidth=1,
        zorder=5,
        label="Origin",
    )


def render_asymptote_lines(
    ax: Axes, asymptote_positions: NDArray[np.float64], alpha: float = 0.3
) -> None:
    """
    Render vertical asymptote lines.

    Draws semi-transparent vertical lines at positions where the
    tangent function has asymptotes.

    Args:
        ax: Matplotlib axes to render on
        asymptote_positions: Array of x-coordinates for asymptotes
        alpha: Transparency level (0=invisible, 1=opaque, default 0.3)
    """
    for x_pos in asymptote_positions:
        ax.axvline(
            x=x_pos, color="red", linestyle="--", linewidth=1, alpha=alpha, zorder=1
        )


def render_period_markers(
    ax: Axes,
    period: float,
    num_periods: int,
    viewport: GraphViewport,
    color: str,
    alpha: float,
) -> None:
    """
    Render vertical lines marking period boundaries.

    Draws semi-transparent vertical lines at the start of each period
    to help visualize the periodic nature of the function.

    Args:
        ax: Matplotlib axes to render on
        period: Fundamental period of the function
        num_periods: Number of periods being displayed (typically 9)
        viewport: Viewport defining the y-range for lines
        color: Hex color string for markers (e.g., "#808080")
        alpha: Transparency level (0.0-1.0)
    """
    # Calculate period boundary positions
    # Start from the leftmost period boundary visible in viewport
    # Generate positions: -4T, -3T, -2T, -T, 0, T, 2T, 3T, 4T for 9 periods
    for i in range(-num_periods // 2, num_periods // 2 + 1):
        x_pos = i * period
        if viewport.x_min <= x_pos <= viewport.x_max:
            ax.axvline(
                x=x_pos,
                color=color,
                linestyle="-",
                linewidth=1.5,
                alpha=alpha,
                zorder=2,
            )
