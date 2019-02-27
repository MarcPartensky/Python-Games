from mywindow import Window

class Lab:
    def __init__(self,name="Lab"):
        """Creates lab using name."""
        self.name=name
        self.entities=[]
        self.window=Window(self.name)


    def __call__(self):
        """Main loop."""
        while self.window.open:
            self.window.check()
            #self.input()
            self.update()
            self.show()

    def input(self):
        """Updates game inputs."""
        self.inputs=self.window.getInput()

    def update(self):
        """Updating all entities."""
        for entity in self.entities:
            entity.update(self.window)

    def show(self):
        """Update screen."""
        self.window.clear()
        for entity in self.entities:
            entity.show(self.window)
        self.window.flip()


if __name__=="__main__":
    lab=Lab("Testing Zone")
    lab()
