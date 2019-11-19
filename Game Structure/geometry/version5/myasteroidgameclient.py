from myconnection import Client
from mymanager import GameManager
from myasteroidgame import AsteroidGame


class AsteroidClient(GameManager):
    def __init__(self, ip, port):
        self.id = id(self)
        self.client = Client(ip, port)
        game = AsteroidGame()
        super().__init__(game, build=False)
        print("ip:", self.client.connection.getsockname()[0])

    def showLoop(self):
        if self.client.connection.getsockname()[0] in self.game.players:
            player = self.game.players[self.client.connection.getsockname()[0]]
            self.context.position = player.position
            self.context.clear()
            self.game.show(self.context)
            self.context.console.show()
            self.context.flip()

    def setup(self):
        self.context.build()

    def update(self):
        super().update()
        try:
            self.receive()
        except:
            print("Client failed to receive.")

    def receive(self):
        self.client.receive()
        self.game = self.client.queue.pop()
        self.client.queue.clear()

    def reactKeyDown(self, key):
        super().reactKeyDown(key)
        self.client.sendForSure(("events/keydown", key))

    def reactMouseMotion(self, position):
        position = self.context.getFromScreen(position)
        self.client.sendForSure(("events/mousemotion", position))

    def reactMouseButtonDown(self, button, position):
        position = self.context.getFromScreen(position)
        self.client.sendForSure(("events/mousebuttondown", (button, position)))


if __name__ == "__main__":
    IP = "172.16.0.39."
    PORT = 1234
    # IP, PORT
    c = AsteroidClient(IP, PORT)
    # print(c)
    c()

    # del c
