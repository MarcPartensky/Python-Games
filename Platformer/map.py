from mycolors import BLACK,WHITE,BLUE,RED
from mycamera import Camera

import random
import pygame

class Map:
    def __init__(self,size):
        self.size=size
        self.colors=[BLACK,WHITE]
        self.camera=Camera(position=[0,0],size=[30,20],borders=[0,0]+self.size)
        self.generate()


    def generate(self):
        sx,sy=self.size
        self.grid=[[0 for x in range(sx)] for x in range(sy)]
        for x in range(sx):
            self.grid[0][x]=1
        for y in range(sy):
            for x in range(sx):
                if random.randint(0,9)==0:
                    self.grid[y][x]=1

    def update(self):
        pass

    def showAll(self,position,size,window):
        psx,psy=size
        px,py=position
        vision=self.camera([px-psx/2,py-psy/2],window)
        window.print(text="Camera's vision: "+str(vision),position=[10,90])
        #print("self.camera.position:",self.camera.position)
        #print("self.camera.direction:",self.camera.direction)
        vx,vy,vsx,vsy=vision
        px,py=position
        wsx,wsy=window.size
        sx,sy=self.size

        #Draw Map
        for y in range(sy):
            for x in range(sx):
                if self.grid[y][x]==1:
                    _x=x
                    _y=(sy-1)-y
                    coordonnates=[_x*wsx/sx,_y*wsy/sy,wsx/sx,wsy/sy]
                    pygame.draw.rect(window.screen,WHITE,coordonnates,0)

        #Draw Player
        _y=(sy-1)-py
        _x=px
        coordonnates=[_x*wsx/sx,_y*wsy/sy,wsx/sx,wsy/sy]
        pygame.draw.rect(window.screen,BLUE,coordonnates,0)
        coordonnates=[_x*wsx/sx,(_y-1)*wsy/sy,wsx/sx,wsy/sy]
        pygame.draw.rect(window.screen,BLUE,coordonnates,0)
        #Draw Camera
        _y=(sy-1)-(vy+vsy) #sy map size, vy vision, vsy vision size
        _x=vx
        coordonnates=[_x*wsx/sx,_y*wsy/sy,vsx*wsx/sx,vsy*wsy/sy]
        pygame.draw.rect(window.screen,RED,coordonnates,1)


    def show(self,position,size,window):
        psx,psy=size
        px,py=position
        vision=self.camera([px-psx/2,py-psy/2],window) #takes position to return coordonnates
        window.print(text="Camera's vision: "+str(vision),position=[10,50])
        #print("self.camera.position:",self.camera.position)
        #print("self.camera.direction:",self.camera.direction)
        self.displayMap(vision,window)
        self.displayPlayer(position,vision,window)

    def displayMap(self,vision,window):
        wsx,wsy=window.size
        vx,vy,vsx,vsy=vision
        vmx,vmy=int(vsx)+1,int(vsy)+1
        sx,sy=self.size
        for y in range(vmy):
            for x in range(vmx):
                _x=(vsx-1)-x
                _y=(vsy-1)-y
                gx=x+int(vx)
                gy=y+int(vy)
                dx=int(vx)-vx
                dy=int(vy)-vy
                #_y=(sy-1)-(vy+vsy) #sy map size, vy vision, vsy vision size
                #_x=vx
                coordonnates=[(dx+x)*wsx/vsx,wsy-(dy+y)*wsy/vsy,wsx/vsx,wsy/vsy]
                if self.grid[gy][gx]==1:
                    #print(coordonnates)
                    pygame.draw.rect(window.screen,WHITE,coordonnates,0)

    def displayPlayer(self,position,vision,window):
        wsx,wsy=window.size
        sx,sy=self.size
        x,y=position
        vx,vy,vsx,vsy=vision
        #_x=(sx-1)-x
        #_y=(sy-1)-y
        _x=x-vx
        _y=y-vy
        coordonnates=[_x*wsx/vsx,wsy-_y*wsy/vsy,wsx/vsx,wsy/vsy]
        pygame.draw.rect(window.screen,BLUE,coordonnates,0)
        coordonnates=[_x*wsx/vsx,wsy-(_y+1)*wsy/vsy,wsx/vsx,wsy/vsy]
        pygame.draw.rect(window.screen,BLUE,coordonnates,0)







    def old_show(self,vision,window):
        wsx,wsy=window.size
        px,py,vx,vy=vision
        for y in range(vy):
            for x in range(vx):
                X,Y=int(x+px),int(y+py)
                size=[wsx/vx,wsy/vy]
                print(vx,vy)
                print(x,y)
                print(vx-x-1,vy-y-1)
                position=[(vx-x-1)*wsx/vx,(vy-y-1)*wsy/vy]
                coordonnates=position+size
                print(X,Y)
                print("")
                color=self.colors[self.grid[Y][X]]
                pygame.draw.rect(window.screen,color,coordonnates,0)
