from asteroid_game import AsteroidGame
import socket
import pickle


class ClientAsteroid(AsteroidGame):
    def __init__(self,ip,port=1234):
        """Create a body game."""
        self.context=Context(fullscreen=True)
        self.connexion=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion=.connect((ip,port))
        self.receiveId()

    def receiveId(self):
        """Receive the id the spaceship that is controlled."""
        #Receive id
        self.id=id

    def main(self):
        """Main loop of the client."""
        while self.context.open:
            self.update()
            self.show()

    def update(self):
        """Update the client."""
        self.send()
        self.receive()

    def send(self):
        """Send data to the server."""
        direction,shooting=self.control()
        #Send direction and shooting state
        pass

    def receive(self):
        """Hydrate the client body game."""
        response=self.connexion.recv()
        response=pickle.loads(response)
        self.bodies=response["bodies"]
        self.players=response["players"]
        self.missiles=response["missiles"]

    def show(self):
        """Show the components on the screen."""
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
        c=Vector(*self.context.point())
        p=self.bodies[self.id].position
        direction=c-p
        return (direction,shooting)

if __name__=="__main__":
    ip=""
    port=1234
    game=ClientBodyGame(ip,port)
    game.main()
