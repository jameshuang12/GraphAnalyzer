from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
    QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox, QDialog, \
    QCheckBox, QVBoxLayout, QGroupBox
from datetime import date
import matplotlib as mpl
from matplotlib import style
import matplotlib.pyplot as plt
from main_functions import StockFunctions
import numpy as np
from datetime import timedelta
# Program Description: This program is used to crate a GUI for the user to interact with
# which will prompt the user for their desire company's stock abbreviation, first date
# they want to use, second date they want to use, and various functions they want the
# program to perform for their liking
# We used https://github.com/ViktorBash/PyStocks.git skeleton to assist us with the GUI

class GraphAnalyzerNameWindow(QMainWindow):
    def __init__(self):
        """
        Calls the constructor using the GraphAnalyzerNameWindow that will accept
        no parameters but initialize the first GUI that will ask for the company name.
        """
        # Begin the operation of the GUI
        super().__init__()
        self.main = StockFunctions()
        # Sets up the name, icon, and size of our GUI
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("stocks.jpg"))
        # self.setFixedSize(3000, 750)

        # Using grid layout with coordinates for this project
        self.generalLayout = QGridLayout()
        # Moves the GUI to open up in the middle of the screen
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        # sets up our main layout of the GUI
        self._centralWidget.setLayout(self.generalLayout)

        # Creates a text search bar
        self._createInput()
        # Create a text box with text that will prompt the user to insert
        # information into the search bar
        self._createTopLabel()
        # Creates the search button that will be pushed to execute other functions
        self._createSearchButton()

        # Sets up the font and the background of the GUI
        label_font = QtGui.QFont("Helvetica Neue", 20)
        self.setFont(label_font)
        self.setStyleSheet("QPushButton { background-color: #29c455}")

    def _createInput(self):  # Creates search bar at the top
        self.input = QLineEdit()
        self.input.setFixedHeight(75)
        self.input.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.input.setFont(input_font)
        self.generalLayout.addWidget(self.input, 2, 0)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel(
            "Thank you for using our program today. Please put in the symbol for the desired stock")
        self.toplabel.setFixedHeight(75)
        self.generalLayout.addWidget(self.toplabel, 1, 0)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(75)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 2, 1)

    def getInput(self):  # Returns what is in the input box at the time. Also returns it capitalized
        user_input = self.input.text()
        return user_input.upper()

    def _removeInput(self):  # Resets input box
        self.input.setText("")

    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    @pyqtSlot()  # Connects the search button to functions
    def _inputSend(self):
        user_data = self.getInput()

        if not self.main.nameActivate(user_data):
            self.show_warning("Error", "Invalid input. Please try again.")
            self._removeInput()
            # it shows the error message twice for some reason
            return
        else:
            self.hide()  # hides the first window
            self.switch_to_second(user_data)

    def switch_to_second(self, user_data):
        print(user_data)
        self.second_window = GraphAnalyzerDateWindow(user_data)
        self.second_window.show()
        # need to store the valid user data into a variable for the actual polygon stock


'''
Crating a second class using nearly the same format as the first window. 
'''
class GraphAnalyzerDateWindow(QMainWindow):
    # Initializes GUI. Calls other functions to make other parts of the GUI.
    def __init__(self,user_data):
        """
        Set up various variables to none.
        Creates the Gui with an input bars, search bar, search button, a data label
        :param user_data: The company name that the user inserted
        """
        super().__init__()
        self.third_window = None
        self.stock_name = user_data
        self.yearInput = QLineEdit()
        self.monthInput = QLineEdit()
        self.dayInput = QLineEdit()

        self.DateOneYear = None
        self.DateOneMonth = None
        self.DateOneDay = None

        self.DateTwoYear = None
        self.DateTwoMonth = None
        self.DateTwoDay = None

        self.dateOne = None
        self.dateTwo = None
        self.clientData = None

        # these variables will be used for the stock_class in the backend
        self.main = StockFunctions()
        self.setWindowTitle("Graph Analyzer Dates")
        self.setWindowIcon(QtGui.QIcon("stocks.jpg"))

        self.generalLayout = QGridLayout()  # Using grid layout with coordinates for this project
        self._centralWidget = QWidget(self)  # Central widget
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)  # .generalLayout is our main layout

        self._createYearInput()  # Creates year input bar
        self._createMonthInput()  # Creates month input bar
        self._createDayInput()  # Creates day input bar
        self._createTopLabel()   # Creates search bar at the top
        self._createSearchButton()  # Creates the search button
        self._createSecondLabel()  # Creates the date label

        label_font = QtGui.QFont("Helvetica Neue", 20)
        self.setFont(label_font)
        self.setStyleSheet("QPushButton { background-color: #29c455}")

        self.firstDateEntered = False  # flag for the first and second dates

    def _createYearInput(self):  # Creates search bar at the top
        self.yearInput = QLineEdit()
        self.yearInput.setFixedHeight(75)
        self.yearInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.yearInput.setFont(input_font)
        self.generalLayout.addWidget(self.yearInput, 1, 0)

    def _createMonthInput(self):  # Creates search bar at the top
        self.monthInput = QLineEdit()
        self.monthInput.setFixedHeight(75)
        self.monthInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.monthInput.setFont(input_font)
        self.generalLayout.addWidget(self.monthInput, 1, 1)

    def _createDayInput(self):  # Creates search bar at the top
        self.dayInput = QLineEdit()
        self.dayInput.setFixedHeight(75)
        self.dayInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.dayInput.setFont(input_font)
        self.generalLayout.addWidget(self.dayInput, 1, 2)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel(
            "             Stock Found! Please enter the earlier first date within two years as numbers: " + "\n"
            + "               Year                                    "
              "Month                                            Day")
        self.toplabel.setFixedHeight(150)
        self.generalLayout.addWidget(self.toplabel, 0, 0, 1, 3)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(75)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 1, 3)

    def _createSecondLabel(self): # Creates a text that says the current date
        today = date.today()
        self.secondlabel = QLabel("Today's date is: " + str(today))
        label_font = QtGui.QFont("Verdana", 20)
        self.secondlabel.setFont(label_font)
        self.generalLayout.addWidget(self.secondlabel, 2, 0, 1, 3)

    def _getYearInput(self): # Checks if the year input exist or not
        year_input = self.yearInput.text()
        if year_input == '':
            return None
        else:
            return year_input

    def _getMonthInput(self): # Checks if the month input exist or not
        month_input = self.monthInput.text()
        if month_input == '':
            return None
        else:
            return month_input

    def _getDayInput(self): # Checks if the day input exist or not
        day_input = self.dayInput.text()
        if day_input == '':
            return None
        else:
            return day_input

    def _removeYearInput(self): # Updates the text for the year input
        self.yearInput.setText("")
        self.yearInput.update()

    def _removeMonthInput(self): # Updates the text for the month input
        self.monthInput.setText("")
        self.monthInput.update()

    def _removeDayInput(self): # Updates the text for the day input
        self.dayInput.setText("")
        self.dayInput.update()

    def show_warning(self, title, message): # Prints out a warming message if the input is incorrect
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    @pyqtSlot()
    def _inputSend(self):
        """
        Checks if the first date and second date are both valid input. Removes and ask the user to
        try again. Checks that if the second date is after the first date rather than before.
        :return: the first and then the second dates from the user input
        """
        if not self.firstDateEntered:
            self.DateOneYear = self._getYearInput()
            self.DateOneMonth = self._getMonthInput()
            self.DateOneDay = self._getDayInput()

            if not self.main.dateActivate(self.DateOneYear, self.DateOneMonth, self.DateOneDay):
                self.show_warning("Error", "Invalid first date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return
            self._removeYearInput()
            self._removeMonthInput()
            self._removeDayInput()
            self.toplabel.setText("Please enter the second date with the same format")
            self.firstDateEntered = True

        else:

            self.DateTwoYear = self._getYearInput()
            self.DateTwoMonth = self._getMonthInput()
            self.DateTwoDay = self._getDayInput()

            if not self.main.dateActivate(self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay):
                self.show_warning("Error", "Invalid second date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return
            self._removeYearInput()
            self._removeMonthInput()
            self._removeDayInput()

            # compare dates
            dateOne, dateTwo = self.main.compareDates(self.DateOneYear, self.DateOneMonth, self.DateOneDay,
                                                      self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay)
            if not dateOne < dateTwo:
                self.show_warning("Error", "First date must be earlier than the second date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return
            else:
                self.hide()  # hides the first window
                self.switch_to_third(self.stock_name, dateOne, dateTwo)
                print(self.DateOneYear, self.DateOneMonth, self.DateOneDay)
                print(self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay)

    def switch_to_third(self, stock_name, date_one, date_two):
        """
        Transitions to the next Gui with all the various options to choose from given the
        stock name, first date and second date
        :param stock_name: the company's name
        :param date_one: the first date inputted by the user
        :param date_two: the second date inputted by the user
        """
        clientData = self.main.stockActivator(stock_name, date_one, date_two)
        self.third_window = GraphAnalyzerStockWindow(clientData, date_one, date_two)
        self.third_window.show()


class GraphAnalyzerStockWindow(QMainWindow):
    # Initializes GUI. Calls other functions to make other parts of the GUI.
    def __init__(self, client_data, date_one, date_two):
        """
        Creates the third window that provides all the value, options to execute, and
        name of the company
        :param client_data: the name of the company
        :param date_one: the first date inputted by the user
        :param date_two: the second date inputted by the user
        """
        super().__init__()
        # sets each parameter to a variable
        self.clientData = client_data
        self.dateOne = date_one
        self.dateTwo = date_two

        self.main = StockFunctions()
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("stocks.jpg"))

        self.generalLayout = QGridLayout()  # Using grid layout with coordinates for this project
        self._centralWidget = QWidget(self)  # Central widget
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)  # .generalLayout is our main layout

        # All creates the buttons for each actions
        self._create_graph_button(client_data)
        self._create_rsi_button(client_data)
        self._create_adx_button(client_data)
        self._create_mov_avg_button(client_data)
        self._create_investment_button(client_data)
        self._create_should_i_invest_button(client_data)
        self.exitButton()

        # Sets up the stock fonts
        info_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font.setUnderline(True)
        name_font = QtGui.QFont("Helvetica Neue", 40)

        # 1st Date's open amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_open = QLabel("1st Date's Open: $" + "{:.2f}".format(client_data.open[0]))
        self.stock_dateone_open.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_open, 1, 6)

        # 1st Date's high amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_high = QLabel("1st Date's High: $" + "{:.2f}".format(client_data.high[0]))
        self.stock_dateone_high.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_high, 2, 6)

        # 1st Date's low amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_low = QLabel("1st Date's Low: $" + "{:.2f}".format(client_data.low[0]))
        self.stock_dateone_low.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_low, 3, 6)

        # 1st Date's close amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_close = QLabel("1st Date's Close: $" + "{:.2f}".format(client_data.close[0]))
        self.stock_dateone_close.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_close, 4, 6)

        # 2nd Date's open amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_open = QLabel(
            "2nd Date's Open: $" + "{:.2f}".format(client_data.open[len(client_data) - 1]))
        self.stock_datetwo_open.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_open, 5, 6)

        # 2nd Date's high amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_high = QLabel(
            "2nd Date's High: $" + "{:.2f}".format(client_data.high[len(client_data) - 1]))
        self.stock_datetwo_high.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_high, 6, 6)

        # 2nd Date's low amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_low = QLabel(
            "2nd Date's Low: $" + "{:.2f}".format(client_data.low[len(client_data) - 1]))
        self.stock_datetwo_low.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_low, 7, 6)

        # 2nd Date's close amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_close = QLabel(
            "2nd Date's Close: $" + "{:.2f}".format(client_data.close[len(client_data) - 1]))
        self.stock_datetwo_close.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_close, 8, 6)

        # This shows the number of stock days the two timestamps had in between
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_open = QLabel("Number of stock days between " + str(date_one) +
                                         " and " + str(date_two) + ": " + str(len(client_data)))
        self.stock_dateone_open.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_open, 9, 6)

        # Creating a TickerToName object for next line
        Company = client_data.tick_name

        # Returns the name of the stock
        self.company_name = QLabel(Company)
        self.company_name.setFont(name_font)
        self.generalLayout.addWidget(self.company_name, 0, 3)

    def _create_graph_button(self, clientdata):
        """
        Creates the graph button that opens up the graph of the company
        :param clientdata: the name of the company
        """
        self.graph_button = QPushButton("Open Graph")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.graph_button.setFont(info_font)
        self.graph_button.setStyleSheet("background-color: #a69695}")
        self.graph_button.clicked.connect(lambda: self.makeGraph(clientdata))
        self.generalLayout.addWidget(self.graph_button, 2, 0, 1, 3)

    @pyqtSlot()  # Plots our matplotlib graph if the button for a graph is clicked
    def makeGraph(self, clientdata):
        """
        Makes the graph itself using ggplot
        :param clientdata: the company name
        :return: shows the graph
        """
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        style.use("ggplot")
        plt.plot(clientdata.high, color="black")
        plt.ioff()
        plt.xlabel("From " + str(clientdata.day_one) + " to " + str(clientdata.day_two) + " in days")
        plt.ylabel("Amount($)")
        plt.title(clientdata.tick_name)
        plt.show()

    def _create_rsi_button(self, clientdata):
        """
        Creates a buttion for the rsi function to execute
        :param clientdata: the company's name
        :return: goes to create the rsi graph
        """
        self.rsi_button = QPushButton("RSI")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.rsi_button.setFont(info_font)
        self.rsi_button.setStyleSheet("background-color: #a69695}")
        self.rsi_button.clicked.connect(lambda: self._make_rsi_graph(clientdata))
        self.generalLayout.addWidget(self.rsi_button, 4, 0, 1, 2)

    @pyqtSlot()
    def _make_rsi_graph(self, clientdata):
        """
        generates a rsi graph for the user
        :param clientdata: the company's name
        :return: the rsi value from the two dates given by the user
        """
        throwaway_bool, rsi_values = self.main.rsi_function(clientdata, 14)

        two_weeks_ago = clientdata.day_two - timedelta(days=21)
        #could find a more accurate way to get the clientdata day_two from 14 days ago

        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        style.use("ggplot")

        fig, ax = plt.subplots()
        ax.plot(rsi_values, color="black")
        ax.axhline(y=30, color="red", label="Oversold")
        ax.axhline(y=70, color="blue", label="Overbought")

        ax.text(len(rsi_values) - 10, 30, "30", color="red", ha="right", va="top")
        ax.text(len(rsi_values) - 10, 70, "70", color="blue", ha="right", va="bottom")

        ax.set_xlabel("From " + str(two_weeks_ago) + " to " + str(clientdata.day_two) + " in days")
        ax.set_ylabel("RSI value")
        ax.set_title(clientdata.tick_name)
        ax.legend()
        plt.show()

    def _create_adx_button(self, clientdata):
        """
        creates a button that will execute the adx function
        :param clientdata: the company's name
        :return: the graph of adx
        """
        self.adx_button = QPushButton("ADX")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.adx_button.setFont(info_font)
        self.adx_button.setStyleSheet("background-color: #a69695}")
        self.adx_button.clicked.connect(lambda: self._make_adx_graph(clientdata))
        self.generalLayout.addWidget(self.adx_button, 5, 0, 1, 2)

    def _make_adx_graph(self, clientdata):
        """
        generates an adx graph for the user
        :param clientdata: the company's name
        :return: the adx value from the two given dates by the user
        """
        throwaway_bool, adx, pos_adx, neg_adx = self.main.average_dir_index(clientdata, 14)

        adx_values_padded = [np.nan] * 13 + adx

        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        style.use("ggplot")

        fig, ax = plt.subplots()
        ax.plot(adx_values_padded, color="black", label="ADX")
        ax.plot(pos_adx, color="blue", label="+DI")
        ax.plot(neg_adx, color="purple", label="-DI")

        ax.axhline(y=25, color="red", label="Weak trend")
        ax.axhline(y=50, color="yellow", label="Moderate trend")
        ax.axhline(y=75, color="green", label="Strong trend")

        ax.text(len(adx) - 10, 25, "25", color="red", ha="right", va="top")
        ax.text(len(adx) - 10, 50, "50", color="yellow", ha="right", va="center")
        ax.text(len(adx) - 10, 75, "75", color="green", ha="right", va="bottom")

        ax.set_xlabel("From " + str(clientdata.day_one) + " to " + str(clientdata.day_two) + " in days")
        ax.set_ylabel("ADX, +DI, -DI values")
        ax.set_title(clientdata.tick_name)
        ax.legend()
        plt.show()

    def _create_mov_avg_button(self, clientdata):
        """
        create a moving average button
        :param clientdata: the company's name
        :return: opens up a checkbox application for the user
        """
        self.moving_average_button = QPushButton("Moving Avg")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.moving_average_button.setFont(info_font)
        self.moving_average_button.setStyleSheet("background-color: #a69695}")
        self.moving_average_button.clicked.connect(lambda: self._mov_avg_checkbox(clientdata))
        self.generalLayout.addWidget(self.moving_average_button, 6, 0, 1, 2)

    def _mov_avg_checkbox(self, clientdata):
        """
        creates 3 separate checkboxes that the user can choose from
        :param clientdata: the company's name
        :return: the graph of the moving averages from the 2 sets of dates the user chooses from
        """
        while True:
            dialog = QDialog()
            dialog.setWindowTitle("Checkbox Popup")

            # first set of checkboxes
            group1 = QGroupBox("Short-term Range:")
            layout1 = QVBoxLayout()
            options1 = ['100', '50', '25', '10']
            checkboxes1 = []

            for option in options1:
                checkbox = QCheckBox(option, group1)
                checkbox.stateChanged.connect(
                    lambda state, option=option, checkboxes=checkboxes1: self.handleStateChanged(
                        state, option, checkboxes))
                layout1.addWidget(checkbox)
                checkboxes1.append(checkbox)

            group1.setLayout(layout1)

            # second set of checkboxes
            group2 = QGroupBox("Long-term Range:")
            layout2 = QVBoxLayout()
            options2 = ['200', '100', '50', '25']
            checkboxes2 = []

            for option in options2:
                checkbox = QCheckBox(option, group2)
                checkbox.stateChanged.connect(
                    lambda state, option=option, checkboxes=checkboxes2: self.handleStateChanged(
                        state, option, checkboxes))
                layout2.addWidget(checkbox)
                checkboxes2.append(checkbox)

            group2.setLayout(layout2)

        # third set of checkboxes
            group3 = QGroupBox("Price Type")
            layout3 = QVBoxLayout()
            options3 = ['high', 'low', 'close', 'open']
            checkboxes3 = []

            for option in options3:
                checkbox = QCheckBox(option, group3)
                checkbox.stateChanged.connect(
                    lambda state, option=option, checkboxes=checkboxes3: self.handleStateChanged(
                        state, option, checkboxes))
                layout3.addWidget(checkbox)
                checkboxes3.append(checkbox)

            group3.setLayout(layout3)

        # enter button
            button = QPushButton("Enter", dialog)
            button.clicked.connect(dialog.accept)

        # main layout
            layout = QVBoxLayout()
            layout.addWidget(group1)
            layout.addWidget(group2)
            layout.addWidget(group3)
            layout.addWidget(button)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                short_term = None
                long_term = None
                price_type = None

                for checkbox in checkboxes1:
                    if checkbox.isChecked():
                        short_term = int(checkbox.text())
                for checkbox in checkboxes2:
                    if checkbox.isChecked():
                        long_term = int(checkbox.text())
                for checkbox in checkboxes3:
                    if checkbox.isChecked():
                        price_type = checkbox.text()

                if short_term >= long_term:
                    self.show_warning("Error ", "Long Term days must be longer than Short Term")
                elif long_term >= len(clientdata):
                    self.show_warning("Error ", "Long Term days must be shorter than days "
                                            "available in the stock")
                    #need to fix loop if error pops up
                else:
                    # Print selected options
                    print("Selected options from Set 1:", short_term)
                    print("Selected options from Set 2:", long_term)
                    print("Selected options from Set 3:", price_type)
                    self._make_mov_avg_graph(clientdata, short_term, long_term, price_type)
                    break

    @pyqtSlot()
    def _make_mov_avg_graph(self, clientdata, short_term, long_term, price_type):
        """
        generates the moving average graph for the user
        :param clientdata: the company's name
        :param short_term: the first date specified by the user
        :param long_term: the second date specified by the user
        :param price_type: the specific type of value the user wants to see
        :return: aa graph of the moving averages of the two dates given by the user.
        """
        throwaway_bool, lt_values, st_values = self.main.moving_avg_crossover(
            clientdata, short_term, long_term, price_type)

        lt_start = (long_term - short_term)
        lt_values_padded = [np.nan] * lt_start + lt_values

        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        style.use("ggplot")

        fig, ax = plt.subplots()
        ax.plot(lt_values_padded, color="red", label="Long Term Moving Average")
        ax.plot(st_values, color="blue", label="Short Term Moving Average")

        ax.set_xlabel("Days")
        ax.set_ylabel("Long term and Short Term values")
        ax.set_title(clientdata.tick_name)
        ax.legend()

        plt.show()


    def handleStateChanged(self, state, option, checkboxes):
        """
        checks to ensure that the checkbox is filled
        :param state: the current state
        :param option: the checkmark itself
        :param checkboxes: inserts the checkboxes for the user to check or not
        :return: a pass if it works, failed if not.
        """
        if state == Qt.Checked:
            for checkbox in checkboxes:
                if checkbox.text() != option:
                    checkbox.setChecked(False)
        elif state == Qt.Unchecked:
            pass

    def _create_investment_button(self, clientdata):
        """
        creates a button for the investment amount wanted by the user
        :param clientdata: the company's name
        :return: a new window asking for more information about the investments
        """
        self.investment_button = QPushButton("Investment")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.investment_button.setFont(info_font)
        self.investment_button.setStyleSheet("background-color: #a69695}")
        self.investment_button.clicked.connect(lambda: self._make_investment_window(clientdata))
        self.generalLayout.addWidget(self.investment_button, 3, 0, 1, 2)

    def _make_investment_window(self, clientdata):
        """
        creates a window that will ask for the amount the user wants to invest
        :param clientdata: the company's name
        :return: opens an investment window asking the user for the investment amount
        """
        invest_window = QDialog(self)
        invest_window.setWindowTitle("Investment Window")

        label = QLabel("Enter how many dollars you would've invested on " +
                                   str(clientdata.day_one), invest_window)

        search_bar = QLineEdit(invest_window)

        enter_button = QPushButton("Enter", invest_window)

        enter_button.clicked.connect(lambda: self._validate_input(search_bar.text(),clientdata))

        layout = QGridLayout(invest_window)
        layout.addWidget(label, 0, 0)
        layout.addWidget(search_bar, 0, 1)
        layout.addWidget(enter_button, 1, 1)

        invest_window.setLayout(layout)
        invest_window.show()

    def _validate_input(self, input, clientdata):
        """
        checks if the input is a valid number
        :param input: the user's input
        :param clientdata: the company's name
        :return: thows errors or warning if the input is incorrect, if not, then create graph
        """
        try:
            investment_amount = float(input)
            if investment_amount < 0:
                self.show_warning("Invalid Input", "Investment amount cannot be negative.")
            else:
                self.show_investment_amount(clientdata, investment_amount)
        except ValueError:
            self.show_warning("Invalid Input", "Investment amount must be a number.")

    def show_investment_amount(self, clientdata, amount):
        """
        generates the investment amount whether there was an increase or decrease
        :param clientdata: the company's name
        :param amount: the amount inserted by the user
        :return: the investment amount, whether it was a gain or a loss
        """
        up_or_down, per_change = self.main.percentageChange(clientdata)
        invested_amount = self.main.investment(per_change, amount)

        amount = '${:,.2f}'.format(amount)  #creates into currency value
        msg = QMessageBox()
        msg.setWindowTitle("Investment")

        #add high, low, open, close???
        if not up_or_down:
            msg.setText(f"Amount invested on {clientdata.day_one}: {amount}\n"
                        f"If withdrawn on {clientdata.day_two}: ${invested_amount} lost\n"
                        f"Percent Change: {per_change}% ")
        else:
            msg.setText(f"Amount invested on {clientdata.day_one}: {amount}\n"
                        f"If withdrawn on {clientdata.day_two}: ${invested_amount} gained\n"
                        f"Percent Change: +{per_change}% ")
        msg.exec_()

    def show_warning(self, title, message):
        """
        gives a warning that the certain action or input is not feasible
        :param title: the title of the error
        :param message: the messages that will appear if the window appears
        :return: the message and error on the screen whenever an action is executed correctly
        """
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def _create_should_i_invest_button(self, clientdata):
        """
        creates a button that is capable to tell the user whether or not it's smart
        to invest in this company at the moment
        :param clientdata: the company's name
        :return: the outcome of the company's future
        """
        self.should_i_button = QPushButton("Should I buy?")
        info_font = QtGui.QFont("Helvetica Neue", 14)
        self.should_i_button.setFont(info_font)
        self.should_i_button.setStyleSheet("background-color: #a69695}")
        self.should_i_button.clicked.connect(lambda: self.should_i_invest_results(clientdata))
        self.generalLayout.addWidget(self.should_i_button, 7, 0, 1, 2)

    def should_i_invest_results(self, client_data):
        """
        tells the user whether or not to invest in this company or not
        :param client_data: the company's name
        :return: the outcome of invest now or don't invest
        """
        msg = QMessageBox()
        msg.setWindowTitle("Should I invest?")

        text = self.main.buy_or_not(client_data)
        msg.setText(text)
        msg.exec_()

    def exitButton(self):
        """
        creates a button to exit the program
        :return: closes the window of the program
        """
        # create a button to exit the application
        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.show_popup)
        self.generalLayout.addWidget(exit_button, 10, 0)

        # will need to fix the windows and such
        self.setWindowTitle('My App')
        self.show()

    def show_popup(self):
        """
        double checks to ensure that is what the user wants
        :return: closes the program
        """
        # show the message box
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No,)

        # if the user clicks Yes, exit the application
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()


