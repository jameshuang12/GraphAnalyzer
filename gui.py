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




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

