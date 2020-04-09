import sys
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import random

from UI.point_table import PointTable


class MainWindow(QtWidgets.QMainWindow):
    continuous_update = True

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = None
        uic.loadUi("UI/mainwindow.ui", self)

        # exit button
        self.btn_Exit: QtWidgets.QPushButton
        self.btn_Exit.clicked.connect(self.exit_program)

        # Create Graph Button
        self.btn_Graph_2: QtWidgets.QPushButton
        self.btn_Graph_2.clicked.connect(self.update_graph)

        # Clear control points table button
        self.btn_DeleteAllPoints: QtWidgets.QPushButton
        self.btn_DeleteAllPoints.clicked.connect(self.clear_control_point_table)

        # Create random points in control points table
        self.btn_GenerateControlPoints: QtWidgets.QPushButton
        self.btn_GenerateControlPoints.clicked.connect(self.generate_random_points)

        # Continuous update checkbox
        self.checkBox_ContinuousUpdate: QtWidgets.QCheckBox
        self.checkBox_ContinuousUpdate.stateChanged.connect(self.set_continuous_update)
        self.checkBox_ContinuousUpdate.setChecked(True)

        # Control point table
        self.table_ControlPoints = PointTable(self.table_ControlPoints)
        self.table_ControlPoints.table_value_changed.connect(self.plot)

    def clear_control_point_table(self):
        print('cleared control point table')
        self.table_ControlPoints.clear()

    def generate_random_points(self):
        self.table_ControlPoints.generate_random_control_points()

    def update_graph(self):
        pts = self.table_ControlPoints.get_control_points()
        self.plot(pts)

    def plot(self, control_points):
        self.graphWidget.clear()

        x = []
        y = []
        for pt in control_points:
            x.append(pt.x)
            y.append(pt.y)

        self.graphWidget.plot(x, y)

    def set_continuous_update(self, val):
        self.continuous_update = bool(val)

    @staticmethod
    def exit_program(self):
        sys.exit()
