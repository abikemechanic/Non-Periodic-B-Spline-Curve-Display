import sys
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import random


class MainWindow(QtWidgets.QMainWindow):
    continuous_update = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        x = []
        y = []
        for i in range(10):
            x.append(random.randrange(1, 200, 1))
            y.append(random.randrange(1, 400, 2))

        print(x)
        print(y)

        uic.loadUi("mainwindow.ui", self)
        self.plot(x, y)

    def plot(self, x, y):
        self.graphWidget.plot(x, y)

    def set_continuous_update(self, val):
        self.continuous_update = val