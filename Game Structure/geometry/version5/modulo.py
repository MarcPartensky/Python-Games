import math


class Modulo:
    def __init__(self, n, a=None):
        """'n' is the number, and 'a' is the modulo"""
        if a == None:
            self.a = float("inf")
        else:
            self.a = a
        self.n = n % self.a

    # Type conversions
    def __str__(self):
        return str(self.n)

    def __int__(self):
        return self.n

    def __float__(self):
        return float(self.n)

    # Operations

    # Addition
    def __add__(self, other):
        return (self.n + other.n) % self.a

    __radd__ = __add__

    def __iadd__(self, other):
        self.n = (self.n + other.n) % self.a
        return self

    # Subtraction
    def __sub__(self, other):
        return (self.n - other.n) % self.a

    __rsub__ = __sub__

    def __isub__(self, other):
        self.n = (self.n - other.n) % self.a
        return self

    # Multiplication
    def __mul__(self, m):
        return (self.n * float(m)) % self.a

    __rmul__ = __mul__

    def __imul__(self, m):
        self.n = (self.n * float(m)) % self.a
        return self

    # True division
    def __truediv__(self, m):
        return (self.n / float(m)) % self.a

    __rtruediv__ = __truediv__

    def __itruediv__(self, m):
        self.n = (self.n / float(m)) % self.a
        return self

    # Floor division
    def __floordiv__(self, m):
        return (self.n // float(m)) % self.a

    __rfloordiv__ = __floordiv__

    def __ifloordiv__(self, m):
        self.n = (self.n // float(m)) % self.a
        return self

    # Exponentiation
    def __pow__(self, m):
        return (self.n ** float(m)) % self.a

    __rpow__ = __pow__

    def __ipow__(self, m):
        self.n = (self.n ** float(m)) % self.a
        return self


if __name__ == "__main__":
    a = Modulo(5, 2 * math.pi)
    b = Modulo(202, 2 * math.pi)
    c = Modulo(62)

    print(((a + b - c * a) * 5 / 2) ** 2)