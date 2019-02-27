from mywindow import Window
from mycolors import *

import pygame

class Paint:
    def __init__(self,tools=[]):
        self.name="Paint"
        self.tools=tools
        self.sets=[]

    def __call__(self,window):
        window.name=self.name
        window.fullscreen=True
        window.build()
        #self.show(window)

        while window.open:
            window.check()
            self.draw()



    def draw(self,window):
        """Allow user to draw on screen."""
        radius=2
        wavelength=380
        color=self.reverseColor(self.background_color)
        form=0
        size=[10,10]
        width=0
        while window.open:
            window.check()
            click=window.click()
            position=window.point()
            if click:
                self.trace(position,size,self.wavelengthToRGB(wavelength),radius,form,width)
            else:
                self.hand[0].points=[]
                #print(size)
            keys=pygame.key.get_pressed()
            if keys[K_LSHIFT] and radius>10:
                radius-=1
            if keys[K_RSHIFT] and radius:
                radius+=1
            if keys[K_LEFT] and wavelength>380:
                wavelength-=1
            if keys[K_RIGHT] and wavelength<780:
                wavelength+=1
            if keys[K_q] and size[0]>0:
                size[0]-=1
            if keys[K_w]:
                size[0]+=1
            if keys[K_e] and size[1]>0:
                size[1]-=1
            if keys[K_r]:
                size[1]+=1
            if keys[K_s]:
                self.screenshot()
            if keys[K_t]:
                width=(width+1)%2
            if keys[K_SPACE]:
                form=(form+1)%4
                print(form)
            if keys[K_RETURN]:
                self.clear()
            self.flip()

    def oldTrace(self,position,color=WHITE,radius=5):
        """Trace a point on the screen using position, size, color."""
        pygame.draw.circle(self.screen,color,position,radius,0)
        #print("position: ",position)


    def trace(self,position,size,color=WHITE,radius=5,form=0,width=0):
        """Trace a point on the screen using position, size, color."""
        for tool in self.hand:
            tool.size=size
            tool.position=position
            tool.points.append(position)
            tool.color=color
            tool.radius=radius
            tool.connect=False
            tool.form=form
            tool.width=width
            tool.draw(self.screen)
        #print("position: ",position)

if __name__=="__main__":
    window=Window("Paint",build=False)
    paint=Paint()
    paint(window)
