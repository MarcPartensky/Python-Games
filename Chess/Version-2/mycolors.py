BLUE       = (  0,  0,255)
RED        = (255,  0,  0)
GREEN      = (  0,255,  0)
YELLOW     = (255,255,  0)
BLACK      = (  0,  0,  0)
WHITE      = (255,255,255)
GREY       = (100,100,100)
PURPLE     = (100,  0,100)
HALFGREY   = ( 50, 50, 50)
DARKGREY   = ( 20, 20, 20)
DARKRED    = ( 10, 10, 10)
DARKGREEN  = ( 10, 10, 10)
DARKBLUE   = ( 10, 10, 10)
LIGHTBROWN = (229,219,222)
LIGHTGREY  = (200,200,200)
BEIGE      = (199,175,138)

def randomColor():
    import random
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    color=(r,g,b)
    return color

def reverseColor(color):
    r,g,b=color
    r=255-r
    g=255-g
    b=255-b
    color=(r,g,b)
    return color

def colorize(image, newColor):
    import pygame
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image

def lighten(color,light=1):
    r,g,b=color
    r*=light
    g*=light
    b*=light
    color=(r,g,b)
    return color

print("mycolors imported")
