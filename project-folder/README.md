# US Weather Data Analysis Platform

A Python analytics project that explores daily weather patterns across major U.S. cities with interactive visualizations, anomaly detection, and similarity ranking.

## Why this project
This project demonstrates practical data engineering and product-thinking skills:
- Turning raw CSV time-series data into reusable analytics functions.
- Designing a desktop GUI for non-technical users.
- Adding advanced analysis features recruiters care about (anomaly detection and similarity ranking).
- Building test coverage for core logic and edge cases.

## Dataset
Source: `data/us-weather-history`
- Cities: 10 U.S. locations (Charlotte, Los Angeles, Houston, Indianapolis, Jacksonville, Chicago, New York City, Philadelphia, Phoenix, Seattle)
- Period covered: **July 2014 to June 2015** (varies by city/month availability)
- Data fields: temperatures, precipitation, historical record values, and record years

## Features
### 1. Core visual analytics
- Single-city line charts
- Two-city comparison charts + difference curve
- Histograms
- 3D scatter plots

### 2. Statistical summaries
- Mean, standard deviation
- Highest/lowest values with positions
- Average rate of change
- Optional threshold counts (>= threshold, <= threshold)

### 3. Anomaly detection (new)
- Z-score-based anomaly detection on any metric
- Configurable z-score threshold in GUI
- Highlighted anomaly points on saved plots
- Tabular anomaly output with date/value/z-score

### 4. City similarity ranking (new)
- Ranks cities by similarity to a selected reference city
- Uses aligned time-series and reports:
  - RMSE (primary ranking metric; lower is better)
  - MAE
  - Pearson correlation
  - Overlap days
- Generates ranking bar chart

### 5. GUI-first user experience
- No console input required
- Human-readable city names
- Valid year range and month availability checks
- Helpful error messages for missing month/year data

## Tech stack
- Python 3
- Tkinter (GUI)
- Matplotlib (visualization)
- Custom CSV parser (`csv_reader.py`)
- `unittest` for test suite

## Project structure
- `src/main.py`: application entrypoint
- `src/gui.py`: GUI layer and user interaction logic
- `src/functions.py`: analysis + plotting engine
- `src/unit_tests.py`: automated tests
- `data/us-weather-history/`: weather CSV files
- `plots/`: generated charts

## Setup
From `project-folder`:

```powershell
python -m pip install -r requirements.txt
```

## Run
```powershell
python src/main.py
```

## Run tests
```powershell
python src/unit_tests.py
```

## What this project demonstrates to recruiters
- Building maintainable analysis APIs (separated from UI concerns)
- Handling real-world data quality and availability constraints
- Implementing feature evolution over an existing codebase
- Writing validations and tests to prevent regressions
- Shipping an end-to-end usable analytics tool (data -> insight -> visualization)

## Suggested portfolio presentation
If you are showcasing this on a portfolio site, include:
1. A screenshot/GIF of the GUI with anomaly detection and similarity ranking results.
2. 2-3 generated chart examples from `plots/`.
3. A short note on design decisions (why z-score, why RMSE ranking, and how month validation works).
