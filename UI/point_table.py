from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import random

from control_point import ControlPoint


class PointTable(QtWidgets.QTableWidget):
    header_labels = ['Point #', 'X Value', 'Y Value']
    column_labels = ['Point 1', 'Point 2',
                     'Point 3', 'Point 4',
                     'Point 5', 'Point 6',
                     'Point 7', 'Point 8',
                     'Point 9', 'Point 10']

    table_value_changed = pyqtSignal(list)

    def __init__(self, table_widget: QtWidgets.QTableWidget):
        super(PointTable, self).__init__()

        self.table: QtWidgets.QTableWidget
        self.table = table_widget
        self.table.setHorizontalHeaderLabels(self.header_labels)

        for i in range(self.table.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setText('Point ' + str(i+1))
            self.table.setItem(i, 0, item)

        self.table.itemChanged.connect(self.update_graph)

    def update_graph(self):
        cp_list = self.get_control_points()

        if len(cp_list) == 0:
            return

        self.table_value_changed.emit(cp_list)

    def clear(self):
        self.table.itemChanged.disconnect()

        for i in range(self.table.rowCount()):
            for j in range(1, 3):   # only the second and third rows
                item = QtWidgets.QTableWidgetItem()
                item.setText('')
                self.table.setItem(i, j, item)

        self.table.itemChanged.connect(self.update_graph)
        self.table_value_changed.emit(self.get_control_points())

    def generate_random_control_points(self):
        x = []
        y = []

        self.table.itemChanged.disconnect()

        for i in range(self.table.rowCount()):
            x.append(random.randint(i, 5 + i*4))
            y.append(random.randint(i, i*4 + 3))

        for i in range(self.table.rowCount()):
            item_x = QtWidgets.QTableWidgetItem()
            item_y = QtWidgets.QTableWidgetItem()

            item_x.setText(str(x[i]))
            item_y.setText(str(y[i]))

            self.table.setItem(i, 1, item_x)
            self.table.setItem(i, 2, item_y)

        self.table.itemChanged.connect(self.update_graph)
        self.table_value_changed.emit(self.get_control_points())

    def get_control_points(self):
        cp_list = []

        for i in range(self.table.rowCount()):
            try:
                x_val = self.table.item(i, 1).text()
                y_val = self.table.item(i, 2).text()
                if x_val == '' or y_val == '':
                    continue
            except (AttributeError, ValueError):
                continue
            ctrl_pt = ControlPoint(int(x_val), int(y_val))
            cp_list.append(ctrl_pt)

        return cp_list
