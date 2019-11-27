from myanatomies import FormAnatomy
from myabstract import Point


class TriangleAnatomy(FormAnatomy):
    def __init__(self, **kwargs):
        points = list(map(lambda t: Point(*t), [(1, 0), (-1, -1), (-0.5, 0), (-1, 1)]))
        super().__init__(points, **kwargs)


if __name__ == "__main__":
    t = TriangleAnatomy()
    print(t)
