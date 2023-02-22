import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
    QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox

from datetime import date
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
        self.setWindowIcon(QtGui.QIcon("stocksimage.png"))
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

    def getInput(self):  # Returns what is in the input box at the time. Also returns it capitalized
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
        user_data = self.getInput()

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
        #these variables will be used for the stock_class in the backend

        self.main = Main()
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("stocksimage.png"))
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
        self.dayInput.setFixedHeight(40)
        self.dayInput.setReadOnly(False)
        input_font = QtGui.QFont("Verdana", 20)
        self.dayInput.setFont(input_font)
        self.generalLayout.addWidget(self.dayInput, 1, 2)

    def _createTopLabel(self):  # Creates the text that says to input a ticker/stock
        self.toplabel = QLabel("             Stock Found! Please enter the earlier first date within two years as numbers: " + "\n"
        + "               Year                            "
        "Month                                   Day")
        self.toplabel.setFixedHeight(80)
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

            #compare dates
            dateOne, dateTwo = self.main.compareDates(self.DateOneYear, self.DateOneMonth, self.DateOneDay, self.DateTwoYear, self.DateTwoMonth, self.DateTwoDay)
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

    def switch_to_third(self,stockName, dateOne, dateTwo):
        clientData = self.main.stockActivator(stockName, dateOne, dateTwo)
        self.third_window = GraphAnalyzerStockWindow(clientData)
        self.third_window.show()


class GraphAnalyzerStockWindow(QMainWindow):
    def __init__(self, clientdata):  # Initializes GUI. Calls other functions to make other parts of the GUI.

        super().__init__()

        self.main = Main()
        self.setWindowTitle("Graph Analyzer")
        self.setWindowIcon(QtGui.QIcon("stocksimage.png"))
        self.setFixedSize(1000, 700)

        self.generalLayout = QGridLayout()  # Using grid layout with coordinates for this project
        self._centralWidget = QWidget(self)  # Central widget
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)  # .generalLayout is our main layout
        self.clientData = clientdata
        self.exitButton()

        info_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font = QtGui.QFont("Helvetica Neue", 14)
        stockname_font.setUnderline(True)

        name_font = QtGui.QFont("Helvetica Neue", 40)


        # 1st Date's open amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_open = QLabel("1st Date's Open $" + str(round(clientdata.high[0], 2)))
        self.stock_dateone_open.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_open, 1, 6)

        # 1st Date's high amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_high = QLabel("1st Date's High $" + str(round(clientdata.open[0], 2)))
        self.stock_dateone_high.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_high, 2, 6)

        # 1st Date's low amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_low = QLabel("1st Date's Low $" + str(round(clientdata.low[0], 2)))
        self.stock_dateone_low.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_low, 3, 6)

        # 1st Date's close amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_dateone_close = QLabel("1st Date's Close $" + str(round(clientdata.close[0], 2)))
        self.stock_dateone_close.setFont(info_font)
        self.generalLayout.addWidget(self.stock_dateone_close, 4, 6)

        # 2nd Date's open amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_open = QLabel("2nd Date's Open $" + str(round(clientdata.open[len(clientdata) - 1], 2)))
        self.stock_datetwo_open.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_open, 5, 6)

        # 2nd Date's high amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_high = QLabel("2nd Date's High $" + str(round(clientdata.high[len(clientdata) - 1], 2)))
        self.stock_datetwo_high.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_high, 6, 6)

        
        # 2nd Date's low amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_low = QLabel("2nd Date's Low $" + str(round(clientdata.low[len(clientdata) - 1], 2)))
        self.stock_datetwo_low.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_low, 7, 6)

        # 2nd Date's close amount that will be added to the 3rd GUI, will also be used in the graph
        # The code is getting the value from that date, setting the font, and adding to the gui
        self.stock_datetwo_close = QLabel("2nd Date's Close $" + str(round(clientdata.close[len(clientdata) - 1], 2)))
        self.stock_datetwo_close.setFont(info_font)
        self.generalLayout.addWidget(self.stock_datetwo_close, 8, 6)

        # Creating a TickerToName object for next line
        Company = clientdata.tick_name

        # Returns the name of the stock
        self.company_name = QLabel(Company)
        self.company_name.setFont(name_font)
        self.generalLayout.addWidget(self.company_name, 0, 3)

        # Will create a button which will open the matplotlib chart for a stock
        self.graph_button = QPushButton("Open Graph")
        self.graph_button.setFont(info_font)
        self.graph_button.setStyleSheet("background-color: #a69695}")
        self.graph_button.clicked.connect(lambda: self.makeGraph(clientdata))
        self.generalLayout.addWidget(self.graph_button, 3, 0, 1, 1)



    @pyqtSlot()  # Plots our matplotlib graph if the button for a graph is clicked
    def makeGraph(self, clientdata):
         mpl.rcParams["toolbar"] = "None"
         plt.style.use("dark_background")
         #this portion can either read the two dates listed and print out the closing between the two dates
         # we can also use the numbers above

         style.use("ggplot")
         # plots the x axis
         plt.plot(clientdata.high, color="black")
         plt.ioff()
         plt.xlabel("From " + str(clientdata.day1) + " to " + str(clientdata.day2) + " in days")
         plt.ylabel("Amount($)")
         plt.title(clientdata.tick_name)
         plt.show()

    def exitButton(self):
        # create a button to exit the application
        exit_button = QPushButton('Exit', self)
        exit_button.move(20, 640)
        exit_button.clicked.connect(self.show_popup)

         #will need to fix the windows and such
        self.setWindowTitle('My App')
        self.show()

    def show_popup(self):
        # show the message box
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if the user clicks Yes, exit the application
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

def main():  # Creates instance of GUI and shows it, and allows us to exit it
    GA = QApplication(sys.argv)

    # First window
    first_window = GraphAnalyzerNameWindow()
    first_window.show()
    #for some reason, the entire gui is ran by the GA.exec_() and once I click the exit button,
    #it runs the code underneath and gets the errors. However, if I put the sys.exit line right under,
    # it still runs and the exit code 0 appears.
    GA.exec_()
    sys.exit(GA.exec_())

    user_data = first_window.getInput()

    # Second window
    second_window = GraphAnalyzerDateWindow(user_data)
    second_window.show()
    clientData = second_window.clientData()

    # Third window
    third_window = GraphAnalyzerStockWindow(clientData)
    third_window.show()
    third_window.close()

if __name__ == "__main__":
    main()