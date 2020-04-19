from myconnection import Server
from myasteroidgame import AsteroidGame

class AsteroidServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = AsteroidGame()
        print("Waiting for players to connect.")

    def update(self):
        super().update()
        self.game.update()
        self.processAll()
        self.sendAllForSure(self.game)

    def accept(self, client):
        super().accept(client)
        self.createPlayer(client)
        print("Client: {} has been accepted by the server.".format(client))
        print("client ip:", client.getsockname()[0])

    def createPlayer(self, client):
        self.game.players[client.getsockname()[0]] = self.game.level.newPlayer()

    def processAll(self):
        """Receive the events of the players and distribute them to their played entity. """
        if len(self.queue) > 0:
            transmission = self.queue.pop()
            self.queue.clear()
            self.process(*transmission)

    def process(self, client, message):
        """Process a message sent by a client."""
        path, value = message
        path = path.split("/")
        if path[0] == "events":
            if path[1] == "keydown":
                self.game.players[client.getsockname()[0]].reactKeyDown(value)
            elif path[1] == "mousemotion":
                self.game.players[client.getsockname()[0]].reactMouseMotion(value)
            elif path[1] == "mousebuttondown":
                self.game.players[client.getsockname()[0]].reactMouseButtonDown(*value)


if __name__ == "__main__":
    IP = "172.16.0.39."
    PORT = 1234

    s = AsteroidServer(IP, PORT)
    s.main()

    del s

