"""
Input panel for parameter entry.

This module provides a PyQt6 widget with input fields for the four
function parameters (a, b, c, d) with real-time validation.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QKeyEvent
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from src.models.colors import ColorSettings
from src.models.parameters import FunctionParameters
from src.validation import validate_all_parameters


class InputPanel(QWidget):
    """
    Input panel widget for entering function parameters.

    Provides four text fields for parameters a, b, c, d with:
    - Pre-filled default values (1, 1, 0, 0.1)
    - Real-time validation
    - Enabled/disabled Start button based on validation
    - Color pickers for graph line and axes colors

    Signals:
        parameters_valid: Emitted when all parameters are valid (passes FunctionParameters)
        start_clicked: Emitted when Start button is clicked
        colors_changed: Emitted when colors are changed (passes ColorSettings)
    """

    parameters_valid = pyqtSignal(FunctionParameters)
    start_clicked = pyqtSignal()
    colors_changed = pyqtSignal(ColorSettings)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Initialize color settings
        self._color_settings = ColorSettings.default()

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the user interface components."""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Function Parameters")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)

        # Parameter form
        form_layout = QFormLayout()

        # Create input fields with default values
        # Default: pure sine wave (a=1, b=1, c=0, d=0)
        self.input_a = QLineEdit("1.0")
        self.input_a.setToolTip("Amplitude of sine wave (can be 0 for pure tangent)")

        self.input_b = QLineEdit("1.0")
        self.input_b.setToolTip(
            "Frequency of sine wave (can be 0 for constant sine offset)"
        )

        self.input_c = QLineEdit("0.0")
        self.input_c.setToolTip("Phase shift in radians (can be 0)")

        self.input_d = QLineEdit("0.0")
        self.input_d.setToolTip(
            "Frequency of tangent component (can be 0 for pure sine)"
        )

        # Add to form
        form_layout.addRow("a (amplitude):", self.input_a)
        form_layout.addRow("b (frequency):", self.input_b)
        form_layout.addRow("c (phase):", self.input_c)
        form_layout.addRow("d (tan frequency):", self.input_d)

        layout.addLayout(form_layout)

        # Add helpful hint
        hint_label = QLabel(
            "💡 Tips:\n"
            "• Pure sine: set d=0\n"
            "• Pure tangent: set a=0, b=1\n"
            "• Constant offset: set b=0 (e.g., sin(1) + tan(x): a=1, b=0, c=1, d=1)"
        )
        hint_label.setStyleSheet(
            "color: #0066cc; font-size: 9pt; margin-top: 5px; "
            "background-color: #e6f2ff; padding: 8px; border-radius: 4px;"
        )
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        # Color pickers section
        color_section = QLabel("Colors")
        color_section.setStyleSheet(
            "font-weight: bold; font-size: 11pt; margin-top: 10px;"
        )
        layout.addWidget(color_section)

        # Graph color picker
        graph_color_layout = QHBoxLayout()
        graph_color_label = QLabel("Graph Line:")
        self.graph_color_button = QPushButton()
        self.graph_color_button.setFixedSize(80, 30)
        self._update_color_button(
            self.graph_color_button, self._color_settings.function_color
        )
        graph_color_layout.addWidget(graph_color_label)
        graph_color_layout.addWidget(self.graph_color_button)
        graph_color_layout.addStretch()
        layout.addLayout(graph_color_layout)

        # Axes color picker
        axes_color_layout = QHBoxLayout()
        axes_color_label = QLabel("Axes/Grid:")
        self.axes_color_button = QPushButton()
        self.axes_color_button.setFixedSize(80, 30)
        self._update_color_button(
            self.axes_color_button, self._color_settings.grid_color
        )
        axes_color_layout.addWidget(axes_color_label)
        axes_color_layout.addWidget(self.axes_color_button)
        axes_color_layout.addStretch()
        layout.addLayout(axes_color_layout)

        # Period markers section
        period_section = QLabel("Period Markers")
        period_section.setStyleSheet(
            "font-weight: bold; font-size: 11pt; margin-top: 10px;"
        )
        layout.addWidget(period_section)

        # Enable/disable checkbox
        self.period_markers_checkbox = QCheckBox("Show Period Markers")
        self.period_markers_checkbox.setChecked(False)
        layout.addWidget(self.period_markers_checkbox)

        # Period marker color picker
        period_color_layout = QHBoxLayout()
        period_color_label = QLabel("Marker Color:")
        self.period_color_button = QPushButton()
        self.period_color_button.setFixedSize(80, 30)
        self._update_color_button(
            self.period_color_button, self._color_settings.period_marker_color
        )
        self.period_color_button.setEnabled(False)  # Initially disabled
        period_color_layout.addWidget(period_color_label)
        period_color_layout.addWidget(self.period_color_button)
        period_color_layout.addStretch()
        layout.addLayout(period_color_layout)

        # Period marker alpha slider
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Transparency:")
        self.period_alpha_slider = QSlider()
        self.period_alpha_slider.setOrientation(Qt.Orientation.Horizontal)
        self.period_alpha_slider.setMinimum(0)
        self.period_alpha_slider.setMaximum(100)
        self.period_alpha_slider.setValue(
            int(self._color_settings.period_marker_alpha * 100)
        )
        self.period_alpha_slider.setEnabled(False)  # Initially disabled
        self.period_alpha_label_value = QLabel(
            f"{self._color_settings.period_marker_alpha:.2f}"
        )
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.period_alpha_slider)
        alpha_layout.addWidget(self.period_alpha_label_value)
        layout.addLayout(alpha_layout)

        # Validation status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: red; font-size: 9pt;")
        layout.addWidget(self.status_label)

        # Start button
        self.start_button = QPushButton("Plot Graph")
        self.start_button.setEnabled(True)  # Initially enabled with valid defaults
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        layout.addWidget(self.start_button)

        # Add stretch to push everything to top
        layout.addStretch()

    def _connect_signals(self) -> None:
        """Connect signal handlers."""
        # Validate on text change
        self.input_a.textChanged.connect(self._validate_inputs)
        self.input_b.textChanged.connect(self._validate_inputs)
        self.input_c.textChanged.connect(self._validate_inputs)
        self.input_d.textChanged.connect(self._validate_inputs)

        # Start button click
        self.start_button.clicked.connect(self._on_start_clicked)

        # Color picker buttons
        self.graph_color_button.clicked.connect(self._on_graph_color_clicked)
        self.axes_color_button.clicked.connect(self._on_axes_color_clicked)

        # Period marker controls
        self.period_markers_checkbox.stateChanged.connect(
            self._on_period_markers_toggled
        )
        self.period_color_button.clicked.connect(self._on_period_color_clicked)
        self.period_alpha_slider.valueChanged.connect(self._on_period_alpha_changed)

        # Initial validation
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate all input fields and update UI state."""
        a_text = self.input_a.text()
        b_text = self.input_b.text()
        c_text = self.input_c.text()
        d_text = self.input_d.text()

        # Validate all parameters
        all_valid, errors = validate_all_parameters(a_text, b_text, c_text, d_text)

        if all_valid:
            # All inputs valid
            self.start_button.setEnabled(True)
            self.status_label.setText("")

            # Create FunctionParameters and emit signal
            try:
                params = FunctionParameters(
                    a=float(a_text), b=float(b_text), c=float(c_text), d=float(d_text)
                )
                self.parameters_valid.emit(params)
            except (ValueError, TypeError) as e:
                # Shouldn't happen if validation passed, but handle gracefully
                self.start_button.setEnabled(False)
                self.status_label.setText(f"Error: {str(e)}")
        else:
            # Some inputs invalid
            self.start_button.setEnabled(False)

            # Show first error message
            error_msgs = [msg for msg in errors.values() if msg is not None]
            if error_msgs:
                self.status_label.setText(error_msgs[0])
            else:
                self.status_label.setText("")

    def _on_start_clicked(self) -> None:
        """Handle Start button click."""
        self.start_clicked.emit()

    def get_parameters(self) -> FunctionParameters:
        """
        Get current parameters if valid.

        Returns:
            FunctionParameters with current values

        Raises:
            ValueError: If current parameters are invalid
        """
        a_text = self.input_a.text()
        b_text = self.input_b.text()
        c_text = self.input_c.text()
        d_text = self.input_d.text()

        all_valid, errors = validate_all_parameters(a_text, b_text, c_text, d_text)

        if not all_valid:
            error_msgs = [msg for msg in errors.values() if msg is not None]
            raise ValueError(f"Invalid parameters: {', '.join(error_msgs)}")

        return FunctionParameters(
            a=float(a_text), b=float(b_text), c=float(c_text), d=float(d_text)
        )

    def get_colors(self) -> ColorSettings:
        """
        Get current color settings.

        Returns:
            ColorSettings with current color values
        """
        return self._color_settings

    def _update_color_button(self, button: QPushButton, hex_color: str) -> None:
        """
        Update a color button's appearance to show the selected color.

        Args:
            button: The button to update
            hex_color: Hex color string (e.g., "#0000FF")
        """
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                border: 2px solid #333333;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                border: 2px solid #666666;
            }}
        """)

    def _on_graph_color_clicked(self) -> None:
        """Handle graph color picker button click."""
        # Parse current color
        current_color = QColor(self._color_settings.function_color)

        # Show color dialog
        color = QColorDialog.getColor(current_color, self, "Select Graph Line Color")

        if color.isValid():
            # Update color settings
            hex_color = color.name()  # Returns "#RRGGBB"
            self._color_settings.function_color = hex_color

            # Update button appearance
            self._update_color_button(self.graph_color_button, hex_color)

            # Emit color changed signal
            self.colors_changed.emit(self._color_settings)

    def _on_axes_color_clicked(self) -> None:
        """Handle axes color picker button click."""
        # Parse current color
        current_color = QColor(self._color_settings.grid_color)

        # Show color dialog
        color = QColorDialog.getColor(current_color, self, "Select Axes/Grid Color")

        if color.isValid():
            # Update color settings
            hex_color = color.name()  # Returns "#RRGGBB"
            self._color_settings.grid_color = hex_color

            # Update button appearance
            self._update_color_button(self.axes_color_button, hex_color)

            # Emit color changed signal
            self.colors_changed.emit(self._color_settings)

    def _on_period_markers_toggled(self, state: int) -> None:
        """Handle period markers checkbox toggle."""
        enabled = state == Qt.CheckState.Checked.value

        # Update color settings
        self._color_settings.period_markers_enabled = enabled

        # Enable/disable related controls
        self.period_color_button.setEnabled(enabled)
        self.period_alpha_slider.setEnabled(enabled)

        # Emit color changed signal
        self.colors_changed.emit(self._color_settings)

    def _on_period_color_clicked(self) -> None:
        """Handle period marker color picker button click."""
        # Parse current color
        current_color = QColor(self._color_settings.period_marker_color)

        # Show color dialog
        color = QColorDialog.getColor(current_color, self, "Select Period Marker Color")

        if color.isValid():
            # Update color settings
            hex_color = color.name()  # Returns "#RRGGBB"
            self._color_settings.period_marker_color = hex_color

            # Update button appearance
            self._update_color_button(self.period_color_button, hex_color)

            # Emit color changed signal
            self.colors_changed.emit(self._color_settings)

    def _on_period_alpha_changed(self, value: int) -> None:
        """Handle period marker alpha slider change."""
        # Convert 0-100 to 0.0-1.0
        alpha = value / 100.0

        # Update color settings
        self._color_settings.period_marker_alpha = alpha

        # Update label
        self.period_alpha_label_value.setText(f"{alpha:.2f}")

        # Emit color changed signal
        self.colors_changed.emit(self._color_settings)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """Handle key press events."""
        if event is None:
            return
        # Trigger plot on Enter/Return key
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.start_button.isEnabled():
                self._on_start_clicked()
        else:
            super().keyPressEvent(event)
