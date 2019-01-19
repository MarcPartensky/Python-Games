import pygame
import random
import time
import math

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *

class Body:
    def __init__(self,position=[0.,0.],velocity=[0.,0.],acceleration=[0.,0.]):
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration
        self.color=[random.randint(0,255) for i in range(3)]

    def move(self):
        x,y=self.position
        vx,vy=self.velocity
        ax,ay=self.acceleration
        vx+=ax
        vy+=ay
        x+=vx
        y+=vy
        self.position=[x,y]
        self.velocity=[vx,vy]

    def borderCollider(self):
        x,y=self.position
        vx,vy=self.velocity
        if x<0:
            x=0
            vx*=-1
        if x>=100:
            x=100
            vx*=-1
        if y<0:
            y=0
            vy*=-1
        if y>=100:
            y=100
            vy*=-1
        self.position=x,y
        self.velocity=vx,vy


class Ball(Body):
    def __init__(self,position):
        Body.__init__(self,position)
        self.radius=20
        self.spawning_position=position
        self.spawn()

    def show(self,window):
        x,y=self.position
        r=self.radius
        wsx,wsy=window.size
        raw_position=[int(wsx*(x)//100),int(wsy*(y)//100)]
        raw_radius=min(wsx,wsy)*r//100
        pygame.draw.circle(window.screen,self.color,raw_position,self.radius,0)

    def spawn(self):
        self.position=self.spawning_position
        self.velocity=[0,0]
        while 0.4>abs(self.velocity[0]):
            self.velocity=[(random.random()-0.5),(random.random()-0.5)]

    def update(self,game):
        self.move()
        self.horizontalBorderCollider()
        self.verticalBorderCollider(game)
        self.paddleCollider(game)

    def paddleCollider(self,game):
        dt=game.delta
        p1sx,p1sy=game.player1.size
        p2sx,p2sy=game.player2.size
        p1x,p1y=game.player1.position
        p2x,p2y=game.player2.position
        p1vx,p1vy=game.player1.velocity
        p2vx,p2vy=game.player2.velocity
        x,y=self.position
        r=self.radius
        vx,vy=self.velocity
        #print("1",self.position,self.velocity)
        if x+vx*dt<p1x+p1sx and p1y<y+vy*dt<p1y+p1sy:
            x=p1x+p1sx
            self.bounce(game.player1)
        #print(x+vx*dt+r)
        if x+vx*dt>p2x and p2y<y+vy*dt<p2y+p2sy:
            x=p2x
            self.bounce(game.player2)
        self.position=x,y
        #print("2",self.position,self.velocity)

    def bounce(self,player):
        px,py=player.position
        psx,psy=player.size
        x,y=self.position
        vx,vy=self.velocity
        #print("a collision clearly happened",vx)
        if player.effect is None:
            vx*=-1.1
        #print(vx)
        self.velocity=vx,vy


    def horizontalBorderCollider(self):
        x,y=self.position
        vx,vy=self.velocity
        if y<0:
            y=0
            vy*=-1
        if y>=100:
            y=100
            vy*=-1
        self.position=x,y
        self.velocity=vx,vy

    def verticalBorderCollider(self,game):
        x,y=self.position
        vx,vy=self.velocity
        if x<0:
            game.player2.score+=1
            self.spawn()
        if x>=100:
            game.player1.score+=1
            self.spawn()



class Player(Body):
    def __init__(self,position):
        Body.__init__(self,position)
        self.score=0
        self.size=[3,10]
        self.effect=None

    def show(self,window):
        x,y=self.position
        sx,sy=self.size
        wsx,wsy=window.size
        raw_position=[int(wsx*(x-sx/2)//100),int(wsy*(y-sy/2)//100)]
        raw_size=[wsx*sx//100,wsx*sy//100]
        pygame.draw.rect(window.screen,self.color,raw_position+raw_size,0)

    def update(self,game):
        self.control()
        self.move()
        self.borderCollider()


class Human(Player):
    def __init__(self,position,side):
        Player.__init__(self,position)
        self.side=side

    def control(self):
        left_player=self.side
        keys=pygame.key.get_pressed()
        k=2
        if keys[K_UP] and not left_player:
            vy=-k
        elif keys[K_DOWN] and not left_player:
            vy=k
        elif keys[K_a] and left_player:
            vy=-k
        elif keys[K_z] and left_player:
            vy=k
        else:
            vy=0
        self.velocity=[0,vy]

class Robot(Player):
    def control(self,ball):
        pass



class Pong:
    def __init__(self):
        self.name="Pong"
        self.size=[700,700]
        self.color_background=BLACK
        self.window=Window(self,[1400,700])
        self.player1=Human([1.,50.],True)
        self.player2=Human([98.,50.],False)
        self.ball=Ball([50.,50.])
        self.delta=0.0000001
        self.font= pygame.font.SysFont("monospace", 50)
        self.session()

    def showScores(self,window):
        wsx,wsy=window.size
        d=wsx//10
        label = self.font.render(str(self.player1.score), 1, self.player1.color)
        window.screen.blit(label, (d, wsy//3))
        label = self.font.render(str(self.player2.score), 1, self.player2.color)
        window.screen.blit(label, (wsx-d-30, wsy//3))

    def update(self):
        self.player1.update(self)
        self.player2.update(self)
        self.ball.update(self)

    def show(self):
        self.window.screen.fill(self.color_background)
        self.ball.show(self.window)
        self.player1.show(self.window)
        self.player2.show(self.window)
        self.showScores(self.window)
        self.window.flip()

    def session(self):
        self.play()

    def play(self):
        self.show()
        while self.window.open:
            self.window.check()
            self.update()
            self.show()
            time.sleep(self.delta)


game=Pong()
