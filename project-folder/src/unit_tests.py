"""
This module contains code for the final course project in
CSSE 120 - Introduction to Software Development.

This module contains unit tests for project functions.

Authors: Sk Naimul Islam Nayeem, Thiago Costa.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.
import functions


# -----------------------------------------------------------------------------
# DONE:
#   Write your TEST functions below this _TODO_.
#   Use the standard naming convention of  run_test_FUNCTION_NAME,
#   where FUNCTION_NAME is the name of the function you are testing.
# -----------------------------------------------------------------------------
def run_test_get_data_whole():
    """ Tests the get_data_whole function. """
    print()
    print("-----------------------------------------------")
    print("Testing the get_data_whole function:")
    print("-----------------------------------------------")

    # Test 1:
    seq1 = [(1, 10), (2, 20), (3, 30)]
    column1 = 1
    expected1 = (20, 30)
    actual1 = functions.get_data_whole(seq1, column1)
    print("Test 1 expected:", expected1)
    print("       actual:  ", actual1)

    # Test 2:
    seq2 = ((4, 40), (5, 50), (6, 60))
    column2 = 0
    expected2 = (5, 6)
    actual2 = functions.get_data_whole(seq2, column2)
    print("Test 2 expected:", expected2)
    print("       actual:  ", actual2)

    # Test 3:
    seq3 = [(7, 70), (8, 80), (9, 90)]
    column3 = 1
    expected3 = (80, 90)
    actual3 = functions.get_data_whole(seq3, column3)
    print("Test 3 expected:", expected3)
    print("       actual:  ", actual3)

    # Test 4:
    seq4 = [(1, 13), (84, 77), (8, 31)]
    column4 = 1
    expected4 = (77, 31)
    actual4 = functions.get_data_whole(seq4, column4)
    print("Test 4 expected:", expected4)
    print("       actual:  ", actual4)


def run_test_average_change():
    """ Tests the average_change function. """

    print()
    print("-----------------------------------------------")
    print("Testing the average_change function:")
    print("-----------------------------------------------")

    # Test 1:
    seq1 = (1, 2, 3, 4, 5)
    expected1 = 0.8
    actual1 = functions.average_change(seq1)
    print("Test 1 expected:", expected1)
    print("       actual:  ", actual1)

    # Test 2:
    seq2 = (5, 10, 15, 20, 25)
    expected2 = 4.0
    actual2 = functions.average_change(seq2)
    print("Test 2 expected:", expected2)
    print("       actual:  ", actual2)

    # Test 3:
    seq3 = (2, 4, 6, 8, 10)
    expected3 = 1.6
    actual3 = functions.average_change(seq3)
    print("Test 3 expected:", expected3)
    print("       actual:  ", actual3)

    # Test 4:
    seq4 = (1, 11, 21, 31)
    expected4 = 7.5
    actual4 = functions.average_change(seq4)
    print("Test 4 expected:", expected4)
    print("       actual:  ", actual4)


def run_test_average():
    """ Tests the get_average function. """

    print()
    print("-----------------------------------------------")
    print("Testing the get_average function:")
    print("-----------------------------------------------")

    # Test 1:
    seq1 = [1, 2, 3, 4, 5]
    expected1 = 3.0
    actual1 = functions.get_average(seq1)
    print("Test 1 expected:", expected1)
    print("       actual:  ", actual1)

    # Test 2:
    seq2 = [5, 10, 15, 20, 25]
    expected2 = 15.0
    actual2 = functions.get_average(seq2)
    print("Test 2 expected:", expected2)
    print("       actual:  ", actual2)

    # Test 3:
    seq3 = [2, 4, 6, 8, 10]
    expected3 = 6.0
    actual3 = functions.get_average(seq3)
    print("Test 3 expected:", expected3)
    print("       actual:  ", actual3)

    # Test 4:
    seq4 = [1, 11, 21, 31]
    expected4 = 16.0
    actual4 = functions.get_average(seq4)
    print("Test 4 expected:", expected4)
    print("       actual:  ", actual4)

# -----------------------------------------------------------------------------
# DONE:
#   Once you have written your tests, call the test functions in  main  to
#   verify that your functions pass the tests.
#  _
#   You may then comment out the testing function calls in  main , but do
#   not remove them.
# -----------------------------------------------------------------------------
