import csv


# -----------------------------------------------------------------------------
# Students:
#   Do NOT touch or modify this file.
#   Do NOT copy code from this file.
#
# Instead, ** CALL ** the functions in this module as needed for your project.
#
# To use this module, add the following import statement to the top of your
# Python code:
#
#       from csv_reader import read_csv
#
# You may then call the read_csv function as normal.
# -----------------------------------------------------------------------------


def read_csv(filename):
    """
    Parameters:  A filename, which must be a .csv file

    Returns: A nested sequence containing the data from the file.

    :type filename:     str
    :rtype:             tuple[tuple[int|float|str|bool]]
    """
    data = ()
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            data_row = ()
            for item in row:
                if is_int(item):
                    data_row += (int(item),)
                elif is_float(item):
                    data_row += (float(item),)
                elif item == "False" or item == "false":
                    data_row += (False,)
                elif item == "True" or item == "true":
                    data_row += (True,)
                else:
                    data_row += (item.strip(),)
            data += (data_row,)
    return data


def is_float(s):
    """
    Parameters:  A string s

    Returns: True if the given string can be converted to a float, False otherwise.

    :type filename:     str
    :rtype:             bool
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s):
    """
    Parameters:  A string s

    Returns: True if the given string can be converted to an integer, False otherwise.

    :type filename:     str
    :rtype:             bool
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
