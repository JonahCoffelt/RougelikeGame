import pygame
import numpy as np
import math
import random
from pygame._sdl2.video import Window, Renderer, Texture

from weapons import weapons
from projectile import bullet, update_projectiles
from encounterGeneration import get_map
from player import Player
from camera import Camera
from spriteSheet import process_image_sheets, images
from tileRules import *
from particles import *

clock = pygame.time.Clock()

winSize = (1280, 720)
win = Window(title="pygame", size=winSize, resizable=True)
renderer = Renderer(win)

mapSize = 150 #Width/Height of map array
fov = 20 #Number of tiles displayed on screen
gridSize = winSize[0]//fov #Pixel lenght/width of tiles

player_character = Player(20, 20) #Initialize player
cam = Camera(player_character, .004) #Initialize camera

projectiles = []

process_image_sheets(pygame.image.load(r'Assets\SpriteSheets\cornerTileTest.png'), 'cornerTileTest', 8)
process_image_sheets(pygame.image.load(r'Assets\SpriteSheets\SampleTileSheet.png'), 'SampleTileSheet', 16)

print(len(images[0]))

run = True
pygame.init()

def load_map_surf():
    map_surf = pygame.Surface((mapSize * gridSize, mapSize * gridSize))
    for x in range(mapSize-1):
        for y in range(mapSize-1):
            if map[x][y] == 1:
                if (map[x + 1][y] != 1 or map[x - 1][y] != 1 or map[x][y + 1] != 1 or map[x][y - 1] != 1 or 
                    map[x + 1][y + 1] != 1 or map[x - 1][y + 1] != 1 or map[x + 1][y - 1] != 1 or map[x - 1][y - 1] != 1):
                    image_surf = pygame.transform.scale(get_tile_state(x, y, map, 1), (gridSize, gridSize))
                    map_surf.blit(image_surf, (x * gridSize, y * gridSize))
            else:
                image_surf = pygame.transform.scale(images[1][0], (gridSize, gridSize))
                map_surf.blit(image_surf, (x * gridSize, y * gridSize))
    return map_surf

def draw():
    map_texture.draw((player_character.x * gridSize - winSize[0]/2 + (cam.x - player_character.x) * gridSize, player_character.y * gridSize - winSize[1]/2 + (cam.y - player_character.y) * gridSize, winSize[0], winSize[1]), (0, 0, winSize[0], winSize[1]))

    renderer.draw_color = (155, 0, 0, 255)
    renderer.fill_rect((winSize[0]/2 - (cam.x - player_character.x) * gridSize - (gridSize * player_character.width)/2, winSize[1]/2 - (cam.y - player_character.y) * gridSize - (gridSize * player_character.width)/2, gridSize * player_character.width, gridSize * player_character.width))

    for projectile in projectiles:
        projectile.update(dt)
        renderer.fill_rect(((projectile.x - cam.x) * gridSize + winSize[0]/2, (projectile.y - cam.y) * gridSize + winSize[1]/2, 10, 10))
        if projectile.life > projectile.flight_time:
            projectiles.remove(projectile)
        if map[int(projectile.x)][int(projectile.y)] == 1:
            #projectile.velocity, projectile.acceleration = 0, 0
            make_particles(projectile.x, projectile.y, projectile.dir, 1, 10)
            projectiles.remove(projectile)

    particle_surf = update_particles(winSize, gridSize, cam.x, cam.y, dt)
    particle_texture = Texture.from_surface(renderer, particle_surf)
    particle_texture.draw((0, 0, winSize[0], winSize[1]))

    renderer.present()

def update():
    cam.move(fov+1, mapSize, dt) #Moves camera towards the player
    player_character.dir = -math.atan2((mousey - winSize[1]/2), (mousex - winSize[0]/2))
    if player_character.fire_time < weapons[player_character.equiped][6]:
        player_character.fire_time += dt
    draw()
    win.title = str(round(clock.get_fps())) #Display FPS

map = get_map(0, 2, mapSize)
map_surf = load_map_surf()
map_texture = Texture.from_surface(renderer, map_surf)

while run:
    dt = clock.tick() #Delta time (time from last fram to current frame)
    
    mousex, mousey = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win.destroy()
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    #Player input for movement
    move_x, move_y = 0, 0
    if keys[pygame.K_s]:
        move_y = 1
    if keys[pygame.K_w]:
        if move_y: move_y = 0
        else: move_y = -1 
    if keys[pygame.K_d]:
        move_x = 1
    if keys[pygame.K_a]:
        if move_x: move_x = 0
        else: move_x = -1
    player_character.move(move_x, move_y, dt, map)
    #Equip Item
    if keys[pygame.K_1]: player_character.equiped = 0
    if keys[pygame.K_2]: player_character.equiped = 1
    if keys[pygame.K_3]: player_character.equiped = 2
    if keys[pygame.K_4]: player_character.equiped = 3
    #Regenerate map
    if keys[pygame.K_r]:
        map = get_map(0, 9, mapSize)
        map_surf = load_map_surf()
        map_texture = Texture.from_surface(renderer, map_surf)
    #Spawn pistol bullet
    if pygame.mouse.get_pressed()[0]:
        if player_character.fire_time >= weapons[player_character.equiped][6]:
            player_character.fire_time = 0
            cam.shake = weapons[player_character.equiped][7]
            cam.shake_magnitude = weapons[player_character.equiped][8]
            for projectile in range(weapons[player_character.equiped][4]):
                projectiles.append(bullet(player_character.x, player_character.y, player_character.dir + random.uniform(-weapons[player_character.equiped][3], weapons[player_character.equiped][3]), weapons[player_character.equiped]))

    update()