from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal


class SpinBoxKSelector(QtWidgets.QSpinBox):
    k_value_changed = pyqtSignal(int)

    def __init__(self, spin_box_widget: QtWidgets.QSpinBox):
        super(SpinBoxKSelector, self).__init__()

        self.k_selector = spin_box_widget
        self._k = 3
        self.k_selector.setValue(self.k)
        self.k_selector.valueChanged.connect(self.value_changed)

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        if self.k == value:
            return

        self.k_selector.setValue(value)
        self.k_value_changed.emit(value)
        self._k = value

    def value_changed(self, val):
        if val < 3:
            val = 3
        elif val > 7:
            val = 7

        self.k = val
