# Cross-Platform Testing Checklist (T059)

This document guides testing on Windows, macOS, and Linux platforms.

---

## Platform: Windows ✅

**Tested By**: _________________ **Date**: _____________

### System Information
- **OS Version**: Windows _______ (e.g., Windows 11, Windows 10)
- **Python Version**: _______ (should be 3.11+)
- **Shell**: PowerShell / Command Prompt
- **Display Resolution**: _______
- **DPI Scaling**: _______%

### Installation Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Virtual env creation | `python -m venv .venv` | [ ] PASS [ ] FAIL | |
| Virtual env activation | `.\.venv\Scripts\Activate.ps1` | [ ] PASS [ ] FAIL | |
| pip upgrade | `python -m pip install --upgrade pip` | [ ] PASS [ ] FAIL | |
| Install requirements | `pip install -r requirements.txt` | [ ] PASS [ ] FAIL | |
| Install dev requirements | `pip install -r requirements-dev.txt` | [ ] PASS [ ] FAIL | |

### Application Launch Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Launch via module | `python -m src.main` | [ ] PASS [ ] FAIL | |
| Launch via run.ps1 | `.\run.ps1` | [ ] PASS [ ] FAIL | |
| Window opens | Visual check | [ ] PASS [ ] FAIL | |
| No console errors | Check terminal | [ ] PASS [ ] FAIL | |

### Functional Tests

| Feature | Status | Notes |
|---------|--------|-------|
| Parameter input | [ ] PASS [ ] FAIL | |
| Color pickers | [ ] PASS [ ] FAIL | |
| Plot button | [ ] PASS [ ] FAIL | |
| Graph rendering | [ ] PASS [ ] FAIL | |
| Window resize | [ ] PASS [ ] FAIL | |
| Graph toolbar | [ ] PASS [ ] FAIL | |

### Development Tools Tests

| Tool | Command | Status | Notes |
|------|---------|--------|-------|
| pytest | `pytest` | [ ] PASS [ ] FAIL | |
| flake8 | `flake8 src/ tests/` | [ ] PASS [ ] FAIL | |
| mypy | `mypy src/` | [ ] PASS [ ] FAIL | |
| black | `black --check src/ tests/` | [ ] PASS [ ] FAIL | |

### Performance Tests

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Graph render time | < 2s | _______s | [ ] PASS [ ] FAIL |
| Window resize time | < 1s | _______s | [ ] PASS [ ] FAIL |
| Memory usage | Reasonable | _______MB | [ ] PASS [ ] FAIL |

### Windows-Specific Issues

**Known Issues**:
- [ ] None
- [ ] List any Windows-specific problems: _______________________

**Overall Windows Status**: [ ] ✅ PASS [ ] ⚠️ PARTIAL [ ] ❌ FAIL

---

## Platform: macOS ❓

**Tested By**: _________________ **Date**: _____________

### System Information
- **macOS Version**: _______ (e.g., Sonoma 14.x, Ventura 13.x)
- **Python Version**: _______ (should be 3.11+)
- **Shell**: zsh / bash
- **Display**: Retina / Standard
- **Resolution**: _______

### Installation Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Virtual env creation | `python3 -m venv .venv` | [ ] PASS [ ] FAIL | |
| Virtual env activation | `source .venv/bin/activate` | [ ] PASS [ ] FAIL | |
| pip upgrade | `python -m pip install --upgrade pip` | [ ] PASS [ ] FAIL | |
| Install requirements | `pip install -r requirements.txt` | [ ] PASS [ ] FAIL | |
| Install dev requirements | `pip install -r requirements-dev.txt` | [ ] PASS [ ] FAIL | |

### Application Launch Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Launch via module | `python -m src.main` | [ ] PASS [ ] FAIL | |
| Window opens | Visual check | [ ] PASS [ ] FAIL | |
| No console errors | Check terminal | [ ] PASS [ ] FAIL | |

### Functional Tests

| Feature | Status | Notes |
|---------|--------|-------|
| Parameter input | [ ] PASS [ ] FAIL | |
| Color pickers | [ ] PASS [ ] FAIL | |
| Plot button | [ ] PASS [ ] FAIL | |
| Graph rendering | [ ] PASS [ ] FAIL | |
| Window resize | [ ] PASS [ ] FAIL | |
| Graph toolbar | [ ] PASS [ ] FAIL | |
| Retina display scaling | [ ] PASS [ ] FAIL [ ] N/A | High DPI rendering |

### Development Tools Tests

| Tool | Command | Status | Notes |
|------|---------|--------|-------|
| pytest | `pytest` | [ ] PASS [ ] FAIL | |
| flake8 | `flake8 src/ tests/` | [ ] PASS [ ] FAIL | |
| mypy | `mypy src/` | [ ] PASS [ ] FAIL | |
| black | `black --check src/ tests/` | [ ] PASS [ ] FAIL | |

### Performance Tests

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Graph render time | < 2s | _______s | [ ] PASS [ ] FAIL |
| Window resize time | < 1s | _______s | [ ] PASS [ ] FAIL |
| Memory usage | Reasonable | _______MB | [ ] PASS [ ] FAIL |

### macOS-Specific Issues

**Known Issues**:
- [ ] None
- [ ] List any macOS-specific problems: _______________________

**Overall macOS Status**: [ ] ✅ PASS [ ] ⚠️ PARTIAL [ ] ❌ FAIL [ ] ❓ NOT TESTED

---

## Platform: Linux 🐧

**Tested By**: _________________ **Date**: _____________

### System Information
- **Distribution**: _______ (e.g., Ubuntu 22.04, Fedora 39)
- **Desktop Environment**: _______ (GNOME, KDE, XFCE, etc.)
- **Python Version**: _______ (should be 3.11+)
- **Shell**: bash / zsh
- **Display Server**: X11 / Wayland
- **Resolution**: _______

### Installation Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Virtual env creation | `python3 -m venv .venv` | [ ] PASS [ ] FAIL | |
| Virtual env activation | `source .venv/bin/activate` | [ ] PASS [ ] FAIL | |
| pip upgrade | `python -m pip install --upgrade pip` | [ ] PASS [ ] FAIL | |
| Install requirements | `pip install -r requirements.txt` | [ ] PASS [ ] FAIL | |
| Install dev requirements | `pip install -r requirements-dev.txt` | [ ] PASS [ ] FAIL | |
| System dependencies | Qt6 libraries | [ ] PASS [ ] FAIL | May need apt/dnf/pacman |

### Application Launch Tests

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| Launch via module | `python -m src.main` | [ ] PASS [ ] FAIL | |
| Window opens | Visual check | [ ] PASS [ ] FAIL | |
| No console errors | Check terminal | [ ] PASS [ ] FAIL | |
| Wayland compatibility | If using Wayland | [ ] PASS [ ] FAIL [ ] N/A | |

### Functional Tests

| Feature | Status | Notes |
|---------|--------|-------|
| Parameter input | [ ] PASS [ ] FAIL | |
| Color pickers | [ ] PASS [ ] FAIL | |
| Plot button | [ ] PASS [ ] FAIL | |
| Graph rendering | [ ] PASS [ ] FAIL | |
| Window resize | [ ] PASS [ ] FAIL | |
| Graph toolbar | [ ] PASS [ ] FAIL | |
| Font rendering | [ ] PASS [ ] FAIL | Check text clarity |

### Development Tools Tests

| Tool | Command | Status | Notes |
|------|---------|--------|-------|
| pytest | `pytest` | [ ] PASS [ ] FAIL | |
| flake8 | `flake8 src/ tests/` | [ ] PASS [ ] FAIL | |
| mypy | `mypy src/` | [ ] PASS [ ] FAIL | |
| black | `black --check src/ tests/` | [ ] PASS [ ] FAIL | |

### Performance Tests

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Graph render time | < 2s | _______s | [ ] PASS [ ] FAIL |
| Window resize time | < 1s | _______s | [ ] PASS [ ] FAIL |
| Memory usage | Reasonable | _______MB | [ ] PASS [ ] FAIL |

### Linux-Specific Issues

**Known Issues**:
- [ ] None
- [ ] Qt6 platform plugin issues: _______________________
- [ ] Font rendering issues: _______________________
- [ ] Wayland-specific issues: _______________________
- [ ] Other: _______________________

**Overall Linux Status**: [ ] ✅ PASS [ ] ⚠️ PARTIAL [ ] ❌ FAIL [ ] ❓ NOT TESTED

---

## Cross-Platform Summary

### Compatibility Matrix

| Feature | Windows | macOS | Linux | Notes |
|---------|---------|-------|-------|-------|
| Installation | [ ] | [ ] | [ ] | |
| Launch | [ ] | [ ] | [ ] | |
| Parameter input | [ ] | [ ] | [ ] | |
| Color pickers | [ ] | [ ] | [ ] | |
| Graph rendering | [ ] | [ ] | [ ] | |
| Window resize | [ ] | [ ] | [ ] | |
| Performance | [ ] | [ ] | [ ] | |
| Development tools | [ ] | [ ] | [ ] | |

**Legend**: ✅ = Pass, ⚠️ = Partial, ❌ = Fail, ❓ = Not Tested

### Platform-Specific Issues Summary

**Windows**:
- _______________________________________

**macOS**:
- _______________________________________

**Linux**:
- _______________________________________

### Recommendations

1. **Primary Support**: List platforms that are fully supported
   - _______________________________________

2. **Secondary Support**: List platforms with known issues
   - _______________________________________

3. **Documentation Updates**: List any README changes needed
   - _______________________________________

4. **Code Changes**: List any platform-specific fixes needed
   - _______________________________________

---

## Overall Cross-Platform Status

- [ ] ✅ **PASS**: All platforms tested and working
- [ ] ⚠️ **PARTIAL**: Some platforms working, others not tested or have issues
- [ ] ❌ **FAIL**: Critical issues on multiple platforms
- [ ] ❓ **INCOMPLETE**: Testing not complete

**Total Platforms Tested**: ____ / 3
**Total Platforms Passing**: ____ / 3

**Tester Notes**: _______________________________________

**Tester Signature**: _______________ **Date**: ___________
