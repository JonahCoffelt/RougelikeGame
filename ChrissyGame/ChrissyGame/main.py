import pygame
import numpy as np
from numba import njit
from pygame._sdl2.video import Window, Renderer, Texture, Image

from weapons import weapons
from projectile import bullet
from encounterGeneration import get_map
from player import Player

clock = pygame.time.Clock()

winSize = (1280, 720)

win = Window(title="pygame", size=winSize)
win.resizable = True
renderer = Renderer(win)

mapSize = 125

player_character = Player(20, 20)
fov = 15
gridSize = winSize[0]//fov

run = True
pygame.init()


@njit()
def get_frame_array(map, posx, posy, fov):
    room_color = ([1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0], [.5, 0.0, 0.0], [0.0, .5, 0.0], [0.0, 0.0, .5])
    frame = np.random.uniform(0, 1, (fov + 1, fov, 3))
    for x in range(fov + 1):
        for y in range(fov):
            frame[x][y] = room_color[map[(posx + x - fov//2) + (posy + y - fov//2) * mapSize]]

    return frame

def draw():
    frame = get_frame_array(map, int(player_character.posx), int(player_character.posy), fov)

    surf = pygame.surfarray.make_surface(frame*255)
    #surf = pygame.transform.scale(surf, (winSize[0], winSize[0]))
    frame_texture = Texture.from_surface(renderer, surf)
    
    #frame_img = Image(frame_texture)
    #renderer.blit(frame_img)
    frame_texture.draw((0, 0, winSize[0] + gridSize, winSize[0]), (gridSize * (int(player_character.posx) - player_character.posx), gridSize * (int(player_character.posy) - player_character.posy), winSize[0] + gridSize, winSize[0]))

    renderer.present()

def update():
    draw()
    win.title = str(round(clock.get_fps()))

map = get_map(0, 2, mapSize)

while run:
    dt = clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_character.move(0, -1, dt)
    if keys[pygame.K_s]:
        player_character.move(0, 1, dt)
    if keys[pygame.K_a]:
        player_character.move(-1, 0, dt)
    if keys[pygame.K_d]:
        player_character.move(1, 0, dt)
    if keys[pygame.K_r]:
        map = get_map(0, 9, mapSize)
    if keys[pygame.K_g]:
        bullet(weapons["pistol"])
    
    update()