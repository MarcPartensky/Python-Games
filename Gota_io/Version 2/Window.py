class Window:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(FONT, 65)
        info = pygame.display.Info()
        w=info.current_w
        h=info.current_h
        self.size=(w/2,h/2)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(GAME_NAME)
        pygame.display.flip()
    def select(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])
    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])
    def display(self):
        pygame.display.flip()
