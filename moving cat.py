import pygame, sys
from pygame.locals import *

pygame.init()

# because we are not 30fps plebs anymore, theres standards you know
fps = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')
WHITE = (255, 255, 255)
catImg = pygame.image.load('Musya.jpg')
catImg = pygame.transform.scale(catImg, (160, 100))
catx = 20
caty = 20
direction = 'right'

while True:
    DISPLAYSURF.fill(WHITE)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 20:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 20:
            direction = 'right'
    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(fps)
