class BlendingFunction:
    def __init__(self, i, k, limit: tuple[int, int]):
        self.i = i
        self.k = k
        self.limit = limit

    def __eq__(self, other):
        # if the ends of the limits are the same then the
        return self.limit[0] == other.limit[0] & self.limit[1] == other.limit[1]
