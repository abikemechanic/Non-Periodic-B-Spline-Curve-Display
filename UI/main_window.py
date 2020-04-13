import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from typing import List

from UI.point_table import PointTable
from b_spline_curve import BSplineCurve
from UI.spin_box_k_selector import SpinBoxKSelector
from control_point import ControlPoint


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = None
        self.b_curve = None
        uic.loadUi("UI/mainwindow.ui", self)

        self._k: int = 3
        self._control_points: List[ControlPoint] = []
        self._continuous_update = True

        # B Spline Curve
        self.b_curve = BSplineCurve(None, self.k)
        self.b_curve.knot_vector_changed.connect(self.update_knot_vector)
        self.b_curve.curve_points_changed.connect(self.auto_plot_curve)
        self.b_curve.failure_message.connect(self.update_failure_message)

        # Exit button
        self.btn_Exit: QtWidgets.QPushButton
        self.btn_Exit.clicked.connect(self.exit_program)

        # Create graph button
        self.btn_Graph_2: QtWidgets.QPushButton
        self.btn_Graph_2.clicked.connect(self.manual_plot_curve)

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
        self.table_ControlPoints.table_value_changed.connect(self.update_control_points)

        # Graph
        self.graphWidget: pg.PlotWidget
        self.graphWidget.setBackground('w')

        # Spinbox K Selector
        self.spinBox_k: SpinBoxKSelector = SpinBoxKSelector(self.spinBox_k)
        self.spinBox_k.k_value_changed.connect(self.update_k_value)

        # Line edit knot vector
        self.lineEdit_KnotVector: QtWidgets.QLineEdit = self.lineEdit_KnotVector

        # Message Display
        self.lbl_FailureMessage: QtWidgets.QLabel

    # PROPERTIES
    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self.b_curve.k_value_changed(value)
        self._k = value

    @property
    def control_points(self):
        return self._control_points

    @control_points.setter
    def control_points(self, value):
        if self._control_points != value:
            self._control_points = value
            self.graphWidget.clear()

        if self.continuous_update:
            self.auto_plot_control_polygon(value)

        self.b_curve.points = value

    @property
    def continuous_update(self):
        return self._continuous_update

    @continuous_update.setter
    def continuous_update(self, value):
        self._continuous_update = value

    # END PROPERTIES

    def clear_control_point_table(self):
        self.table_ControlPoints.clear()

    def generate_random_points(self):
        self.table_ControlPoints.generate_random_control_points()

    # def update_graph(self):
    #     self.b_curve.create_b_spline_curve()

    def auto_plot_control_polygon(self, control_points: List[ControlPoint]):
        x = []
        y = []
        
        for cp in control_points:
            x.append(cp.x)
            y.append(cp.y)

        pen = pg.mkPen(color='b', width=1)
        self.graphWidget.plot(x, y, pen=pen, name='Control Polygon')

    def manual_plot_control_polygon(self, control_points:List[ControlPoint]):
        self.auto_plot_control_polygon(control_points)

    def auto_plot_curve(self, points: List[List[int]]):
        self.graphWidget.clear()
        
        p_x = points[0]
        p_y = points[1]

        b_curve_pen = pg.mkPen('r', width=2)
        self.graphWidget.plot(p_x, p_y, pen=b_curve_pen, name='B-Spline Curve')
        self.auto_plot_control_polygon(self.b_curve.points)

    def manual_plot_curve(self):
        self.graphWidget.clear()

        p_x = self.b_curve.p_x
        p_y = self.b_curve.p_y

        pen = pg.mkPen('r', width=2)
        self.graphWidget.plot(p_x, p_y, pen=pen, name='B-Spline Curve')
        self.manual_plot_control_polygon(self.b_curve.points)

    def set_continuous_update(self, val):
        self.continuous_update = bool(val)

        if not val:
            self.b_curve.curve_points_changed.disconnect()
        else:
            self.b_curve.curve_points_changed.connect(self.auto_plot_curve)

    def update_k_value(self, k: int):
        self.k = k

    def update_control_points(self, ctrl_pts):
        self.control_points = ctrl_pts

    def update_knot_vector(self, knot_vector: str):
        self.lineEdit_KnotVector.setText(knot_vector)

    def update_failure_message(self, msg: str):
        self.lbl_FailureMessage.setText(msg)

    @staticmethod
    def exit_program(self):
        sys.exit()
