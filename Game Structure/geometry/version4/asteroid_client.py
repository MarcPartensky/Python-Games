from asteroid_game import AsteroidGame
from myabstract import Point
from mysurface import Context
from pygame.locals import *
import pickle
import socket
import select
import errno
import sys
import time

HEADER_LENGTH=10


duration=20

IP=socket.gethostname()
PORT=1237

class ClientAsteroid(AsteroidGame):
    def __init__(self,ip,port,max_duration=float("inf")):
        """Create a body game."""
        self.context=Context(fullscreen=False)
        self.connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        self.connection.setblocking(False)
        self.to=time.time()
        self.max_duration=max_duration
        self.user={"key":random.randint(0,10**10),"alive":True}
        self.sendMessage(self.user)

    def receiveMessage(self,client_socket):
        """Receive a message from a client."""
        try:
            message_header=client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return None
            else:
                message_length=int(message_header.decode("utf-8").strip())
                return {"header":message_header,"data":client_socket.recv(message_length)}
        except:
            return None

    def makeMessage(self):

    def sendMessage(self,dictionary,client_socket):
        """Send a message to a client."""
        message=pickle.dumps(dictionary)
        header=f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(header+message)

    def main(self):
        """Main loop of the client."""
        while self.context.open and time.time()-self.to<self.max_duration:
            self.receive()
            self.show()
            self.send()

    def send(self):
        """Send data to the server."""
        cursor,shooting,spawn=self.control()
        dictionary={"cursor":cursor,
                    "shooting":shooting,
                    "spawn":spawn}
        self.sendMessage(dictionary,self.connection)

    def receive(self):
        """Hydrate the client body game."""
        try:
            dictionary=self.receiveMessage(self.connection)
            self.asteroids=dictionary["asteroids"]
            self.spaceships=dictionary["spaceships"]
            self.missiles=dictionary["missiles"]
            self.user=dictionary["user"]
        except IOError as e:
            if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                print("Client: Reading error",str(e))
                sys.exit()
            else:
                print("Client: Other io error",str(e))
                sys.exit()
        except Exception as e:
            print("Client: General error",str(e))
            sys.exit()

    def show(self):
        """Show the components on the screen."""
        self.context.draw.plane.position=self.spaceships[self.user["key"]]
        self.context.check()
        self.context.clear()
        self.context.show()
        self.showBodies()
        self.showInfo()
        self.context.controlZoom()
        self.context.flip()

    def showBodies(self):
        """Show all the bodies of the game."""
        self.showSpaceships()
        self.showMissiles()
        self.showAsteroids()

    def showSpaceships(self):
        """Show all the spaceships on the context."""
        for i in range(len(self.spaceships)):
            self.spaceships[i].absolute.show(self.context)

    def showMissiles(self):
        """Show all the missiles on the context."""
        for i in range(len(self.missiles)):
            self.missiles[i].absolute.show(self.context)

    def showAsteroids(self):
        """Show all the asteroids on the context."""
        for i in range(len(self.asteroids)):
            self.asteroids[i].absolute.show(self.context)

    def showInfo(self):
        """Show infos about the game."""
        pass

    def control(self):
        """Control the body."""
        keys=self.context.press()
        if keys[K_SPACE]:
            shooting=True
        else:
            shooting=False
        cursor=Point(*self.context.point())
        spawn=keys[K_r]
        return (cursor,shooting,spawn)

if __name__=="__main__":
    game=ClientAsteroid(IP,PORT,max_duration=20)
    game.main()
    print("The client is done running.")
