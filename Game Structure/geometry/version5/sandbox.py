from mymanager import Manager
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from pygame.locals import *
import pygame

import math


matrix=np.random.randint(2,size=(5,5,5))

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

#Make sure that the cube is of surface 1.
verticies=tuple([(x/2,y/2,z/2) for (x,y,z) in verticies])

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )


#colors=tuple([(0,0,1) for i in range(12)])
colors=tuple([(1,1,0) for i in range(12)])


def showCubeBordures(x=0,y=0,z=0):
    """Show the cubes but with transparent faces."""
    glBegin(GL_LINES)
    glColor3fv((0,0,0))
    for edge in edges:
        for i,vertex in enumerate(edge):
            vx,vy,vz=verticies[vertex]
            glVertex3fv((vx+x,vy+y,vz+z))
    glEnd()

def showCube(x=0,y=0,z=0):
    """Show the cube with colored faces."""
    glBegin(GL_QUADS)
    for surface in surfaces:
        for i,vertex in enumerate(surface):
            glColor3fv(colors[i])
            vx,vy,vz=verticies[vertex]
            glVertex3fv((vx+x,vy+y,vz+z))
    glEnd()


def showCube2(x=0,y=0,z=0):
    glBegin(GL_QUADS)
    glVertex3fv(-1.0,-1.0,0.0)
    glVertext3fv(1.0,-1.0,0.0)
    glVertex3fv(1.0,1.0,0.0)
    glVertex3fv(-1.0,1.0,0.0)
    glEnd()



def showMatrix(matrix,x=0,y=0,z=0):
    """Show the matrix."""
    sx,sy,sz=matrix.shape[:3]
    for ix in range(sx):
        for iy in range(sy):
            for iz in range(sz):
                if matrix[ix][iy][iz]:
                    cx=-sx/2+ix+x
                    cy=-sy/2+iy+y
                    cz=-sz/2+iz+z
                    showCube(cx,cy,cz)
                    showCubeBordures(cx,cy,cz)


def main():
    pygame.init()
    display = (800,600)
    resolution = (display[0]/display[1])
    angles=[1,3,1,1]
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, resolution, 0.1, 50.0)
    glTranslatef(0,0,-30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEMOTION:
                pass

        glRotatef(*angles)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        showMatrix(matrix)
        pygame.display.flip()
        pygame.time.wait(10)


class SandBox(Manager):
    def __init__(self,*args,**kwargs):
        """Create a sandbox."""
        super().__init__(*args,**kwargs)
        self.context.screen=pygame.display.set_mode(self.context.size,DOUBLEBUF|OPENGL)
        self.matrix=np.random.randint(2,size=(5,5,5))
        self.angles=[1,3,1,1]
        self.perspective=[45,0.1,50.0]
        self.rotation=[-30,0]
        #self.position=[0.5,1.5,1.5]
        self.position=[0.5,1.5,30]
        self.step=10
        self.dt=0.0001

    def showMatrix(self,x=0,y=0,z=0):
        """Show the matrix."""
        sx,sy,sz=self.matrix.shape[:3]
        for ix in range(sx):
            for iy in range(sy):
                for iz in range(sz):
                    if matrix[ix][iy][iz]:
                        cx=-sx/2+ix+x
                        cy=-sy/2+iy+y
                        cz=-sz/2+iz+z
                        self.showCube(cx,cy,cz)
                        self.showCubeBordures(cx,cy,cz)

    def showCubeBordures(self,x=0,y=0,z=0):
        """Show the cubes but with transparent faces."""
        glBegin(GL_LINES)
        glColor3fv((0,0,0))
        for edge in edges:
            for i,vertex in enumerate(edge):
                vx,vy,vz=verticies[vertex]
                glVertex3fv((vx+x,vy+y,vz+z))
        glEnd()

    def showCube(self,x=0,y=0,z=0):
        """Show the cube with colored faces."""
        glBegin(GL_QUADS)
        for surface in surfaces:
            for i,vertex in enumerate(surface):
                glColor3fv(colors[i])
                vx,vy,vz=verticies[vertex]
                glVertex3fv((vx+x,vy+y,vz+z))
        glEnd()


    def setup(self):
        """Setup the gl view before the loop."""
        p1,p2,p3=self.perspective
        gluPerspective(p1,self.context.resolution,p2,p3)
        glTranslatef(-self.position[0],-self.position[1],-self.position[2],)

    def showLoop(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(*self.angles)
        self.showMatrix()
        self.context.flip()

    def oldshowLoop(self):
        """Show the sandbox."""
        #glRotatef(*self.angles)

        #Clear
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #Set3d
        #-Projection
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        #-Perspective
        p1,p2,p3=self.perspective
        gluPerspective(p1,self.context.resolution,p2,p3)
        #Model
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()

        #Push
        glPushMatrix()
        glRotatef(-self.rotation[0],1,0,0)
        glRotatef(-self.rotation[1],0,1,0)
        glTranslatef(-self.position[0],-self.position[1],-self.position[2],)

        #Draw the objects
        self.showMatrix()

        #Pop Matrix
        glPopMatrix()
        self.context.flip()

    def reactKeyDown(self,key):
        """React to keydown events."""
        super().reactKeyDown(key)
        if key == K_UP:
            glTranslatef(0,0,1)
        if key == K_DOWN:
            glTranslatef(0,0,-1)

        s = self.dt*self.step
        rotY = -self.rotation[1]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        if key == K_w: glTranslatef(dx,0,-dz)
        if key == K_s: glTranslatef(-dx,0,dz);
        if key == K_a: glTranslatef(-dx,0,-dz);
        if key == K_d: glTranslatef(dx,0,dz);

        #if keys[key.SPACE]: self.pos[1]+=s
        #if keys[key.LSHIFT]: self.pos[1]-=s

    def reactMouseMotion(self,event):
        """React to a mouse motion."""
        dx,dy=event.pos
        dx/=8; dy/=8; self.rotation[0]+=dy; self.rotation[1]-=dx
        if self.rotation[0]>90: self.rotation[0] = 90
        elif self.rotation[0]<-90: self.rotation[0] = -90

if __name__=="__main__":
    s=SandBox()
    s()
