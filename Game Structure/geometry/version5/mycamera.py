from mymanager import Manager

from pygame.locals import *
import numpy as np
import pygame
import cv2

#import sys
#camera = cv2.VideoCapture(0)
#pygame.init()
#pygame.display.set_caption("OpenCV camera stream on Pygame")
#screen = pygame.display.set_mode([1280,720])
"""
try:
    while True:

        ret, frame = camera.read()

        screen.fill([0,0,0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                sys.exit(0)
except (KeyboardInterrupt,SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()"""


class CameraManager(Manager):
    def __init__(self,*args,**kwargs):
        """Create the capture using the arguments of the manager but create its
        own camera in addition."""
        Manager.__init__(self,*args,**kwargs)
        self.camera=cv2.VideoCapture(0)

    def show(self):
        """Show the video."""
        ret, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.context.draw.image(self.context.screen,frame,(0,0))

        








class Camera:
    """The camera rely on opencv, pygame and numpy."""
    def __init__(self):
        """Create an opencv camera."""
        self.camera=cv2.VideoCapture(0)

    def show(self,draw,position=[0,0]):
        """Show the video."""
        ret, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        draw.image(draw.window.screen,frame,position)


if __name__=="__main__":
    c=CameraManager(name="capture")
    c()
