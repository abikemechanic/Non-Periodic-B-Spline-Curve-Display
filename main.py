import sys
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import random

from main_window import MainWindow
from control_point import ControlPoint
from b_spline_curve import BSplineCurve

cp_list = []

for i in range(1, 10):
    cp = ControlPoint(i, i + 2)
    cp_list.append(cp)

b_curve = BSplineCurve(cp_list)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
