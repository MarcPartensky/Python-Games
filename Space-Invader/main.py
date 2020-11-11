#!/usr/bin/env python
from pygame_geometry.context import Context
from pygame_geometry.events import on, Manager
from pygame_geometry.triangle import Triangle
from pygame_geometry.body import Body
from pygame_geometry.anatomies import Anatomy
from pygame_geometry.motion import Motion
from pygame_geometry.abstract import Vector
from pygame_geometry import colors
from controls import controls
import pygame

class TriangleAnatomy(Anatomy):
    def __init__(self):
        self.triangle:Triangle = Triangle.random(area_color=colors.RED)

    def show(self, context):
        self.triangle.show(context)

    def rotate(self, angle):
        self.triangle.rotate(angle)


class PlaneController(Manager):
    @on.press(pygame.KEYDOWN, pygame.K_RSHIFT)
    def zoom(self):
        print('zoom')
        self.context.zoom()


class SpaceInvader(Manager):
    def __init__(self, context:Context, controls:list):
        super().__init__(context)
        self.player = Body(
            TriangleAnatomy(),
            [Motion(Vector(0, 0), Vector(0, 0))]
        )
        self.controls.extend(controls)

    @on.press(pygame.KEYDOWN, pygame.K_ESCAPE)
    def quit(self):
        """Quit the game."""
        self.on = False

    @on.press(pygame.KEYDOWN, pygame.K_w)
    def up(self):
        """Make the player go up."""
        self.player.position.y += 1

    def show(self):
        """Show the game."""
        super().show()
        self.player.show(self.context)
        self.context.console.show()


class SpaceInvaderDebugger(Manager):
    @on.press(pygame.KEYDOWN, pygame.K_t)
    def triangle(self):
        self.context.console(self.player.anatomy.triangle)

    @on.press(pygame.KEYDOWN, pygame.K_p)
    def position(self):
        """Show the position of the player."""
        self.context.console(self.player.position)


if __name__=="__main__":
    context = Context(name="Space Invader")
    # controls = SpaceInvaderDebugger(context).controls + PlaneController(context).controls
    space_invader = SpaceInvader(context, controls)
    space_invader()
