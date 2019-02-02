from mywindow import Window

class Game:
    def __init__(self,name="Unnamed",window=[],entities=[]):
        """Create a game object using name, window and entities."""
        self.name=name
        self.window=window
        self.entities=entities
        self.load()

    def load(self):
        """Loads specifics attributs of game object."""
        self.cursor=None
        self.click=None
        self.keys=None
        self.turn=0

    def __call__(self):
        self.loop()


    def loop(self):
        """Main game loop."""
        self.show()
        while self.window.open:
            self.window.check()
            self.turn+=1
            self.input()
            self.update()
            self.show()
        self.window.kill()

    def show(self):
        """Show all game entities on window."""
        self.window.clear
        for entity in self.entities:
            entity.show()
        self.window.flip()

    def update(self):
        """Update all game entities on window."""
        for entity in self.entities:
            entity.update(self.cursor,self.click,self.keys)

    def input(self):
        """Wait for user to insert input."""
        change=False
        while not change:
            cursor=self.window.point()
            if cursor is not self.cursor:
                self.cursor=cursor
                change=True
            click=self.window.click()
            if click is not self.click:
                self.click=click
                change=True
            keys=self.window.press()
            if keys is not self.keys:
                self.keys=keys
                change=True

    def log(self,message):
        """Print message with game mention."""
        output=str(type(self))
        print(output)

if __name__=="__main__":
    game=Game("test",Window())
    game()
    game.log("salut")
