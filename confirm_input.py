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



def userInputDate(user_data):
    '''

    :param user_data: valid ticker stamp
    :return: not updated in GUI either but will should return boolean value that makes sure
    the timestamps are valid
    '''
    today = date.today()
    print("Today's date is:", today)

    dates = _timeStamps(today)
    # checks if timestamps are valid

    first_date = dates[0]
    second_date = dates[1]

    return user_data, first_date, second_date


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


def _timeStamps(today):
    """
    :param today's date
    :return: two valid dates within the 2 years and the first date is earlier than the second.
    This however doesn't include if the ipo was less than 2 yrs ago
    """

    while True:
        print('Enter the date for the first data point')
        date1 = _askTimestamp(today)
        print(date1)

        print('Enter the date for the second data point')
        date2 = _askTimestamp(today)
        print(date2)

        if date1 < date2:
            return date1, date2
        else:
            print('first date cannot be later than second date. please write both dates again.')
            continue


def _askTimestamp(today):
    """
    :param today: today's date
    :return: a valid time format within 2 years
    """

    while True:
        year = int(_validate_number('year'))
        month = int(_validate_number('month'))
        day = int(_validate_number('day'))

        fulldate = date(year, month, day)

        delta = relativedelta.relativedelta(today, fulldate)

        if delta.years < 2:
            return fulldate
        else:
            print("date given is beyond two years of allotted data given by the api program. "
                  "Please enter a valid date between today and two years ago. ")
            continue


def _validate_number(value):
    """
    :param value: a value
    :return: a valid number
    """
    while True:
        userInput = (input(f"Enter the {value}: "))
        if userInput.isdigit():
            return userInput
        else:
            print(f"PLease enter a valid {value}.")
            continue


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