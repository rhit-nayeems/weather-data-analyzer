"""Streamlit dashboard for weather data analysis."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

import functions


ANALYSIS_TYPES = (
    "Single curve",
    "Compare 2 curves",
    "Histogram",
    "3D scatter",
    "Anomaly detection",
    "City similarity ranking",
)

SCOPE_TYPES = (
    "Whole dataset",
    "Specific month",
)


def _available_months(analysis_type, year, station1, station2=None):
    """Return valid month list for current selection."""
    months_station1 = set(functions.get_available_months_for_year(station1, year))

    if analysis_type == "Compare 2 curves" and station2 is not None:
        months_station2 = set(functions.get_available_months_for_year(station2, year))
        return sorted(months_station1 & months_station2)

    return sorted(months_station1)


def _render_result(result):
    """Render analysis output in Streamlit."""
    st.subheader("Results")

    for key, value in result.items():
        if key == "statistics" and isinstance(value, dict):
            st.markdown("**Statistics**")
            st.json(value)
            continue

        if key in ("anomalies", "ranked_cities") and isinstance(value, list):
            st.markdown(f"**{key.replace('_', ' ').title()}**")
            if value:
                st.dataframe(value, use_container_width=True)
            else:
                st.info("No rows to show.")
            continue

        if key == "plot_files" and isinstance(value, list):
            st.markdown("**Generated plots**")
            for plot_path in value:
                image_path = Path(plot_path)
                if image_path.exists():
                    st.image(str(image_path), caption=image_path.name, use_container_width=True)
                else:
                    st.warning(f"Plot file not found: {plot_path}")
            continue

        st.write(f"**{key.replace('_', ' ').title()}:** {value}")


def main():
    """Launch the Streamlit dashboard."""
    st.set_page_config(page_title="Weather Analytics Dashboard", layout="wide")

    st.title("Weather Analytics Dashboard")
    st.caption(
        "Scaled-up version of a freshman-year project: now includes anomaly detection and city similarity ranking."
    )

    with st.sidebar:
        st.header("Controls")

        analysis_type = st.selectbox("Analysis type", ANALYSIS_TYPES)
        scope = st.radio("Scope", SCOPE_TYPES, index=0)

        station_options = functions.get_station_display_options()
        station1 = st.selectbox("City", station_options, index=0)
        station2 = None

        if analysis_type == "Compare 2 curves":
            default_index = 1 if len(station_options) > 1 else 0
            station2 = st.selectbox("City 2", station_options, index=default_index)

        column = None
        x_column = None
        y_column = None
        z_column = None

        if analysis_type == "3D scatter":
            x_column = st.selectbox("X axis", functions.COLUMNS, index=0)
            y_column = st.selectbox("Y axis", functions.COLUMNS, index=1)
            z_column = st.selectbox("Z axis", functions.COLUMNS, index=2)
        else:
            column = st.selectbox("Metric", functions.COLUMNS, index=0)

        year = None
        month = None
        use_month = scope == "Specific month"

        min_year, max_year = functions.get_valid_year_range()
        if use_month:
            year = st.number_input("Year", min_value=min_year, max_value=max_year, value=min_year, step=1)
            year = int(year)

            month_options = _available_months(analysis_type, year, station1, station2=station2)
            if month_options:
                month = st.selectbox("Month", month_options, index=0)
                month = int(month)
                st.caption(f"Available months for {year}: {', '.join(str(item) for item in month_options)}")
            else:
                st.warning("No months available for the selected filters.")

        threshold = None
        if analysis_type == "Single curve":
            use_threshold = st.checkbox("Use stats threshold", value=False)
            if use_threshold:
                threshold = st.number_input("Threshold value", value=0.0)

        z_threshold = 2.0
        if analysis_type == "Anomaly detection":
            z_threshold = st.number_input("Z-score threshold", min_value=0.1, value=2.0, step=0.1)
            st.info(
                "Z-score = (value - mean) / standard deviation. "
                "Higher absolute z-score means a point is farther from typical behavior."
            )

        top_n = 5
        if analysis_type == "City similarity ranking":
            top_n = st.slider("Top N cities", min_value=1, max_value=len(station_options) - 1, value=5)
            st.info(
                "Ranking uses RMSE (lower is more similar), with MAE and correlation shown for extra context."
            )

        run_analysis = st.button("Run Analysis", type="primary", use_container_width=True)

    st.markdown("---")

    if not run_analysis:
        st.write("Choose options on the left and click **Run Analysis**.")
        return

    if use_month and month is None:
        st.error("Please choose a valid month for the selected filters.")
        return

    try:
        if analysis_type == "Single curve":
            result = functions.analyze_single_curve(
                station=station1,
                column=column,
                use_month=use_month,
                year=year,
                month=month,
                threshold=threshold,
                show_plot=False,
            )
        elif analysis_type == "Compare 2 curves":
            if station1 == station2:
                raise ValueError("Pick two different cities for comparison.")
            result = functions.analyze_two_curves(
                station1=station1,
                station2=station2,
                column=column,
                use_month=use_month,
                year=year,
                month=month,
                show_plot=False,
            )
        elif analysis_type == "Histogram":
            result = functions.analyze_histogram(
                station=station1,
                column=column,
                use_month=use_month,
                year=year,
                month=month,
                show_plot=False,
            )
        elif analysis_type == "3D scatter":
            result = functions.analyze_3d_scatter(
                station=station1,
                x_column=x_column,
                y_column=y_column,
                z_column=z_column,
                use_month=use_month,
                year=year,
                month=month,
                show_plot=False,
            )
        elif analysis_type == "Anomaly detection":
            result = functions.analyze_anomalies(
                station=station1,
                column=column,
                use_month=use_month,
                year=year,
                month=month,
                z_threshold=float(z_threshold),
                show_plot=False,
            )
        elif analysis_type == "City similarity ranking":
            result = functions.analyze_city_similarity(
                reference_station=station1,
                column=column,
                use_month=use_month,
                year=year,
                month=month,
                top_n=int(top_n),
                show_plot=False,
            )
        else:
            raise ValueError("Unsupported analysis type.")

        st.success("Analysis complete.")
        _render_result(result)

    except Exception as exc:
        st.error(str(exc))


if __name__ == "__main__":
    main()
