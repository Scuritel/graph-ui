# Manual Edge Case Testing (T058)

## Test Date: 2025-01-XX
## Tester: [Name]

This document guides manual testing of edge cases and boundary conditions.

---

## Test Case 1: b=0 (Zero Frequency - Should Error)

**Purpose**: Verify validation prevents division by zero in period calculation

**Steps**:
1. Launch application: `.\run.ps1`
2. Enter parameters: a=1.0, **b=0.0**, c=0.0, d=0.1
3. Click "Plot" or press Enter

**Expected Result**:
- ❌ Validation error displayed
- Error message: "Frequency (b) cannot be zero"
- Graph NOT updated
- Status bar shows error

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 2: d=0 (Zero Vertical Scale - Should Error)

**Purpose**: Verify validation prevents division by zero in function evaluation

**Steps**:
1. Enter parameters: a=1.0, b=1.0, c=0.0, **d=0.0**
2. Click "Plot"

**Expected Result**:
- ❌ Validation error displayed
- Error message: "Vertical scale (d) cannot be zero"
- Graph NOT updated
- Status bar shows error

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 3: Large Amplitude (a=1000 - Should Warn)

**Purpose**: Verify warning for extreme amplitude values

**Steps**:
1. Enter parameters: **a=1000.0**, b=1.0, c=0.0, d=0.1
2. Click "Plot"

**Expected Result**:
- ⚠️ Warning displayed (if implemented)
- Graph still renders successfully
- Y-axis range: approximately [-10000, 10000]
- Performance: render time < 2s

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Render time: _________ seconds
- Notes: ___________________________________________

---

## Test Case 4: Small Frequency (b=0.001 - Should Warn)

**Purpose**: Verify warning for very small frequency values

**Steps**:
1. Enter parameters: a=1.0, **b=0.001**, c=0.0, d=0.1
2. Click "Plot"

**Expected Result**:
- ⚠️ Warning displayed (if implemented)
- Graph renders with very long period
- Multiple periods visible
- Performance: render time < 2s

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Render time: _________ seconds
- Notes: ___________________________________________

---

## Test Case 5: Asymptote Visualization (d=1.0)

**Purpose**: Verify asymptote detection and visualization

**Steps**:
1. Enter parameters: a=1.0, b=1.0, c=0.0, **d=1.0**
2. Click "Plot"
3. Observe vertical dashed lines

**Expected Result**:
- ✅ Graph renders successfully
- Vertical dashed red lines visible at asymptotes
- Function curve has gaps at asymptotes
- Asymptotes at x = π/2 + kπ (k integer)
- Asymptote locations shown in status bar or tooltip

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Number of asymptotes visible: _________
- Asymptote positions: ___________________________________________
- Notes: ___________________________________________

---

## Test Case 6: Negative Amplitude (a=-5.0)

**Purpose**: Verify function works with negative amplitude

**Steps**:
1. Enter parameters: **a=-5.0**, b=1.0, c=0.0, d=0.1
2. Click "Plot"

**Expected Result**:
- ✅ Graph renders successfully
- Function is vertically flipped compared to a=5.0
- Y-axis range: approximately [-50, 50]

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 7: Very High Frequency (b=100.0)

**Purpose**: Verify performance with high-frequency functions

**Steps**:
1. Enter parameters: a=1.0, **b=100.0**, c=0.0, d=0.1
2. Click "Plot"
3. Measure render time

**Expected Result**:
- ✅ Graph renders successfully
- Many oscillations visible
- Performance: render time < 2s
- Graph remains smooth (sufficient sampling)

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Render time: _________ seconds
- Notes: ___________________________________________

---

## Test Case 8: Phase Shift Boundary (c = π)

**Purpose**: Verify phase shift works at π boundary

**Steps**:
1. Enter parameters: a=1.0, b=1.0, **c=3.14159**, d=0.1
2. Click "Plot"

**Expected Result**:
- ✅ Graph renders successfully
- Function shifted by π (half period)
- Equivalent to negative amplitude for sine

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 9: Color Picker Edge Cases

**Purpose**: Verify color selection works correctly

**Steps**:
1. Click each color button:
   - Function color
   - Asymptote color
   - Grid color
   - Background color
2. Try selecting:
   - Same color for multiple elements
   - Very light colors (near white)
   - Very dark colors (near black)
   - High contrast combinations

**Expected Result**:
- ✅ Color picker opens for each button
- Selected color applies immediately
- All color combinations render correctly
- Graph remains readable

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 10: Window Resize Edge Cases

**Purpose**: Verify graph adapts to window size changes

**Steps**:
1. Launch application
2. Plot a function
3. Test resize scenarios:
   - Maximize window
   - Minimize and restore
   - Resize to very small (e.g., 400x300)
   - Resize to very large (e.g., 1920x1080)
   - Rapid resize changes

**Expected Result**:
- ✅ Graph rescales smoothly
- Graph toolbar remains accessible
- No layout breakage
- No performance degradation

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 11: Invalid Input Strings

**Purpose**: Verify input validation handles non-numeric input

**Steps**:
1. Try entering invalid values:
   - Text: "abc"
   - Empty string: ""
   - Special characters: "!@#"
   - Multiple decimals: "1.2.3"
2. Click "Plot"

**Expected Result**:
- ❌ Validation error for each invalid input
- Clear error message indicating which field is invalid
- Focus returns to invalid field
- Graph NOT updated

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Test Case 12: Rapid Parameter Changes

**Purpose**: Verify stability under rapid user input

**Steps**:
1. Rapidly change parameters and click Plot repeatedly
2. Test:
   - Quick Plot button clicks (5-10 times)
   - Enter key spam
   - Parameter changes without plotting
3. Observe for:
   - Memory leaks
   - Performance degradation
   - UI freezing
   - Crash

**Expected Result**:
- ✅ Application remains stable
- Each plot request completes
- No memory buildup
- No UI freezing

**Actual Result**:
- [ ] PASS
- [ ] FAIL
- Notes: ___________________________________________

---

## Summary

**Total Test Cases**: 12
**Passed**: ___ / 12
**Failed**: ___ / 12

**Critical Issues Found**:
1. ___________________________________________
2. ___________________________________________

**Non-Critical Issues Found**:
1. ___________________________________________
2. ___________________________________________

**Overall Assessment**: [ ] PASS [ ] FAIL

**Tester Signature**: _______________ **Date**: ___________
