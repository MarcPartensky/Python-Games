import pygame
from pygame.locals import *
from myentity import Entity

class Player(Entity):
    def __init__(self,position=[0,1],velocity=[0,0],acceleration=[0,-0.1],friction=0.5,size=[1,2],borders=None):
        Entity.__init__(self,position=position,velocity=velocity,acceleration=acceleration,friction=friction,borders=borders)
        self.view=[15,10]
        self.hitbox=self.size=size

    def move(self,map):
        ax,ay=self.acceleration
        vx,vy=self.velocity
        x,y=self.position
        vx+=ax
        vy+=ay
        self.velocity=[vx,vy]
        #future_position=[x+vx,y+vy]
        #if self.checkCollision(future_position,self.size,map.grid):
        #    self.position=future_position
        self.affectCollision(map.grid)

    def checkGround(self,map,area=1):
        px,py=self.position
        sx,sy=self.size
        y=int(py)-1
        self.ground=False
        for x in range(int(px),int(px+sx)+1):
            if map.grid[y][x]==area:
                self.ground=True




    def update(self,map,window):
        keys=window.press()
        self.checkGround(map)
        #window.print(text="Ground: "+str(self.ground),position=[10,100])
        self.lead(keys)
        self.affectFriction()
        self.move(map)
        self.affectBorders()
        self.position=self.round(self.position)

    def round(self,position,precision=1):
        position[0]=round(position[0],precision)
        position[1]=round(position[1],precision)
        return position

    def checkCollision(self,position,size,grid,area=1):
        px,py=position
        sx,sy=size
        mx,my=int(px),int(py)
        Mx,My=int(px+sx)+1,int(py+sy)+1
        positions=[(x,y) for x in range(mx,Mx+1) for y in range(my,My+1)]
        for position in positions:
            x,y=position
            if grid[y][x]==area:
                return True
        else:
            return False






    def affectCollision(self,grid,area=1):
        px,py=self.position
        vx,vy=self.velocity
        sx,sy=self.size
        fpx,fpy=self.round([px+vx,py+vy])
        print("self.velocity:",self.velocity)
        if vx>0:
            print("moving right:")
            print("old:",px,fpx)
            print("int(py),int(py+sy)+1:",int(py),int(py+sy)+1)
            for y in range(int(py),int(py+sy)+1):
                print("y:",y)
                print("int(px+sx),int(px+sx)+1:",int(px+sx),int(px+sx)+1)
                for x in range(int(px+sx),int(px+sx)+1):
                    print("x:",x)
                    if grid[y][x]==area:
                        fpx=min(x-1,fpx)
                        vx=0
                        print("fpx:",fpx)
                        break
            print("new:",px,fpx)
            print("")
        if vx<0:
            for y in range(int(py),int(py+sy)+1):
                for x in range(int(px+sx)+1,int(fpx+sx)-1,-1):
                    if grid[y][x]==area:
                        fpx=max(x+1,fpx)
                        vx=0
                        break
        if vy>0:
            for x in range(int(px),int(px+sx)+1):
                for y in range(int(py+sy),int(fpy+sy)+1):
                    if grid[y][x]==area:
                        fpy=min(y-2,fpy)
                        vy=0
                        break
        if vy<0:
            print("moving down:")
            print("old:",py,fpy)
            print("int(px),int(px+sx)+1:",int(px),int(px+sx)+1)
            for x in range(int(px),int(px+sx)+1):
                print("x:",x)
                print("int(py),int(fpy)-1:",int(py),int(fpy)-1)
                for y in range(int(py),int(fpy)-1,-1):
                    print("y:",y)
                    if grid[y][x]==area:
                        fpy=max(y+1,fpy)
                        vy=0
                        print("fpy:",fpy)
                        break
            print("new:",py,fpy)
            print("")
        self.position=[fpx,fpy]
        self.velocity=[vx,vy]
        print(self.position)





    def collide(self,position,hitbox,map):
        px,py=position
        hx,hy=hitbox
        #print([(round(x+px),round(y+py)) for x in range(int(hx)+1) for y in range(int(hy)+1)])
        positions=[(x+int(px),y+int(py)) for x in range(int(hx)) for y in range(int(hy))]
        #print("positions:",positions)
        return sum([self.contact(position,map.grid) for position in positions])>0


    def contact(self,position,grid,area=1):
        x,y=position
        return grid[y][x]==area

    def lead(self,keys):
        vx,vy=self.velocity
        v=0.5
        jump=2
        if keys[K_LEFT]:
            vx-=v
        if keys[K_RIGHT]:
            vx+=v
        if keys[K_UP] and self.ground:
            vy+=jump
        if keys[K_DOWN]:
            vy-=v
        self.velocity=[vx,vy]

    def old_direct(self):
        ax,ay=self.acceleration
        vx,vy=self.velocity
        vx+=ax
        vy+=ay
        self.velocity=[vx,vy]
