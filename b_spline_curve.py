from control_point import ControlPoint

from typing import List


class BSplineCurve:
    def __init__(self, points: List[ControlPoint], k=3):
        self.points = points
        self.k = k              # degree of curve
        self.knot_vector = []

        self.create_knot_vector()

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
