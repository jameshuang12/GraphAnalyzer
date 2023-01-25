import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication,QCheckBox,QComboBox,QDateEdit,QDateTimeEdit,
    QDial,QDoubleSpinBox,QFontComboBox,QLabel,QLCDNumber,QLineEdit,QMainWindow,QProgressBar,
    QPushButton,QRadioButton,QSlider,QSpinBox,QTimeEdit,QVBoxLayout,QWidget,
)

# The link for the GUI: https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Graph Analyzer")

        widget = QLabel("Welcome to our website")
        font = widget.font()
        font.setPointSize(25)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)


        # This create a checkbox in our gui, this is not seen as it is not set in this code


        widget = QCheckBox()
        widget.setCheckState(Qt.Checked)

        widget.setCheckState(Qt.PartiallyChecked)
        widget.setTristate(True)
        widget.stateChanged.connect(self.show_state)

        self.setCentralWidget(widget)

        # This is to create a slidedown option, this is not shown since widget is not set

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        # Sends the current index (position) of the selected item.
        widget.currentIndexChanged.connect(self.index_changed)





    def index_changed(self, i):  # i is an int
        print(i)

    def text_changed(self, s):  # s is a str
        print(s)

    def show_state(self, s):
        print(s == Qt.Checked)
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

