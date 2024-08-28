import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
from gl import *

width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen) 
rend.glLoadBackground("textures/granjita.bmp")

modelo1 = Model("models/Mushroom.OBJ")
modelo1.LoadTexture("textures/textures.bmp")
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = waveShader
modelo1.translate[0] = 1
modelo1.translate[1] = -1
modelo1.translate[2] = -5
modelo1.scale[0] = 0.05
modelo1.scale[1] =  0.05
modelo1.scale[2] =  0.05
rend.models.append(modelo1)

modelo2 = Model("models\cow.obj")
modelo2.LoadTexture("textures\Cow_tornado_cow_material_BaseColor.bmp")
modelo2.vertexShader = vertexShader
modelo2.fragmentShader =shatteredGlassShader
modelo2.translate[2] = -25
modelo2.translate[0] = -20
modelo2.translate[1] = -2
modelo2.scale[0] = 0.3
modelo2.scale[1] = 0.3
modelo2.scale[2] = 0.3

rend.models.append(modelo2)

modelo3 = Model("models\Goat.obj")
modelo3.LoadTexture("textures\Goat_D.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = greenStripesShader
modelo3.translate[2] = -15
modelo3.translate[0] = -5
modelo3.translate[1] = - 2
modelo3.scale[0] = 1.5
modelo3.scale[1] = 1.5
modelo3.scale[2] = 1.5
modelo3.rotate[2] = 90
rend.models.append(modelo3)


modelo4 = Model("models/3DModel_LowPoly.obj")
modelo4.LoadTexture("textures/3DModel.bmp")
modelo4.vertexShader = vertexShader
modelo4.fragmentShader =  fireShader
modelo4.translate[2] = 2
modelo4.translate[0] = 2
modelo4.translate[1] = -6
modelo4.scale[0] = 2
modelo4.scale[1] = 2
modelo4.scale[2] = 2
#modelo4.rotate[1] = 90
rend.models.append(modelo4)

puntoA = [50, 50, 0]
puntoB = [250, 500, 0]
puntoC = [500, 50, 0]



isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 5 
            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 5 
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_m:  # Medium shot
                modelo1.translate[0] = -2
                modelo1.translate[1] = -1
                modelo1.translate[2] = -10
                modelo1.rotate = [0, 0, 0]
                rend.glGenerateFrameBuffer("medium_shot.bmp")
            elif event.key == pygame.K_l:  # Low angle
                modelo1.translate[0] = -2
                modelo1.translate[1] = 0
                modelo1.translate[2] = -8
                modelo1.rotate = [0, 0, 0]
                rend.glGenerateFrameBuffer("low_angle.bmp")
            elif event.key == pygame.K_h:  # High angle
                modelo1.translate[0] = -2
                modelo1.translate[1] = -3
                modelo1.translate[2] = -12
                modelo1.rotate = [0, 0, 0]
                rend.glGenerateFrameBuffer("high_angle.bmp")
            elif event.key == pygame.K_d:  # Dutch angle
                modelo1.translate[0] = -2
                modelo1.translate[1] = -1
                modelo1.translate[2] = -10
                modelo1.rotate = [0, 0, 15]
                rend.glGenerateFrameBuffer("dutch_angle.bmp")
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES

    rend.glClear()
    rend.glClearBackground()

    rend.glRender()

    # poly1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
    # poly2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
    # poly3 = [(377, 249), (411, 197), (436, 249)]
    # poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
    #         (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
    #         (597, 215), (552, 214), (517, 144), (466, 180)]
    # poly5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

    # rend.glFillPolygon(poly1, [1, 0.5, 1])  
    # rend.glFillPolygon(poly2, [1,0.5,1])
    # rend.glFillPolygon(poly3, [1,0.5,1])
    # rend.glFillPolygon(poly4, [1,0.5,1])
    # rend.glFillPolygon(poly5, [0,0,0])

    pygame.display.flip()
    clock.tick(60)
    rend.glGenerateFrameBuffer("output.bmp")
    # rend.glRender()

pygame.quit()