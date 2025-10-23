# Quickstart Validation Checklist (T057)

This document validates that the actual application matches the quickstart.md documentation.

**Date**: _____________
**Tester**: _____________

---

## Section 1: Prerequisites ✅

| Requirement | Documented | Actual | Status |
|------------|-----------|--------|--------|
| Python 3.11+ | ✅ | ✅ (3.12) | ✅ PASS |
| pip included | ✅ | ✅ | ✅ PASS |
| Git for cloning | ✅ | ✅ | ✅ PASS |
| Windows/macOS/Linux | ✅ | ✅ (Windows) | ✅ PASS |

---

## Section 2: Setup Instructions

### 2.1 Virtual Environment Setup ✅

**Windows PowerShell command documented**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- [ ] Commands work as documented
- [ ] `.venv` folder created
- [ ] `(.venv)` prefix appears in prompt
- **Status**: _______ **Notes**: _______

### 2.2 Dependencies Installation ✅

**Requirements.txt exists**:
- [✅] `requirements.txt` present
- [✅] `requirements-dev.txt` present

**Documented dependencies** (production):
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- PyQt6 >= 6.5.0

**Actual dependencies** (check with `pip list`):
- [ ] numpy version: _______
- [ ] matplotlib version: _______
- [ ] PyQt6 version: _______

**Status**: _______ **Notes**: _______

---

## Section 3: Running the Application

### 3.1 Launch Command ✅

**Documented command**:
```bash
python -m src.main
```

**Alternative** (if launcher script exists):
```bash
python run.py
```

**Tests**:
- [ ] `python -m src.main` works
- [ ] `run.py` exists and works (if created)
- [ ] Application launches without errors

**Actual command used**: _______________________
**Status**: _______ **Notes**: _______

### 3.2 Expected Behavior on Launch

**Quickstart says**:
1. Window opens with minimum size 600x400 pixels
2. Left panel shows:
   - Parameter input fields pre-filled with `a=1, b=1, c=0, d=0`
   - Color picker buttons for graph and axes (defaults: blue graph, black axes)
   - "Start" button at the bottom (enabled since default values are valid)
3. Right/main area shows an empty graph canvas
4. Click "Start" to plot the default function `f(x) = sin(x)` (9 periods displayed)

**Actual behavior**:

| Item | Documented | Actual | Match? |
|------|-----------|--------|--------|
| Window min size | 600x400 | _______ | [ ] YES [ ] NO |
| Default a | 1 | _______ | [ ] YES [ ] NO |
| Default b | 1 | _______ | [ ] YES [ ] NO |
| Default c | 0 | _______ | [ ] YES [ ] NO |
| Default d | 0 | _______ | [ ] YES [ ] NO |
| Default graph color | blue | _______ | [ ] YES [ ] NO |
| Default axes color | black | _______ | [ ] YES [ ] NO |
| "Start" button | At bottom, enabled | _______ | [ ] YES [ ] NO |
| Initial canvas | Empty | _______ | [ ] YES [ ] NO |
| After "Start" click | sin(x), 9 periods | _______ | [ ] YES [ ] NO |

**Discrepancies**: _______________________
**Status**: _______ **Notes**: _______

---

## Section 4: Development Workflow

### 4.1 Project Structure ✅

**Documented structure**:
```
graph-ui/
├── .venv/
├── src/
│   ├── main.py
│   ├── ui/
│   ├── computation/
│   ├── rendering/
│   ├── models/
│   └── validation/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── visual/
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .flake8
├── pyproject.toml
└── README.md
```

**Verify each item exists**:
- [✅] `src/main.py`
- [✅] `src/ui/`
- [✅] `src/computation/`
- [✅] `src/rendering/`
- [✅] `src/models/`
- [✅] `src/validation/`
- [✅] `tests/` (flat structure, not subdivided)
- [✅] `requirements.txt`
- [✅] `requirements-dev.txt`
- [✅] `pytest.ini`
- [✅] `.flake8`
- [✅] `pyproject.toml`
- [✅] `README.md`

**NOTE**: Tests are in flat `tests/` structure, not `tests/unit/`, `tests/integration/`, `tests/visual/`

**Status**: ⚠️ PARTIAL (test structure differs) **Notes**: _______

### 4.2 Running Tests ✅

**Documented commands**:
```bash
pytest
pytest tests/unit/           # Won't work - no subdirs
pytest tests/integration/    # Won't work - no subdirs
pytest tests/visual/         # Won't work - no subdirs
pytest --cov=src --cov-report=html
pytest tests/unit/test_function.py -v  # Won't work
```

**Actual commands that work**:
```bash
pytest
pytest --cov=src --cov-report=html
pytest tests/ -v
pytest tests/test_function.py -v  # If this file exists
```

**Tests**:
- [ ] `pytest` runs all tests
- [ ] Coverage report generates
- [ ] 80%+ coverage on core modules (target from docs)

**Actual coverage**: _______% **Target**: 80%+
**Status**: _______ **Notes**: _______

### 4.3 Code Quality Checks ✅

**Documented commands**:
```bash
flake8 src/ tests/
black --check src/ tests/
black src/ tests/
mypy src/
```

**Tests**:
- [ ] flake8 runs with 0 errors
- [ ] black check passes (already formatted)
- [ ] mypy runs with 0 errors

**Status**: _______ **Notes**: _______

---

## Section 5: Usage Guide

### 5.1 Basic Usage Steps

**Documented steps**:
1. Launch the application
2. Enter parameters in left panel
3. Choose colors (optional)
4. Click "Start" to render

**Test**:
- [ ] All steps work as documented
- [ ] Parameters accept input correctly
- [ ] Color pickers open and work
- [ ] "Start" button triggers render

**Status**: _______ **Notes**: _______

### 5.2 Example Test Cases

**Example 1: Pure Sine Wave**
- Parameters: `a=1, b=1, c=0, d=0`
- Expected: Classic sine wave with 9 periods

**Test**:
- [ ] Enter parameters as documented
- [ ] Click "Start"
- [ ] 9 complete periods visible
- [ ] Classic sine wave shape

**Status**: _______ **Notes**: _______

**Example 2: High Frequency Sine**
- Parameters: `a=1, b=2, c=0, d=0`
- Expected: Doubled frequency (18 oscillations in 9 periods)

**Test**:
- [ ] Enter parameters
- [ ] Click "Start"
- [ ] 18 oscillations visible (9 periods of f(x) = sin(2x))

**Status**: _______ **Notes**: _______

**Example 3: Sine + Tangent**
- Parameters: `a=1, b=1, c=0, d=0.5`
- Expected: Combined function with asymptotes shown as dashed red lines

**Test**:
- [ ] Enter parameters
- [ ] Click "Start"
- [ ] Asymptotes visible as dashed red lines
- [ ] Semi-transparent appearance

**Status**: _______ **Notes**: _______

**Example 4: Constant Function**
- Parameters: `a=2, b=0, c=0, d=0`
- Expected: Horizontal line at `y = 0`

**NOTE**: This example is WRONG in the quickstart!
- `b=0` should trigger validation error (frequency cannot be zero)
- This should fail, not produce a constant function

**Test**:
- [ ] Enter parameters
- [ ] Click "Start"
- [ ] Validation error occurs (expected)
- [ ] Error message: "Frequency (b) cannot be zero"

**Status**: ⚠️ DOCUMENTATION BUG **Notes**: _______

### 5.3 Documented Features

| Feature | Documented | Verified | Status |
|---------|-----------|----------|--------|
| 9 periods always | ✅ | [ ] | _______ |
| Centered at origin | ✅ | [ ] | _______ |
| Auto Y-axis scaling | ✅ | [ ] | _______ |
| Responsive resize | ✅ (<1s) | [ ] | _______ |
| Asymptote visualization | ✅ (red dashed) | [ ] | _______ |
| Origin marker O(0,0) | ✅ | [ ] | _______ |
| Validation (button disable) | ✅ | [ ] | _______ |

**Notes**: _______________________

### 5.4 Troubleshooting Section

**Issue 1: "Start" button grayed out**
- Quickstart says: Check all fields have valid values between -1000 and 1000

**Test**:
- [ ] Empty field grays out button
- [ ] Invalid value grays out button
- [ ] Value < -1000 or > 1000 grays out button
- [ ] Valid values enable button

**Status**: _______ **Notes**: _______

**Issue 2: Graph clipped near asymptotes**
- Quickstart says: Expected behavior near tangent asymptotes

**Test**:
- [ ] Asymptotes cause breaks in curve (expected)
- [ ] Try reducing `d` parameter

**Status**: _______ **Notes**: _______

**Issue 3: Application crashes on launch**
- Quickstart suggests: Check virtual env, dependencies, Python version

**Test**:
- [ ] Application launches successfully (no crash)

**Status**: _______ **Notes**: _______

**Issue 4: Import errors**
- Quickstart says: Run as module `python -m src.main`, not `python src/main.py`

**Test**:
- [ ] `python -m src.main` works
- [ ] Running from project root

**Status**: _______ **Notes**: _______

---

## Section 6: Configuration Files

### 6.1 requirements.txt ✅

**Documented dependencies**:
```
numpy>=1.24.0
matplotlib>=3.7.0
PyQt6>=6.5.0
```

**Actual requirements.txt**:
- [ ] Check file contents match
- [ ] All dependencies present
- [ ] Version constraints correct

**Status**: _______ **Notes**: _______

### 6.2 requirements-dev.txt ✅

**Documented dependencies**:
```
pytest>=7.4.0
pytest-qt>=4.2.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0
```

**Actual requirements-dev.txt**:
- [ ] Check file contents match
- [ ] All dependencies present
- [ ] Version constraints correct

**Status**: _______ **Notes**: _______

---

## Summary

### Overall Validation Results

**Total Checks**: _______ / _______
**Passed**: _______
**Failed**: _______
**Documentation Issues Found**: _______

### Critical Discrepancies

1. **Example 4 (b=0)**: Quickstart claims constant function, but b=0 should error
2. **Test structure**: Docs say `tests/unit/`, `tests/integration/`, `tests/visual/`, actual is flat `tests/`
3. **Other**: _______________________________________

### Recommended Documentation Updates

1. Fix Example 4 - change to valid parameters or document expected error
2. Update test structure documentation to match flat `tests/` layout
3. Clarify "Start" button vs "Plot" button (which is actual name?)
4. Update command examples: `pytest tests/unit/test_function.py` → `pytest tests/test_function.py`
5. Other: _______________________________________

### Conclusion

- [ ] ✅ Application matches quickstart documentation (with noted exceptions)
- [ ] ⚠️ Application mostly matches, minor discrepancies
- [ ] ❌ Significant discrepancies found

**Tester Signature**: _______________ **Date**: ___________
