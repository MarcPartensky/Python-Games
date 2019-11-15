from myconnection import Server
from myasteroidgame import AsteroidDuo


class AsteroidDuoServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = AsteroidDuo()
        self.playing = False
        # self.player1 = deque({})
        # self.player2 = deque({})
        self.ready = [True, False, False]

    def distributeIds(self):
        """Send the id to all users."""
        for user_id, user in enumerate(self.clients):
            user.send({"id": user_id})

    def main(self):
        self.prepare()
        self.loop()

    def prepare(self):
        """Wait for all players to be ready."""
        print("Waiting for all players to be ready.")
        while not (self.ready[1] and self.ready[2]):
            self.update()
            self.checkReady()

    def checkReady(self):
        """Update the list ready when a player is ready."""
        while len(self.queue) > 0:
            user_request = self.queue.popleft()
            print(self.queue)
            print(user_request)
            for (user_id, user_message) in user_request.items():
                if user_message == "ready":
                    self.ready[user_id] = True
                    print("user {} is ready".format(user_id))

    def loop(self):
        self.update()
        self.game.update()

    def areReady(self):
        return not (False in self.ready)


if __name__ == "__main__":
    IP = "172.16.0.39."
    PORT = 1234

    s = AsteroidDuoServer(IP, PORT)
    s.main()

    del s