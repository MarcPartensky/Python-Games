from pygame_geometry.events import Control, Event, Manager
import pygame

def zoom_in(manager:Manager):
    manager.context.plane.zoom([1.1, 1.1])

def zoom_out(manager:Manager):
    manager.context.plane.zoom([0.9, 0.9])

controls = [
    Control(Event(pygame.KEYDOWN, key=pygame.K_RSHIFT), zoom_in),
    Control(Event(pygame.KEYDOWN, key=pygame.K_LSHIFT), zoom_out),
]