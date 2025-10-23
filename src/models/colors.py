"""
Data models for color settings.

This module defines the ColorSettings dataclass which holds color
preferences for the graph visualization.
"""

from dataclasses import dataclass


@dataclass
class ColorSettings:
    """
    Mutable color settings for graph visualization.

    Attributes:
        function_color: Hex color string for the function curve (e.g., "#0000FF")
        grid_color: Hex color string for the grid lines (e.g., "#000000")
        period_markers_enabled: Whether to show period boundary markers
        period_marker_color: Hex color string for period markers (e.g., "#808080")
        period_marker_alpha: Transparency of period markers (0.0-1.0)
    """

    function_color: str
    grid_color: str
    period_markers_enabled: bool = False
    period_marker_color: str = "#808080"
    period_marker_alpha: float = 0.3

    def __post_init__(self) -> None:
        """Validate color format after initialization."""
        self._validate_hex_color(self.function_color, "function_color")
        self._validate_hex_color(self.grid_color, "grid_color")
        self._validate_hex_color(self.period_marker_color, "period_marker_color")
        self._validate_alpha(self.period_marker_alpha)

    @staticmethod
    def _validate_hex_color(color: str, field_name: str) -> None:
        """
        Validate that a color string is in valid hex format.

        Args:
            color: Color string to validate
            field_name: Name of the field (for error messages)

        Raises:
            ValueError: If color is not a valid hex color string
        """
        if not isinstance(color, str):
            raise TypeError(
                f"{field_name} must be a string, got {type(color).__name__}"
            )

        if not color.startswith("#"):
            raise ValueError(f"{field_name} must start with '#', got: {color}")

        hex_part = color[1:]
        if len(hex_part) != 6:
            raise ValueError(
                f"{field_name} must be 7 characters (#RRGGBB), got: {color}"
            )

        try:
            int(hex_part, 16)
        except ValueError:
            raise ValueError(
                f"{field_name} must contain valid hex digits, got: {color}"
            )

    @staticmethod
    def _validate_alpha(alpha: float) -> None:
        """
        Validate that an alpha value is in valid range.

        Args:
            alpha: Alpha transparency value to validate

        Raises:
            ValueError: If alpha is not in range 0.0-1.0
        """
        if not isinstance(alpha, (int, float)):
            raise TypeError(f"Alpha must be numeric, got {type(alpha).__name__}")

        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Alpha must be in range 0.0-1.0, got: {alpha}")

    @staticmethod
    def default() -> "ColorSettings":
        """
        Return default color settings as specified in requirements.

        Returns:
            ColorSettings with blue function curve (#0000FF) and black grid (#000000)
        """
        return ColorSettings(function_color="#0000FF", grid_color="#000000")
