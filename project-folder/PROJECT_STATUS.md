# Project Status

Assessment date: 2026-04-03

## Executive Summary

This repository is a functional Python weather analytics project with two user interfaces:

- a desktop application built with `tkinter`
- a web dashboard built with `Streamlit`

The application is centered around a single shared analytics module that loads daily weather CSVs, computes descriptive statistics and advanced metrics, and saves plots to disk.

Current status:

- Core data analysis workflows are implemented and working.
- The dataset is present locally and complete for the intended analysis period.
- Both UI entrypoints exist and are wired into the same backend logic.
- Automated tests for key helpers and analytics functions are present and currently passing.
- The project is portfolio-ready as a personal showcase application.
- The project is not yet production-grade from a packaging, maintainability, deployment-hardening, or CI perspective.

## Repository State At Time Of Assessment

- Git working tree status: clean
- Test command executed: `python src/unit_tests.py`
- Test result: `14` tests passed
- Primary runtime dependencies declared: `matplotlib`, `streamlit`
- Standard-library UI dependency used: `tkinter`
- No external API calls, database, authentication, or backend service layer are used

## Top-Level Repository Inventory

The real project is contained in `project-folder`.

Top-level contents inside `project-folder`:

| Path | Purpose |
| --- | --- |
| `README.md` | High-level project overview and usage instructions |
| `requirements.txt` | Root dependency file |
| `data/` | Weather dataset and dataset notes |
| `plots/` | Generated chart output files |
| `src/` | Application source code |
| `LICENSE` | License file |
| `.gitignore` | Ignore rules for Python and IDE artifacts |

Tracked project source files under `src/`:

| File | Lines | Role |
| --- | ---: | --- |
| `src/csv_reader.py` | 78 | CSV loader and type coercion helper |
| `src/functions.py` | 1255 | Core analytics, validation, and plotting engine |
| `src/gui.py` | 425 | Desktop UI |
| `src/main.py` | 16 | Desktop app entrypoint |
| `src/unit_tests.py` | 109 | Automated test suite |
| `src/web_app.py` | 229 | Streamlit web dashboard |

Other notable inventory counts:

- Weather station CSV files: `10`
- Station metadata CSV files: `1`
- Checked-in PNG plot files currently present in `plots/`: `37`

## Application Architecture

### 1. Data Layer

The project uses local CSV files stored in `data/us-weather-history`.

The file `src/csv_reader.py` exposes `read_csv(filename)`, which:

- reads CSV rows with Python's built-in `csv` module
- converts integer-looking values to `int`
- converts float-looking values to `float`
- converts `"true"` and `"false"` strings to booleans
- leaves other values as stripped strings

Important implications:

- Date values remain strings such as `2014-7-1`.
- The rest of the project does not use `pandas`; all data handling is tuple-based.
- The parsed data structure is a tuple of tuples, not a dataframe or custom model object.

### 2. Core Analytics Layer

Nearly all business logic lives in `src/functions.py`.

This module is responsible for:

- path resolution for `data/` and `plots/`
- station code and display-name normalization
- metric name normalization
- loading station CSVs
- determining valid years and valid months
- slicing time series by month/year
- computing descriptive statistics
- generating plots with matplotlib
- anomaly detection
- city similarity ranking

This file is effectively the service layer for the whole application.

Key design characteristics:

- one large monolithic module instead of smaller domain-specific modules
- procedural helper functions rather than classes
- common return format: dictionaries containing summary data and saved plot file paths
- minimal shared state, except for cached year-range discovery

### 3. Desktop UI Layer

The desktop entrypoint is `src/main.py`, which simply imports and launches the Tk GUI.

The actual UI is in `src/gui.py`.

The GUI:

- creates a single window with form controls
- allows the user to choose analysis type, city, metric, and optional month/year filters
- dynamically shows and hides relevant fields depending on the selected analysis
- validates month/year, threshold, z-score, and top-N inputs
- calls the shared functions from `src/functions.py`
- displays the returned result dictionary as formatted text

The GUI does not contain analysis logic. It is a controller and presentation layer.

### 4. Web UI Layer

The web interface is implemented in `src/web_app.py`.

The Streamlit dashboard:

- provides sidebar controls for the same analysis options as the desktop app
- dispatches into the same backend functions as the desktop app
- renders structured results with `st.json`, `st.dataframe`, and `st.image`
- always runs with `show_plot=False`, because Streamlit displays saved image files rather than interactive matplotlib windows

The web app is therefore a second presentation layer over the same backend engine.

## Runtime Flow

### Desktop Flow

1. `python src/main.py`
2. `main()` calls `launch_gui()`
3. `WeatherAnalysisGUI` builds the form and loads dataset-derived validation info
4. User chooses an analysis type and inputs parameters
5. `_run_analysis()` validates inputs
6. `_run_analysis()` calls one `functions.analyze_*` helper
7. The helper loads CSV data, computes analytics, generates plot files, and returns a result dictionary
8. The GUI formats that dictionary into readable text and writes it to the results panel

### Web Flow

1. `streamlit run src/web_app.py`
2. Streamlit builds the control sidebar
3. User chooses inputs and clicks `Run Analysis`
4. The app validates required filters
5. The app calls one `functions.analyze_*` helper
6. The helper returns a result dictionary
7. Streamlit renders summary values, tabular results, and saved PNG plots

## Data Status

### Dataset Coverage

The repository contains `10` station datasets:

- `KCLT`
- `KCQT`
- `KHOU`
- `KIND`
- `KJAX`
- `KMDW`
- `KNYC`
- `KPHL`
- `KPHX`
- `KSEA`

Observed actual coverage:

- Earliest date in every station file: `2014-7-1`
- Latest date in every station file: `2015-6-30`
- Daily rows per station: `365`
- Covered months: July 2014 through June 2015

This means the data is complete for one continuous 12-month period across all included cities.

### Dataset Schema

The station CSVs contain:

- date
- actual mean temperature
- actual minimum temperature
- actual maximum temperature
- long-term average minimum temperature
- long-term average maximum temperature
- record minimum temperature
- record maximum temperature
- year of record minimum
- year of record maximum
- actual precipitation
- average precipitation
- record precipitation

The file `data/us-weather-history/station_locations.csv` provides station metadata, but it is not currently used by the application.

### Dataset Snapshot

The table below reflects simple aggregate values computed from the current local CSV files.

| Station | Days | Avg actual mean temp | Total actual precipitation |
| --- | ---: | ---: | ---: |
| KCLT | 365 | 61.05 | 37.38 |
| KCQT | 365 | 68.56 | 8.52 |
| KHOU | 365 | 69.72 | 64.60 |
| KIND | 365 | 51.39 | 38.59 |
| KJAX | 365 | 68.98 | 43.91 |
| KMDW | 365 | 51.05 | 36.04 |
| KNYC | 365 | 54.74 | 46.05 |
| KPHL | 365 | 55.88 | 45.46 |
| KPHX | 365 | 77.32 | 10.12 |
| KSEA | 365 | 56.54 | 37.43 |

## Feature Status

### Implemented And Working

| Feature | Status | Notes |
| --- | --- | --- |
| Single-city line analysis | Implemented | Supports whole-dataset and month-scoped views |
| Summary statistics | Implemented | Average, standard deviation, min, max, average change, optional threshold counts |
| Temperature amplitude chart | Implemented | Added automatically for mean/min/max temperature metrics |
| Two-city comparison | Implemented | Saves overlay plot and difference plot |
| Histogram generation | Implemented | Supports whole dataset and month-scoped view |
| 3D scatter plotting | Implemented | User can select any three metrics |
| Anomaly detection | Implemented | Uses absolute z-score thresholding |
| City similarity ranking | Implemented | Uses RMSE ordering and also reports MAE and Pearson correlation |
| Desktop GUI | Implemented | Tkinter-based |
| Web dashboard | Implemented | Streamlit-based |
| Input validation | Implemented | Covers invalid months, years, duplicate city comparison, invalid thresholds |
| Automated tests | Implemented | Focused on core helpers and analytics |

### Advanced Analytics Behavior

#### Anomaly Detection

Anomaly detection is implemented with z-scores:

- mean is calculated from the selected series
- population standard deviation is calculated from the selected series
- each point gets a z-score of `(value - mean) / std_dev`
- points with `abs(z_score) >= threshold` are considered anomalies
- anomalies are sorted from largest absolute z-score to smallest

This is simple, interpretable, and effective for a portfolio project, but it is still a basic anomaly model rather than a seasonal or domain-aware one.

#### Similarity Ranking

City similarity ranking:

- loads the selected metric for a reference city
- loads the same metric for every other city
- aligns the two time series by shared dates
- computes RMSE, MAE, and Pearson correlation
- sorts cities by lowest RMSE

This is the strongest analytical feature in the repository because it goes beyond visualization into measurable comparison.

## Plot Output Status

The `plots/` folder currently contains `37` PNG files.

Observed output categories:

- 3D scatter plots: `5`
- anomaly plots: `2`
- difference plots: `6`
- histograms: `5`
- city-to-city overlay plots: `7`
- single-city line plots: `6`
- similarity ranking charts: `2`
- temperature amplitude charts: `4`

Important status note:

- The `plots/` directory is not a pure cache.
- It contains historical generated outputs that have been checked into the repository.
- Some filenames follow older naming conventions and are inconsistent with the newer backend naming scheme.

This is acceptable for a portfolio repository, but it means `plots/` is part generated artifact store and part demonstration gallery.

## Validation And Testing Status

### Test Coverage Present

The test suite in `src/unit_tests.py` currently verifies:

- header skipping in column extraction
- month parsing for single- and double-digit date formats
- basic sequence statistics behavior
- threshold counting
- empty-sequence error handling
- station display-name mapping
- dataset year-range assumptions
- available-month behavior for Los Angeles in 2014
- anomaly detection behavior
- similarity metric behavior
- date alignment behavior
- top-N similarity ranking output shape

### Test Result

Executed during this assessment:

```powershell
python src/unit_tests.py
```

Result:

- `14` tests run
- `0` failures
- `0` errors

### Coverage Gaps

The current tests do not cover:

- Tkinter GUI interaction
- Streamlit UI interaction
- visual regression of plots
- file naming consistency
- every analysis path end to end
- dependency/environment setup failures

## Documentation Status

### Present Documentation

- `README.md` provides a clear high-level overview
- `data/us-weather-history/README.md` documents the dataset columns
- `plots/instructions.md` and `data/instructions.md` are leftover workflow/instruction files from setup

### Documentation Quality

Current documentation is generally good for a portfolio project, but the repo still benefits from a more explicit internal-status document because:

- architecture details are implicit in code rather than documented
- the dual-UI structure is not deeply explained
- some implementation realities differ slightly from how a reader may infer the repo works from the README alone

## Current Strengths

- Clear user-facing value proposition
- Complete local dataset included in repo
- Two usable interfaces over the same backend logic
- Analytics layer is straightforward and readable
- Advanced features add depth beyond basic plotting
- Error messages are reasonably user-friendly
- Tests exist and currently pass
- Project demonstrates end-to-end ownership from raw data to UI

## Known Technical Debt And Risks

### 1. Monolithic Core Module

`src/functions.py` is `1255` lines long and mixes:

- path configuration
- station metadata
- data loading
- validation
- statistics
- plotting
- orchestration

This increases coupling and makes future changes harder to isolate and test.

### 2. Duplicated UI Dispatch Logic

Both `src/gui.py` and `src/web_app.py` contain similar decision trees that map user selections to backend function calls.

Impact:

- adding a new analysis requires changes in two UI layers
- UI behavior can drift over time

### 3. Inconsistent Plot Naming History

Existing plot artifacts show mixed naming conventions. This is mostly cosmetic, but it makes the artifact folder harder to reason about.

### 4. Comparison Mode Uses Length Truncation

The direct comparison helper trims series to the shorter available length. Similarity ranking does proper date alignment, but standard two-curve comparison does not use the same alignment strategy.

With the current dataset this is not causing visible trouble, because coverage is complete and synchronized, but the behavior would matter if future datasets become irregular.

### 5. Streamlit Month Validation Is Slightly Less Strict

The GUI computes shared valid months more aggressively for some scenarios than the Streamlit helper does.

Current impact:

- low, because the present dataset is fully aligned

Future impact:

- moderate, if incomplete or uneven station coverage is introduced

### 6. Unused Data Asset

`station_locations.csv` is available but not consumed anywhere in the application.

### 7. Duplicate Dependency Files

There is a `requirements.txt` at the project root and another under `src/`, with the same contents.

This is harmless but redundant.

### 8. No Packaging Or CI

The project currently has:

- no package structure
- no linter configuration
- no formatter configuration
- no type checker
- no CI workflow
- no automated deployment configuration

That is acceptable for a portfolio project, but it is the clearest gap between the current state and a more professional engineering baseline.

## Maintainability Assessment

Overall maintainability status: moderate

Reasons:

- The code is understandable.
- The logic is not deeply abstracted.
- There is a clear separation between UI files and the core functions file.
- The main maintainability problem is concentration of responsibility in one backend module rather than unreadable code.

In other words, the project is easy to understand today but will become harder to evolve if new features continue to accumulate inside `src/functions.py`.

## Portfolio Readiness Assessment

Overall portfolio status: strong

Reasons:

- demonstrates data ingestion, transformation, analytics, visualization, and UI delivery
- includes both desktop and web presentations
- includes error handling and tests
- goes beyond class-project plotting by adding anomaly detection and similarity ranking

If presented to recruiters or hiring managers, this repo already communicates useful engineering signals. The biggest gains now would come from polish and structure, not from adding many more features.

## Recommended Next Actions

### High Priority

1. Split `src/functions.py` into smaller modules.

   Suggested boundaries:
   - `data_access.py`
   - `stats.py`
   - `plotting.py`
   - `analysis.py`
   - `stations.py`

2. Centralize analysis dispatch so both UIs call a shared command layer rather than duplicating branching logic.

3. Standardize plot filename conventions and decide whether `plots/` should remain a checked-in gallery or become a generated-only output directory.

4. Add at least a few end-to-end tests for the public `analyze_*` functions.

### Medium Priority

1. Remove duplicate `requirements.txt` or define a clear reason to keep both.

2. Either use `station_locations.csv` in the UI or remove it from the critical project narrative.

3. Add a lightweight CI workflow that installs dependencies and runs `python src/unit_tests.py`.

4. Add clearer developer documentation for project structure and execution flow.

### Low Priority

1. Consider packaging the project so imports do not depend on running from a specific directory layout.

2. Consider replacing tuple-based data plumbing with a more explicit internal representation if the project grows.

3. Consider richer statistical methods if the goal shifts from portfolio demonstration to deeper analytical rigor.

## Bottom-Line Status

The project is currently:

- working
- understandable
- verified at a basic automated-test level
- suitable for portfolio presentation
- not yet fully refactored or operationalized

The core feature set is complete enough to be shown publicly. The next phase should focus on structure, consistency, and engineering polish rather than feature sprawl.
