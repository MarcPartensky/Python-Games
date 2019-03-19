from __future__ import division

from mycolors import *

import pygame
from pygame.locals import *
import time
import json



class Window:
    made=0
    draw=pygame.draw

    def __init__(self,name="Unnamed Game",taille=[700,600],text_font="monospace",text_size=65,text_color=WHITE,background_color=BLACK,fullscreen=False,set=True):
        """Create a window object using name, taille text_font, text_size, text_color, background and set."""
        Window.made+=1
        self.number=Window.made
        self.name=name
        self.taille=taille
        self.text_font=text_font
        self.taille_du_texte=text_size
        self.text_color=text_color
        self.couleur_de_fond=background_color
        self.fullscreen=fullscreen
        self.load()
        if set:
            self.set()

    def load(self):
        """Load builtins attributs of window object."""
        self.RIGHT = 0
        self.UP    = 1
        self.LEFT  = 2
        self.DOWN  = 3
        if self.taille is None:
            self.taille=(self.info.current_w//2,self.info.current_h//2)
        #self.mouse_position=pygame.mouse.get_pos()
        #self.mouse_click=bool(pygame.mouse.get_pressed()[0])
        self.selecter_color=self.reverseColor(self.couleur_de_fond)
        self.pausing=False
        self.open=False
        self.coordonnates=[0,0]+self.taille
        self.picture_saved=0
        self.pause_cool_down=1
        self.time=time.time()

    def set(self):
        """Creates apparent window."""
        self.log("Window has been created.")
        pygame.init()
        self.info = pygame.display.Info()
        self.font = pygame.font.SysFont(self.text_font, self.taille_du_texte)
        if self.fullscreen:
            self.screen=pygame.display.set_mode(self.taille,FULLSCREEN)
        else:
            self.screen=pygame.display.set_mode(self.taille,RESIZABLE)
        pygame.display.set_caption(self.name)
        self.clear()
        self.flip()
        self.open=True

    def clear(self,color=None):
        """Clear to background color."""
        if color is None:
            color=self.couleur_de_fond
        self.screen.fill(color)

    def scale(self,picture,taille):
        """Return scaled picture using picture and taille."""
        return pygame.transform.scale(picture,taille)

    def check(self):
        """Update window's state depending if close buttons are pressed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open=False
                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    self.size=[event.w,event.h]
                    self.screen=pygame.display.set_mode(self.size,pygame.RESIZABLE)
                    self.flip()

    def update(self):
        """Updates all window's main attributs."""
        self.mouse_click=bool(pygame.mouse.get_pressed()[0])
        self.mouse_position=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open=False

    def pause(self):
        """Wait for user to click on space."""
        self.pausing=True
        while self.pausing and self.open:
            self.check()
            keys=pygame.key.get_pressed()
            if keys[K_SPACE]:
                self.pausing=False
        if self.open:
            time.sleep(0.1)

    def sleep(self,waiting_time): #useless
        """Wait for giving time."""
        import time
        time.sleep(waiting_time)

    def press(self):
        """Return all keys."""
        return pygame.key.get_pressed()

    def direction(self):
        """Return keys for arrows pressed. Trigonometric orientation is used."""
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
            left=True
        else:
            left=False
        if keys[K_RIGHT]:
            right=True
        else:
            right=False
        if keys[K_UP]:
            up=True
        else:
            up=False
        if keys[K_DOWN]:
            down=True
        else:
            down=False
        return [right,up,right,down]


    def select(self):
        """Wait for user to click on screen, then return cursor position."""
        while self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])

    def point(self):
        """Return cursor position on screen."""
        return pygame.mouse.get_pos()

    def click(self):
        """Return bool value for clicking on screen."""
        return bool(pygame.mouse.get_pressed()[0])

    def press(self):
        """Return bool value for clicking on screen."""
        return pygame.key.get_pressed()

    def flip(self):
        """Refresh screen."""
        pygame.display.flip()

    def screenshot(self):
        """Save picture of the surface."""
        self.picture_saved+=1
        pygame.image.save(self.screen,self.name+"-"+str(self.picture_saved)+".png")


    def getPicture(self,picture_directory):
        """Return picture using picture directory."""
        return pygame.image.load(picture_directory)

    def placePicture(self,picture_directory,coordonnates,color=None):
        """Draw a picture on screen using pygame picture directory and position."""
        x,y,sx,sy=coordonnates
        picture=pygame.image.load(picture_directory)
        picture=pygame.transform.scale(picture,(sx,sy))
        if color is not None:
            picture=colorize(picture,color)
        self.screen.blit(picture, position)

    def centerText(self,message,taille=None):
        sx,sy=self.taille
        if taille is None:
            taille=self.taille_du_texte
        l=len(message)
        letter_size=taille/4
        x=sx//2-letter_size*l//2
        y=sy//2-taille/3
        return (x,y)


    def alert(self,message):
        """Quickly display text on window."""
        position=self.centerText(message)
        self.print(message,position)
        self.flip()

    def print(self,text,position,taille=None,color=None,couleur_de_fond=None,font=None):
        """Display text on screen using position, taille, color and font."""
        sx,sy=taille
        x,y=position
        pygame.draw.rect(self.screen,self.reverseColor(couleur_de_fond),position+taille,0)
        pygame.draw.rect(self.screen,couleur_de_fond,(x+1,y+1,sx-2,sy-2),0)
        if taille is None:
            taille=self.taille_du_texte
        if color is None:
            color=self.text_color
        if font is None:
            font=self.font
        label = font.render(text, 1, color)
        self.screen.blit(label, position)

    def drawRect(self,coordonnates,color):
        """Draw a rectangle on the screen using color and coordonnates relative to window's fiducials."""
        wsx,wsy=self.taille
        wcx,wcy,wcsx,wcsy=self.coordonnates
        rcx,rcy,rcsx,rcsy=coordonnates
        x,y=(rcx-wcx,rcy-wcy)
        w,h=(rcsx*wsx/wcsx,rcsy*wsy/wcsy)
        pygame.draw.rect(self.screen,color,(x,y,w,h),0)

    def place(self,position):
        """Return position relative to window's fiducials."""
        wcx,wcy,wcsx,wcsy=self.coordonnates
        pcx,pcy=position
        x,y=(rcx-wcx,rcy-wcy)
        return (x,y)


    def randomColor(self):
        """Return random color."""
        import random
        r=random.randint(0,255)
        g=random.randint(0,255)
        b=random.randint(0,255)
        color=(r,g,b)
        return color

    def reverseColor(self,color):
        """Return reverse color."""
        r,g,b=color
        r=255-r
        g=255-g
        b=255-b
        color=(r,g,b)
        return color

    def lighten(self,color,luminosity=80): #View later
        """Return lightened color using color and luminosity percentage."""
        r,g,b=color
        if luminosity>=50:
            r+=(255-r)*luminosity/100
            g+=(255-g)*luminosity/100
            b+=(255-b)*luminosity/100
        else:
            r-=r*luminosity/100
            g-=g*luminosity/100
            b-=b*luminosity/100
        color=r,g,b
        return color

    def colorize(self,image, color):
        """Return image colorized"""
        image = image.copy()
        image.fill((0,0,0,255),None,pygame.BLEND_RGBA_MULT)
        image.fill(color[0:3]+(0,),None,pygame.BLEND_RGBA_ADD)
        return image

    def oldTrace(self,position,color=WHITE,radius=5):
        """Trace a point on the screen using position, taille, color."""
        pygame.draw.circle(self.screen,color,position,radius,0)
        #print("position: ",position)


    def trace(self,position,taille,color=WHITE,radius=5,form=0,width=0):
        """Trace a point on the screen using position, taille, color."""
        for tool in self.hand:
            tool.taille=taille
            tool.position=position
            tool.points.append(position)
            tool.color=color
            tool.radius=radius
            tool.connect=False
            tool.form=form
            tool.width=width
            tool.draw(self.screen)
        #print("position: ",position)

    def wavelengthToRGB(self,wavelength):
        """Convert wavelength to rgb color type."""
        gamma,max_intensity=0.80,255
        def adjust(color, factor):
            if color==0: return 0
            else: return round(max_intensity*pow(color*factor,gamma))
        if 380<=wavelength<=440: r,g,b=-(wavelength-440)/(440-380),0,1
        elif 440<=wavelength<=490: r,g,b=0,(wavelength-440)/(490-440),1
        elif 490<=wavelength<=510: r,g,b=0,1,-(wavelength-510)/(510-490)
        elif 510<=wavelength<=580: r,g,b=(wavelength-510)/(580-510),1,0
        elif 580<=wavelength<=645: r,g,b=1,-(wavelength-645)/(645-580),0
        elif 645<=wavelength<=780: r,g,b=1,0,0
        else: r,g,b=0,0,0
        if 380<=wavelength<=420: factor=0.3+0.7*(wavelength-380)/(420-380)
        elif 420<=wavelength<=701: factor=1
        elif 701<=wavelength<=780: factor=0.3+0.7*(780-wavelength)/(780-700)
        else: factor=0
        r,g,b=adjust(r,factor),adjust(g,factor),adjust(b,factor)
        return (r,g,b)

    def kill(self):
        """Quit pygame."""
        pygame.quit()

    def log(self,message):
        """Print message with window mention."""
        text="["+self.name+"] "+message
        print(text)

    def __del__(self):
        """Executed before the window is destroyed."""
        self.log("Window has been closed.")


if __name__=="__main__":
    w=Window("Game")
    #save(w,"grosse fenetre")
    #w=load("grosse fenetre")
    #print(w.lighten(BLUE))
    #w.alert("test")
    w.draw()
    w.pause()
    w.clear()
    w.alert("test2")
    w.pause()
    w.kill()
