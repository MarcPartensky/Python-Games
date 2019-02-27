class Scene:
    made=0
    def __init__(self,name="Unnamed",pannels=[]):
        Scene.made+=1
        self.made=Scene.made
        self.name=name
        self.pannels=pannels
        self.focus=0

    def set(self):
        pass

    def update(self):
        for pannel in self.pannels:
            pannel.update()


    def show(self,window):
        for pannel in self.pannels:
            pannel.show(window)


if __name__=="__main__":
    window=Window(build=False)
    scene=Scene("Name")
