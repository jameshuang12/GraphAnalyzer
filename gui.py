import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
    QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox

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
        self.searchButton.clicked.connect(self._inputSend)

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

        if not self.main.activate(user_data):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Invalid input. Please try again.")
            msg.exec_()
            #it shows the error message twice for some reason
            return
        else:
            self.close() #closes the current window

            '''
            tried to use the pyqt signal library to see if I can close a first window and
            create a second window to get the two dates.
            '''
            #self.second_window_signal.emit(user_data)



'''
Attempted to create a second class using nearly the same format as the first window. 
'''
'''class GraphAnalyzerDateWindow(QMainWindow):

    def __init__(self):  # Initializes GUI. Calls other functions to make other parts of the GUI.
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
        first_window = GraphAnalyzerNameWindow()
        first_window.second_window_signal.connect(self.show_second_window)

    def _createInput(self):  # Creates search bar at the top
        self.input = QLineEdit()
        self.input.setFixedHeight(35)
        self.input.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.input.setFont(input_font)
        self.generalLayout.addWidget(self.input, 2, 0)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel("Stock Found! Please enter the first date within two years of today.")
        self.toplabel.setFixedHeight(35)
        self.generalLayout.addWidget(self.toplabel, 1, 0)

    def _createSearchButton(self):  # Creates the search button
        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(35)
        self.searchButton.clicked.connect(self._inputSend)
        self.generalLayout.addWidget(self.searchButton, 2, 1)

    def _getInput(self):  # Returns what is in the input box at the time. Also returns it capitalized
        input = self.input.text()
        return input

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
        user_date_one = self._getInput()
        user_date_two = self._getInput()'''


'''
this would've been the third window for the gui with all the rest of the backend in it.
'''
def _createStockInfo(self, user_data):  # Creates all the info about a stock, with QLabels

        QtGui.QFont("Helvetica Neue", 14)
        stockname_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font.setUnderline(True)

        # Stock name
        self.stockname = QLabel(user_data + ":")
        self.stockname.setFont(stockname_font)
        self.generalLayout.addWidget(self.stockname, 1, 0)
        '''
        # Creating stock object so we can get data about it
        clientData = stock_class.Stock(user_data)

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
    pystock_ = QApplication(sys.argv)
    NameView = GraphAnalyzerNameWindow()
    NameView.show()
    sys.exit(pystock_.exec_())
''' 
This wouldve been the instantiation of the second window but nothing happens for now.

    dateView = GraphAnalyzerDateWindow()
    dateView.show()
'''




if __name__ == "__main__":
    main()