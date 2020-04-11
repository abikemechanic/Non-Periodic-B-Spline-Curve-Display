from control_point import ControlPoint
from blending_function import BlendingFunction
import numpy as np

from typing import List


class BSplineCurve:
    def __init__(self, points: List[ControlPoint], k=3):
        self.points = points
        self._k = k              # degree of curve
        self.m = self.k + len(self.points) - 2
        self._knot_vector = []
        self.create_knot_vector()
        self.p_x = []
        self.p_y = []

        self.blending_functions = []
        self.create_blending_function_array()
        self.get_curve_points()

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        if value < 3:
            value = 3
        elif value > 7:
            value = 7

        self._k = value
        self.create_knot_vector()
        self.create_blending_function_array()
        self.get_curve_points()

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

    def create_knot_vector(self):
        """
        create a uniform non-periodic knot vector
        """
        self.knot_vector = []
        point_count = len(self.points)  # number of control points

        knot_vector_size = point_count + self.k     # point_count = n + 1
        # assert knot_vector_size >= self.k * 2

        knot_vector = [0 for i in range(self.k)]
        high_val = knot_vector_size - (self.k * 2) + 1
        val = 1

        for i in range(self.k, knot_vector_size - self.k):
            knot_vector.append(val)
            val += 1

        for i in range(self.k):
            knot_vector.append(val)

        self.knot_vector = knot_vector

    def create_blending_function_array(self):
        self.blending_functions = [[] for i in range(self.k)]

        for k in range(1, self.k + 1):
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
        p_x = []
        p_y = []
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
