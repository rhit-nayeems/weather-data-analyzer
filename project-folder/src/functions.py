"""
This module contains reusable weather analysis and plotting functions.

Authors: Sk Naimul Islam Nayeem, Thiago Costa
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

try:
    matplotlib.use("TkAgg")
except Exception:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

from csv_reader import read_csv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "us-weather-history"
PLOTS_DIR = BASE_DIR / "plots"

STATIONS = (
    "KCLT",
    "KCQT",
    "KHOU",
    "KIND",
    "KJAX",
    "KMDW",
    "KNYC",
    "KPHL",
    "KPHX",
    "KSEA",
)

STATION_LABELS_BY_CODE = {
    "KCLT": "Charlotte, North Carolina",
    "KCQT": "Los Angeles, California",
    "KHOU": "Houston, Texas",
    "KIND": "Indianapolis, Indiana",
    "KJAX": "Jacksonville, Florida",
    "KMDW": "Chicago, Illinois",
    "KNYC": "New York City, New York",
    "KPHL": "Philadelphia, Pennsylvania",
    "KPHX": "Phoenix, Arizona",
    "KSEA": "Seattle, Washington",
}

STATION_DISPLAY_OPTIONS = tuple(STATION_LABELS_BY_CODE[code] for code in STATIONS)
STATION_CODE_BY_DISPLAY = {label: code for code, label in STATION_LABELS_BY_CODE.items()}

COLUMNS = (
    "Mean temperature",
    "Minimum temperature",
    "Maximum temperature",
    "Average minimum temperature",
    "Average Maximum temperature",
    "Record minimum temperature",
    "Record maximum temperature",
    "Year of the record minimum",
    "Year of the record maximum",
    "Precipitation",
    "Average precipitation",
    "Record precipitation",
)


def menu():
    """Legacy console entrypoint kept for compatibility."""
    print("Console mode has been replaced by the GUI. Run main.py to launch it.")


def _resolve_plot_file(filename):
    """Resolve a plot filename against this project and ensure parent folder exists."""
    plot_path = Path(filename)
    if not plot_path.suffix:
        plot_path = plot_path.with_suffix(".png")
    if not plot_path.is_absolute():
        plot_path = (Path(__file__).resolve().parent / plot_path).resolve()
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    return plot_path


def _station_to_code(station):
    """Normalize station input (1-based index, station code, or display label)."""
    if isinstance(station, int):
        if 1 <= station <= len(STATIONS):
            return STATIONS[station - 1]
        raise ValueError(f"Station index must be in 1..{len(STATIONS)}")

    station_value = str(station).strip()
    station_code = station_value.upper()
    if station_code in STATIONS:
        return station_code

    if station_value in STATION_CODE_BY_DISPLAY:
        return STATION_CODE_BY_DISPLAY[station_value]

    valid_values = ", ".join(STATION_DISPLAY_OPTIONS)
    raise ValueError(f"Unknown station '{station}'. Valid options: {valid_values}")


def station_code_to_display(station):
    """Return the user-facing station name for a station code or label."""
    station_code = _station_to_code(station)
    return STATION_LABELS_BY_CODE.get(station_code, station_code)


def get_station_display_options():
    """Return all user-facing station names in a stable display order."""
    return STATION_DISPLAY_OPTIONS


def _column_to_display_index(column):
    """Normalize column input (0-based index or column label string)."""
    if isinstance(column, int):
        if 0 <= column < len(COLUMNS):
            return column
        raise ValueError(f"Column index must be in 0..{len(COLUMNS) - 1}")

    column_name = str(column).strip()
    if column_name not in COLUMNS:
        raise ValueError(f"Unknown column '{column}'.")
    return COLUMNS.index(column_name)


def load_station_data(station):
    """Read and return station CSV data."""
    station_code = _station_to_code(station)
    return read_csv(str(DATA_DIR / f"{station_code}.csv"))


_VALID_YEAR_RANGE = None


def get_valid_year_range():
    """Return the minimum and maximum years present in the dataset."""
    global _VALID_YEAR_RANGE

    if _VALID_YEAR_RANGE is not None:
        return _VALID_YEAR_RANGE

    min_year = None
    max_year = None
    for station_code in STATIONS:
        data = load_station_data(station_code)
        for row in data[1:]:
            year = int(str(row[0]).split("-")[0])
            if min_year is None or year < min_year:
                min_year = year
            if max_year is None or year > max_year:
                max_year = year

    if min_year is None or max_year is None:
        raise ValueError("Could not determine a valid year range from the dataset.")

    _VALID_YEAR_RANGE = (min_year, max_year)
    return _VALID_YEAR_RANGE


def get_available_months_for_year(station, year):
    """Return sorted month numbers available for a station in a specific year."""
    station_code = _station_to_code(station)
    target_year = int(year)

    months = set()
    data = load_station_data(station_code)
    for row in data[1:]:
        row_year, row_month = check_year_and_month(row[0])
        if int(row_year) == target_year:
            months.add(int(row_month))

    return tuple(sorted(months))


def get_station_date_bounds(station):
    """Return earliest and latest date strings available for a station."""
    station_code = _station_to_code(station)
    data = load_station_data(station_code)

    if len(data) <= 1:
        raise ValueError(f"No data rows found for station {station_code}.")

    parsed_dates = []
    for row in data[1:]:
        date_text = str(row[0]).strip()
        parts = date_text.split("-")
        if len(parts) < 3:
            continue
        parsed_dates.append((int(parts[0]), int(parts[1]), int(parts[2]), date_text))

    if not parsed_dates:
        raise ValueError(f"No valid date rows found for station {station_code}.")

    parsed_dates.sort()
    return parsed_dates[0][3], parsed_dates[-1][3]


def _no_data_month_message(station_code, year, month):
    """Build a clear no-data message with available months and date bounds."""
    station_label = station_code_to_display(station_code)
    months = get_available_months_for_year(station_code, year)

    if months:
        month_text = ", ".join(str(value) for value in months)
        return (
            f"No data found for {station_label} in {month}/{year}. "
            f"Available months in {year}: {month_text}."
        )

    first_date, last_date = get_station_date_bounds(station_code)
    return (
        f"No data found for {station_label} in {month}/{year}. "
        f"Dataset range is {first_date} to {last_date}."
    )


# -----------------------------------------------------------------------------
# Data extraction helpers
# -----------------------------------------------------------------------------

def get_data_whole(seq, column):
    """Extract one column from all data rows (skipping header)."""
    return tuple(row[column] for row in seq[1:])


def get_files(number):
    """Legacy helper retained for compatibility with old console workflow."""
    chosen = ()
    for _ in range(number):
        print("Choose a number from any of the following:")
        print(
            "1) KCLT",
            "2) KCQT",
            "3) KHOU",
            "4) KIND",
            "5) KJAX",
            "6) KMDW",
            "7) KNYC",
            "8) KPHL",
            "9) KPHX",
            "10) KSEA",
            sep=" ",
        )

        file_number = int(input("Which file do you want to open? "))
        while file_number in chosen:
            file_number = int(input("You already chose this file once, please choose another: "))
        chosen += (file_number,)
    return chosen


def check_year_and_month(data_point):
    """Extract year and month tokens from date strings like YYYY-M-D or YYYY-MM-DD."""
    parts = str(data_point).strip().split("-")
    if len(parts) < 2:
        raise ValueError(f"Unsupported date format: {data_point}")

    year = parts[0]
    month = str(int(parts[1]))
    return year, month


def get_data_date(seq, parameter, year, month):
    """Extract one column for rows matching a specific year and month."""
    target_year = int(year)
    target_month = int(month)

    data_date = ()
    for row in seq[1:]:
        row_year, row_month = check_year_and_month(row[0])
        if int(row_year) == target_year and int(row_month) == target_month:
            data_date += (row[parameter],)
    return data_date


def get_headers(seq):
    """Return all date values (column 0) excluding header row."""
    return tuple(row[0] for row in seq[1:])


# -----------------------------------------------------------------------------
# File comparison helpers
# -----------------------------------------------------------------------------

def compare_two_files_month(file_number1, file_number2, parameter, year, month):
    """Return absolute point-by-point differences between two files for one month."""
    file1 = load_station_data(file_number1)
    file2 = load_station_data(file_number2)
    data_period_file1 = get_data_date(file1, parameter, year, month)
    data_period_file2 = get_data_date(file2, parameter, year, month)
    point_count = min(len(data_period_file1), len(data_period_file2))
    return tuple(
        abs(data_period_file1[point] - data_period_file2[point])
        for point in range(point_count)
    )


def compare_two_files(file_number1, file_number2, parameter):
    """Return absolute point-by-point differences between two whole files."""
    file1 = load_station_data(file_number1)
    file2 = load_station_data(file_number2)
    data_period_file1 = get_data_whole(file1, parameter)
    data_period_file2 = get_data_whole(file2, parameter)
    point_count = min(len(data_period_file1), len(data_period_file2))
    return tuple(
        abs(data_period_file1[point] - data_period_file2[point])
        for point in range(point_count)
    )


def two_files_to_plot_whole(file_number1, file_number2, parameter):
    """Return one column from two whole files."""
    file1 = load_station_data(file_number1)
    file2 = load_station_data(file_number2)
    data_period_file1 = get_data_whole(file1, parameter)
    data_period_file2 = get_data_whole(file2, parameter)
    return data_period_file1, data_period_file2


def two_files_to_plot_month(file_number1, file_number2, parameter, year, month):
    """Return dates and one column from two files for one month."""
    file1 = load_station_data(file_number1)
    file2 = load_station_data(file_number2)
    data_period_file1 = get_data_date(file1, parameter, year, month)
    data_period_file2 = get_data_date(file2, parameter, year, month)
    dates = get_data_date(file1, 0, year, month)
    point_count = min(len(data_period_file1), len(data_period_file2), len(dates))
    return dates[:point_count], data_period_file1[:point_count], data_period_file2[:point_count]


# -----------------------------------------------------------------------------
# Temperature helpers
# -----------------------------------------------------------------------------

def temperature_amplitude_whole(seq):
    """Return daily max-min temperature amplitude for a whole file."""
    max_temp_list = get_data_whole(seq, 3)
    min_temp_list = get_data_whole(seq, 2)
    point_count = min(len(max_temp_list), len(min_temp_list))
    return tuple(max_temp_list[i] - min_temp_list[i] for i in range(point_count))


def temperature_amplitude_month(seq, year, month):
    """Return daily max-min temperature amplitude for a specific month."""
    max_temp_list = get_data_date(seq, 3, year, month)
    min_temp_list = get_data_date(seq, 2, year, month)
    point_count = min(len(max_temp_list), len(min_temp_list))
    return tuple(max_temp_list[i] - min_temp_list[i] for i in range(point_count))


# -----------------------------------------------------------------------------
# Statistics helpers
# -----------------------------------------------------------------------------

def above_threshold(data_seq, threshold):
    """Count values >= threshold."""
    total = 0
    for value in data_seq:
        if value >= threshold:
            total += 1
    return total


def below_threshold(data_seq, threshold):
    """Count values <= threshold."""
    total = 0
    for value in data_seq:
        if value <= threshold:
            total += 1
    return total


def average_change(seq):
    """Return average point-to-point change across a sequence."""
    if len(seq) < 2:
        return 0.0
    return (seq[-1] - seq[0]) / (len(seq) - 1)


def highest_in_sequence(seq):
    """Return (highest value, index) from a sequence."""
    if not seq:
        raise ValueError("Sequence is empty.")

    biggest = seq[0]
    biggest_index = 0
    for index, value in enumerate(seq):
        if value > biggest:
            biggest = value
            biggest_index = index
    return biggest, biggest_index


def lowest_in_sequence(seq):
    """Return (lowest value, index) from a sequence."""
    if not seq:
        raise ValueError("Sequence is empty.")

    lowest = seq[0]
    lowest_index = 0
    for index, value in enumerate(seq):
        if value < lowest:
            lowest = value
            lowest_index = index
    return lowest, lowest_index


def get_average(seq):
    """Return sequence average."""
    if not seq:
        raise ValueError("Sequence is empty.")
    return sum(seq) / len(seq)


def get_standard_deviation(data_seq):
    """Return sequence standard deviation (population)."""
    if not data_seq:
        raise ValueError("Sequence is empty.")

    average = get_average(data_seq)
    squared_sum = 0.0
    for value in data_seq:
        squared_sum += (value - average) ** 2
    return math.sqrt(squared_sum / len(data_seq))


def statistics_whole(seq, threshold=None):
    """Return common summary statistics for a sequence."""
    if not seq:
        raise ValueError("Cannot calculate statistics for empty data.")

    highest_value, highest_index = highest_in_sequence(seq)
    lowest_value, lowest_index = lowest_in_sequence(seq)
    stats = {
        "average": get_average(seq),
        "standard_deviation": get_standard_deviation(seq),
        "highest_value": highest_value,
        "highest_index": highest_index,
        "lowest_value": lowest_value,
        "lowest_index": lowest_index,
        "average_change": average_change(seq),
    }

    if threshold is not None:
        stats["threshold"] = threshold
        stats["count_at_or_above_threshold"] = above_threshold(seq, threshold)
        stats["count_at_or_below_threshold"] = below_threshold(seq, threshold)

    return stats


def statistics_month(seq, threshold=None):
    """Alias of statistics_whole kept for compatibility."""
    return statistics_whole(seq, threshold)


# -----------------------------------------------------------------------------
# Plot helpers
# -----------------------------------------------------------------------------

def plot_data(x, y, xlabel, ylabel, title, filename, show_plot=False):
    """Create and save a line plot."""
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    if len(x) > 1:
        interval = max(1, len(x) // 12)
        ax.set_xticks(range(0, len(x), interval))
        ax.set_xticklabels(x[::interval], rotation=45, ha="right")

    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def plot_data_month(x, y, xlabel, ylabel, title, filename, show_plot=False):
    """Create and save a monthly line plot."""
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    if len(x) > 1:
        interval = max(1, len(x) // 6)
        ax.set_xticks(range(0, len(x), interval))
        ax.set_xticklabels(x[::interval], rotation=45, ha="right")

    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def plot_two_curves(data1, label1, data2, label2, title, filename, x_values=None, y_label="Data", show_plot=False):
    """Create and save a two-curve comparison plot."""
    fig, ax = plt.subplots()

    if x_values is None:
        ax.plot(data1, label=label1)
        ax.plot(data2, label=label2)
        ax.set_xlabel("Index")
    else:
        ax.plot(x_values, data1, label=label1)
        ax.plot(x_values, data2, label=label2)
        ax.set_xlabel("Date")

        if len(x_values) > 1:
            interval = max(1, len(x_values) // 6)
            ax.set_xticks(range(0, len(x_values), interval))
            ax.set_xticklabels(x_values[::interval], rotation=45, ha="right")

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def histogram_plot(data, column_index, title, xlabel, ylabel, filename, show_plot=False):
    """Create and save a histogram from whole-file data."""
    column_to_plot = get_data_whole(data, column_index)
    if not column_to_plot:
        raise ValueError("No data available to plot histogram.")

    fig, ax = plt.subplots()
    ax.hist(column_to_plot, bins=80, color="blue", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def histogram_plot_month(data, year, month, column_index, title, xlabel, ylabel, filename, show_plot=False):
    """Create and save a histogram from month-filtered data."""
    column_to_plot = get_data_date(data, column_index, year, month)
    if not column_to_plot:
        raise ValueError("No data available to plot histogram for the selected month.")

    fig, ax = plt.subplots()
    ax.hist(column_to_plot, bins=80, color="blue", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def scatter_3d_plot(data, x_column, y_column, z_column, title, xlabel, ylabel, zlabel, filename, show_plot=False):
    """Create and save a whole-file 3D scatter plot."""
    x_data = get_data_whole(data, x_column)
    y_data = get_data_whole(data, y_column)
    z_data = get_data_whole(data, z_column)

    point_count = min(len(x_data), len(y_data), len(z_data))
    if point_count == 0:
        raise ValueError("No data available to plot 3D chart.")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x_data[:point_count], y_data[:point_count], z_data[:point_count], c="blue", marker="o")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


def scatter_3d_plot_month(data, year, month, x_column, y_column, z_column, title, xlabel, ylabel, zlabel, filename,
                          show_plot=False):
    """Create and save a month-filtered 3D scatter plot."""
    x_data = get_data_date(data, x_column, year, month)
    y_data = get_data_date(data, y_column, year, month)
    z_data = get_data_date(data, z_column, year, month)

    point_count = min(len(x_data), len(y_data), len(z_data))
    if point_count == 0:
        raise ValueError("No data available to plot 3D chart for the selected month.")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x_data[:point_count], y_data[:point_count], z_data[:point_count], c="blue", marker="o")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)
    return str(plot_path)


# -----------------------------------------------------------------------------
# GUI-facing orchestration helpers
# -----------------------------------------------------------------------------

def analyze_single_curve(station, column, use_month=False, year=None, month=None, threshold=None, show_plot=False):
    """Analyze one station and one metric, then return stats and generated plot files."""
    station_code = _station_to_code(station)
    station_label = station_code_to_display(station_code)
    column_index = _column_to_display_index(column)
    csv_column = column_index + 1
    data = load_station_data(station_code)

    plot_files = []
    if use_month:
        if year is None or month is None:
            raise ValueError("Year and month are required when month filtering is enabled.")

        x_data = get_data_date(data, 0, year, month)
        y_data = get_data_date(data, csv_column, year, month)
        if not y_data:
            raise ValueError(_no_data_month_message(station_code, year, month))

        plot_files.append(
            plot_data_month(
                x_data,
                y_data,
                "Date",
                COLUMNS[column_index],
                f"{COLUMNS[column_index]} in {station_label} ({month}/{year})",
                str(PLOTS_DIR / f"{station_code}_{COLUMNS[column_index]}({month}.{year}).png"),
                show_plot=show_plot,
            )
        )

        if column_index in (0, 1, 2):
            amplitude = temperature_amplitude_month(data, year, month)
            plot_files.append(
                plot_data_month(
                    x_data,
                    amplitude,
                    "Date",
                    "Temperature Amplitude",
                    f"Temperature amplitude in {station_label} ({month}/{year})",
                    str(PLOTS_DIR / f"temp_amplitude_{station_code}_{month}_{year}.png"),
                    show_plot=show_plot,
                )
            )
    else:
        x_data = get_headers(data)
        y_data = get_data_whole(data, csv_column)
        if not y_data:
            raise ValueError("No data found for the selected station.")

        plot_files.append(
            plot_data(
                x_data,
                y_data,
                "Date",
                COLUMNS[column_index],
                f"{COLUMNS[column_index]} in {station_label}",
                str(PLOTS_DIR / f"{station_code}_{COLUMNS[column_index]}.png"),
                show_plot=show_plot,
            )
        )

        if column_index in (0, 1, 2):
            amplitude = temperature_amplitude_whole(data)
            plot_files.append(
                plot_data(
                    x_data,
                    amplitude,
                    "Date",
                    "Temperature Amplitude",
                    f"Temperature amplitude in {station_label}",
                    str(PLOTS_DIR / f"temp_amplitude_{station_code}.png"),
                    show_plot=show_plot,
                )
            )

    return {
        "station": station_label,
        "column": COLUMNS[column_index],
        "point_count": len(y_data),
        "statistics": statistics_whole(y_data, threshold=threshold),
        "plot_files": plot_files,
    }


def analyze_two_curves(station1, station2, column, use_month=False, year=None, month=None, show_plot=False):
    """Compare two stations on one metric and return generated plot files."""
    station_code1 = _station_to_code(station1)
    station_code2 = _station_to_code(station2)
    station_label1 = station_code_to_display(station_code1)
    station_label2 = station_code_to_display(station_code2)
    column_index = _column_to_display_index(column)
    csv_column = column_index + 1

    data1 = load_station_data(station_code1)
    data2 = load_station_data(station_code2)

    if use_month:
        if year is None or month is None:
            raise ValueError("Year and month are required when month filtering is enabled.")

        x_data = get_data_date(data1, 0, year, month)
        curve1 = get_data_date(data1, csv_column, year, month)
        curve2 = get_data_date(data2, csv_column, year, month)
    else:
        x_data = get_headers(data1)
        curve1 = get_data_whole(data1, csv_column)
        curve2 = get_data_whole(data2, csv_column)

    point_count = min(len(x_data), len(curve1), len(curve2))
    if point_count == 0:
        if use_month:
            if not curve1:
                raise ValueError(_no_data_month_message(station_code1, year, month))
            if not curve2:
                raise ValueError(_no_data_month_message(station_code2, year, month))
            raise ValueError(f"No overlapping data points available for {month}/{year}.")
        raise ValueError("No overlapping data points available for comparison.")

    x_data = x_data[:point_count]
    curve1 = curve1[:point_count]
    curve2 = curve2[:point_count]

    suffix = f"_{month}_{year}" if use_month else ""
    title_suffix = f" ({month}/{year})" if use_month else ""

    comparison_file = plot_two_curves(
        curve1,
        station_label1,
        curve2,
        station_label2,
        f"Comparison of {COLUMNS[column_index]}{title_suffix}",
        str(PLOTS_DIR / f"{station_code1}_{station_code2}_{COLUMNS[column_index]}{suffix}.png"),
        x_values=x_data,
        y_label=COLUMNS[column_index],
        show_plot=show_plot,
    )

    difference = tuple(abs(curve1[i] - curve2[i]) for i in range(point_count))
    difference_file = plot_data(
        x_data,
        difference,
        "Date",
        "Difference",
        f"Difference between {station_label1} and {station_label2}{title_suffix}",
        str(PLOTS_DIR / f"Difference_{station_code1}_{station_code2}_{COLUMNS[column_index]}{suffix}.png"),
        show_plot=show_plot,
    )

    return {
        "stations": (station_label1, station_label2),
        "column": COLUMNS[column_index],
        "point_count": point_count,
        "average_difference": get_average(difference),
        "plot_files": [comparison_file, difference_file],
    }


def analyze_histogram(station, column, use_month=False, year=None, month=None, show_plot=False):
    """Generate a histogram for one station and one metric."""
    station_code = _station_to_code(station)
    station_label = station_code_to_display(station_code)
    column_index = _column_to_display_index(column)
    csv_column = column_index + 1
    data = load_station_data(station_code)

    if use_month:
        if year is None or month is None:
            raise ValueError("Year and month are required when month filtering is enabled.")

        month_data = get_data_date(data, csv_column, year, month)
        if not month_data:
            raise ValueError(_no_data_month_message(station_code, year, month))

        file_path = histogram_plot_month(
            data,
            year,
            month,
            csv_column,
            f"Histogram of {COLUMNS[column_index]} in {station_label} ({month}/{year})",
            COLUMNS[column_index],
            "Frequency",
            str(PLOTS_DIR / f"Histogram_{station_code}_{COLUMNS[column_index]}_{month}_{year}.png"),
            show_plot=show_plot,
        )
    else:
        file_path = histogram_plot(
            data,
            csv_column,
            f"Histogram of {COLUMNS[column_index]} in {station_label}",
            COLUMNS[column_index],
            "Frequency",
            str(PLOTS_DIR / f"Histogram_{station_code}_{COLUMNS[column_index]}.png"),
            show_plot=show_plot,
        )

    return {
        "station": station_label,
        "column": COLUMNS[column_index],
        "plot_files": [file_path],
    }


def analyze_3d_scatter(station, x_column, y_column, z_column, use_month=False, year=None, month=None,
                       show_plot=False):
    """Generate a 3D scatter plot for one station using three metrics."""
    station_code = _station_to_code(station)
    station_label = station_code_to_display(station_code)
    x_index = _column_to_display_index(x_column)
    y_index = _column_to_display_index(y_column)
    z_index = _column_to_display_index(z_column)

    data = load_station_data(station_code)

    if use_month:
        if year is None or month is None:
            raise ValueError("Year and month are required when month filtering is enabled.")

        x_data = get_data_date(data, x_index + 1, year, month)
        y_data = get_data_date(data, y_index + 1, year, month)
        z_data = get_data_date(data, z_index + 1, year, month)
        if not x_data or not y_data or not z_data:
            raise ValueError(_no_data_month_message(station_code, year, month))

        plot_file = scatter_3d_plot_month(
            data,
            year,
            month,
            x_index + 1,
            y_index + 1,
            z_index + 1,
            f"{COLUMNS[x_index]}, {COLUMNS[y_index]}, {COLUMNS[z_index]} in {station_label} ({month}/{year})",
            COLUMNS[x_index],
            COLUMNS[y_index],
            COLUMNS[z_index],
            str(PLOTS_DIR / f"3D_{station_code}_{x_index + 1}_{y_index + 1}_{z_index + 1}_{month}_{year}.png"),
            show_plot=show_plot,
        )
    else:
        plot_file = scatter_3d_plot(
            data,
            x_index + 1,
            y_index + 1,
            z_index + 1,
            f"{COLUMNS[x_index]}, {COLUMNS[y_index]}, {COLUMNS[z_index]} in {station_label}",
            COLUMNS[x_index],
            COLUMNS[y_index],
            COLUMNS[z_index],
            str(PLOTS_DIR / f"3D_{station_code}_{x_index + 1}_{y_index + 1}_{z_index + 1}.png"),
            show_plot=show_plot,
        )

    return {
        "station": station_label,
        "columns": (COLUMNS[x_index], COLUMNS[y_index], COLUMNS[z_index]),
        "plot_files": [plot_file],
    }


# -----------------------------------------------------------------------------
# Advanced analytics helpers
# -----------------------------------------------------------------------------

def detect_anomalies(values, z_threshold=2.0):
    """Detect anomalies using absolute z-score thresholding.

    Returns a tuple: (anomaly_records, mean_value, std_dev).
    Each anomaly record contains: index, value, z_score.
    """
    if not values:
        raise ValueError("Cannot detect anomalies on empty data.")
    if z_threshold <= 0:
        raise ValueError("z_threshold must be greater than 0.")

    mean_value = get_average(values)
    std_dev = get_standard_deviation(values)
    if std_dev == 0:
        return [], mean_value, std_dev

    anomalies = []
    for index, value in enumerate(values):
        z_score = (value - mean_value) / std_dev
        if abs(z_score) >= z_threshold:
            anomalies.append(
                {
                    "index": index,
                    "value": value,
                    "z_score": z_score,
                }
            )

    anomalies.sort(key=lambda item: abs(item["z_score"]), reverse=True)
    return anomalies, mean_value, std_dev


def _pearson_correlation(values1, values2):
    """Calculate Pearson correlation for two equally-sized numeric sequences."""
    point_count = min(len(values1), len(values2))
    if point_count < 2:
        return 0.0

    seq1 = values1[:point_count]
    seq2 = values2[:point_count]

    mean1 = get_average(seq1)
    mean2 = get_average(seq2)

    variance1 = sum((value - mean1) ** 2 for value in seq1) / point_count
    variance2 = sum((value - mean2) ** 2 for value in seq2) / point_count
    if variance1 == 0 or variance2 == 0:
        return 0.0

    covariance = sum((seq1[i] - mean1) * (seq2[i] - mean2) for i in range(point_count)) / point_count
    return covariance / math.sqrt(variance1 * variance2)


def calculate_similarity_metrics(values1, values2):
    """Calculate similarity metrics between two numeric sequences.

    Returns RMSE, MAE, and Pearson correlation.
    """
    point_count = min(len(values1), len(values2))
    if point_count == 0:
        raise ValueError("Cannot calculate similarity metrics with no overlapping points.")

    seq1 = values1[:point_count]
    seq2 = values2[:point_count]
    differences = [seq1[i] - seq2[i] for i in range(point_count)]

    mae = sum(abs(delta) for delta in differences) / point_count
    rmse = math.sqrt(sum(delta * delta for delta in differences) / point_count)
    correlation = _pearson_correlation(seq1, seq2)

    return {
        "rmse": rmse,
        "mae": mae,
        "correlation": correlation,
    }


def _align_series_by_date(dates1, values1, dates2, values2):
    """Align two time-series by shared date labels."""
    point_count2 = min(len(dates2), len(values2))
    values_by_date2 = {dates2[i]: values2[i] for i in range(point_count2)}

    aligned_dates = []
    aligned_values1 = []
    aligned_values2 = []

    point_count1 = min(len(dates1), len(values1))
    for i in range(point_count1):
        date_value = dates1[i]
        if date_value in values_by_date2:
            aligned_dates.append(date_value)
            aligned_values1.append(values1[i])
            aligned_values2.append(values_by_date2[date_value])

    return tuple(aligned_dates), tuple(aligned_values1), tuple(aligned_values2)


def _load_series_for_station(station_code, csv_column, use_month=False, year=None, month=None):
    """Load date/value series for one station and column."""
    data = load_station_data(station_code)

    if use_month:
        if year is None or month is None:
            raise ValueError("Year and month are required when month filtering is enabled.")
        dates = get_data_date(data, 0, year, month)
        values = get_data_date(data, csv_column, year, month)
        if not values:
            raise ValueError(_no_data_month_message(station_code, year, month))
    else:
        dates = get_headers(data)
        values = get_data_whole(data, csv_column)
        if not values:
            raise ValueError(f"No data found for {station_code_to_display(station_code)}.")

    return dates, values


def plot_anomaly_detection(dates, values, anomaly_indices, title, ylabel, filename, show_plot=False):
    """Plot a line chart and highlight anomaly points."""
    fig, ax = plt.subplots()
    ax.plot(dates, values, color="steelblue", label="Value")

    if anomaly_indices:
        x_points = [dates[index] for index in anomaly_indices if index < len(dates)]
        y_points = [values[index] for index in anomaly_indices if index < len(values)]
        ax.scatter(x_points, y_points, color="crimson", label="Anomaly", zorder=3)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)

    if len(dates) > 1:
        interval = max(1, len(dates) // 12)
        ax.set_xticks(range(0, len(dates), interval))
        ax.set_xticklabels(dates[::interval], rotation=45, ha="right")

    ax.legend()
    ax.grid()
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)

    return str(plot_path)


def plot_similarity_ranking(reference_city, ranking_items, filename, show_plot=False):
    """Plot a bar chart of city similarity ranking (RMSE lower is better)."""
    if not ranking_items:
        raise ValueError("No ranking data available to plot.")

    labels = [item["city"] for item in ranking_items]
    scores = [item["rmse"] for item in ranking_items]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(len(labels)), scores, color="#2a9d8f")

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("RMSE (lower is more similar)")
    ax.set_title(f"City Similarity to {reference_city}")

    for i, bar in enumerate(bars):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {scores[i]:.2f}",
            va="center",
            ha="left",
        )

    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    plot_path = _resolve_plot_file(filename)
    fig.savefig(plot_path)

    if show_plot:
        plt.show(block=False)
    else:
        plt.close(fig)

    return str(plot_path)


def analyze_anomalies(station, column, use_month=False, year=None, month=None, z_threshold=2.0,
                      show_plot=False, max_results=15):
    """Detect and summarize anomalies for one station/metric."""
    station_code = _station_to_code(station)
    station_label = station_code_to_display(station_code)
    column_index = _column_to_display_index(column)
    csv_column = column_index + 1

    dates, values = _load_series_for_station(
        station_code,
        csv_column,
        use_month=use_month,
        year=year,
        month=month,
    )

    anomalies, mean_value, std_dev = detect_anomalies(values, z_threshold=z_threshold)
    anomaly_indices = [item["index"] for item in anomalies]

    suffix = f"_{month}_{year}" if use_month else ""
    title_suffix = f" ({month}/{year})" if use_month else ""
    plot_file = plot_anomaly_detection(
        dates,
        values,
        anomaly_indices,
        f"Anomaly Detection: {COLUMNS[column_index]} in {station_label}{title_suffix}",
        COLUMNS[column_index],
        str(PLOTS_DIR / f"Anomaly_{station_code}_{COLUMNS[column_index]}{suffix}.png"),
        show_plot=show_plot,
    )

    top_anomalies = []
    for item in anomalies[:max_results]:
        index = item["index"]
        if index < len(dates):
            date_value = dates[index]
        else:
            date_value = f"Index {index}"
        top_anomalies.append(
            {
                "date": date_value,
                "value": item["value"],
                "z_score": round(item["z_score"], 3),
            }
        )

    return {
        "station": station_label,
        "column": COLUMNS[column_index],
        "z_threshold": z_threshold,
        "mean": round(mean_value, 3),
        "standard_deviation": round(std_dev, 3),
        "point_count": len(values),
        "anomaly_count": len(anomalies),
        "anomalies": top_anomalies,
        "plot_files": [plot_file],
    }


def analyze_city_similarity(reference_station, column, use_month=False, year=None, month=None,
                            top_n=5, show_plot=False):
    """Rank other cities by similarity to the reference city for one metric."""
    reference_code = _station_to_code(reference_station)
    reference_label = station_code_to_display(reference_code)
    column_index = _column_to_display_index(column)
    csv_column = column_index + 1

    if top_n is None:
        top_n = len(STATIONS) - 1
    top_n = int(top_n)
    if top_n <= 0:
        raise ValueError("top_n must be at least 1.")

    ref_dates, ref_values = _load_series_for_station(
        reference_code,
        csv_column,
        use_month=use_month,
        year=year,
        month=month,
    )

    ranking = []
    for station_code in STATIONS:
        if station_code == reference_code:
            continue

        try:
            other_dates, other_values = _load_series_for_station(
                station_code,
                csv_column,
                use_month=use_month,
                year=year,
                month=month,
            )
        except ValueError:
            continue

        aligned_dates, aligned_ref, aligned_other = _align_series_by_date(ref_dates, ref_values, other_dates, other_values)
        if not aligned_ref:
            continue

        metrics = calculate_similarity_metrics(aligned_ref, aligned_other)
        ranking.append(
            {
                "city": station_code_to_display(station_code),
                "rmse": round(metrics["rmse"], 3),
                "mae": round(metrics["mae"], 3),
                "correlation": round(metrics["correlation"], 3),
                "overlap_days": len(aligned_dates),
            }
        )

    if not ranking:
        raise ValueError("No comparable cities found for the selected filters.")

    ranking.sort(key=lambda item: item["rmse"])
    top_n = min(top_n, len(ranking))
    ranking_top = ranking[:top_n]

    suffix = f"_{month}_{year}" if use_month else ""
    plot_file = plot_similarity_ranking(
        reference_label,
        ranking_top,
        str(PLOTS_DIR / f"Similarity_{reference_code}_{COLUMNS[column_index]}{suffix}.png"),
        show_plot=show_plot,
    )

    return {
        "reference_city": reference_label,
        "column": COLUMNS[column_index],
        "ranking_metric": "RMSE (lower is more similar)",
        "ranked_cities": ranking_top,
        "plot_files": [plot_file],
    }
