from control_point import ControlPoint
from blending_function import BlendingFunction
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from typing import List


class BSplineCurve(QtWidgets.QWidget):
    knot_vector_changed = pyqtSignal(str)
    curve_points_changed = pyqtSignal(list)
    k_value_changed = pyqtSignal(int)
    failure_message = pyqtSignal(str)

    def __init__(self, points: List[ControlPoint], k=3):
        super(BSplineCurve, self).__init__()
        self.first = True

        # self.k_value_changed.connect(self.update_k_value)
        # self.curve_points_changed.connect(self.update_points_value)

        self._points = points
        self._k_value = k              # degree of curve
        self.m = 0
        self._knot_vector = []
        self.p_x = []
        self.p_y = []
        self.blending_functions = []

        # self.create_blending_function_array()
        # self.get_curve_points()
        self.first = False

    @property
    def k_value(self):
        return self._k_value

    @k_value.setter
    def k_value(self, value):
        if self.k_value != value:
            self._k_value = value

        if self.points and not self.first:
            self.m = self.k_value + len(self.points) - 2
            self.create_b_spline_curve()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if self.points != value:
            self._points = value

        if self.k_value and not self.first:
            self.m = self.k_value + len(self.points) - 2
            self.create_b_spline_curve()

    @property
    def knot_vector(self):
        if self._knot_vector:
            return self._knot_vector
        else:
            self.create_knot_vector()
            return self._knot_vector

    @knot_vector.setter
    def knot_vector(self, value):
        self._knot_vector = value

    def create_b_spline_curve(self):
        try:
            if not self.k_value or not self.points:
                print('no k or points')
                return
        except AttributeError:
            print('attribute error')
            return

        if self.k_value > len(self.points):
            self.failure_message.emit("not enough points for order of curve")
            return

        self.create_knot_vector()
        self.create_blending_function_array()
        self.get_curve_points()
        self.failure_message.emit('')

    def create_knot_vector(self):
        """
        create a uniform non-periodic knot vector
        """
        self.knot_vector = []
        point_count = len(self.points)  # number of control points

        knot_vector_size = point_count + self.k_value     # point_count = n + 1
        # assert knot_vector_size >= self.k_value * 2

        knot_vector = [0 for i in range(self.k_value)]
        high_val = knot_vector_size - (self.k_value * 2) + 1
        val = 1

        for i in range(self.k_value, knot_vector_size - self.k_value):
            knot_vector.append(val)
            val += 1

        for i in range(self.k_value):
            knot_vector.append(val)

        self.knot_vector = knot_vector
        self.format_knot_vector()

    def create_blending_function_array(self):
        self.blending_functions = [[] for i in range(self.k_value)]

        for k in range(1, self.k_value + 1):
            b_func_list = []
            for i in range(self.m):
                if k == 1:
                    bf = BlendingFunction(i, k, (self.knot_vector[i], self.knot_vector[i + 1]), self.knot_vector)
                elif i == self.m - 1:
                    bf = BlendingFunction(i, k, (self.knot_vector[i], self.knot_vector[i + 1]), self.knot_vector,
                                          self.blending_functions[k-2][i])
                else:
                    bf = BlendingFunction(i, k, (self.knot_vector[i], self.knot_vector[i+1]), self.knot_vector,
                                          self.blending_functions[k-2][i], self.blending_functions[k-2][i+1])

                b_func_list.append(bf)

            self.blending_functions[k-1] = b_func_list

    def get_curve_points(self):
        self.p_x = []
        self.p_y = []
        for u in range((len(self.points) + 1) * 100):
            u_ = u/100
            n = 0.0
            n_x = 0.0
            n_y = 0.0

            i = 0
            for bf in self.blending_functions[-1][:]:
                # use only the last column of blending functions
                if bf.limit[0] == bf.limit[1]:
                    i += 1
                    continue

                n_ = bf.blending_func(u_)
                if n_:
                    n_x_ = n_ * self.points[i].x
                    n_y_ = n_ * self.points[i].y

                    n_x += n_x_
                    n_y += n_y_
                i += 1

            if not (n_x == 0 and n_y == 0):
                self.p_x.append(n_x)
                self.p_y.append(n_y)

        self.curve_points_changed.emit([self.p_x, self.p_y])

    def format_knot_vector(self):
        knot_vector_str: str = '('

        for t in self.knot_vector:
            knot_vector_str += str(t) + ', '

        knot_vector_str = knot_vector_str[:-2] + ')'
        self.knot_vector_changed.emit(knot_vector_str)

    def update_k_value(self, k_value):
        self.k_value = k_value

    def update_points_value(self, pts):
        self.points = pts

    def k_value_changed(self, k):
        self.k_value = k
