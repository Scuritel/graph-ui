# Tasks: Function Graph Plotter

**Input**: Design documents from `/specs/001-function-graph-plotter/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/module-contracts.md  
**Feature Branch**: `001-function-graph-plotter`

**Tests**: Tests are OPTIONAL for this feature. Test tasks are NOT included since the specification focuses on rapid prototyping and visual validation. Unit tests can be added incrementally after initial implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Single desktop application structure:
- `src/` - Source code
- `tests/` - Tests (optional)
- Repository root configuration files

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and Python environment setup

- [X] T001 Create project directory structure: src/, src/models/, src/validation/, src/computation/, src/rendering/, src/ui/, tests/
- [X] T002 Create Python virtual environment: python -m venv .venv
- [X] T003 [P] Install production dependencies: pip install numpy>=1.24.0 matplotlib>=3.7.0 PyQt6>=6.5.0
- [X] T004 [P] Install development dependencies: pip install pytest>=7.4.0 pytest-qt>=4.2.0 flake8>=6.0.0 black>=23.0.0 mypy>=1.5.0
- [X] T005 [P] Create .gitignore with Python patterns (.venv/, __pycache__/, *.pyc, .pytest_cache/, .mypy_cache/)
- [X] T006 [P] Configure linting: Create setup.cfg or pyproject.toml with flake8 and mypy rules
- [X] T007 [P] Create README.md with project description and quickstart instructions from specs/001-function-graph-plotter/quickstart.md

---

## Phase 2: Foundational (Data Models & Core Infrastructure) ✅ COMPLETE

**Purpose**: Core data structures and validation that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Create FunctionParameters dataclass in src/models/parameters.py (a, b, c, d with defaults 1, 1, 0, 0 and validation)
- [X] T009 [P] Create ColorSettings dataclass in src/models/colors.py (graph_color=#0000FF, axes_color=#000000, period markers with alpha)
- [X] T010 [P] Create GraphViewport dataclass in src/models/viewport.py (x_min, x_max, y_min, y_max, width, height, to_screen_coords method)
- [X] T011 [P] Create FunctionCurve dataclass in src/models/curve.py (x_values, y_values, asymptote_positions arrays)
- [X] T012 [P] Implement validate_parameter() in src/validation/input.py (returns ValidationResult with is_valid, value, error_message)
- [X] T013 Implement validate_all_parameters() in src/validation/input.py (uses validate_parameter for a, b, c, d)
- [X] T014 [P] Create src/__init__.py and src/models/__init__.py package files

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel ✅

---

## Phase 3: User Story 1 - Basic Function Plotting (Priority: P1) 🎯 MVP ✅ COMPLETE

**Goal**: Display a mathematical function graph with 9 periods, proper axes, and origin marker

**Independent Test**: Launch application with default parameters (a=1, b=1, c=0, d=0), click Start button, verify sine wave displays with 9 complete periods centered around O(0,0) with labeled axes and origin marker

### Implementation for User Story 1

**Step 1: Period Calculation (Mathematical Foundation)**

- [X] T015 [P] [US1] Implement compute_fundamental_period(b, d) in src/computation/period.py (handles b=0, d=0, LCM algorithm per research.md)
- [X] T016 [P] [US1] Implement compute_display_range(period, num_periods=9) in src/computation/period.py (returns symmetric x_min, x_max)

**Step 2: Function Evaluation**

- [X] T017 [US1] Implement evaluate_function(params, x_array) in src/computation/function.py (NumPy vectorized: a*sin(x*b + c) + tan(d*x))
- [X] T018 [US1] Implement detect_asymptotes(d, x_min, x_max) in src/computation/function.py (finds vertical asymptotes where cos(d*x) ≈ 0)
- [X] T019 [US1] Implement compute_function_curve(params, viewport) in src/computation/function.py (orchestrates period calc, sampling, evaluation, asymptote detection)

**Step 3: Viewport Calculation**

- [X] T020 [US1] Implement compute_viewport(params, canvas_width, canvas_height) in src/computation/viewport.py (creates GraphViewport with 9-period x-range, auto-scaled y-range)
- [X] T021 [US1] Implement auto_scale_y_axis(y_values) in src/computation/viewport.py (finds y_min, y_max with 10% padding, handles clipping for asymptotes)

**Step 4: Graph Rendering**

- [X] T022 [P] [US1] Implement setup_matplotlib_figure(width, height, dpi) in src/rendering/graph.py (creates Figure and Axes with high-DPI support)
- [X] T023 [P] [US1] Implement render_axes(ax, viewport, axes_color) in src/rendering/axes.py (draws X/Y axes with labels, tick marks, arrows)
- [X] T024 [P] [US1] Implement render_origin_marker(ax, marker_size=8) in src/rendering/markers.py (draws circle/dot at O(0,0))
- [X] T025 [US1] Implement render_function_curve(ax, curve, graph_color) in src/rendering/graph.py (plots x_values, y_values with specified color)
- [X] T026 [US1] Implement render_asymptote_lines(ax, asymptote_positions, viewport, alpha=0.3) in src/rendering/markers.py (draws semi-transparent vertical lines)
- [X] T027 [US1] Implement render_complete_graph(params, colors, viewport) in src/rendering/graph.py (orchestrates all rendering steps, returns matplotlib Figure)

**Step 5: User Interface**

- [X] T028 [US1] Create MainWindow class in src/ui/main_window.py (QMainWindow with 600x400 minimum size, split layout: left panel + graph canvas)
- [X] T029 [US1] Create InputPanel widget in src/ui/input_panel.py (QWidget with 4 QLineEdit fields for a/b/c/d, pre-filled with defaults, real-time validation)
- [X] T030 [US1] Implement validation_changed signal/slot in src/ui/input_panel.py (emits all_valid boolean when any field changes)
- [X] T031 [US1] Add Start button to InputPanel in src/ui/input_panel.py (QPushButton at bottom, enabled/disabled based on validation)
- [X] T032 [US1] Create GraphCanvas widget in src/ui/graph_canvas.py (QWidget with FigureCanvasQTAgg embedding, update_graph(figure) method)
- [X] T033 [US1] Connect Start button clicked → plot_graph() in src/ui/main_window.py (reads params, computes graph, updates canvas)
- [X] T034 [US1] Create application entry point in src/main.py (QApplication, show MainWindow, sys.exit)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can plot basic function with 9 periods ✅ **VERIFIED - APPLICATION RUNS SUCCESSFULLY**

---

## Phase 4: User Story 2 - Visual Customization (Priority: P2) ✅ COMPLETE

**Goal**: Enable users to customize graph line and axes colors using color pickers

**Independent Test**: Launch application, open color pickers for graph line and axes, select custom colors (e.g., red graph, blue axes), click Start, verify colors are applied correctly

### Implementation for User Story 2

- [X] T035 [P] [US2] Add graph_color_picker (QColorDialog button) to InputPanel in src/ui/input_panel.py (default blue #0000FF)
- [X] T036 [P] [US2] Add axes_color_picker (QColorDialog button) to InputPanel in src/ui/input_panel.py (default black #000000)
- [X] T037 [US2] Implement color_changed signal in src/ui/input_panel.py (emits ColorSettings when either picker changes)
- [X] T038 [US2] Update plot_graph() in src/ui/main_window.py to read ColorSettings from InputPanel and pass to render_complete_graph()
- [X] T039 [US2] Update render_function_curve() and render_axes() to use ColorSettings.to_rgb_tuple() for matplotlib color conversion

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently ✅

---

## Phase 5: User Story 4 - Responsive Window Resizing (Priority: P2) ✅ COMPLETE

**Goal**: Maintain 9 periods and symmetry when window is resized

**Independent Test**: Plot a function, resize window horizontally and vertically (staying above 600x400), verify graph rescales to maintain 9 periods centered at origin

### Implementation for User Story 4

- [X] T040 [US4] Implement resizeEvent handler in src/ui/main_window.py (enforces 600x400 minimum size)
- [X] T041 [US4] Add resize timer/debouncing in src/ui/main_window.py (delays graph recompute until 200ms after resize stops)
- [X] T042 [US4] Connect resize event → recompute_and_render() in src/ui/main_window.py (updates viewport dimensions, triggers plot_graph if parameters exist)
- [X] T043 [US4] Update GraphCanvas to handle dynamic figure size changes in src/ui/graph_canvas.py (calls figure.set_size_inches on resize)

**Checkpoint**: All P1 and P2 user stories should now be independently functional ✅

---

## Phase 6: User Story 3 - Period Markers with Transparency Controls (Priority: P3) ✅ COMPLETE

**Goal**: Display optional period boundary markers with customizable color and alpha transparency

**Independent Test**: Enable period markers, set custom color (e.g., red) and alpha (e.g., 0.5), click Start, verify 9 semi-transparent vertical lines appear at period boundaries

### Implementation for User Story 3

- [X] T044 [P] [US3] Add period_markers_enabled checkbox to InputPanel in src/ui/input_panel.py (default unchecked)
- [X] T045 [P] [US3] Add period_marker_color_picker (QColorDialog button) to InputPanel in src/ui/input_panel.py (default gray #808080, enabled when checkbox checked)
- [X] T046 [P] [US3] Add period_marker_alpha slider (QSlider 0-100 → 0.0-1.0) to InputPanel in src/ui/input_panel.py (default 30 → 0.3, enabled when checkbox checked)
- [X] T047 [US3] Update color_changed signal to emit full ColorSettings including period marker settings
- [X] T048 [US3] Implement render_period_markers(ax, period, num_periods, viewport, color, alpha) in src/rendering/markers.py (draws vertical lines at period boundaries)
- [X] T049 [US3] Update render_complete_graph() to conditionally call render_period_markers() if ColorSettings.period_markers_enabled is True

**Checkpoint**: All user stories (P1, P2, P3) should now be independently functional ✅

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T050 [P] Add error handling for extreme parameter values in src/computation/function.py (catch NumPy overflow, return error message to UI)
- [X] T051 [P] Add keyboard shortcut (Enter key) to trigger Start button in src/ui/input_panel.py
- [X] T052 [P] Add status bar to MainWindow showing current function equation in src/ui/main_window.py (e.g., "f(x) = 1.0*sin(x*1.0 + 0.0) + tan(0.0*x)")
- [X] T053 Code cleanup: Run black formatter on all Python files
- [ ] T054 Code cleanup: Run flake8 and fix linting warnings
- [ ] T055 Code cleanup: Run mypy and add type hints to all public functions
- [X] T056 [P] Create user documentation in docs/user-guide.md (how to use the application, parameter meanings, edge cases)
- [ ] T057 Validate application against quickstart.md from specs/001-function-graph-plotter/quickstart.md
- [ ] T058 Test edge cases: b=0, d=0, b=0 and d=0, extreme values (a=1000, b=0.001), asymptotes
- [ ] T059 Test cross-platform: Verify on Windows, macOS (if available), Linux (if available)
- [ ] T060 Performance profiling: Measure graph render time, ensure <2s for 9 periods per SC-001

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
├── Phase 3 (User Story 1 - Basic Plotting) [P1] ← MVP DELIVERY POINT 🎯
├── Phase 4 (User Story 2 - Visual Customization) [P2] (can start in parallel)
├── Phase 5 (User Story 4 - Responsive Resize) [P2] (can start in parallel)
└── Phase 6 (User Story 3 - Period Markers) [P3] (can start in parallel)
    ↓
Phase 7 (Polish)
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 (Foundational) completion - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Phase 2 completion - Can work in parallel with US1 after T033 (MainWindow.plot_graph exists)
- **User Story 4 (P2)**: Depends on Phase 2 completion - Integrates with US1 after T033 (requires plot_graph method)
- **User Story 3 (P3)**: Depends on Phase 2 completion - Can work in parallel but optional/lowest priority

### Within Each User Story

**User Story 1 (Basic Plotting)**:
1. Period calculation (T015-T016) - foundational math
2. Function evaluation (T017-T019) - uses period calculation
3. Viewport calculation (T020-T021) - uses period calculation
4. Rendering (T022-T027) - uses viewport and curve data
5. UI (T028-T034) - orchestrates all components

**User Story 2 (Visual Customization)**:
- All tasks (T035-T039) can proceed in parallel once US1 T033 exists

**User Story 4 (Responsive Resize)**:
- All tasks (T040-T043) require US1 T028-T033 (MainWindow and GraphCanvas exist)

**User Story 3 (Period Markers)**:
- All tasks (T044-T049) can proceed in parallel once US1 rendering layer exists (T022-T027)

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004, T005, T006, T007 can all run in parallel after T001-T002

**Phase 2 (Foundational)**:
- T008, T009, T010, T011, T012, T014 can all run in parallel
- T013 depends on T012

**Phase 3 (User Story 1)**:
- T015, T016 can run in parallel (both in period.py)
- T022, T023, T024 can run in parallel (different rendering modules)
- T017-T019, T020-T021, T022-T026 can be worked on by different developers simultaneously

**Phase 4 (User Story 2)**:
- T035, T036 can run in parallel
- All tasks are small UI additions

**Phase 6 (User Story 3)**:
- T044, T045, T046 can run in parallel (all InputPanel widgets)

**Phase 7 (Polish)**:
- T050, T051, T052, T056 can run in parallel (different files)
- T053, T054, T055 should run sequentially (formatting → linting → type checking)

---

## Parallel Execution Examples

### Example 1: Phase 2 (Foundational) - 3 Developers

**Dev 1**: T008, T009 (data models in separate files)  
**Dev 2**: T010, T011 (data models in separate files)  
**Dev 3**: T012, T014 (validation + package setup)  
Then **Dev 3**: T013 (after T012 completes)

**Timeline**: ~2-3 hours instead of ~6 hours sequential

---

### Example 2: Phase 3 (User Story 1) - 4 Developers

**Dev 1 (Math)**: T015 → T016 → T017 → T018 → T019  
**Dev 2 (Viewport)**: T020 → T021  
**Dev 3 (Rendering)**: T022 → T023 → T024 → T025 → T026 → T027  
**Dev 4 (UI)**: T028 → T029 → T030 → T031 → T032 → T033 → T034

**Dependencies**:
- Dev 4 waits for Dev 1 (T019) and Dev 2 (T021) and Dev 3 (T027) before T033 integration
- But can build UI structure (T028-T032) in parallel

**Timeline**: ~1-2 days instead of ~4 days sequential

---

### Example 3: Phases 4-6 (User Stories 2, 3, 4) - 3 Developers

After Phase 3 (US1) completes:

**Dev 1**: Phase 4 (US2) - T035 → T036 → T037 → T038 → T039  
**Dev 2**: Phase 5 (US4) - T040 → T041 → T042 → T043  
**Dev 3**: Phase 6 (US3) - T044 → T045 → T046 → T047 → T048 → T049

**Timeline**: ~1 day instead of ~3 days sequential

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**MVP = Phase 1 + Phase 2 + Phase 3 (User Story 1)**

This delivers:
- ✅ Functional graph plotting with 9 periods
- ✅ Symmetric display around origin
- ✅ Proper axes and origin marker
- ✅ Edge case handling (b=0, d=0, asymptotes)
- ✅ Default colors (blue graph, black axes)
- ✅ Input validation and Start button
- ✅ Desktop application with GUI

**Estimated effort**: ~60 tasks (T001-T034 + foundational tests if added)

**Timeline**: 
- Single developer: ~4-5 days
- 2 developers: ~2-3 days
- 4 developers: ~1-2 days

### Incremental Delivery After MVP

**Iteration 2**: Add User Story 2 (Visual Customization) - ~5 tasks, <1 day  
**Iteration 3**: Add User Story 4 (Responsive Resize) - ~4 tasks, <1 day  
**Iteration 4**: Add User Story 3 (Period Markers) - ~6 tasks, <1 day  
**Iteration 5**: Polish phase - ~11 tasks, 1-2 days

### Testing Strategy (Optional)

Since tests are optional for this feature, implement in this order if testing is desired:

1. **After Phase 2**: Add unit tests for data models (FunctionParameters, ColorSettings validation)
2. **After Phase 3 (MVP)**: Add unit tests for computation modules (period calculation, function evaluation, asymptote detection)
3. **After Phase 3 (MVP)**: Add integration tests for basic plotting workflow
4. **After Phase 7**: Add visual regression tests comparing matplotlib outputs to baseline images

---

## Task Count Summary

| Phase | Task Count | Story | Priority |
|-------|------------|-------|----------|
| Phase 1 (Setup) | 7 | - | - |
| Phase 2 (Foundational) | 7 | - | - |
| Phase 3 (User Story 1) | 20 | US1 | P1 (MVP) |
| Phase 4 (User Story 2) | 5 | US2 | P2 |
| Phase 5 (User Story 4) | 4 | US4 | P2 |
| Phase 6 (User Story 3) | 6 | US3 | P3 |
| Phase 7 (Polish) | 11 | - | - |
| **TOTAL** | **60** | - | - |

**Parallel opportunities**: 25+ tasks can be parallelized (marked with [P])

---

## Format Validation ✅

All tasks follow the required format:
- ✅ Checkbox: `- [ ]`
- ✅ Task ID: Sequential (T001-T060)
- ✅ [P] marker: Present on parallelizable tasks
- ✅ [Story] label: Present on user story tasks (US1, US2, US3, US4)
- ✅ Description: Includes exact file paths and clear actions
- ✅ User story organization: Tasks grouped by story for independent implementation

**Quality checks**:
- ✅ Each user story has independent test criteria
- ✅ MVP scope clearly defined (Phase 3 = User Story 1)
- ✅ Dependencies documented in Dependencies & Execution Order section
- ✅ Parallel execution examples provided
- ✅ All file paths follow src/ structure from plan.md
