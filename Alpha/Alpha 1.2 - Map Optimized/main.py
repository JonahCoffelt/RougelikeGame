import pygame
import numpy as np
from pygame._sdl2.video import Window, Renderer, Texture

from weapons import weapons
from projectile import bullet, update_projectiles
from encounterGeneration import get_map
from player import Player
from camera import Camera
from spriteSheet import process_image_sheets, images

clock = pygame.time.Clock()

winSize = (1280, 720)
win = Window(title="pygame", size=winSize, resizable=True)
renderer = Renderer(win)

mapSize = 250 #Width/Height of map array
fov = 20 #Number of tiles displayed on screen
gridSize = winSize[0]//fov #Pixel lenght/width of tiles

player_character = Player(20, 20) #Initialize player
cam = Camera(player_character, .004) #Initialize camera

projectiles = []

process_image_sheets(pygame.image.load(r'Assets\SpriteSheets\SampleTileSheet.png'), 'SampleTileSheet')

run = True
pygame.init()

def load_map_surf():
    map_surf = pygame.Surface((mapSize * gridSize, mapSize * gridSize))
    for x in range(mapSize-1):
        for y in range(mapSize-1):
            if map[x][y] == 1:
                if map[x + 1][(y)] != 1 or map[x - 1][y] != 1 or map[x][y + 1] != 1 or map[x][y - 1] != 1:
                    image_surf = pygame.transform.scale(images[0][1], (gridSize, gridSize))
                    map_surf.blit(image_surf, (x * gridSize, y * gridSize))
            else:
                image_surf = pygame.transform.scale(images[0][0], (gridSize, gridSize))
                map_surf.blit(image_surf, (x * gridSize, y * gridSize))
    return map_surf

def draw():
    map_texture.draw((player_character.x * gridSize - winSize[0]/2 + (cam.x - player_character.x) * gridSize, player_character.y * gridSize - winSize[1]/2 + (cam.y - player_character.y) * gridSize, winSize[0], winSize[1]), (0, 0, winSize[0], winSize[1]))

    renderer.draw_color = (155, 0, 0, 255)
    renderer.fill_rect((winSize[0]/2 - (cam.x - player_character.x) * gridSize - (gridSize * player_character.width)/2, winSize[1]/2 - (cam.y - player_character.y) * gridSize - (gridSize * player_character.width)/2, gridSize * player_character.width, gridSize * player_character.width))

    renderer.present()

def update():
    cam.move(fov+1, mapSize, dt) #Moves camera towards the player
    draw()
    if len(projectiles):
        update_projectiles(np.array(projectiles))
    win.title = str(round(clock.get_fps())) #Display FPS

map = get_map(0, 2, mapSize)
map_surf = load_map_surf()
map_texture = Texture.from_surface(renderer, map_surf)

while run:
    dt = clock.tick() #Delta time (time from last fram to current frame)
    
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
    #Regenerate map
    if keys[pygame.K_r]:
        map = get_map(0, 9, mapSize)
        map_surf = load_map_surf()
        map_texture = Texture.from_surface(renderer, map_surf)
    #Spawn pistol bullet
    if keys[pygame.K_g]:
        projectiles.append(bullet(player_character.x, player_character.y, player_character.dir, weapons["pistol"]))
    
    update()