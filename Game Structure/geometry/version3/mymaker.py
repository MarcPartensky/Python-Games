from mywindow import Window
from myplane import Plane
from myform import Form
from mypoint import Point

from mycolors import WHITE,RED,GREEN

from copy import deepcopy

from pygame.locals import *

class Maker(Plane):
    """Form maker is a tool which purpose is to be able to create forms in real time and interact with them."""
    def __init__(self,forms=[],theme={},view=None):
        Plane.__init__(self,theme,view)
        self.forms=forms
        self.selection=None

    def startForm(self,screen_position,window):
        """Start a new form to create using screen_position and window."""
        position=self.getFromScreen(screen_position,window)
        point=Point(position)
        self.selection=len(self.forms)
        self.forms.append(Form([point]))

    def changeForm(self,screen_position,window,selection=None):
        """Change the selected form using screen_position, window and optional selection."""
        self.addPointToForm(screen_position,window,selection)

    def addPointToForm(self,screen_position,window,selection=None):
        """Add a point to the selected form."""
        if not selection: selection=self.selection
        position=self.getFromScreen(screen_position,window)
        point=Point(position)
        self.forms[selection]+=point

    def endForm(self):
        """End the creation of a form."""
        self.selection=None

    def update(self,window):
        """Update all the forms using window."""
        self.rotateForms()
        self.detectCollisions()

    def rotateForms(self):
        """Allow the forms to rotate, this function is only made in order to draw cool stuff on screen."""
        for i in range(len(self.forms)):
            self.forms[i].rotate(0.1,self.forms[i].center())

    def detectCollisions(self):
        """Detect collisions between shapes and change the colliding forms in red."""
        """Just testing if we can have cool effects."""
        for i in range(len(self.forms)):
            self.forms[i].side_color=WHITE
        for i in range(len(self.forms)):
            for j in range(i+1,len(self.forms)):
                if self.forms[i]|self.forms[j]:
                    self.forms[i].side_color=RED
                    self.forms[j].side_color=RED



    def show(self,window):
        """Show all the form using window."""
        for form in self.forms:
            self.showForm(form,window)
            center=form.center(color=GREEN)
            center.show(window)

    def showForm(self,plane_form,window):
        """Show a form using window."""
        screen_form=self.getFormToScreen(plane_form,window)
        screen_form.show(window)

    def getFormToScreen(self,plane_form,window):
        """Create a new form according screen coordonnates using a form and the window."""
        points=[Point(self.getToScreen(point,window)) for point in plane_form]
        screen_form=deepcopy(plane_form)
        screen_form.points=points
        return screen_form

    def event(self,window):
        """Handle window events specifics to the maker."""
        keys=window.press()
        click=window.click()
        cursor=window.point()
        if click:
            if not self.selection:
                self.startForm(cursor,window)
            else:
                self.changeForm(cursor,window)
        if keys[K_SPACE]:
            self.endForm()


    def select(self,window):
        """Still not clear what it does. (it means its useless)"""
        pass


if __name__=="__main__":
    window=Window(fullscreen=True)
    maker=Maker()
    maker(window)
