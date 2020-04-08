from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic


class PointTable(QtWidgets.QTableWidget):
    header_labels = ['Point #', 'X Value', 'Y Value']
    column_labels = ['Point 1', 'Point 2',
                     'Point 3', 'Point 4',
                     'Point 5', 'Point 6',
                     'Point 7', 'Point 8',
                     'Point 9', 'Point 10']

    table_value_changed = pyqtSignal()

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
        print('item changed')
        self.table_value_changed.emit()

    def clear(self):
        self.table.itemChanged.disconnect()

        for i in range(self.table.rowCount()):
            for j in range(1, 3):
                item = QtWidgets.QTableWidgetItem()
                item.setText('')
                self.table.setItem(i, j, item)

        self.table.itemChanged.connect(self.update_graph)
