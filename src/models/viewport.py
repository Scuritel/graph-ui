"""
Data models for graph viewport.

This module defines the GraphViewport dataclass which holds the
visible range and transformation information for the graph display.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphViewport:
    """
    Immutable viewport settings for graph rendering.

    Defines the visible range of the graph in mathematical coordinates
    and provides transformation between pixel and math coordinates.

    Attributes:
        x_min: Minimum x-coordinate visible on the graph
        x_max: Maximum x-coordinate visible on the graph
        y_min: Minimum y-coordinate visible on the graph
        y_max: Maximum y-coordinate visible on the graph
    """

    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def __post_init__(self) -> None:
        """Validate viewport bounds after initialization."""
        if self.x_min >= self.x_max:
            raise ValueError(
                f"x_min ({self.x_min}) must be less than x_max ({self.x_max})"
            )
        if self.y_min >= self.y_max:
            raise ValueError(
                f"y_min ({self.y_min}) must be less than y_max ({self.y_max})"
            )

    @property
    def width(self) -> float:
        """Get the width of the viewport in mathematical coordinates."""
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        """Get the height of the viewport in mathematical coordinates."""
        return self.y_max - self.y_min

    @property
    def center_x(self) -> float:
        """Get the x-coordinate of the viewport center."""
        return (self.x_min + self.x_max) / 2

    @property
    def center_y(self) -> float:
        """Get the y-coordinate of the viewport center."""
        return (self.y_min + self.y_max) / 2

    @property
    def aspect_ratio(self) -> float:
        """Get the aspect ratio (width / height) of the viewport."""
        return self.width / self.height

    @staticmethod
    def symmetric(half_width: float, half_height: float) -> "GraphViewport":
        """
        Create a viewport symmetric around the origin (0, 0).

        Args:
            half_width: Distance from center to edge in x-direction
            half_height: Distance from center to edge in y-direction

        Returns:
            GraphViewport centered at origin with specified dimensions
        """
        return GraphViewport(
            x_min=-half_width, x_max=half_width, y_min=-half_height, y_max=half_height
        )
