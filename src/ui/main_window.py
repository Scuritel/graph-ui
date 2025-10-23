"""
Main application window.

This module provides the main PyQt6 window that contains the input
panel and graph canvas.
"""

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QWidget

from src.computation import (
    compute_viewport_for_nine_periods,
    evaluate_function,
)
from src.models.colors import ColorSettings
from src.models.parameters import FunctionParameters
from src.rendering import render_complete_graph
from src.ui.graph_canvas import GraphCanvas
from src.ui.input_panel import InputPanel


class MainWindow(QMainWindow):
    """
    Main application window.

    Contains an input panel on the left and a graph canvas on the right.
    Coordinates parameter input, computation, and graph rendering.
    """

    def __init__(self) -> None:
        super().__init__()
        self._current_params: FunctionParameters | None = None
        self._current_colors = ColorSettings.default()
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._on_resize_finished)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the user interface components."""
        self.setWindowTitle("Function Graph Plotter")
        self.setMinimumSize(QSize(800, 600))

        # Create status bar
        status_bar = self.statusBar()
        if status_bar is not None:
            status_bar.showMessage("Ready - Enter parameters and click Plot Graph")

        # Create central widget with horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Create input panel (left side, fixed width)
        self.input_panel = InputPanel()
        self.input_panel.setFixedWidth(300)
        layout.addWidget(self.input_panel)

        # Create graph canvas (right side, expandable)
        self.graph_canvas = GraphCanvas()
        layout.addWidget(self.graph_canvas, stretch=1)

    def _connect_signals(self) -> None:
        """Connect signal handlers."""
        self.input_panel.parameters_valid.connect(self._on_parameters_changed)
        self.input_panel.start_clicked.connect(self._on_plot_clicked)
        self.input_panel.colors_changed.connect(self._on_colors_changed)

        # Initialize current params with default values
        try:
            self._current_params = self.input_panel.get_parameters()
            self._current_colors = self.input_panel.get_colors()
        except ValueError:
            # If defaults aren't valid, leave as None
            pass

    def _on_parameters_changed(self, params: FunctionParameters) -> None:
        """Handle parameter validation changes."""
        self._current_params = params

    def _on_colors_changed(self, colors: ColorSettings) -> None:
        """Handle color changes."""
        self._current_colors = colors

    def _on_plot_clicked(self) -> None:
        """Handle Plot button click."""
        if self._current_params is None:
            QMessageBox.warning(
                self,
                "Invalid Parameters",
                "Please enter valid parameters before plotting.",
            )
            return

        try:
            self.plot_graph(self._current_params)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate graph: {str(e)}")

    def plot_graph(self, params: FunctionParameters) -> None:
        """
        Generate and display the function graph.

        Orchestrates computation and rendering of the complete graph.

        Args:
            params: Function parameters to plot
        """
        try:
            # Check for extreme parameter values that might cause issues
            if abs(params.a) > 1000:
                QMessageBox.warning(
                    self,
                    "Large Amplitude Warning",
                    f"Amplitude (a={params.a}) is very large. Graph may be difficult to visualize.",
                )

            if abs(params.b) < 0.001 and params.b != 0:
                QMessageBox.warning(
                    self,
                    "Small Frequency Warning",
                    f"Frequency (b={params.b}) is very small. Period will be very large.",
                )

            # Update status bar with function equation
            equation = (
                f"f(x) = {params.a}*sin({params.b}*x + {params.c}) + tan({params.d}*x)"
            )
            status_bar = self.statusBar()
            if status_bar is not None:
                status_bar.showMessage(equation)

            # Compute viewport for 9 periods
            viewport = compute_viewport_for_nine_periods(params)

            # Evaluate function over the viewport range
            curve = evaluate_function(
                params, x_min=viewport.x_min, x_max=viewport.x_max, num_points=1000
            )

            # Use current color settings
            colors = self._current_colors

            # Render the complete graph
            figure = render_complete_graph(
                params=params,
                colors=colors,
                viewport=viewport,
                curve=curve,
                width=8.0,
                height=6.0,
                dpi=100,
            )

            # Update the canvas
            self.graph_canvas.update_graph(figure)

        except Exception as e:
            raise RuntimeError(f"Graph generation failed: {str(e)}") from e

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """
        Handle window resize events.

        Implements debouncing: graph is only recomputed 200ms after
        resize stops to avoid excessive redraws.

        Args:
            event: QResizeEvent
        """
        super().resizeEvent(event)

        # Enforce minimum size (600x400 per spec, but we use 800x600)
        if self.width() < 800 or self.height() < 600:
            return

        # Restart the debounce timer
        self._resize_timer.stop()
        self._resize_timer.start(200)  # 200ms delay

    def _on_resize_finished(self) -> None:
        """Handle resize completion after debounce delay."""
        # Only replot if we have valid parameters and a graph is currently displayed
        if self._current_params is not None and self.graph_canvas.has_graph():
            try:
                self.plot_graph(self._current_params)
            except Exception as e:
                # Silently fail on resize errors to avoid annoying popups
                print(f"Warning: Failed to replot on resize: {e}")
