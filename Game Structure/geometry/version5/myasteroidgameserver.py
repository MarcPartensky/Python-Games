from myconnection import Server, get_ip
from myasteroidgame import AsteroidGame

class AsteroidServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = AsteroidGame(stage=0)
        self.game.start()
        self.redirection = {}
        print("Ready for players to connect.")

    def update(self):
        super().update()
        self.game.update()
        self.processAll()
        for client in self.clients[1:]:
            self.send(client, self.game)

    def accept(self, client):
        client_socket, client_address = client.accept()
        self.clients.append(client_socket)
        self.game.players.append(self.game.level.newPlayer())
        self.redirection[client_socket.getsockname()[0]] = len(self.game.players)-1
        print("Client: {} has been accepted by the server.".format(client))
        print("client ip:", client_socket.getsockname()[0])

    def processAll(self):
        """Receive the events of the players and distribute them to their played entity. """
        if len(self.queue) > 0:
            transmission = self.queue.pop()
            self.queue.clear()
            self.process(*transmission)

    def process(self, client, message):
        """Process a message sent by a client."""
        # print(self.redirection, client.getsockname()[0], message)
        if client.getsockname()[0] in self.redirection:
            path, value = message
            path = path.split("/")
            player = self.game.players[self.redirection[client.getsockname()[0]]]
            print(client.getsockname()[0], player, path, value)
            if path[0] == "events":
                if path[1] == "keydown":
                    player.reactKeyDown(value)
                elif path[1] == "mousemotion":
                    player.reactMouseMotion(value)
                elif path[1] == "mousebuttondown":
                    player.reactMouseButtonDown(*value)


if __name__ == "__main__":
    import socket

    IP = ''
    PORT = 1234
    s = AsteroidServer(IP, PORT)
    print("IP:",get_ip())
    print("PORT:",PORT)
    s.main()
    del s
