from mycase import Case

class Panel(Case):
    def random(corners=[-1,-1,1,1],n=5):
        """Create a random pannel within the optional corners given and the number of buttons."""
        return Panel(position,size,buttons)

    def __init__(self,position,size,buttons=[],color=None):
        """Create a pannel using the buttons."""
        super().__init__(position,size,color)
        self.buttons=buttons

    def splitButtons(self):
        """Place the buttons so they are the most sparsed as possible in the panel."""
        pass

    def update(self,keys):
        """Update the pannel by updating all its components such as buttons."""
        self.updateButtons(keys)

    def updateButtons(self,keys):
        """Update all the buttons of the pannel."""
        for button in self.buttons:
            button.update(keys)

    def show(self,surface):
        """Show the pannel."""
        self.showCase(surface)
        for button in self.buttons:
            button.show(surface)


class Button(Case):
    def random(corners=[-1,-1,1,1]):
        """Create a random button."""
        case=Case.random(corners)
        super().__init__(*args,**kwargs)
        self.position=case.position
        return self

    def __init__(self,*args,**kwargs):
        """Create a button object using its position and size."""
        super().__init__(*args,**kwargs)
        self.focus=False
        self.clicked=False
        self.hovered=False

    def update(self):
        """Update the buttons and its parameters."""
        self.isHovered()
        self.isClicked()
        self.isFocused()

    def isHovered(self,keys):
        """Determine if the button is being pointed."""
        x,y=position
        xmin,ymin,xmax,ymax=self.getCorners()
        self.hovered=bool((xmin<=x<=xmax) and (ymin<=y<=ymax))

    def isClicked(self,keys):
        """Determine if the button is being clicked."""
        self.clicked=bool(self.hovered and keys[0])

    def isFocused(self,keys):
        """Determine if the button is being focused."""
        self.focus=(self.clicked and not self.focus) or (self.focus and not self.clicked)

    def onClick(self):
        """Allow the user to overload the button to trigger an action when the button is clicked."""
        pass

    def onFocus(self):
        """Allow the user to overload the button to trigger an action when the button is focused."""
        pass

    def onHovering(self):
        """Allow the user to overload the button to trigger an action when the button is hovered."""
        pass

if __name__=="__main__":
    from mysurface import Context
    context=Context()
    buttons=[Button([0,0],[1,1])]
    panel=Panel([0,0],[10,10],buttons)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        panel.update(context)
        panel.show(context)
        context.flip()
