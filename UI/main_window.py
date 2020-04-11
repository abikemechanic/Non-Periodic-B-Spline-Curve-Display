import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from typing import List

from UI.point_table import PointTable
from b_spline_curve import BSplineCurve
from UI.spin_box_k_selector import SpinBoxKSelector


class MainWindow(QtWidgets.QMainWindow):
    continuous_update = True

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = None
        self.b_curve = None
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
        self.table_ControlPoints.table_value_changed.connect(self.auto_update_graph)

        # Graph
        self.graphWidget: pg.PlotWidget
        self.graphWidget.setBackground('w')

        # Increase K button
        self.pb_IncreaseK: QtWidgets.QPushButton
        self.pb_IncreaseK.clicked.connect(self.increase_k)

        # Decrease K button
        self.pb_DecreaseK: QtWidgets.QPushButton
        self.pb_DecreaseK.clicked.connect(self.decrease_k)

        # Line edit K display
        self.lineEdit_K: QtWidgets.QLineEdit
        self.lineEdit_K.setText(str(3))

    def clear_control_point_table(self):
        print('cleared control point table')
        self.table_ControlPoints.clear()

    def generate_random_points(self):
        self.table_ControlPoints.generate_random_control_points()

    def auto_update_graph(self, control_points):
        if self.continuous_update and len(control_points) >= 3:
            self.plot(control_points)

    def update_graph(self):
        ctrl_pts = self.table_ControlPoints.get_control_points()

        if ctrl_pts:
            self.plot(self.table_ControlPoints.get_control_points())

    def plot(self, control_points):
        self.graphWidget.clear()

        x = []
        y = []
        for pt in control_points:
            x.append(pt.x)
            y.append(pt.y)

        control_polygon_pen = pg.mkPen(color='b', width=1)
        self.graphWidget.plot(x, y, pen=control_polygon_pen)

        self.b_curve = BSplineCurve(control_points, int(self.lineEdit_K.text()))
        knot_vector = self.b_curve.knot_vector

        # set knot vector line edit widget
        self.lineEdit_KnotVector: QtWidgets.QLineEdit
        knot_vector_str = '('
        for kv in knot_vector:
            knot_vector_str += str(kv) + ', '
        knot_vector_str = knot_vector_str[:-2] + ')'
        self.lineEdit_KnotVector.setText(knot_vector_str)

        self.plot_curve()

    def plot_curve(self):
        b_curve_pen = pg.mkPen('r', width=2)
        self.graphWidget.plot(self.b_curve.p_x, self.b_curve.p_y, pen=b_curve_pen)

    def set_continuous_update(self, val):
        self.continuous_update = bool(val)

    def update_k_value(self, k: int):
        if self.b_curve:
            self.b_curve.k = k
            self.update_graph()
            
    def increase_k(self):
        if not self.b_curve:
            return

        self.b_curve.k += 1
        self.update_k_value(self.b_curve.k)
        self.lineEdit_K.setText(str(self.b_curve.k))
        
    def decrease_k(self):
        if not self.b_curve:
            return

        self.b_curve.k -= 1
        self.update_k_value(self.b_curve.k)
        self.lineEdit_K.setText(str(self.b_curve.k))

    @staticmethod
    def exit_program(self):
        sys.exit()
