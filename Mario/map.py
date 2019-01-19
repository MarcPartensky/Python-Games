import numpy as np
import random
import noise

from block import *

class Map:
    def __init__(self,blocks,size=[500,20],view=[0,0],view_size=[20,20]):
        self.blocks=blocks
        self.size=size
        self.view=view
        self.view_size=view_size
        self.grid=[[None for i in range(self.size[0])] for j in range(self.size[1])]
        self.randomGenerate()

    def randomGenerate(self):
        b=self.blocks
        sx,sy=self.size
        hights=[0 for i in range(self.size[0])]

        for x in range(sx):
            hights[x]=int(5.*noise.pnoise1(float(x)/20))+1
            #print(hights[x])
            for y in range(sy):
                #print(hights[x])
                z=hights[x]
                if z<0 and y==1:
                    self.grid[y][x]=b["water"]
                elif y<=z:
                    self.grid[y][x]=b["dirt"]



    def generate(self):
        hights=np.zeros(self.size[0])

    def show(self,window):
        wsx,wsy=window.size
        vsx,vsy=self.view_size
        vx,vy=self.view
        for y in range(vsy):
            for x in range(vsx):
                gx=x+int(vy)
                gy=y+int(vx)
                if isinstance(self.grid[gy][gx],Block):
                    cx=vx+x*wsx/vsx
                    cy=vy+wsy-y*wsy/vsy
                    csx=wsx/vsx
                    csy=wsy/vsy
                    coordonnates=[cx,cy,csx,csy]
                    self.grid[gy][gx].show(window,coordonnates)

    def update(self,game):
        pass
        #self.view=game.player.position[0]
