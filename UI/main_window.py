import sys
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import random

from UI.point_table import PointTable


class MainWindow(QtWidgets.QMainWindow):
    continuous_update = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = None
        uic.loadUi("UI/mainwindow.ui", self)

        self.btn_Exit: QtWidgets.QPushButton
        self.btn_Exit.clicked.connect(self.exit_program)

        self.table_ControlPoints = PointTable(self.table_ControlPoints)
        self.table_ControlPoints.table_value_changed.connect(self.plot)

        self.plot()

    def plot(self):
        self.graphWidget.clear()
        x = []
        y = []
        for i in range(10):
            x.append(random.randrange(1, 200, 1))
            y.append(random.randrange(1, 400, 2))

        print(x)
        print(y)
        self.graphWidget.plot(x, y)

    def set_continuous_update(self, val):
        self.continuous_update = val

    @staticmethod
    def exit_program(self):
        sys.exit()
