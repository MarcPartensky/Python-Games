from asteroid_game import AsteroidGame,Asteroid,Spaceship,Missile
import socket
import itertools


class ServerAsteroid(AsteroidGame):
    """This game must be executed on the server side."""
    def __init__(self,port=1234,dt=0.5,
                player_number=10,asteroid_number=10):
        """Create an asteroid game on the server side."""
        self.connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connexion.bind((socket.gethostname(),port))
        self.connexion.listen(player_number)
        self.dt=dt

        self.spaceship=[Spaceship() for i in range(player_number)]
        self.asteroids=[Asteroid() for i in range(asteroid_number)]
        self.missiles=[]
        self.context=Context(fullscreen=True)
        self.open=True
        self.index=0


    def main(self):
        """Main loop of the server."""
        while self.open:
            self.update()

    def update(self):
        """Update the server."""
        self.hydratePlayers(dt)
        self.updatePlayers(dt)
        self.updateAsteroids(dt)
        self.updateMissiles(dt)
        self.handleCollision()

    def hydratePlayers(self):
        """Hydrate the players."""
        for i in range(len(self.players)):
            client,info=self.connexion.accept()
            client.send
            print(client)
            self.players[i]

    def updatePlayers(self,dt):
        """Update the players."""
        for i in range(len(self.players)):
            self.players[i].update(dt)
            if self.players[i].shooting:
                missile=Missile(1,self.players[i].direction.angle)
                self.missiles.append(missile)

    def updateAsteroids(self,dt):
        """Update the bodies of the game."""
        for i in range(len(self.asteroids)):
            self.asteroids[i].update(dt)

    def updateMissiles(self,dt):
        """Update the missiles of the game."""
        indices=[]
        for i in range(len(missiles)):
            self.missiles[i].update(dt)
            self.indices.append(self.missiles[i].alive)
        self.missiles=itertools.compress(self.missiles,indices)




    def handleCollision(self):
        """Handle collisions between the missiles and the bodies."""
        self.players,self.missiles=self.handleGroupCollisions(self.players,self.missiles)
        self.players,self.asteroids=self.handleGroupCollisions(self.players,self.asteroids)
        self.missiles,self.asteroids=self.handleGroupCollisions(self.missiles,self.asteroids)

    def handleGroupCollisions(self,group1,group2):
        """Handle collisions between the players and the missiles."""
        indices1=[]
        indices2=[]
        for i in range(len(group1)):
            for j in range(len(group2)):
                p=int(len(group1[i].absolute.crossSegment(group2[j].absolute))>0)
                indices1.append(p)
                indices2.append(p)
        group1=itertools.compress(group1,indices1)
        group2=itertools.compress(group2,indices2)
        return (group1,group2)


if __name__=="__main__":
    server=ServerAsteroid(port=1234)
    server.main()
