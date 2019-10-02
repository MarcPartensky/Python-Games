# Programme : mandelbrot.py
# Langage : Python 3.6 - Pygame 1.9
# Auteur : Mathieu
# Description : Calcule et affiche la fractale de Mandelbrot en noir et blanc
import pygame
# Constantes
MAX_ITERATION = 50 # nombre d'itérations maximales avant de considérer que la suite converge
XMIN, XMAX, YMIN, YMAX = -2, +0.5, -1.25, +1.25 # bornes du repère
LARGEUR, HAUTEUR = 500, 500 # taille de la fenêtre en pixels
# Initialisation et création d'une fenêtre aux dimensions spécifiéés munie d'un titre
pygame.init()
screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Fractale de Mandelbrot")
# Création de l'ensemble de Mandelbrot
# Principe : on balaye l'écran pixel par pixel en convertissant le pixel en un point du plan de notre repère
# Si la suite converge, le point appartient à l'ensemble de Mandelbrot et on colore le pixel en noir
# Sinon la suite diverge, le point n'appartient pas à l'ensemble et on colore le pixel en blanc
for y in range(HAUTEUR):
  for x in range(LARGEUR):
    # Les deux lignes suivantes permettent d'associer à chaque pixel de l'écran de coordonnées (x;y)
    # un point C du plan de coordonnées (cx;cy) dans le repère défini par XMIN:XMAX et YMIN:YMAX
    cx = (x * (XMAX - XMIN) / LARGEUR + XMIN)
    cy = (y * (YMIN - YMAX) / HAUTEUR + YMAX)
    xn = 0
    yn = 0
    n = 0
    while (xn * xn + yn * yn) < 4 and n < MAX_ITERATION: # on teste que le carré de la distance est inférieur à 4 -> permet d'économiser un calcul de racine carrée coûteux en terme de performances
      # Calcul des coordonnes de Mn
      tmp_x = xn
      tmp_y = yn
      xn = tmp_x * tmp_x - tmp_y * tmp_y + cx
      yn = 2 * tmp_x * tmp_y + cy
      n = n + 1
    if n == MAX_ITERATION:
      screen.set_at((x, y), (0, 0, 0)) # On colore le pixel en noir -> code RGB : (0,0,0)
    else:
      screen.set_at((x, y), (255, 255, 255)) # On colore le pixel en blanc -> code RGB : (255,255,255)
pygame.display.flip() # Mise à jour et rafraîchissement de la fenêtre graphique pour affichage
# Boucle infinie permettant d'afficher à l'écran la fenêtre graphique
# Sans ça, la fenêtre apparaît et disparaît aussitôt
loop = True
while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # Pour quitter l'application en fermant la fenêtre
      loop = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      p = pygame.mouse.get_pos()
      px = (p[0] * (XMAX - XMIN) / LARGEUR + XMIN)
      py = (p[1] * (YMIN - YMAX) / HAUTEUR + YMAX)
      print("({};{})".format(px,py))

pygame.quit()
