from mywindow import Window

class Lab:
    def __init__(self,name="Lab"):
        """Creates lab using name."""
        self.name=name
        self.entities=[]
        self.window=Window(self.name,set=False)

    def __call__(self):
        """Main loop."""
        self.spawn()
        while self.window.open:
            self.window.check()
            self.update()
            self.show()

    def update(self):
        """Updating all entities."""
        for entity in self.entities:
            entity.update()

    def show(self):
        """Update screen."""
        self.window.clear()
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
