from typing import Tuple, List


class BlendingFunction:
    def __init__(self, i, k, limit: Tuple[int, int], knot_vector: List[int],
                 N1=None, N2=None):
        self.i = i
        self.k = k
        self.limit = limit
        self.knot_vector = knot_vector
        self.N1: BlendingFunction = N1
        self.N2: BlendingFunction = N2

        # set limits of previous blending functions
        if not (N1 is None or N2 is None):
            limits = set()
            for i in N1.limit:
                limits.add(i)
            for i in N2.limit:
                limits.add(i)

            self.limit = (min(limits), max(limits))

    def blending_func(self, u: float):
        # u not between function limits, otherwise zero
        if self.limit[0] < u <= self.limit[1]:
            pass
        else:
            return None

        if self.limit[0] == self.limit[1]:
            return None
        elif self.k == 1:
            return 1
        else:
            # if self.N1 is None:
            #     self.N1 = 0
            # if self.N2 is None:
            #     self.N2 = 0

            try:
                term_1 = (u - self.knot_vector[self.i]) / (self.knot_vector[self.i + self.k - 1]
                                                           - self.knot_vector[self.i])
                term_1 = term_1 * self.N1.blending_func(u)
            except (ZeroDivisionError, TypeError):
                term_1 = 0

            try:
                term_2 = (self.knot_vector[self.i + self.k] - u) / (self.knot_vector[self.i + self.k]
                                                                    - self.knot_vector[self.i + 1])
                term_2 = term_2 * self.N2.blending_func(u)
            except (ZeroDivisionError, TypeError):
                term_2 = 0

            if term_1 == 0 and term_2 == 0:
                return None

            N_u = term_1 + term_2
            return N_u
