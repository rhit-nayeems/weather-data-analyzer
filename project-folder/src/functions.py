"""
This module contains code for the final course project in
CSSE 120 - Introduction to Software Development.

This module contains functions written for the project.

Authors: Sk Naimul Islam Nayeem, Thiago Costa
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from csv_reader import read_csv
import math


# -----------------------------------------------------------------------------
# TO DO:
#   Write your functions below this _TODO_.
#   Make sure each function has a complete doc-string to go with it!
#  _
#   Alternatively, you may write your functions in multiple files. A good
#   organizational strategy is to group functions by purpose. All function
#   code files should be named  <description of functions>_functions.py,
#   where  <description of functions>  is a placeholder.
# -----------------------------------------------------------------------------

def menu():
    """
        Display the main menu for the US Weather Data Analysis Tool.

        This function continuously prompts the user to choose from various options and performs actions accordingly.

        The user is prompted to enter their desired option, and the corresponding action is taken based on the input.

        Returns:
        None
        """

    columns = (
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
        "Record precipitation"
    )
    files = (" ", "KCLT", "KCQT", "KHOU", "KIND", "KJAX", "KMDW", "KNYC", "KPHL", "KPHX", "KSEA")
    while True:
        print("Hello, welcome to our US Weather Data Analysis Tool!")
        print("This program was developed by Thiago Costa and Sk Nayeem for the CSSE120 Final Project")
        print("1) Plot a single curve", "2) Plot 2 curves", "3) Plot a histogram", "4) Plot a 3D Graph",
              sep=" ")
        option_action = input("What option do you want? ")
        if option_action == "1":
            list = get_files(1)
            print("1) Plot data from the whole file  2)Plot data from a specific month")
            period = input("Choose an option: ")
            if period == "1":
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                seq_to_plot = get_data_whole(data_to_plot, column_chosen + 1)
                plot_headers = get_headers(data_to_plot)
                plot_data(plot_headers, seq_to_plot, "Date", columns[column_chosen],
                          columns[column_chosen] + " over the year", "../plots/" +
                          files[list[0]] + "_" + columns[column_chosen] + ".png")
                if column_chosen in (0, 1, 2):
                    amplitude = temperature_amplitude_whole(data_to_plot)
                    plot_data(plot_headers, amplitude, "Date", "Temperature Amplitude",
                              "Temperature amplitude of " + files[list[0]],
                              "../plots/temp_amplitude" + files[list[0]] + "_.png")
                statistics_whole(seq_to_plot)
            elif period == "2":
                year = int(input("Choose the year: "))
                month = int(input("Choose the month: "))
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                seq_to_plot = get_data_date(data_to_plot, column_chosen + 1, year, month)
                plot_headers = get_data_date(data_to_plot, 0, year, month)
                plot_data_month(plot_headers, seq_to_plot, "Date", columns[column_chosen],
                                columns[column_chosen] + " (" + str(month) + "/" + str(year) + ")", "../plots/" +
                                files[list[0]] + "_" + columns[column_chosen] +
                                "(" + str(month) + "." + str(year) + ").png")
                if column_chosen in (0, 1, 2):
                    amplitude = temperature_amplitude_month(data_to_plot, year, month)
                    plot_data_month(plot_headers, amplitude, "Date", "Temperature Amplitude",
                                    "Temperature amplitude of " + files[list[0]] + " (" + str(month) +
                                    "/" + str(year) + ")",
                                    "../plots/temp_amplitude" + files[list[0]] + "_.png")
                statistics_whole(seq_to_plot)
        elif option_action == "2":
            list = get_files(2)
            print("1) Plot all the data from the files  2)Plot data from a specific month")
            period = input("Choose an option: ")
            if period == "1":
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                data1, data2 = two_files_to_plot_whole(list[0], list[1], column_chosen + 1)
                plot_two_curves(data1, files[list[0]], data2, files[list[1]], "Comparison of " +
                                columns[column_chosen],
                                "../plots/" + files[list[0]] + "_" + files[list[1]] + "_" +
                                columns[column_chosen] + ".png")
                difference = compare_two_files(list[0], list[1], column_chosen + 1)
                data_with_headers = read_csv(f"../data/us-weather-history/" + files[list[0]] + ".csv")
                plot_headers = get_headers(data_with_headers)
                plot_data(plot_headers, difference, "Date", "Difference",
                          "Difference between " + files[list[0]] + " and " + files[list[1]],
                          "../plots/Difference_" + files[list[0]] + "_" + files[list[1]] + "_" +
                          columns[column_chosen] + ".png")
            elif period == "2":
                year = int(input("Choose the year: "))
                month = int(input("Choose the month: "))
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                dates, data1, data2 = two_files_to_plot_month(list[0], list[1], column_chosen + 1, year, month)
                plot_two_curves(data1, files[list[0]], data2, files[list[1]], "Comparison of " + columns[column_chosen]
                                + " (" + str(month) + "." + str(year) + ")",
                                "../plots/" + files[list[0]] + "_" + files[list[1]] + "_" +
                                " (" + str(month) + "." + str(year) + ")_" + columns[column_chosen] + ".png")
        elif option_action == "3":
            list = get_files(1)
            print("1) Plot data from the whole file  2)Plot data from a specific month")
            period = input("Choose an option: ")
            if period == "1":
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                histogram_plot(data_to_plot, column_chosen + 1, "Histogram of " + columns[column_chosen],
                               columns[column_chosen], "Frequency", "../plots/Histogram_" + files[list[0]]
                               + "_" + columns[column_chosen] + ".png")
            elif period == "2":
                year = int(input("Choose the year: "))
                month = int(input("Choose the month: "))
                print("What data do you want to plot?\n")
                for i in range(len(columns)):
                    print(i + 1, ")", columns[i])
                column_chosen = int(input("Choose an option: ")) - 1
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                histogram_plot_month(data_to_plot, year, month, column_chosen + 1,
                                     "Histogram of " + columns[column_chosen] +
                                     " (" + str(month) + "/" + str(year) + ")",
                                     columns[column_chosen], "Frequency", "../plots/Histogram_" + files[list[0]]
                                     + "_" + columns[column_chosen] + ".png")
        elif option_action == "4":
            list = get_files(1)
            print("1) Plot data from the whole file  2)Plot data from a specific month")
            period = input("Choose an option: ")
            if period == "1":
                print("What data do you want to plot?\n")
                xyz = ()
                for axis in range(3):
                    for i in range(len(columns)):
                        print(str(i + 1) + ")" + columns[i])
                    if axis == 0:
                        xyz += (int(input("Choose the X axis: ")) - 1,)
                    elif axis == 1:
                        xyz += (int(input("Choose the Y axis: ")) - 1,)
                    elif axis == 2:
                        xyz += (int(input("Choose the Z axis: ")) - 1,)
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                scatter_3d_plot(data_to_plot, xyz[0] + 1, xyz[1] + 1, xyz[2] + 1,
                                columns[xyz[0]] + ", " + columns[xyz[1]] + ", " + columns[xyz[2]],
                                columns[xyz[0]], columns[xyz[1]], columns[xyz[2]],
                                "../plots/3D_" + files[list[0]] + str(xyz[0] + 1) + "_" + str(xyz[1] + 1) +
                                "_" + str(xyz[2] + 1))
            elif period == "2":
                year = int(input("Choose the year: "))
                month = int(input("Choose the month: "))
                print("What data do you want to plot?\n")
                xyz = ()
                for axis in range(3):
                    for i in range(len(columns)):
                        print(str(i + 1) + ")" + columns[i])
                    if axis == 0:
                        xyz += (int(input("Choose the X axis: ")) - 1,)
                    elif axis == 1:
                        xyz += (int(input("Choose the Y axis: ")) - 1,)
                    elif axis == 2:
                        xyz += (int(input("Choose the Z axis: ")) - 1,)
                data_to_plot = read_csv("../data/us-weather-history/" + files[list[0]] + ".csv")
                scatter_3d_plot_month(data_to_plot, year, month, xyz[0] + 1, xyz[1] + 1, xyz[2] + 1,
                                      columns[xyz[0]] + ", " + columns[xyz[1]] + ", " + columns[xyz[2]] +
                                      " (" + str(month) + "/" + str(year) + ")",
                                      columns[xyz[0]], columns[xyz[1]], columns[xyz[2]],
                                      "../plots/3D_" + str(year) + "." + str(month) + "_" +
                                      files[list[0]] + str(xyz[0] + 1) + "_" + str(xyz[1] + 1) +
                                      "_" + str(xyz[2] + 1) + ".png")
        else:
            print("Please select an available option")


def histogram_plot(data, column_index, title, xlabel, ylabel, filename):
    """
        Generate and save a histogram plot for a specific column in the input dataset.

        Parameters:
        - data (list): The input dataset.
        - column_index (int): The index of the column to plot.
        - title (str): The title of the histogram plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - filename (str): The name of the file to save the histogram plot.

        Returns:
        None
    """

    column_to_plot = get_data_whole(data, column_index)

    fig, ax = plt.subplots()
    ax.hist(column_to_plot, bins=80, color='blue', edgecolor='black')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()
    ax.grid()

    fig.savefig(filename)
    print("Histogram plot saved to", filename)
    plt.show()


def histogram_plot_month(data, year, month, column_index, title, xlabel, ylabel, filename):
    """
        Generate a histogram plot for a specific month and year from the given data.

        Parameters:
        - data: The input dataset.
        - year (int): The target year for filtering the data.
        - month (int): The target month for filtering the data (1-12).
        - column_index (int): The index of the column in the data to be plotted.
        - title (str): The title of the histogram plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - filename (str): The name of the file to save the histogram plot.

        Returns:
        None
    """

    column_to_plot = get_data_date(data, column_index, year, month)

    fig, ax = plt.subplots()
    ax.hist(column_to_plot, bins=80, color='blue', edgecolor='black')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()
    ax.grid()

    fig.savefig(filename)
    print("Histogram plot saved to", filename)
    plt.show()


def scatter_3d_plot(data, x_column, y_column, z_column, title, xlabel, ylabel, zlabel, filename):
    """
        Generate and save a 3D scatter plot using specified columns from the input dataset.

        Parameters:
        - data (list): The input dataset.
        - x_column (int): The index of the column for the x-axis.
        - y_column (int): The index of the column for the y-axis.
        - z_column (int): The index of the column for the z-axis.
        - title (str): The title of the 3D scatter plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - zlabel (str): The label for the z-axis.
        - filename (str): The name of the file to save the 3D scatter plot.

        Returns:
        None
    """
    x_data = get_data_whole(data, x_column)
    y_data = get_data_whole(data, y_column)
    z_data = get_data_whole(data, z_column)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_data, y_data, z_data, c='blue', marker='o')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    fig.tight_layout()

    fig.savefig(filename)
    print("3D Scatter plot saved to", filename)
    plt.show()


def scatter_3d_plot_month(data, year, month, x_column, y_column, z_column, title, xlabel, ylabel, zlabel, filename):
    """
        Generate a 3D scatter plot for a specific month and year from the given data.

        Parameters:
        - data: The input data.
        - year (int): The target year for filtering the data.
        - month (int): The target month for filtering the data (1-12).
        - x_column (int): The index of the column in the DataFrame for the x-axis.
        - y_column (int): The index of the column in the DataFrame for the y-axis.
        - z_column (int): The index of the column in the DataFrame for the z-axis.
        - title (str): The title of the 3D scatter plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - zlabel (str): The label for the z-axis.
        - filename (str): The name of the file to save the 3D scatter plot.

        Returns:
        None
    """

    x_data = get_data_date(data, x_column, year, month)
    y_data = get_data_date(data, y_column, year, month)
    z_data = get_data_date(data, z_column, year, month)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_data, y_data, z_data, c='blue', marker='o')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    fig.tight_layout()

    fig.savefig(filename)
    print("3D Scatter plot saved to", filename)
    plt.show()


def get_data_whole(seq, column):
    """
        Extract a specific column of data from a sequence.

        Parameters:
        - seq (list of lists): The sequence containing the data.
        - column (int): The index of the column to extract.

        Returns:
        tuple: A tuple containing the values from the specified column.
    """

    seq_section = ()
    for i in range(1, len(seq)):
        seq_section += (seq[i][column],)
    return seq_section


def get_files(number):
    """
        Prompt the user to choose file numbers from a list.

        Parameters:
        - number (int): The number of files to choose.

        Returns:
        tuple: A tuple containing the selected file numbers.
    """

    list = ()
    for i in range(number):
        print("Choose a number from any of the following: ")
        print("1) KCLT", "2) KCQT", "3) KHOU", "4) KIND", "5) KJAX", "6) KMDW", "7) KNYC", "8) KPHL", "9) KPHX",
              "10) KSEA", sep=" ")

        file = int(input("Which file do you want to open? "))
        while file in list:
            file = int(input("You already chose this file once, please choose another: "))
        list += (file,)
    return list


def get_data_date(seq, parameter, year, month):
    """
        Extract data for a specific parameter(column) from a sequence based on the specified year and month.

        Parameters:
        - seq (list of lists): The sequence containing the data.
        - parameter (int): The index of the parameter to extract.
        - year (int): The target year for filtering data.
        - month (int): The target month for filtering data.

        Returns:
        tuple: A tuple containing the data for the specified parameter and date.
    """

    data_date = ()
    for i in range(1, len(seq)):
        year_data, month_data = check_year_and_month(seq[i][0])
        if year_data == str(year) and month_data == str(month):
            data_date += (seq[i][parameter],)
    return data_date


def compare_two_files_month(file_number1, file_number2, parameter, year, month):
    """
        Compare the values of a specific parameter for two weather files in a given month and year.

        Parameters:
        - file_number1 (int): The index of the first weather file to compare.
        - file_number2 (int): The index of the second weather file to compare.
        - parameter (str): The parameter/column to compare in the weather files.
        - year (int): The target year for filtering the data.
        - month (int): The target month for filtering the data (1-12).

        Returns:
        - difference_list (tuple): A tuple containing the absolute differences between corresponding
          values of the specified parameter in the two weather files for the given month and year.
    """

    files = ("KCLT", "KCQT", "KHOU", "KIND", "KJAX", "KMDW", "KNYC", "KPHL", "KPHX", "KSEA")
    file1 = read_csv("../data/us-weather-history/" + files[file_number1 - 1] + ".csv")
    file2 = read_csv("../data/us-weather-history/" + files[file_number2 - 1] + ".csv")
    data_period_file1 = get_data_date(file1, parameter, year, month)
    data_period_file2 = get_data_date(file2, parameter, year, month)
    difference_list = ()
    for point in range(len(data_period_file1)):
        difference_list += (abs(data_period_file1[point] - data_period_file2[point]),)
    return difference_list


def compare_two_files(file_number1, file_number2, parameter):
    """
        Compare data for a specific parameter between two files for a given year and month.

        Parameters:
        - file_number1 (int): The index of the first file to compare.
        - file_number2 (int): The index of the second file to compare.
        - parameter (int): The index of the parameter to compare.
        - year (int): The target year for filtering data.
        - month (int): The target month for filtering data.

        Returns:
        tuple: A tuple containing the absolute differences between corresponding data points in the two files.
    """

    files = ("KCLT", "KCQT", "KHOU", "KIND", "KJAX", "KMDW", "KNYC", "KPHL", "KPHX", "KSEA")
    file1 = read_csv("../data/us-weather-history/" + files[file_number1 - 1] + ".csv")
    file2 = read_csv("../data/us-weather-history/" + files[file_number2 - 1] + ".csv")
    data_period_file1 = get_data_whole(file1, parameter)
    data_period_file2 = get_data_whole(file2, parameter)
    difference_list = ()
    for point in range(len(data_period_file1)):
        difference_list += (abs(data_period_file1[point] - data_period_file2[point]),)
    return difference_list


def two_files_to_plot_whole(file_number1, file_number2, parameter):
    """
        Extract data for a specific parameter from two files.

        Parameters:
        - file_number1 (int): The index of the first file.
        - file_number2 (int): The index of the second file.
        - parameter (int): The index of the parameter to extract.

        Returns:
        tuple: Two tuples containing the data for the specified parameter from each file.
    """

    files = ("KCLT", "KCQT", "KHOU", "KIND", "KJAX", "KMDW", "KNYC", "KPHL", "KPHX", "KSEA")
    file1 = read_csv(f"../data/us-weather-history/" + files[file_number1 - 1] + ".csv")
    file2 = read_csv(f"../data/us-weather-history/" + files[file_number2 - 1] + ".csv")
    data_period_file1 = get_data_whole(file1, parameter)
    data_period_file2 = get_data_whole(file2, parameter)
    return data_period_file1, data_period_file2


def two_files_to_plot_month(file_number1, file_number2, parameter, year, month):
    """
        Extract data for a specific parameter from two files for a given year and month.

        Parameters:
        - file_number1 (int): The index of the first file.
        - file_number2 (int): The index of the second file.
        - parameter (int): The index of the parameter to extract.
        - year (int): The target year for filtering data.
        - month (int): The target month for filtering data.

        Returns:
        tuple: Three tuples containing dates, data for the specified parameter from each file.
    """

    files = ("KCLT", "KCQT", "KHOU", "KIND", "KJAX", "KMDW", "KNYC", "KPHL", "KPHX", "KSEA")
    file1 = read_csv(f"../data/us-weather-history/" + files[file_number1 - 1] + ".csv")
    file2 = read_csv(f"../data/us-weather-history/" + files[file_number2 - 1] + ".csv")
    data_period_file1 = get_data_date(file1, parameter, year, month)
    data_period_file2 = get_data_date(file2, parameter, year, month)
    dates = get_data_date(file1, 0, year, month)
    return dates, data_period_file1, data_period_file2


def temperature_amplitude_whole(seq):
    """
        Calculate the temperature amplitude for each entry in the input sequence.

        Parameters:
        - seq (list of lists): The sequence containing data.

        Returns:
        tuple: A tuple containing the temperature amplitude for each corresponding entry.
    """

    max_temp_list = get_data_whole(seq, 3)
    min_temp_list = get_data_whole(seq, 2)
    temp_amplitude_list = ()
    for i in range(len(max_temp_list)):
        temp_amplitude_list += (max_temp_list[i] - min_temp_list[i],)
    return temp_amplitude_list


def temperature_amplitude_month(seq, year, month):
    """
        Calculate the temperature amplitude for each entry in the input sequence for a specific year and month.

        Parameters:
        - seq (list of lists): The sequence containing temperature data.
        - year (int): The target year for filtering data.
        - month (int): The target month for filtering data.

        Returns:
        tuple: A tuple containing the temperature amplitude for each corresponding entry in the specified month.
    """

    max_temp_list = (get_data_date(seq, 3, year, month))
    min_temp_list = (get_data_date(seq, 2, year, month))
    temp_amplitude_month_list = ()
    for i in range(len(max_temp_list)):
        temp_amplitude_month_list += (max_temp_list[i] - min_temp_list[i],)
    return temp_amplitude_month_list


def above_threshold(data_seq, threshold):
    """
        Count the number of elements in the sequence that are equal to or above the specified threshold.

        Parameters:
        - data_seq (list): The sequence of data to be analyzed.
        - threshold (float): The threshold value for comparison.

        Returns:
        int: The count of elements in the sequence that are equal to or above the threshold.
    """
    total = 0
    for i in range(len(data_seq)):
        if data_seq[i] >= threshold:
            total += 1
    return total


def below_threshold(data_seq, threshold):
    """
        Count the number of elements in the sequence that are equal to or below the specified threshold.

        Parameters:
        - data_seq (list): The sequence of data to be analyzed.
        - threshold (float): The threshold value for comparison.

        Returns:
        int: The count of elements in the sequence that are equal to or below the threshold.
    """

    total = 0
    for i in range(len(data_seq)):
        if data_seq[i] <= threshold:
            total += 1
    return total


def average_change(seq):
    """
        Calculate the average change per element in the sequence.

        Parameters:
        - seq (list): The sequence of data.

        Returns:
        float: The average change per element in the sequence.
    """

    return (seq[len(seq) - 1] - seq[0]) / len(seq)


def highest_in_sequence(seq):
    """
        Find the highest value in a specific column of the sequence.

        Parameters:
        - seq (list of lists): The sequence containing the data.
        - column (int): The index of the column to search for the highest value.

        Returns:
        tuple: A tuple containing the highest value and its corresponding row index.
    """

    biggest = float('-inf')
    biggest_index = 0
    for point in range(1, len(seq)):
        if seq[point] > biggest:
            biggest = seq[point]
            biggest_index = point

    return biggest, biggest_index


def lowest_in_sequence(seq):
    """
        Find the lowest value in a specific column of the sequence.

        Parameters:
        - seq (list of lists): The sequence containing the data.
        - column (int): The index of the column to search for the lowest value.

        Returns:
        tuple: A tuple containing the lowest value and its corresponding row index.
    """

    lowest = float('inf')
    lowest_index = 0
    for point in range(len(seq)):
        if seq[point] < lowest:
            lowest = seq[point]
            lowest_index = point

    return lowest, lowest_index


def get_standard_deviation(data_seq):
    """
        Calculate the standard deviation of a data sequence.

        Parameters:
        - data_seq (list): The sequence of data.

        Returns:
        float: The standard deviation of the data sequence.
    """

    average = get_average(data_seq)
    sum = 0
    for i in range(len(data_seq)):
        sum += ((data_seq[i] - average) ** 2)
    return math.sqrt(sum / len(data_seq))


def get_average(seq):
    """
        Calculate the average of the elements in the sequence.

        Parameters:
        - seq (list): The sequence of data.

        Returns:
        float: The average of the elements in the sequence.
    """

    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total / (len(seq))


def get_headers(seq):
    """
        Extract the headers from a sequence, excluding the first row.

        Parameters:
        - seq (list of lists): The sequence containing the data.

        Returns:
        tuple: A tuple containing the headers from the specified column.
    """

    seq_section = ()
    for i in range(1, len(seq)):
        seq_section += (seq[i][0],)
    return seq_section


def check_year_and_month(data_point):
    """
        Extract the year and month from a date string.

        Parameters:
        - data_point (str): The date string.

        Returns:
        tuple: A tuple containing the extracted year and month.
    """

    year = data_point[:4]
    if data_point[6] != "-":
        month = data_point[5:7]
    else:
        month = data_point[5]
    return year, month


def statistics_whole(seq):
    """
       Display various statistical measures for a given sequence.

       Parameters:
       - seq: The specific sequence (column) from the dataset for analysis.

       Returns:
       None
    """

    print("Average value: ", get_average(seq))
    print("Standard deviation: ", get_standard_deviation(seq))
    highest_value, highest_index = highest_in_sequence(seq)
    print("Highest value: ", highest_value, " (In day number ", highest_index, ")")
    lowest_value, lowest_index = lowest_in_sequence(seq)
    print("Lowest value: ", lowest_value, " (In day number ", lowest_index, ")")
    print("Average rate of change: ", average_change(seq))
    threshold = int(input("Choose a threshold: "))
    print("Amount of times above threshold: ", above_threshold(seq, threshold))
    print("Amount of times below threshold: ", below_threshold(seq, threshold))


def statistics_month(seq):
    """
        Display various statistical measures for a given sequence in a specific month and year.

        Parameters:
        - seq: The specific sequence (column) from the dataset for analysis.
        Returns:
        None
    """

    print("Average value: ", get_average(seq))
    print("Standard deviation: ", get_standard_deviation(seq))
    highest_value, highest_index = highest_in_sequence(seq)
    print("Highest value: ", highest_value, " (In day number ", highest_index, ")")
    lowest_value, lowest_index = lowest_in_sequence(seq)
    print("Lowest value: ", lowest_value, " (In day number ", lowest_index, ")")
    print("Average rate of change: ", average_change(seq))
    threshold = int(input("Choose a threshold: "))
    print("Amount of times above threshold: ", above_threshold(seq, threshold))
    print("Amount of times below threshold: ", below_threshold(seq, threshold))


def plot_data(x, y, xlabel, ylabel, title, filename):
    """
        Create a line plot with the given data and save it to a file.

        Parameters:
        - x (list): The x-axis data.
        - y (list): The y-axis data.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - title (str): The title of the plot.
        - filename (str): The filename to save the plot.

        Returns:
        None
    """

    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    interval = 30

    ax.set_xticks(range(0, len(x), interval))
    ax.set_xticklabels(x[::interval], rotation=45, ha='right')

    fig.tight_layout()

    ax.grid()

    fig.savefig(filename)
    print("Plot saved to", filename)

    plt.show()


def plot_two_curves(data1, label1, data2, label2, title, filename):
    """
        Create a plot with two curves using the given data and save it to a file.

        Parameters:
        - data1 (list): The data for the first curve.
        - label1 (str): The label for the first curve.
        - data2 (list): The data for the second curve.
        - label2 (str): The label for the second curve.
        - title (str): The title of the plot.
        - filename (str): The filename to save the plot.

        Returns:
        None
    """

    fig, ax = plt.subplots()

    ax.plot(data1, label=label1)
    ax.plot(data2, label=label2)

    ax.set(xlabel="Index", ylabel="Data", title=title)

    ax.legend()

    fig.tight_layout()

    ax.grid()

    fig.savefig(filename)
    print("Plot saved to", filename)

    plt.show()


def plot_data_month(x, y, xlabel, ylabel, title, filename):
    """
        Generate a line plot for the given data with specific formatting for the x-axis.

        Parameters:
        - x (list or array-like): The x-axis data.
        - y (list or array-like): The y-axis data.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        - title (str): The title of the plot.
        - filename (str): The name of the file to save the plot.

        Returns:
        None
    """
    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    interval = 7

    ax.set_xticks(range(0, len(x), interval))
    ax.set_xticklabels(x[::interval], rotation=45, ha='right')

    fig.tight_layout()

    ax.grid()

    fig.savefig(filename)
    print("Plot saved to", filename)

    plt.show()

# -----------------------------------------------------------------------------
# DONE O:
#   Write unit tests for your functions in  unit_tests.py
# -----------------------------------------------------------------------------
