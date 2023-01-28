import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGridLayout, QLineEdit, QPushButton

from name_to_ticker import TickerToName
from yfinance_part import YahooStockInfo

import matplotlib as mpl
import matplotlib.dates
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")

#we are going to use this guy's gui so here the link
# https://github.com/ViktorBash/PyStocks/blob/master/Stock%20Project/gui_part.py