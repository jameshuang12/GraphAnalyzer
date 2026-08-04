import sys
from gui import QApplication, GraphAnalyzerNameWindow


def main():
    app = QApplication(sys.argv)
    first_window = GraphAnalyzerNameWindow()
    first_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
