from datetime import date
from dateutil import relativedelta
import csv
import re


class StockReader:
    """
    The Stock Reader class will create a hashmap that will read the Stock Symbols to
    figure out if the user's stock symbol exist or not and then grab each date's stock value.
    """
    def __init__(self):
        super().__init__()

    def generate_hashmap(self, user_data:str):
        """
        Call the function to create the hashmap
        :return: boolean value that makes sure the user_data is a valid ticker for the first window
        """
        my_hashmap = self.create_hashmap('StockSymbols.csv')
        return self.search(my_hashmap, user_data)

    def user_input_dates_plus_current_date(self, year:str, month:str, day:str) -> bool:
        """
        grabs the current date and takes the user's input dates to be checked in the timestamp
        :param year: The first or second year input by the user
        :param month: The first or second month input by the user
        :param day: The first or second month input by the user
        :return: The timestamp function that will check for values
        """
        today = date.today()
        return self.time_stamp(today, year, month, day)

    @staticmethod
    def search(hashmap, user_data):
        """
        Looks through the hashmap to find the company name
        :param hashmap: The hashmap that has all the company's stock abbreviation
        :param user_data: The date asked by the user
        :return: returns boolean value if stock ticker exists for the GUI window.
        """
        # Check if the input contains only letters and symbols
        if re.fullmatch(r'[A-Z\^]+', user_data) and len(user_data) <= 5:
            return user_data in hashmap

    def time_stamp(self, today:date, consumer_year:str, consumer_month:str, consumer_day:str) -> bool:
        """
        Checks the timestamps to ensure all of it is valid and that it's not past the
        two-year checkmark or else it will throw an error to try again
        :param today: The current date
        :param consumer_year: The first or second year of the user's input
        :param consumer_month: The first or second month of the user's input
        :param consumer_day: The first or second day of the user's input
        :return: the boolean value to continue with the program, or else throw an error
        """
        year = self.validate_number(consumer_year)
        month = self.validate_number(consumer_month)
        day = self.validate_number(consumer_day)
        full_date = date(year, month, day)
        delta = relativedelta.relativedelta(today, full_date)

        return delta.years < 2

    @staticmethod
    def validate_number(consumer_value:str) -> int:
        """
        Checks to ensure the value is a number rather than a string or another char
        :param consumer_value: a value that is either the year, month, or day
        :return: true or false
        """
        if consumer_value.isdigit():
            return int(consumer_value)
        else:
            raise ValueError("The date is not valid")


    @staticmethod
    def create_hashmap(filename:csv) -> dict:
        """
        This will read the csv file and compute it into a hashmap for us to access
        :param filename: csv file with all the tickers(company's stock abbreviation)
        :return: a hashmap to use for the program
        """
        # Open the CSV file and read the data
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            stock_hashmap = {row[0]: None for row in reader if row and len(row) >= 1}

        return stock_hashmap
