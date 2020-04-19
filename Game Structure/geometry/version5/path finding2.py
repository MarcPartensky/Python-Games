from mywidgets import Button, WidgetManager
from mymap import SimpleMap
from myrectangle import Square

import numpy as np
import mycolors
import random
import pickle


class Terrain(SimpleMap):
    @classmethod
    def random(cls, size, frequency=10):
        cases = [mycolors.BLACK, mycolors.WHITE]
        w, h = size
        grid = [[int(random.randint(1, 10) == 1) for x in range(w)] for y in range(h)]
        grid = np.array(grid)
        return cls(grid, cases)


class AStar:
    def __init__(self, start, end, grid, color=mycolors.BLUE, start_color=mycolors.GREEN, end_color=mycolors.RED):
        self.position = start  # By definition we start at the start...
        self.start = start
        self.end = end
        self.grid = grid
        self.color = color
        self.start_color = start_color
        self.end_color = end_color

    def show(self, context):
        self.end_square.show(context)
        self.start_square.show(context)
        self.square.show(context)

    def getSquare(self):
        """Return the square that corresponds to the position."""
        x, y = self.position
        return Square((x+1/2, y+1/2), 1, area_color=self.color, fill=True)

    def getStartSquare(self):
        """Return the square that corresponds to the start."""
        x, y = self.start
        return Square((x+1/2, y+1/2), 1, area_color=self.start_color, fill=True)

    def getEndSquare(self):
        """Return the square that corresponds to the end."""
        x, y = self.end
        return Square((x+1/2, y+1/2), 1, area_color=self.end_color, fill=True)

    square = property(getSquare)
    start_square = property(getStartSquare)
    end_square = property(getEndSquare)


class PathFinderManager(WidgetManager):
    def __init__(self, size=(10, 10), start=(0, 0), end=(9, 9), **kwargs):
        """Create a new path finder using size, start, end and optional arguments."""
        self.terrain = Terrain.random(size)
        self.path_finder = AStar(start, end, self.terrain.grid)
        widgets = [Button((-5, size[1]-1), (5, 1), text="start"),
                   Button((-5, size[1]-3), (5, 1), text="pause"),
                   Button((-5, size[1]-5), (5, 1), text="restart")]
        super().__init__(widgets, **kwargs)

    def show(self):
        """Show the terrain, the widgets and the path_finder."""
        self.terrain.show(self.context)
        for widget in self.widgets:
            widget.show(self.context)
        self.path_finder.show(self.context)


if __name__ == "__main__":
    finder = PathFinderManager()
    finder()
