from control_point import ControlPoint
from blending_function import BlendingFunction
import numpy as np

from typing import List


class BSplineCurve:
    def __init__(self, points: List[ControlPoint], k=3):
        self.points = points
        self.k = k              # degree of curve
        self.m = self.k + len(self.points) - 1
        self.knot_vector = []
        self.create_knot_vector()
        self.p_x = []
        self.p_y = []

        self.blending_functions = [[] for i in range(self.k)]
        self.create_blending_function_array()
        self.get_curve_points()

    def create_knot_vector(self):
        """
        create a uniform non-periodic knot vector
        """
        point_count = len(self.points)  # number of control points

        knot_vector_size = point_count + 1 + self.k
        assert knot_vector_size >= self.k * 2

        knot_vector = [0, 0, 0]
        high_val = knot_vector_size - (self.k * 2) + 1
        val = 1

        for i in range(3, knot_vector_size - 3):
            knot_vector.append(val)
            val += 1

        for i in range(3):
            knot_vector.append(val)

        self.knot_vector = knot_vector

    def create_blending_function_array(self):
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
        for u in range(self.knot_vector[-1] * 10):
            p = 0.0

            for i in self.blending_functions[self.k-1][:]:
                p_ = i.blending_func(u/10)
                print(p_)
                p = p + p_

            print('u = ' + str(u))
            print('p = ' + str(p))
            
            self.p_x.append(u)
            self.p_y.append(p)
