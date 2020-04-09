from typing import Tuple, List


class BlendingFunction:
    def __init__(self, i, k, limit: Tuple[int, int], control_points: List[int]):
        self.i = i
        self.k = k
        self.limit = limit
        self.control_points = control_points

    def blending_func(self, u):
        if self.limit[0] == self.limit[1]:
            return 0
        elif self.k == 1:
            return 1
        else:

