from gui import  QApplication,\
    GraphAnalyzerNameWindow, GraphAnalyzerDateWindow, GraphAnalyzerStockWindow
import sys
def main():  # Creates instance of GUI and shows it, and allows us to exit it
    GA = QApplication(sys.argv)

    # First window
    first_window = GraphAnalyzerNameWindow()
    first_window.show()
    sys.exit(GA.exec_())
    user_data = first_window.getInput()

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