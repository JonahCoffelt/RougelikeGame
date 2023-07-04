import pygame
import numpy as np
from numba import njit
from pygame._sdl2.video import Window, Renderer, Texture, Image

from weapons import weapons
from projectile import bullet
from encounterGeneration import get_map

clock = pygame.time.Clock()

winSize = (1280, 720)

win = Window(title="pygame", size=winSize)
win.resizable = True
renderer = Renderer(win)

drawLength = int(winSize[0]/5)
gridSizex = winSize[0]/drawLength
gridSizey = winSize[1]/drawLength

mapSize = 50
gridSize = winSize[1]/mapSize

run = True
pygame.init()

@njit()
def get_frame_array(map):
    frame = np.random.uniform(0, 1, (mapSize, mapSize, 3))
    for x in range(mapSize):
        for y in range(mapSize):
            if map[x + y * mapSize]:
                frame[x][y] = [.5, .5, .5]

    #for x in range(drawLength):
    #    for y in range(drawLength):
    #        frame[x][y] = [x/drawLength, y/drawLength, .5]
    return frame

def draw():
    frame = get_frame_array(map)

    #surf = pygame.surfarray.make_surface(frame*255)
    #frame_texture = Texture.from_surface(renderer, surf)
    #frame_texture.draw()

    renderer.draw_color = (25, 25, 25, 255)

    for x in range(mapSize):
        for y in range(mapSize):
            if map[x + y * mapSize]:
                renderer.fill_rect((x * gridSize, y * gridSize, gridSize - 1, gridSize - 1))

    renderer.present()

def update():
    draw()
    win.title = str(round(clock.get_fps()))

map = get_map(0, 1, mapSize)

while run:
    dt = clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        bullet(weapons["pistol"])
    
    update()