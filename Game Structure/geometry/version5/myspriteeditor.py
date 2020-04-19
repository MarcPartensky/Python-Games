from mymanager import ActivityManager
from myactivity import Activity, Component
from myrectangle import Square
from mywidgets import Widget, Slider

import math
import mycolors


class SquareComponent(Square, Component, Widget):
    def __init__(self, *args, **kwargs):
        Square.__init__(self, *args, **kwargs)
        Component.__init__(self)
        Widget.__init__(self)
        self.side_width = 3

    def show(self, context):
        if self.state == Widget.default:
            self.side_color = mycolors.WHITE
        elif self.state == Widget.hovered:
            self.side_color = mycolors.GREEN
        elif self.state == Widget.focused:
            self.side_color = mycolors.BLUE
        elif self.state == Widget.clicked:
            self.side_color = mycolors.RED
        super().show(context)


class SpriteActivity(Activity):

    def __init__(self, *args):
        super().__init__(*args)
        self.event_now = False

    def onMouseMotion(self, position):
        for component in self:
            component.state = Widget.default
            if position in component:
                component.state = Widget.hovered

    def onMouseButtonDown(self, button, position):
        selection = None
        for component in self:
            if position in component:
                selection = component
                break
        if selection:
            self.remove(selection)
        else:
            x, y = position
            x = math.floor(x) + 0.5
            y = math.floor(y) + 0.5
            self.append(SquareComponent(x, y, 1, fill=True))
        self.event_now = True

    def show(self, context):
        super().show(context)
        if self.event_now:
            context.console("new component:", self[-1])
            self.event_now = False


if __name__ == "__main__":
    sa = SpriteActivity()
    m = ActivityManager([sa])
    m()
