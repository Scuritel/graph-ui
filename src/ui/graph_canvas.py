"""
Graph canvas widget for displaying matplotlib plots.

This module provides a PyQt6 widget that embeds a matplotlib canvas
for displaying the function graph.
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget


class GraphCanvas(QWidget):
    """
    Widget for displaying matplotlib graphs in PyQt6.

    Embeds a FigureCanvasQTAgg to render matplotlib figures.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._has_graph = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create initial empty figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.canvas)

        # Show placeholder
        self._show_placeholder()

    def _show_placeholder(self) -> None:
        """Show a placeholder message when no graph is displayed."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5,
            0.5,
            'Enter parameters and click "Plot Graph"',
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=14,
            color="gray",
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        self.canvas.draw()

    def update_graph(self, figure: Figure) -> None:
        """
        Update the displayed graph with a new figure.

        Args:
            figure: Matplotlib Figure to display
        """
        # Replace the figure
        self.figure = figure
        self._has_graph = True

        # Remove old canvas
        old_canvas = self.canvas
        layout = self.layout()
        if layout is not None:
            layout.removeWidget(old_canvas)
        old_canvas.deleteLater()

        # Create new canvas with the new figure
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        if layout is not None:
            layout.addWidget(self.canvas)

        # Draw the new figure
        self.canvas.draw()

    def has_graph(self) -> bool:
        """
        Check if a graph is currently displayed.

        Returns:
            True if a graph has been plotted, False if showing placeholder
        """
        return self._has_graph
