import pygame

class Window:
    made=0
    def __init__(self,game=None,size=None,font="monospace",set=True):
        Window.made+=1
        self.number=Window.made
        self.title=game.name
        self.font=font
        self.open=True
        if set:
            self.set()

    def set(self):
        pygame.init()
        self.setSize(size)
        self.font = pygame.font.SysFont(self.font, 65)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def setSize(self,size=None):
        if size is None:
            info = pygame.display.Info()
            self.size=(info.current_w/2,info.current_h/2)
        else:
            self.size=size

    def pop_up(self,message):
        pass

    def scale(self,picture,size):
        return pygame.transform.scale(picture,size)

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False

    def select(self):
        while self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])

    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])

    def flip(self):
        pygame.display.flip()

    def drawPicture(self,picture,position):
        self.screen.blit(picture, position)

    def display(page):
        pass
