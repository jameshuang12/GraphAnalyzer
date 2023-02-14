import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
    QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox

from datetime import date

from GraphAnalyzer import main
import matplotlib as mpl
import matplotlib.dates
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt

# we are going to use this guy's gui so here the link
# https://github.com/ViktorBash/PyStocks/blob/master/Stock%20Project/gui_part.py
from GraphAnalyzer.main import Main


class GraphAnalyzerNameWindow(QMainWindow):
    '''
    This will create the first window, which will ask the user to enter the ticker symbol.
    Currently facing problems with the transition from the first window to the second where
    after the user puts in the correct ticker symbol it will close the first window (but also
    retaining the name data) and opening up the second window that is similar to the first but
    it will ask for the two timestamps.
    '''


    def __init__(self,):  # Initializes GUI. Calls other functions to make other parts of the GUI.
        super().__init__()

        self.main = Main()
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("StockClipart.jpg"))
        # self.setFixedSize(500, 500)

        self.generalLayout = QGridLayout()  # Using grid layout with coordinates for this project
        self._centralWidget = QWidget(self)  # Central widget
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)  # .generalLayout is our main layout

        self._createInput()  # Creates search bar at the top
        self._createTopLabel()  # Creates the text that says "Search for a stock"
        self._createSearchButton()  # Creates the search button

        label_font = QtGui.QFont("Helvetica Neue", 20)
        self.setFont(label_font)
        self.setStyleSheet("QPushButton { background-color: #29c455}")

    def _createInput(self):  # Creates search bar at the top
        self.input = QLineEdit()
        self.input.setFixedHeight(35)
        self.input.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.input.setFont(input_font)
        self.generalLayout.addWidget(self.input, 2, 0)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel("Thank you for using our program today. Please put in the symbol for the desired stock")
        self.toplabel.setFixedHeight(35)
        self.generalLayout.addWidget(self.toplabel, 1, 0)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(35)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 2, 1)

    def _getInput(self):  # Returns what is in the input box at the time. Also returns it capitalized
        input = self.input.text()
        return input.upper()

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
        user_data = self._getInput()

        if not self.main.nameActivate(user_data):
            self.show_warning("Error", "Invalid input. Please try again.")
            self._removeInput()
            #it shows the error message twice for some reason
            return
        else:
            self.hide() #hides the first window
            self.switch_to_second(user_data)

    def switch_to_second(self, user_data):
        print(user_data)
        self.second_window = GraphAnalyzerDateWindow(user_data)
        self.second_window.show()
        #need to store the valid user data into a variable for the actual polygon stock


'''
Crating a second class using nearly the same format as the first window. 
'''
class GraphAnalyzerDateWindow(QMainWindow):

    def __init__(self, user_data):  # Initializes GUI. Calls other functions to make other parts of the GUI.

        super().__init__()
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
        #these variables will be used for the stock_class in the backend

        self.main = Main()
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("StockClipart.jpg"))
        # self.setFixedSize(500, 500)

        self.generalLayout = QGridLayout()  # Using grid layout with coordinates for this project
        self._centralWidget = QWidget(self)  # Central widget
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)  # .generalLayout is our main layout

        self._createYearInput()  # Creates year input bar
        self._createMonthInput()  # Creates month input bar
        self._createDayInput()  # Creates day input bar  # Creates search bar at the top
        self._createTopLabel()
        self._createSearchButton()  # Creates the search button
        self._createSecondLabel()  # Creates the date label

        label_font = QtGui.QFont("Helvetica Neue", 20)
        self.setFont(label_font)
        self.setStyleSheet("QPushButton { background-color: #29c455}")

        self.firstDateEntered = False #flag for the first and second dates

    def _createYearInput(self):  # Creates search bar at the top
        self.yearInput = QLineEdit()
        self.yearInput.setFixedHeight(35)
        self.yearInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.yearInput.setFont(input_font)
        self.generalLayout.addWidget(self.yearInput, 1, 0)

    def _createMonthInput(self):  # Creates search bar at the top
        self.monthInput = QLineEdit()
        self.monthInput.setFixedHeight(35)
        self.monthInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.monthInput.setFont(input_font)
        self.generalLayout.addWidget(self.monthInput, 1, 1)

    def _createDayInput(self):  # Creates search bar at the top
        self.dayInput = QLineEdit()
        self.dayInput.setFixedHeight(35)
        self.dayInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.dayInput.setFont(input_font)
        self.generalLayout.addWidget(self.dayInput, 1, 2)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel("Stock Found! Please enter the first date within two years of today by year, month, and day respectively.")
        self.toplabel.setFixedHeight(35)
        self.generalLayout.addWidget(self.toplabel, 0, 0, 1, 3)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(35)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 1, 3)

    def _createSecondLabel(self):
        today = date.today()
        self.secondlabel = QLabel("Today's date is: " + str(today))
        label_font = QtGui.QFont("Verdana", 20)
        self.secondlabel.setFont(label_font)
        self.generalLayout.addWidget(self.secondlabel, 2, 0, 1, 3)

    def _getYearInput(self):
        year_input = self.yearInput.text()
        if year_input == '':
            return None
        else:
            return year_input

    def _getMonthInput(self):
        month_input = self.monthInput.text()
        if month_input == '':
            return None
        else:
            return month_input

    def _getDayInput(self):
        day_input = self.dayInput.text()
        if day_input == '':
            return None
        else:
            return day_input

    def _removeYearInput(self):
        self.yearInput.setText("")
        self.yearInput.update()

    def _removeMonthInput(self):
        self.monthInput.setText("")
        self.monthInput.update()

    def _removeDayInput(self):
        self.dayInput.setText("")
        self.dayInput.update()


    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    @pyqtSlot()
    def _inputSend(self):

        if not self.firstDateEntered:
            self.DateOneYear = self._getYearInput()
            self.DateOneMonth = self._getMonthInput()
            self.DateOneDay = self._getDayInput()

            print(self.DateOneYear, self.DateOneMonth, self.DateOneDay)
            if not self.main.dateActivate(self.DateOneYear, self.DateOneMonth, self.DateOneDay):
                self.show_warning("Error", "Invalid first date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return
            self._removeYearInput()
            self._removeMonthInput()
            self._removeDayInput()
            self.toplabel.setText("Enter Second Date")
            self.firstDateEntered = True

        else:

            self.DateTwoYear = self._getYearInput()
            self.DateTwoMonth = self._getMonthInput()
            self.DateTwoDay = self._getDayInput()

            print(self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay)

            if not self.main.dateActivate(self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay):
                self.show_warning("Error", "Invalid second date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return
            self._removeYearInput()
            self._removeMonthInput()
            self._removeDayInput()

            #compare dates
            dateOne, dateTwo = self.main.compareDates(self.DateOneYear, self.DateOneMonth, self.DateOneDay, self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay)
            if not dateOne < dateTwo:
                self.show_warning("Error", "First date must be earlier than the second date. Please try again.")
                self._removeYearInput()
                self._removeMonthInput()
                self._removeDayInput()
                return

            print("completed!")

            self.hide()  # hides the first window
            self.switch_to_third(self.stock_name, self.dateOne, self.dateTwo)

    def switch_to_third(self,stockName, dateOne, dateTwo):

        self.clientData = self.main.stockActivator(stockName, dateOne, dateTwo)
        self.third_window = GraphAnalyzerDateWindow(self.clientData)
        self.third_window.show()



class GraphAnalyzerStockWindow(QMainWindow):
    def __init__(self, clientData):  # Initializes GUI. Calls other functions to make other parts of the GUI.

        super().__init__()
        self.clientData = clientData


        QtGui.QFont("Helvetica Neue", 14)
        stockname_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font.setUnderline(True)

        # Stock name
        self.stockname = QLabel(user_data + ":")
        self.stockname.setFont(stockname_font)
        self.generalLayout.addWidget(self.stockname, 1, 0)
        '''
        # 1 Year high
        self.stock_high_1y = QLabel("1 Year High $" + str(round(YahooObject.stock_high_1y, 2)))
        self.stock_high_1y.setFont(info_font)
        self.generalLayout.addWidget(self.stock_high_1y, 1, 1)

        # 1 Year low
        self.stock_low_1y = QLabel("1 Year Low $" + str(round(YahooObject.stock_low_1y, 2)))
        self.stock_low_1y.setFont(info_font)
        self.generalLayout.addWidget(self.stock_low_1y, 2, 1)

        # Price on closing yesterday
        self.stock_closing_price = QLabel(
            "Price From Closing Yesterday: $" + str(round(YahooObject.stock_closing_price, 2)))
        self.stock_closing_price.setFont(info_font)
        self.generalLayout.addWidget(self.stock_closing_price, 3, 1)

        # If the stock has had more up or down days.
        self.up_or_down_days = QLabel("1Y Up/Down: " + str(YahooObject.GoingUpOrDown()))
        self.up_or_down_days.setFont(info_font)
        self.generalLayout.addWidget(self.up_or_down_days, 4, 1)

        # Creating a TickerToName object for next line
        TickerObject = TickerToName(stock_name)

        # Returns the name of the stock
        self.company_name = QLabel(str(TickerObject.company_name))
        self.company_name.setFont(info_font)
        self.generalLayout.addWidget(self.company_name, 2, 0)

        # Will create a button which will open the matplotlib chart for a stock
        self.graph_button = QPushButton("Open Chart")
        self.graph_button.setFont(info_font)
        self.graph_button.setStyleSheet("background-color: #a69695}")
        self.graph_button.clicked.connect(self.makeGraph)
        self.generalLayout.addWidget(self.graph_button, 3, 0)

        # Old worse way of adding a graph that auto opens.
        # canvas = Canvas(self, width=8, height=4)
        # self.generalLayout.addWidget(canvas, 4, 1)
        # This adds a non functional graph to the actual pyqt5 area

    @pyqtSlot()  # Plots our matplotlib graph if the button for a graph is clicked
    def makeGraph(self):
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        data = pd.read_csv("Databases\\" + PyStock.global_stock_name + "_data_base.csv")
        style.use("ggplot")
        plt.plot(data["Date"], data["Close"], color="black")
        plt.ioff()
        plt.ylabel("Price")
        plt.xlabel("1 Year")
        plt.title(PyStock.global_stock_name)
        plt.show()'''


def main():  # Creates instance of GUI and shows it, and allows us to exit it
    GA = QApplication(sys.argv)

    # First window
    first_window = GraphAnalyzerNameWindow()
    user_data = first_window._getInput()

    # Second window
    second_window = GraphAnalyzerDateWindow(user_data)
    second_window.show()
    GA.exec_()
    clientData = second_window.clientData

    # Third window
    third_window = GraphAnalyzerStockWindow(clientData)
    third_window.show()
    third_window.closeEvent = lambda event: sys.exit(0)
    GA.exec_()
''' 
This wouldve been the instantiation of the second window but nothing happens for now.

    dateView = GraphAnalyzerDateWindow()
    dateView.show()
'''




if __name__ == "__main__":
    main()