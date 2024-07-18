import pygame
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen) 

rend.glColor(1,0.5,1)


isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCPAE:
                isRunning = False

    rend.glClear()

    poly1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
    poly2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
    poly3 = [(377, 249), (411, 197), (436, 249)]
    poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
            (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
            (597, 215), (552, 214), (517, 144), (466, 180)]
    poly5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

    rend.glFillPolygon(poly1, [1, 0.5, 1])  
    rend.glFillPolygon(poly2, [1,0.5,1])
    rend.glFillPolygon(poly3, [1,0.5,1])
    rend.glFillPolygon(poly4, [1,0.5,1])
    rend.glFillPolygon(poly5, [0,0,0])


    pygame.display.flip()
    rend.glGenerateFrameBuffer("render.bmp")
    clock.tick(60)

pygame.quit()