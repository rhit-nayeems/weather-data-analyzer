"""
This module contains code for the final course project in
CSSE 120 - Introduction to Software Development.

This module houses the main function, which is the main driver of the program.

Authors: Sk Naimul Islam Nayeem, Thiago Costa,. 
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# Import the provided csv reader
from csv_reader import read_csv
# To use the read_csv function, simply call it as normal

# The matplotlib library allows Python to generate plots.
# Don't worry about this strange import - it sets the GUI backend for
# matplotlib so that PyCharm can display the plots.
# You'll be able to use the library as normal once you
# install the package to PyCharm.
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import functions


# -----------------------------------------------------------------------------
# DONE: 2.
#   Students - Write code for your project in the provided template files.
#   You may also add .py files to better organize your functions if you like.
#  _
#   As this template is only a skeleton, refer back to the project requirements
#   document EARLY and OFTEN as you work on this project.
#  _
#   Once you understand the purpose of this file, mark this _TODO_ as done.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# DONE:
#   Write code in the  main  function below to 'drive' your program.
#   But remember that most of your code should be in reusable functions!
# -----------------------------------------------------------------------------


def main():
    functions.menu()


# -----------------------------------------------------------------------------
# DONE:
#   Write your program functions in  functions.py  , or other similarly
#   named files added by you.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# DONE:
#   Write unit tests for your functions in  unit_tests.py
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
