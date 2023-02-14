from datetime import date
from dateutil import relativedelta
import csv
import re

'''

'''
def userInput(user_data):
    """
    will have a helper functions: the name
    :return: boolean value that makes sure the user_data is a valid ticker for the first window
    """
    #print('Thank you for using our program today. Please put in the symbol for the desired stock')

    my_hashmap = create_hashmap('../StockSymbols.csv')

    return search(my_hashmap, user_data)


def userInputDate(year, month, day):
    '''

    :param user_data: valid ticker stamp
    :return: return boolean value that makes sure the timestamp is valid
    '''
    today = date.today()
    return _timeStamp(today, year, month, day)


def search(hashmap, user_data):
    """
    :param hashmap with all the stock symbols, also where the user inputs the stock symbol
    :return: returns boolean value if stock ticker exists for the GUI window.
    """

    # Use a regular expression to check if the input contains only letters and symbols
    if re.fullmatch(r'[A-Z\^]+', user_data) and len(user_data) <= 5:
        if user_data in hashmap:
            return True
    else:
        # Input is not valid, will pop up in the window where the user will need to try again
        return False

def _timeStamp(today, user_year, user_month, user_day):
    """
    :param today: today's date
    :return: a boolean value of a valid time format within 2 years
    """

    year = int(_validate_number(user_year))
    if not year:
        return False

    month = int(_validate_number(user_month))
    if not month:
        return False

    day = int(_validate_number(user_day))
    if not day:
        return False

    fulldate = date(year, month, day)

    delta = relativedelta.relativedelta(today, fulldate)

    if not delta.years < 2:
        return False
    else:
        return True



def _validate_number(value):
    """
    :param value: a value
    :return: a valid number
    """
    while True:
        if value.isdigit():
            return value
        else:
            return False


def create_hashmap(filename):
    """
    :param filename: csv file with all the tickers
    :return: a hashmap to use for the program
    """
    hashmap = {}

    # Open the CSV file and read the data
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assign the first and second columns to the key and value, respectively
            if len(row) == 0:
                continue
            hashmap[row[0]] = None

    return hashmap