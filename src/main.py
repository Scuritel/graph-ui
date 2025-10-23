"""
Function Graph Plotter Application.

A desktop application for plotting the mathematical function
f(x) = a*sin(x*b + c) + tan(d*x) with interactive parameter controls.
"""

import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main() -> int:
    """
    Application entry point.

    Returns:
        Exit code (0 for success)
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Function Graph Plotter")
    app.setOrganizationName("GraphUI")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
