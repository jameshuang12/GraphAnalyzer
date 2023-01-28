import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,\
    QLabel, QGridLayout, QLineEdit, QPushButton

from name_to_ticker import TickerToName
from yfinance_part import YahooStockInfo

import matplotlib as mpl
import matplotlib.dates
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt

#we are going to use this guy's gui so here the link
# https://github.com/ViktorBash/PyStocks/blob/master/Stock%20Project/gui_part.py

class PyStock(QMainWindow):
    amount_searched = 0  # Will be useful later when we want to delete widgets to update our search data
    global_stock_name = " "

    def __init__(self):  # Initializes GUI. Calls other functions to make other parts of the GUI.
        super().__init__()
        self.setWindowTitle("PyStocks")
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
        self.generalLayout.addWidget(self.input, 0, 1)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel("Enter Ticker")
        self.toplabel.setFixedHeight(35)
        self.generalLayout.addWidget(self.toplabel, 0, 0)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(35)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 0, 3)

    def _getInput(
            self):  # Returns what is in the input box at the time. Also returns it capitalized
        input = self.input.text()
        return input.upper()

    def _removeInput(self):  # Resets input box
        self.input.setText("")

    @pyqtSlot()  # Connects the search button to functions
    def _inputSend(self):
        # Because something is searched, the search counter goes up
        PyStock.amount_searched = PyStock.amount_searched + 1
        if PyStock.amount_searched > 1:
            """
                       When we first search something this if statement will not activate because amount_searched is one.
                       This is fine because when we search again it does activate and it resets the text so new data can be
                       displayed. Without this the old search would still remain in our GUI and mush with the new search data.
                       """
            self.stockname.setText("")
            self.stock_high_1y.setText("")
            self.stock_low_1y.setText("")
            self.stock_closing_price.setText("")
            self.up_or_down_days.setText("")
            self.company_name.setText("")
        print(self._getInput())  # For debugging purposes to the console
        PyStock.global_stock_name = self._getInput()
        self._createStockInfo(self._getInput())  # Creates the labels with the stock info.
        self._removeInput()  # Removes input from the search bar

    def _createStockInfo(self, stock_name):  # Creates all the info about a stock, with QLabels

        info_font = QtGui.QFont("Helvetica Neue", 14)  # Styling
        stockname_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font.setUnderline(True)

        # Stock name
        self.stockname = QLabel(stock_name + ":")
        self.stockname.setFont(stockname_font)
        self.generalLayout.addWidget(self.stockname, 1, 0)

        # Creating stock object so we can get data about it
        YahooObject = YahooStockInfo(stock_name)

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
        # self.generalLayout.addWidget(canvas, 4, 1)  # This adds a non functional graph to the actual pyqt5 area

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
        plt.show()
def main():  # Creates instance of GUI and shows it, and allows us to exit it
    pystock_ = QApplication(sys.argv)
    view = PyStock()
    view.show()
    sys.exit(pystock_.exec())


if __name__ == "__main__":
    main()