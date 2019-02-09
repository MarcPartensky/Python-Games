class Body:
    def __init__(self,name,position,size):
        """Create a body object."""
        self.name=name
        self.position=position
        self.size=size
        self.selected=False


    def check(self,cursor):
        cx,cy=cursor
        x,y=self.position
        sx,sy=self.size
        if x<=cx<sx and y<=cy<sy:
            self.selected=True
            self.cursor_position=cursor
        else:
            self.selected=False
            self.cursor_position=None



    def pick(self,cursor):
        cx,cy=cursor
        cpx,cpy=self.cursor_position
        x,y=self.position
        self.position=x+cx-cpx,y+cy-cpy

    def show(self,window):
        pass



"""
Syntax:

if self.click:
    for body in self.bodies:
        body.check()
        if body.selected:
            body.pick(cursor)








"""
