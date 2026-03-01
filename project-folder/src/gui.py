"""Tkinter GUI for the weather analysis project."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

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


class WeatherAnalysisGUI(tk.Tk):
    """Main GUI window for weather-data analysis."""

    def __init__(self):
        super().__init__()
        self.title("US Weather Data Analysis")
        self.geometry("980x760")
        self.minsize(920, 680)

        self.station_options = functions.get_station_display_options()
        self.min_year, self.max_year = functions.get_valid_year_range()

        self.analysis_var = tk.StringVar(value=ANALYSIS_TYPES[0])
        self.scope_var = tk.StringVar(value=SCOPE_TYPES[0])
        self.station1_var = tk.StringVar(value=self.station_options[0])
        self.station2_var = tk.StringVar(value=self.station_options[1])
        self.column_var = tk.StringVar(value=functions.COLUMNS[0])
        self.x_column_var = tk.StringVar(value=functions.COLUMNS[0])
        self.y_column_var = tk.StringVar(value=functions.COLUMNS[1])
        self.z_column_var = tk.StringVar(value=functions.COLUMNS[2])
        self.year_var = tk.StringVar(value=str(self.min_year))
        self.month_var = tk.StringVar(value="1")
        self.threshold_var = tk.StringVar(value="")
        self.anomaly_z_var = tk.StringVar(value="2.0")
        self.top_n_var = tk.StringVar(value="5")
        self.show_plot_var = tk.BooleanVar(value=True)

        self._build_layout()
        self._bind_events()
        self._refresh_field_visibility()

    def _build_layout(self):
        """Build and place all widgets."""
        main = ttk.Frame(self, padding=16)
        main.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main.columnconfigure(1, weight=1)
        main.rowconfigure(16, weight=1)

        ttk.Label(main, text="Weather Data Analysis", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        ttk.Label(main, text="Analysis type").grid(row=1, column=0, sticky="w", pady=4)
        self.analysis_combo = ttk.Combobox(main, textvariable=self.analysis_var, values=ANALYSIS_TYPES, state="readonly")
        self.analysis_combo.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(main, text="Scope").grid(row=2, column=0, sticky="w", pady=4)
        self.scope_combo = ttk.Combobox(main, textvariable=self.scope_var, values=SCOPE_TYPES, state="readonly")
        self.scope_combo.grid(row=2, column=1, sticky="ew", pady=4)

        self.station1_label = ttk.Label(main, text="City")
        self.station1_label.grid(row=3, column=0, sticky="w", pady=4)
        self.station1_combo = ttk.Combobox(main, textvariable=self.station1_var, values=self.station_options, state="readonly")
        self.station1_combo.grid(row=3, column=1, sticky="ew", pady=4)

        self.station2_label = ttk.Label(main, text="City 2")
        self.station2_label.grid(row=4, column=0, sticky="w", pady=4)
        self.station2_combo = ttk.Combobox(main, textvariable=self.station2_var, values=self.station_options, state="readonly")
        self.station2_combo.grid(row=4, column=1, sticky="ew", pady=4)

        self.column_label = ttk.Label(main, text="Data column")
        self.column_label.grid(row=5, column=0, sticky="w", pady=4)
        self.column_combo = ttk.Combobox(main, textvariable=self.column_var, values=functions.COLUMNS, state="readonly")
        self.column_combo.grid(row=5, column=1, sticky="ew", pady=4)

        self.x_label = ttk.Label(main, text="X axis column")
        self.x_label.grid(row=6, column=0, sticky="w", pady=4)
        self.x_combo = ttk.Combobox(main, textvariable=self.x_column_var, values=functions.COLUMNS, state="readonly")
        self.x_combo.grid(row=6, column=1, sticky="ew", pady=4)

        self.y_label = ttk.Label(main, text="Y axis column")
        self.y_label.grid(row=7, column=0, sticky="w", pady=4)
        self.y_combo = ttk.Combobox(main, textvariable=self.y_column_var, values=functions.COLUMNS, state="readonly")
        self.y_combo.grid(row=7, column=1, sticky="ew", pady=4)

        self.z_label = ttk.Label(main, text="Z axis column")
        self.z_label.grid(row=8, column=0, sticky="w", pady=4)
        self.z_combo = ttk.Combobox(main, textvariable=self.z_column_var, values=functions.COLUMNS, state="readonly")
        self.z_combo.grid(row=8, column=1, sticky="ew", pady=4)

        self.year_label = ttk.Label(main, text=f"Year ({self.min_year}-{self.max_year})")
        self.year_label.grid(row=9, column=0, sticky="w", pady=4)
        self.year_spinbox = ttk.Spinbox(main, from_=self.min_year, to=self.max_year, textvariable=self.year_var)
        self.year_spinbox.grid(row=9, column=1, sticky="ew", pady=4)

        self.month_label = ttk.Label(main, text="Month (1-12)")
        self.month_label.grid(row=10, column=0, sticky="w", pady=4)
        self.month_spinbox = ttk.Spinbox(main, from_=1, to=12, textvariable=self.month_var)
        self.month_spinbox.grid(row=10, column=1, sticky="ew", pady=4)

        self.threshold_label = ttk.Label(main, text="Stats threshold (single curve)")
        self.threshold_label.grid(row=11, column=0, sticky="w", pady=4)
        self.threshold_entry = ttk.Entry(main, textvariable=self.threshold_var)
        self.threshold_entry.grid(row=11, column=1, sticky="ew", pady=4)

        self.anomaly_z_label = ttk.Label(main, text="Anomaly z-score threshold")
        self.anomaly_z_label.grid(row=12, column=0, sticky="w", pady=4)
        self.anomaly_z_entry = ttk.Entry(main, textvariable=self.anomaly_z_var)
        self.anomaly_z_entry.grid(row=12, column=1, sticky="ew", pady=4)

        self.top_n_label = ttk.Label(main, text="Top N similar cities")
        self.top_n_label.grid(row=13, column=0, sticky="w", pady=4)
        self.top_n_spinbox = ttk.Spinbox(main, from_=1, to=max(1, len(self.station_options) - 1), textvariable=self.top_n_var)
        self.top_n_spinbox.grid(row=13, column=1, sticky="ew", pady=4)

        options_row = ttk.Frame(main)
        options_row.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(8, 8))
        options_row.columnconfigure(0, weight=1)

        ttk.Checkbutton(options_row, text="Show matplotlib windows", variable=self.show_plot_var).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(options_row, text="Run Analysis", command=self._run_analysis).grid(row=0, column=1, sticky="e")

        ttk.Label(main, text="Results").grid(row=15, column=0, sticky="w", pady=(4, 2))
        self.result_box = tk.Text(main, height=16, wrap="word")
        self.result_box.grid(row=16, column=0, columnspan=2, sticky="nsew")
        self.result_box.configure(state="disabled")

    def _bind_events(self):
        """Bind field update events."""
        self.analysis_combo.bind("<<ComboboxSelected>>", self._refresh_field_visibility)
        self.scope_combo.bind("<<ComboboxSelected>>", self._refresh_field_visibility)
        self.station1_combo.bind("<<ComboboxSelected>>", self._on_selection_change)
        self.station2_combo.bind("<<ComboboxSelected>>", self._on_selection_change)
        self.year_var.trace_add("write", self._on_year_change)

    def _on_selection_change(self, _event=None):
        """Refresh month options when station selections change."""
        self._update_month_selector()

    def _on_year_change(self, *_args):
        """Refresh month options when the year changes."""
        self._update_month_selector()

    def _set_visible(self, label_widget, input_widget, is_visible):
        """Show or hide a label/input pair."""
        if is_visible:
            label_widget.grid()
            input_widget.grid()
        else:
            label_widget.grid_remove()
            input_widget.grid_remove()

    def _current_available_months(self):
        """Return available month values for current selection context."""
        try:
            year = int(self.year_var.get())
        except ValueError:
            return []

        if year < self.min_year or year > self.max_year:
            return []

        analysis = self.analysis_var.get()
        months_station1 = set(functions.get_available_months_for_year(self.station1_var.get(), year))

        if analysis == "Compare 2 curves":
            months_station2 = set(functions.get_available_months_for_year(self.station2_var.get(), year))
            return sorted(months_station1 & months_station2)

        if analysis == "City similarity ranking":
            # Keep only months available across all comparable cities.
            shared_months = set(months_station1)
            for station_name in self.station_options:
                if station_name == self.station1_var.get():
                    continue
                station_months = set(functions.get_available_months_for_year(station_name, year))
                shared_months &= station_months
            return sorted(shared_months)

        return sorted(months_station1)

    def _update_month_selector(self):
        """Constrain month input to available months for selected year and city/cities."""
        months = self._current_available_months()

        if not months:
            self.month_label.config(text="Month (no data for current selection)")
            self.month_spinbox.config(from_=1, to=12)
            return

        self.month_spinbox.config(from_=months[0], to=months[-1])
        if len(months) == 1:
            month_text = f"{months[0]}"
        else:
            month_text = f"{months[0]}-{months[-1]}"
        self.month_label.config(text=f"Month (available: {month_text})")

        try:
            selected_month = int(self.month_var.get())
        except ValueError:
            selected_month = months[0]

        if selected_month not in months:
            self.month_var.set(str(months[0]))

    def _refresh_field_visibility(self, _event=None):
        """Toggle fields based on analysis/scope selection."""
        analysis = self.analysis_var.get()
        is_month_scope = self.scope_var.get() == "Specific month"

        is_compare = analysis == "Compare 2 curves"
        is_3d = analysis == "3D scatter"
        is_single = analysis == "Single curve"
        is_anomaly = analysis == "Anomaly detection"
        is_similarity = analysis == "City similarity ranking"

        if is_compare:
            self.station1_label.config(text="City 1")
            self.station2_label.config(text="City 2")
        else:
            self.station1_label.config(text="City")

        self._set_visible(self.station2_label, self.station2_combo, is_compare)
        self._set_visible(self.column_label, self.column_combo, not is_3d)
        self._set_visible(self.x_label, self.x_combo, is_3d)
        self._set_visible(self.y_label, self.y_combo, is_3d)
        self._set_visible(self.z_label, self.z_combo, is_3d)
        self._set_visible(self.year_label, self.year_spinbox, is_month_scope)
        self._set_visible(self.month_label, self.month_spinbox, is_month_scope)
        self._set_visible(self.threshold_label, self.threshold_entry, is_single)
        self._set_visible(self.anomaly_z_label, self.anomaly_z_entry, is_anomaly)
        self._set_visible(self.top_n_label, self.top_n_spinbox, is_similarity)
        self._update_month_selector()

    def _read_month_year(self):
        """Parse year/month fields when month filtering is enabled."""
        if self.scope_var.get() != "Specific month":
            return None, None

        year = int(self.year_var.get())
        month = int(self.month_var.get())
        if year < self.min_year or year > self.max_year:
            raise ValueError(f"Year must be between {self.min_year} and {self.max_year}.")

        valid_months = self._current_available_months()
        if not valid_months:
            raise ValueError(f"No data is available for the selected cities in {year}.")
        if month not in valid_months:
            month_text = ", ".join(str(value) for value in valid_months)
            raise ValueError(f"Month {month} is not available. Choose one of: {month_text}.")

        return year, month

    def _read_threshold(self):
        """Parse optional threshold field for single-curve stats."""
        raw = self.threshold_var.get().strip()
        if not raw:
            return None
        return float(raw)

    def _read_anomaly_z(self):
        """Parse z-score threshold for anomaly detection."""
        raw = self.anomaly_z_var.get().strip()
        if not raw:
            return 2.0
        value = float(raw)
        if value <= 0:
            raise ValueError("Anomaly z-score threshold must be > 0.")
        return value

    def _read_top_n(self):
        """Parse top-N value for similarity ranking."""
        raw = self.top_n_var.get().strip()
        if not raw:
            return 5
        value = int(raw)
        if value <= 0:
            raise ValueError("Top N must be at least 1.")
        return value

    def _run_analysis(self):
        """Execute the selected analysis and show structured results."""
        try:
            year, month = self._read_month_year()
            use_month = year is not None and month is not None
            show_plot = self.show_plot_var.get()
            analysis = self.analysis_var.get()

            if analysis == "Single curve":
                result = functions.analyze_single_curve(
                    station=self.station1_var.get(),
                    column=self.column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    threshold=self._read_threshold(),
                    show_plot=show_plot,
                )
            elif analysis == "Compare 2 curves":
                if self.station1_var.get() == self.station2_var.get():
                    raise ValueError("Pick two different cities for comparison.")
                result = functions.analyze_two_curves(
                    station1=self.station1_var.get(),
                    station2=self.station2_var.get(),
                    column=self.column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    show_plot=show_plot,
                )
            elif analysis == "Histogram":
                result = functions.analyze_histogram(
                    station=self.station1_var.get(),
                    column=self.column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    show_plot=show_plot,
                )
            elif analysis == "3D scatter":
                result = functions.analyze_3d_scatter(
                    station=self.station1_var.get(),
                    x_column=self.x_column_var.get(),
                    y_column=self.y_column_var.get(),
                    z_column=self.z_column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    show_plot=show_plot,
                )
            elif analysis == "Anomaly detection":
                result = functions.analyze_anomalies(
                    station=self.station1_var.get(),
                    column=self.column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    z_threshold=self._read_anomaly_z(),
                    show_plot=show_plot,
                )
            elif analysis == "City similarity ranking":
                result = functions.analyze_city_similarity(
                    reference_station=self.station1_var.get(),
                    column=self.column_var.get(),
                    use_month=use_month,
                    year=year,
                    month=month,
                    top_n=self._read_top_n(),
                    show_plot=show_plot,
                )
            else:
                raise ValueError("Unsupported analysis type.")

        except Exception as exc:
            messagebox.showerror("Analysis error", str(exc))
            return

        self._write_results(self._format_result(result))

    def _format_result(self, result):
        """Convert result dictionary to readable text."""
        lines = ["Analysis complete.", ""]

        for key, value in result.items():
            if key == "statistics" and isinstance(value, dict):
                lines.append("Statistics:")
                for stat_key, stat_value in value.items():
                    lines.append(f"  {stat_key}: {stat_value}")
                lines.append("")
                continue

            if key == "plot_files":
                lines.append("Saved plots:")
                for path_value in value:
                    lines.append(f"  {path_value}")
                lines.append("")
                continue

            if key in ("anomalies", "ranked_cities") and isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  {item}")
                lines.append("")
                continue

            lines.append(f"{key}: {value}")

        return "\n".join(lines).strip()

    def _write_results(self, text):
        """Write text into the results panel."""
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")


def launch_gui():
    """Launch the GUI application."""
    app = WeatherAnalysisGUI()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()
