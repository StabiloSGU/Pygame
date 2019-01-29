import pygame, sys
from pygame.locals import *

#starts background loops?
#tutorial says this call has to be made at the begining
pygame.init()

#why is it a variable?
dispsurf = pygame.display.set_mode((500, 400), 0, 32)
 
pygame.display.set_caption('Derp')

#color section
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#draw on sceen surface
dispsurf.fill(white)
pygame.draw.polygon(dispsurf, green, ((146,0), (291, 106), (236, 277), (56, 277),
                                      (0, 106)))
pygame.draw.line(dispsurf, blue, (60, 60), (120, 60), 4)
pixObj = pygame.PixelArray(dispsurf)
pixObj[480][380] = black
pixObj[482][382] = black
pixObj[484][384] = black
pixObj[486][386] = black
pixObj[488][388] = black
#main loop
while True:
    #oh boy, here you handle events, update game state and redraw visuals
    for event in pygame.event.get():
        #pygame.locals.QUIT = QUIT because import *
        if event.type == QUIT:
            pygame.quit()            
            sys.exit()
    #redraws visuals
    pygame.display.update()
