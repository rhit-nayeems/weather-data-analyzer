# US Weather Data Analysis Platform

A Python analytics project that explores daily weather patterns across major U.S. cities with interactive visualizations, anomaly detection, and similarity ranking.

## Why this project
I initially built this project in freshman year. While organizing my GitHub, I decided to scale it up into a stronger portfolio piece by adding advanced analytics and a deployable web dashboard.

## Dataset
Source: `data/us-weather-history`
- Cities: 10 U.S. locations (Charlotte, Los Angeles, Houston, Indianapolis, Jacksonville, Chicago, New York City, Philadelphia, Phoenix, Seattle)
- Period covered: **July 2014 to June 2015** (month availability depends on station)
- Fields: mean/min/max temperatures, precipitation, historical records, and record years

## Features
### Core analysis
- Single-city line charts + statistical summary
- Two-city comparison + difference plot
- Histograms
- 3D scatter plots

### Advanced analysis
- **Anomaly detection** with z-scores
- **City similarity ranking** using RMSE, MAE, and Pearson correlation

### UX and reliability
- Desktop GUI (`tkinter`) with validation
- Web dashboard (`Streamlit`) for easy sharing
- Month/year validation against actual data availability
- Automated tests for key analytics and edge cases

## Tech stack
- Python 3
- Tkinter
- Streamlit
- Matplotlib
- `unittest`

## Project structure
- `src/main.py`: desktop GUI entrypoint
- `src/gui.py`: tkinter UI
- `src/web_app.py`: Streamlit web dashboard
- `src/functions.py`: analysis and plotting engine
- `src/csv_reader.py`: CSV parsing and type conversion
- `src/unit_tests.py`: test suite
- `data/us-weather-history/`: datasets
- `plots/`: generated charts

## Local setup
From `project-folder`:

```powershell
python -m pip install -r requirements.txt
```

## Run desktop app
```powershell
python src/main.py
```

## Run web dashboard locally
```powershell
streamlit run src/web_app.py
```

## Run tests
```powershell
python src/unit_tests.py
```

## Free hosting (recommended): Streamlit Community Cloud
This is the easiest free option for a recruiter-friendly live link.

1. Push this repo to GitHub.
2. Go to Streamlit Community Cloud: https://share.streamlit.io/
3. Click **New app**.
4. Select your repo + branch.
5. Set entrypoint to: `src/web_app.py`
6. Deploy.

After deploy, you’ll get a public `.streamlit.app` URL you can add to your resume and portfolio.

## Metrics explained for non-technical viewers
- **MAE (Mean Absolute Error):** average day-to-day difference between two city curves.
- **RMSE (Root Mean Squared Error):** similar to MAE, but penalizes large differences more heavily.
- Lower MAE/RMSE means cities are more similar for the selected metric.

## Recruiter-facing impact
This project demonstrates:
- End-to-end data product thinking (raw files -> analysis -> visuals -> deployable app)
- Refactoring a class project into a production-style portfolio artifact
- Feature expansion with statistical methods (anomaly detection and similarity ranking)
- Input validation, error handling, and automated testing
