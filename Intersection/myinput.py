import pygame

class Input:
    getKeys=pygame.key.get_pressed()
    getClick=bool(pygame.mouse.get_pressed()[0])
    getCursor=pygame.mouse.get_pos()

    def __init__(self):
        self()
        
    def __call__(self):
        self.click=Input.getClick()
        self.cursor=Input.getCursor()
        self.keys=Input.getKeys()
