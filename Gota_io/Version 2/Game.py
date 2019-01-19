class Game:
    def __init__(self,window,map,entities):
        self.name="Gota.io"
        self.window=window
        self.map=map
        self.entities=entities
        self.active=True

    def play(self):
        while self.active:
            for entity in self.entities:
                entity.play(self)

    def show(self,player):
        self.window.screen.fill(self.map.background_color)
        (cx,cy,sx,sy)=player.view_field
        px,py=player.coordonnates
        player.draw(self.window,(0,0))
        for entity in self.entities:
            (x,y)=entity.coordonnates
            if cx<x<sx and cy<y<sy:
                coordonnates=(cx-px,cy-py)
                entity.draw(self.window,coordonnates)
        self.window.display()

    def collision(self,player1,player2):
        pass
