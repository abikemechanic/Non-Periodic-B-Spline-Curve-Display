class BlendingFunction:
    def __init__(self, i, k, limit: tuple[int, int]):
        self.i = i
        self.k = k
        self.limit = limit

    def blending_func(self):
        if self.limit[0] == self.limit[1]:
            return 0
        elif self.k == 1:
            return 1
        else:
            pass
