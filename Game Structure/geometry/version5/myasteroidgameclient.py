from myconnection import Client
from mymanager import GameManager
from myasteroidgame import AsteroidGame


class AsteroidClient(GameManager):
    def __init__(self, ip, port):
        self.id = id(self)
        self.client = Client(ip, port)
        game xxxx= AsteroidGame()
        super().__init__(game, build=False)

    def showLoop(self):
        if self.client.connection.getsockname()[0] in self.game.players:
            player = self.game.players[self.client.connection.getsockname()[0]]
            self.context.position = player.position
            self.context.clear()
            self.game.show(self.context)
            self.context.console.show()
            self.context.flip()
            print("showLoop")

    def setup(self):
        self.context.build()

    def update(self):
        super().update()
        self.context.position = Vector(0, 0)
        try:
            self.receive()
        except Exception as e:
            print(e)

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
    #IP: 25.71.207.126
    #PORT: 1234
    IP = input("IP: ")
    PORT = int(input("PORT: "))
    # IP, PORT
    c = AsteroidClient(IP, PORT)
    # print(c)
    c()

    # del c
