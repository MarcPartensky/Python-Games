from mywindow import Window

class Lab:
    def __init__(self,name="Lab",entities=[]):
        """Creates lab using name."""
        self.name=name
        self.entities=entities
        self.loop=[]
        self.window=Window(self.name)

    def __call__(self):
        """Main loop."""
        #self.spawn()
        while self.window.open:
            self.window.check()
            self.window.clear()
            for function in self.loop:
                function()
            self.update()
            self.show()

    def update(self):
        """Updating all entities."""
        for entity in self.entities:
            entity.update(self.window.input)

    def show(self):
        """Update screen."""

        for entity in self.entities:
            entity.show(self.window)
        self.window.flip()

    def spawn(self):
        """Spawn all entites."""
        for entity in self.entities:
            entity.spawn()

if __name__=="__main__":
    #import mypanel

    lab=Lab("Testing Zone")
    lab()
