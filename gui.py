import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit,
                             QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit,
                             QMainWindow, QProgressBar,
                             QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,
                             QWidget, QHBoxLayout, QStackedLayout,
                             )
from layout_colorwidget import Color

# The link for the GUI: https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Graph Analyzer")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        widget = QLabel("Welcome to our website")
        font = widget.font()
        font.setPointSize(20)

        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)

        widget2 = QWidget()
        widget2.setLayout(pagelayout)
        self.setCentralWidget(widget2)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

