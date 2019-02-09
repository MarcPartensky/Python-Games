import pygame

class Fenetre:
    def __init__(self,taille=[800,800]):
        """Crée une fenêtre et ses caractérisque
          """
        pygame.init()
        self.taille=taille
        self.nom="Othello"
        self.ecran = pygame.display.set_mode(self.taille)
        self.icon = pygame.image.load("icon.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.nom)
        self.ouverte=True

    def verifier(self):
        """Verifie si la fenetre est ouverte."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ouverte=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.ouverte=False
