import sys
from PyQt5 import QtWidgets

from UI.main_window import MainWindow
from control_point import ControlPoint
from b_spline_curve import BSplineCurve

cp_list = []

for i in range(1, 10):
    cp = ControlPoint(i, i + 2)
    cp_list.append(cp)

# b_curve = BSplineCurve(cp_list)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
