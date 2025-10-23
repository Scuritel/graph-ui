# Quickstart Guide: Function Graph Plotter

**Feature**: 001-function-graph-plotter  
**Date**: 2025-10-23  
**Branch**: `001-function-graph-plotter`

This guide provides step-by-step instructions for setting up the development environment and running the function graph plotter application.

---

## Prerequisites

- **Python**: Version 3.11 or higher
- **pip**: Python package installer (included with Python 3.11+)
- **Git**: For cloning the repository
- **Operating System**: Windows, macOS, or Linux

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd graph-ui
git checkout 001-function-graph-plotter
```

### 2. Create Virtual Environment

Using `venv` (Python's built-in virtual environment):

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` prefix in your terminal prompt indicating the virtual environment is active.

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install Dependencies

**Production dependencies** (required to run the application):
```bash
pip install -r requirements.txt
```

**Development dependencies** (required for testing and development):
```bash
pip install -r requirements-dev.txt
```

### 5. Verify Installation

Check that all dependencies are installed:

```bash
pip list
```

You should see:
- `numpy` >= 1.24.0
- `matplotlib` >= 3.7.0
- `PyQt6` >= 6.5.0 (or skip if using Tkinter fallback)
- `pytest` >= 7.4.0 (dev dependency)
- `flake8`, `black`, `mypy` (dev dependencies)

---

## Running the Application

### Run the Main Application

From the project root directory (with virtual environment activated):

```bash
python -m src.main
```

Or using the launcher script (if created):

```bash
python run.py
```

### Expected Behavior

1. A window opens with minimum size 600x400 pixels
2. Left panel shows:
   - Parameter input fields pre-filled with `a=1, b=1, c=0, d=0`
   - Color picker buttons for graph and axes (defaults: blue graph, black axes)
   - "Start" button at the bottom (enabled since default values are valid)
3. Right/main area shows an empty graph canvas
4. Click "Start" to plot the default function `f(x) = sin(x)` (9 periods displayed)

---

## Development Workflow

### Project Structure

```
graph-ui/
├── .venv/              # Virtual environment (not in git)
├── src/                # Source code
│   ├── main.py         # Entry point
│   ├── ui/             # User interface modules
│   ├── computation/    # Mathematical computation
│   ├── rendering/      # Graph rendering
│   ├── models/         # Data structures
│   └── validation/     # Input validation
├── tests/              # Test suite
│   ├── unit/
│   ├── integration/
│   └── visual/
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── pytest.ini          # Pytest configuration
├── .flake8             # Flake8 linter configuration
├── pyproject.toml      # Black formatter and mypy configuration
└── README.md           # Project overview
```

### Running Tests

**Run all tests**:
```bash
pytest
```

**Run specific test suite**:
```bash
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest tests/visual/         # Visual regression tests only
```

**Run with coverage report**:
```bash
pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` in a browser to view coverage report. Target: 80%+ coverage for `src/computation/`, `src/validation/`, `src/models/`.

**Run specific test file**:
```bash
pytest tests/unit/test_function.py -v
```

### Code Quality Checks

**Linting (flake8)**:
```bash
flake8 src/ tests/
```

**Code Formatting (black)**:
```bash
# Check formatting
black --check src/ tests/

# Auto-format
black src/ tests/
```

**Type Checking (mypy)**:
```bash
mypy src/
```

### Pre-Commit Checklist

Before committing code, run:

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Check types
mypy src/

# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=term
```

All checks should pass before pushing to the repository.

---

## Usage Guide

### Basic Usage

1. **Launch the application** (see "Running the Application" above)
2. **Enter parameters** in the left panel:
   - `a`: Amplitude scalar for sine (default: 1)
   - `b`: Frequency multiplier for sine (default: 1)
   - `c`: Phase shift for sine in radians (default: 0)
   - `d`: Frequency multiplier for tangent (default: 0)
3. **Choose colors** (optional):
   - Click "Graph Color" button to change the function line color
   - Click "Axes Color" button to change X/Y axes color
4. **Click "Start"** to render the graph

### Examples

**Example 1: Pure Sine Wave**
- Parameters: `a=1, b=1, c=0, d=0`
- Result: Classic sine wave with 9 periods

**Example 2: High Frequency Sine**
- Parameters: `a=1, b=2, c=0, d=0`
- Result: Sine wave with doubled frequency (18 oscillations in 9 periods)

**Example 3: Sine + Tangent**
- Parameters: `a=1, b=1, c=0, d=0.5`
- Result: Combined sine and tangent function with asymptotes shown as dashed red lines

**Example 4: Constant Function**
- Parameters: `a=2, b=0, c=0, d=0`
- Result: Horizontal line at `y = 0` (since `sin(0) = 0`)

### Features

- **9 Periods Always**: The graph always shows exactly 9 complete periods of the function
- **Symmetry**: Graph is centered at origin O(0,0) with symmetric X range
- **Auto-Scaling**: Y-axis automatically scales to fit the function values
- **Responsive**: Resize the window - graph updates within 1 second
- **Asymptotes**: Tangent asymptotes shown as semi-transparent red dashed lines
- **Origin Marker**: O(0,0) marked with a visible circle and label
- **Validation**: "Start" button is disabled if any parameter field is empty or invalid

### Troubleshooting

**Issue: "Start" button is grayed out**
- Check all parameter fields have valid numeric values
- Fields cannot be empty
- Values must be between -1000 and 1000

**Issue: Graph looks clipped or distorted**
- This may occur near tangent asymptotes (expected behavior)
- Try reducing the `d` parameter for fewer asymptotes

**Issue: Application crashes on launch**
- Ensure virtual environment is activated: `(.venv)` should appear in terminal prompt
- Verify all dependencies installed: `pip list`
- Check Python version: `python --version` (should be 3.11+)

**Issue: Import errors**
- Make sure you're running from the project root directory
- Run as module: `python -m src.main` (not `python src/main.py`)

---

## Configuration Files

### `requirements.txt`

Production dependencies (minimal, required to run the app):

```txt
numpy>=1.24.0
matplotlib>=3.7.0
PyQt6>=6.5.0
```

### `requirements-dev.txt`

Development dependencies (testing, linting, formatting):

```txt
pytest>=7.4.0
pytest-qt>=4.2.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0
flake8>=6.0.0
black>=23.0.0
mypy>=1.5.0
```

### `pytest.ini`

Pytest configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    visual: Visual regression tests
    slow: Slow-running tests
```

### `.flake8`

Flake8 linter configuration:

```ini
[flake8]
max-line-length = 100
exclude = 
    .venv,
    __pycache__,
    .git,
    build,
    dist
ignore = 
    E203,  # Whitespace before ':' (conflicts with black)
    W503   # Line break before binary operator (conflicts with black)
```

### `pyproject.toml`

Black formatter and mypy configuration:

```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  | .venv
  | __pycache__
)/
'''

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true

[[tool.mypy.overrides]]
module = "matplotlib.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "PyQt6.*"
ignore_missing_imports = true
```

---

## Performance Benchmarks

Expected performance (from Success Criteria):

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Graph render time | < 2 seconds | Time from clicking "Start" to graph displayed |
| Window resize response | < 1 second | Time from resize to updated graph |
| Startup time | < 3 seconds | Time from launch to window displayed |

To run performance benchmarks:

```bash
pytest tests/integration/test_performance.py --benchmark-only
```

---

## Next Steps

1. **Implement core modules**: Start with `src/models/`, then `src/computation/`, then `src/rendering/`, finally `src/ui/`
2. **Write tests alongside code**: Follow test-first approach for mathematical functions
3. **Run CI checks frequently**: Lint, format, type-check, and test after each module
4. **Visual testing**: Generate baseline images for visual regression tests
5. **Performance profiling**: Use `pytest-benchmark` to ensure render times meet targets

For detailed implementation guidance, see:
- `plan.md`: Overall implementation plan
- `research.md`: Technology decisions and algorithms
- `data-model.md`: Data structure specifications
- `contracts/module-contracts.md`: Module interface contracts

---

## Support

For issues or questions:
1. Check this quickstart guide
2. Review `plan.md` and `research.md` for design decisions
3. Check module contracts in `contracts/module-contracts.md`
4. Run tests to verify environment: `pytest tests/unit/`

Happy coding! 🎉
