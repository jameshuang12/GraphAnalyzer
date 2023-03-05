from datetime import date
from dateutil import relativedelta
import csv
import re

# Program Description: This program will create a hashmap that will read the StockSymbol.csv
# grab the current date, search for each of the date's stock value and confirm it exist
def generate_hashmap(user_data):
    """
    Call the function to create the hashmap
    :return: boolean value that makes sure the user_data is a valid ticker for the first window
    """

    my_hashmap = create_hashmap('StockSymbols.csv')
    return search(my_hashmap, user_data)

def user_input_dates_plus_current_date(year, month, day):
    """
    grabs the current date and takes the user's input dates to be checked in the timestamp
    :param year: The first or second year input by the user
    :param month: The first or second month input by the user
    :param day: The first or second month input by the user
    :return: The timestamp function that will check for values
    """
    today = date.today()
    return time_stamp(today, year, month, day)


def search(hashmap, user_data):
    """
    Looks through the hashmap to find the company name
    :param hashmap: The hashmap that has all the company's stock abbreviation
    :param user_data: The date asked by the user
    :return: returns boolean value if stock ticker exists for the GUI window.
    """
    # Check if the input contains only letters and symbols
    if re.fullmatch(r'[A-Z\^]+', user_data) and len(user_data) <= 5:
        if user_data in hashmap:
            return True
    else:
        # Input is not valid, it will ask the user to try another input
        return False

def time_stamp(today, user_year, user_month, user_day):
    """
    Checks the timestamps to ensure all of it is valid and that it's not past the
    two-year checkmark or else it will throw an error to try again
    :param today: The current date
    :param user_year: The first or second year of the user's input
    :param user_month: The first or second month of the user's input
    :param user_day: The first or second day of the user's input
    :return: the boolean value to continue with the program, or else throw an error
    """

    year = int(_validate_number(user_year))
    month = int(_validate_number(user_month))
    day = int(_validate_number(user_day))
    fulldate = date(year, month, day)
    delta = relativedelta.relativedelta(today, fulldate)

    if not delta.years < 2:
        return False
    else:
        return True



def _validate_number(users_value_requested):
    """
    Checks to ensure the value is a number rather than a string or another char
    :param users_value_requested: a value that is either the year, month, or day
    :return: the value since its true or false
    """
    while True:
        if users_value_requested.isdigit():
            return users_value_requested
        else:
            return False


def create_hashmap(filename):
    """
    This will read the csv file and compute it into a hashmap for us to access
    :param filename: csv file with all the tickers(company's stock abbreviation)
    :return: a hashmap to use for the program
    """
    my_hashmap = {}

    # Open the CSV file and read the data
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assign the first and second columns to the key and value, respectively
            if len(row) == 0:
                continue
            my_hashmap[row[0]] = None

    return my_hashmap