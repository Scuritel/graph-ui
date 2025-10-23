"""
UI module for the function graph plotter.

This package contains PyQt6 widgets for the user interface.
"""

from src.ui.graph_canvas import GraphCanvas
from src.ui.input_panel import InputPanel
from src.ui.main_window import MainWindow

__all__ = [
    "MainWindow",
    "InputPanel",
    "GraphCanvas",
]
