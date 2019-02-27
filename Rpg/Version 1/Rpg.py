from mywindow import Window
from mycolors import *

import numpy as np

import noise




class Entity:
    def __init__(self,name="Unnamed"):
        self.name=name

class Case:
    def __init__(self,number,size=[10,10]):
        self.size=size
        self.generate(number)
        self.grid=np.zeros[self.size]

    def generate(self,n):
        if n<0.4:
            self.color=BLUE
            #(0,0,(255.0/0.2)*n)
        elif n<0.45:
            self.color=YELLOW
        elif n<0.9:
            self.color=GREEN
        elif n<1.0:
            self.color=GREY
        else:
            self.color=WHITE

    def edit(self,window):
        pass

    def show(self,window,coordonnates):
        wsx,wsy=window.size
        sx,sy=self.size
        cx,cy,csx,csy=coordonnates
        tx,ty=(float(wsx)/float(csx),float(wsy)/float(csy))
        raw_size=(tx,ty)
        for y in range(sy):
            for x in range(sx):
                color=self.grid[y][x]
                raw_position=(cx*csx+x*tx,cy*csy+y*ty)
                raw_coordonnates=raw_position+raw_size
                pygame.draw.rect(window.screen,color,raw_coordonnates,self.width)



class Map:
    def __init__(self,size=[1000,1000]):
        self.size=size
        self.generate()

    def generate(self):
        self.dimensions=3
        self.grid=np.zeros(self.size)
        sx,sy=self.size
        noise=self.getNoise()

        for y in range(sy):
            for x in range(sx):
                n=noise[y][x]
                n=(3*n+1)/2
                #print(n)

                self.grid[y][x]=color

    def getNoise(self,size):
        #shape = (1024,1024)
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        terrain = np.zeros(size)
        for i in range(size[0]):
            for j in range(size[1]):
                terrain[i][j] = noise.pnoise2(i/scale,
                                            j/scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=0)
        return terrain

    def show(self,window):
        sx,sy=self.size
        #print(cx,cy)
        for y in range(sy):
            for x in range(sx):
                self.grid[y][x].show(window,(x,y,sx,sy))

    def view(self,position):
        pass





class Player(Entity):
    def __init__(self,name):
        Entity.__init__(name)
        self.view_field=[20,10]
        self.view_position=[0,0]
        self.view_velocity=[0,0]
        self.view_acceleration=[0,0]
        self.position=[0,0]
        self.spawn_position=[0,0]
        self.velocity=[1,1]

    def see(self,map,window):
        pass

    def show(self):
        pass


class Rpg:
    def __init__(self):
        self.name="Rpg"
        self.map=Map("Rpg")
        self.players=[Player("Marc")]
        self.window=Window(self.name)
        self.scenes=[]
        self.map.generate()

    def __call__(self):
        self.show()
        while self.window.open:
            self.window.check()
            self.getInput()
            self.update()
            self.show()
        self.end()

    def end(self):
        self.window.kill()

    def show(self):
        self.window.screen.fill(WHITE)
        self.player.see(self.map,self.window)
        self.window.flip()

    def update(self):
        for player in self.players:
            player.update()

if __name__=="__main__":
    game=Rpg()
    game()
