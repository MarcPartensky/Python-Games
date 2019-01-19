class Page:
    def __init__(self,game,window,position=[0,0],size=None,components=[],button_colors=[BLACK,WHITE,BLACK]):
        self.game=game
        self.window=window
        self.position=position
        self.button_colors=button_colors

        if size is None:
            self.size=self.window.size
        else:
            self.size=size

        if component=[]:
            sx,sy=self.size
            self.components=[Button("Play",self.game.play,self.button_colors),
                             Button("Quit",self.game.quit,self.button_colors)]


    def set(self):
        nb=len(self.components)
        sx,sy=self.size
        x,y=self.position
        bsx,bsy=button_size=[sx/3,sy/(nb*2+1)]

        component_size=[bx,by]
        for i in range(nb):
            component_position=[x+i*bx,y+i*by]
            component[i].set(component_position,component_size)

    def addComponent(self,component):
        self.components+=component
        self.set()

    def show(self):
        for component in self.components:
            component.show(self.window)
