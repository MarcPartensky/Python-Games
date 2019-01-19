class Manager:
    def __init__(self):
        self.window=Window()

        self.play()

    def play(self):
        self.players=PLAYERS
        self.player=PLAYERS[0]
        self.map=Map()
        game=game(self.window,self.map,self.players)
        for player in self.players:
            player.spawn(game.map)
        game.play()
