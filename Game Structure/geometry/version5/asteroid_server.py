from asteroid_game import AsteroidGame, Asteroid, Spaceship, Missile
import itertools
import socket
import select
import time

# Constants
HEADER_LENGTH = 10
IP = socket.gethostname()
PORT = 1237


class ServerAsteroid(AsteroidGame):
    """This game must be executed on the server side."""

    def __init__(self, ip, port, dt=0.5,
                 asteroid_number=10,
                 max_player_number=5,
                 max_duration=float("inf")):
        """Create an asteroid game on the server side."""
        self.ip = ip
        self.port = port
        self.asteroid_number = asteroid_number
        self.max_player_number = max_player_number
        self.max_duration = max_duration

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((ip, port))
        self.connection.listen(max_player_number)
        self.sockets_list = [self.connection]
        self.clients = {}

        self.dt = dt
        self.to = time.time()

        self.spaceships = []
        self.asteroids = [Asteroid(self.random(-10, 10, 2)) for i in range(asteroid_number)]
        self.missiles = []
        # self.context=Context(fullscreen=True)
        self.open = True
        self.index = 0

    def receiveMessage(self, client_socket):
        """Receive a message from a client."""
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return None
            else:
                message_length = int(message_header.decode("utf-8").strip())
                return {"header": message_header, "data": client_socket.recv(message_length)}
        except:
            return None

    def sendMessage(self, dictionary, client_socket):
        """Send a message to a client."""
        message = pickle.dumps(dictionary)
        header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(header + message)

    def main(self):
        """Main loop of the server."""
        while self.open and time.time() - self.to < self.max_duration:
            # Get the sockets
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            self.update()
            # Read all the sockets
            for notified_socket in read_sockets:
                if notified_socket == self.connection:
                    # If the socket correspond to the server, somehow it means that there is
                    # a new client so we need to deal with him
                    self.acceptNewClient(notified_socket)
                else:
                    # Else the socket correspond to an already known user and we
                    # need to treat it a such.
                    self.connectRegistedClient(notified_socket)

            # If the connection between a client and the server triggers an exception
            # the client is removed from the server.
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    def acceptNewClient(self, notified_socket):
        """Accept a new client to the server."""
        client_socket, client_address = notified_socket.accept()
        user = self.receiveMessage(client_socket)
        # We receive the dictionary
        if user is not None:
            # If there is an user, we add it to the list of sockets and users
            self.sockets_list.append(client_socket)
            self.clients[client_socket] = user
            self.summonSpaceship(user)
            print(
                f"Server: Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

    def connectRegisteredClient(self, notified_socket):
        """Accept the message of an already registered client."""
        controls = self.receiveMessage(notified_socket)
        if controls is None:
            # If no there is no message we remove the concerned client from the server.
            print("Server: Closed connection from {}".format(self.clients[notified_socket]['data'].decode('utf-8')))
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]
        else:
            # Else there is a message so we receive, update and send.
            print("Server: Received message from " + str(notified_socket))
            user = self.clients[notified_socket]
            self.contact(notified_socket, user, controls)

    def contact(self, notified_socket, user, controls):
        """Contact a client."""
        self.receive(user, controls)
        self.send(notified_socket, user)

    def receive(self, user, controls):
        """Receive data from an user."""
        if user["key"] is not None:
            key = user["key"]
            c = controls["cursor"]
            s = controls["shooting"]
            p = self.spaceships[key].position
            v = (c - p) / 10
            self.spaceships[key].velocity = v
        else:
            if controls["spawn"]:
                self.summonSpaceship(user)

    def summonSpaceship(self, user):
        """Summon a spaceship for an user to control."""
        spaceship = Spaceship()
        self.spaceships[user["key"]] == spaceship

    def send(self, clientsocket, user):
        """Send the bodies to the player."""
        dictionary = {"spaceships": self.spaceships,
                      "asteroids": self.asteroids,
                      "missiles": self.missiles}
        self.sendMessage(dictionary)

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
            client, info = self.connexion.accept()
            client.send
            print(client)
            self.players[i]

    def updatePlayers(self, dt):
        """Update the players."""
        for i in range(len(self.players)):
            self.players[i].update(dt)
            if self.players[i].shooting:
                missile = Missile(1, self.players[i].direction.angle)
                self.missiles.append(missile)

    def updateAsteroids(self, dt):
        """Update the bodies of the game."""
        for i in range(len(self.asteroids)):
            self.asteroids[i].update(dt)

    def updateMissiles(self, dt):
        """Update the missiles of the game."""
        indices = []
        for i in range(len(missiles)):
            self.missiles[i].update(dt)
            self.indices.append(self.missiles[i].alive)
        self.missiles = itertools.compress(self.missiles, indices)

    def handleCollision(self):
        """Handle collisions between the missiles and the bodies."""
        alive_spaceships = self.getAlive(self.spaceships)
        alive_missiles = self.getAlive(self.missiles)
        alive_asteroids = self.getAlive(self.asteroids)
        self.spaceships, self.missiles = self.handleSpaceshipMissileCollisions(aliveplayers, alivemissiles)
        self.players, self.asteroids = self.handleGroupCollisions(self.players, self.asteroids)
        self.missiles, self.asteroids = self.handleGroupCollisions(self.missiles, self.asteroids)

    def getAlive(self, objects):
        """Return the objects that are alive."""
        return [(i, object) for enumerate(object) in objects in object.alive]

    def handleGroupCollisions(self):
        """When a collision between a player and a missile occures the missile
        dispawns but the state 'alive' of the space ship is set to False only."""
        # for i in range(len(self.missiles)):
        # for

    def handleGroupCollisions(self, group1, group2):
        """Handle collisions between the players and the missiles."""
        l1 = len(group1)
        l2 = len(group2)
        indices1 = [1 for i in range(l1)]
        indices2 = [1 for i in range(l2)]
        for i in range(l1):
            for j in range(l2):
                ps = group1[i].absolute | group2[j].absolute
                c = int(len(ps) == 0)
                indices1[i] = c
                indices2[j] = c
        group1 = list(itertools.compress(group1, indices1))
        group2 = list(itertools.compress(group2, indices2))
        return (group1, group2)


if __name__ == "__main__":
    server = ServerAsteroid(IP, PORT, max_duration=20)
    server.main()
    print("the server is done running.")
