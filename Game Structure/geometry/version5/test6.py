import pygame

imgsurface = pygame.image.load('output.png')
imgarray = pygame.surfarray.array2d(imgsurface)

print(imgarray)
