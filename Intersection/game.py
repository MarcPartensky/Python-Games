from mygeometry import Forms
from mywindow import Window


class Level:
    def __init__(self,name="Unnamed",over=False):
        self.name=name
        self.over=over
    def create(self):
        self.entities

class Game:
    def __init__(self,name="Asteroid",window=None):
        self.name=name
        self.window=window
        if self.window==None: self.window=Window(self.name,build=False)
        self.window.build()
        self.plan=Plan(lines=False)
        self.levels=[Level("First level")]
        self.round=0
        self.over=False
    def __call__(self):
        while self.window.open and not self.over:
            self.window.check()
            self.update()
            self.show()
    def update(self):
        level=self.levels[self.round]
        if level.over:
            self.round+=1
        else:
            level()
            entities=self.levels[self.level].entities
            player=level.control()
            for entity in entities:
                entity.update(entities)

    def show(self):
        self.window.clear()
        for entity in self.levels[self.round].entities:
            entity.show(self.window,self.plan)
        self.window.flip()




if __name__=="__main__":
    window=Window(build=False)
    game=Game(window=window)
    game()
