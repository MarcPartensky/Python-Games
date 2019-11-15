from myconnection import Client
from mymanager import Manager
from myasteroidgame import AsteroidDuo


class AsteroidDuoClient(Client, Manager):
    def __init__(self, ip, port):
        Client.__init__(self, ip, port)
        Manager.__init__(self, build=False)
        self.game = AsteroidDuo()
        self.id = None

    def prepare(self):
        self.send("ready")
        while self.id is None:
            self.receiveID()

    def main(self):
        self.prepare()
        self.build()
        super().main()

    def update(self):
        self.game = self.queue.popleft()

    def show(self):
        self.game.show(self.context)



    def receiveID(self):
        while len(self.queue) > 0:
            message = self.queue.popleft()
            if "id" in message:
                self.id = message["id"]
            self.context.console("Id:",self.id)


if __name__ == "__main__":
    IP = "172.16.0.39."
    PORT = 1234

    c = AsteroidDuoClient(IP, PORT)
    c()

    del c
