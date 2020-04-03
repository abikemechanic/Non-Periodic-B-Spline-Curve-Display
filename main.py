import sys
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import random


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graph_widget = pg.PlotWidget()
        self.setCentralWidget(self.graph_widget)

        x = []
        y = []

        for i in range(10):
            x.append(random.randrange(1, 20, 1))
            y.append(random.randrange(1, 40, 2))

        print(x)
        print(y)

        self.graph_widget.plot(x, y)

        # uic.loadUi('mainwindow.ui', self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
