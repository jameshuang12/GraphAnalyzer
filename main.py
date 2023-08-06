from gui import QApplication, \
    GraphAnalyzerNameWindow, GraphAnalyzerDateWindow, GraphAnalyzerStockWindow
import sys


def main():
    """
    Creates the instances of the GUI that gets the name of the company, two dates the user's
    wants to utilize, and give the user various options to execute with that company's stock option. 
    """
    GA = QApplication(sys.argv)

    # First window
    first_window = GraphAnalyzerNameWindow()
    first_window.show()
    user_data = first_window.getInput()
    GA.exec_()

    # Second window
    second_window = GraphAnalyzerDateWindow(user_data)
    second_window.show()
    client_data = second_window.clientData()

    # Third window
    third_window = GraphAnalyzerStockWindow(client_data)
    third_window.show()
    third_window.close()


if __name__ == "__main__":
    main()
