# Function Graph Plotter

A desktop application for plotting the mathematical function `f(x) = a*sin(x*b + c) + tan(d*x)` with interactive parameter controls and visual customization.

## Features

- **Interactive Plotting**: Adjust parameters `a`, `b`, `c`, `d` in real-time
- **Automatic Scaling**: Graph always displays exactly 9 periods of the combined function
- **Visual Customization**: Customize function curve and grid colors
- **Period Markers**: Optional markers showing the start of each period
- **Responsive UI**: Smooth resizing and real-time validation

## Requirements

- Python 3.11 or higher
- Windows, macOS, or Linux with GUI support

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd graph-ui
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python src/main.py
```

## Development

### Install development dependencies

```bash
pip install -r requirements-dev.txt
```

### Run tests

```bash
pytest
```

### Run linting

```bash
flake8 src tests
black --check src tests
mypy src
```

### Format code

```bash
black src tests
```

## Project Structure

```
graph-ui/
├── src/               # Application source code
│   ├── models/        # Data structures (parameters, viewport, etc.)
│   ├── validation/    # Input validation logic
│   ├── computation/   # Mathematical computations (periods, function eval)
│   ├── rendering/     # Graph rendering (matplotlib)
│   └── ui/            # PyQt6 user interface
├── tests/             # Unit tests
├── requirements.txt   # Production dependencies
└── requirements-dev.txt  # Development dependencies
```

## User Stories

### US1: Basic Function Plotting (P1 - MVP)
Enter parameters → Click "Plot" → Graph appears showing 9 periods centered at origin

### US2: Visual Customization (P2)
Choose function color → Choose grid color → Graph updates with new colors

### US3: Responsive Resize (P2)
Resize window → Graph scales proportionally maintaining aspect ratio

### US4: Period Markers (P3)
Enable period markers → Vertical lines appear at the start of each period

## License

[Your License Here]
