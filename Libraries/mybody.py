class Body:
    made=0
    def __init__(self,name="Unnamed",position=None,velocity=None,acceleration=None,size=None):
        """Create a body object."""
        Body.made+=1
        self.made=Body.made
        self.name=name
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration
        self.size=size











"""
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


"""
Syntax:

if self.click:
    for body in self.bodies:
        body.check()
        if body.selected:
            body.pick(cursor)








"""
