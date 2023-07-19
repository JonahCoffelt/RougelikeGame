import pygame
import numpy as np
from numba import njit
from pygame._sdl2.video import Window, Renderer, Texture, Image

from weapons import weapons
from projectile import bullet, update_projectiles
from encounterGeneration import get_map
from player import Player
from camera import Camera
from spriteSheet import processImageSheets, images

clock = pygame.time.Clock()

winSize = (1280, 720)
win = Window(title="pygame", size=winSize)
win.resizable = True

renderer = Renderer(win)

mapSize = 500 #Width/Height of map array
fov = 50 #Number of tiles displayed on screen
gridSize = winSize[0]//fov #Pixel lenght/width of tiles

player_character = Player(20, 20) #Initialize player
cam = Camera(player_character.posx, player_character.posy, .004) #Initialize camera

projectiles = []

processImageSheets(pygame.image.load(r'Assets\SpriteSheets\SampleTileSheet.png'), 'SampleTileSheet')
texture_cache = []

run = True
pygame.init()

def load_image_cache():
    for sheet in images:
        texture_cache.append([])
        for image in sheet:
            #surf = pygame.transform.scale(image, (gridSize, gridSize))
            texture = Texture.from_surface(renderer, image)
            texture_cache[-1].append(texture)
            
@njit()
def get_frame_array(map, posx, posy, fov):

    #Placeholder colors to display the rooms
    room_color = ([0.3, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.3, 0.0], [0.0, 0.0, 0.3], [0.3, 0.3, 0.0], [0.3, 0.0, 0.3], [0.0, 0.3, 0.3], [0.3, 0.3, 0.3], [.5, 0.0, 0.0], [0.0, .5, 0.0], [0.0, 0.0, .5])

    frame = np.random.uniform(0, 1, (fov + 1, fov, 3)) #Initialize frame as random array
    for x in range(fov + 1):
        for y in range(fov):
            id = int(map[(posx + x - fov//2)][(posy + y - fov//2)])
            if id == 1:
                if map[(posx + x - fov//2) + 1][(posy + y - fov//2)] != 1 or map[(posx + x - fov//2) - 1][(posy + y - fov//2)] != 1 or map[(posx + x - fov//2)][(posy + y - fov//2) + 1] != 1 or map[(posx + x - fov//2)][(posy + y - fov//2) - 1] != 1:
                    frame[x][y] = [.25, .25, .35] #Wall
                else:
                    frame[x][y] = room_color[1]
            else:
                frame[x][y] = room_color[id]

    return frame

#@njit()
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
    #frame = get_frame_array(map, int(cam.x), int(cam.y), fov) #Get frame as array
    #surf = pygame.surfarray.make_surface(frame*255) #Covert frame array to pygame surface
    #frame_texture = Texture.from_surface(renderer, surf) #Create SDL2 texture from the frame surface
    #frame_texture.draw((0, 0, winSize[0] + gridSize, winSize[0]), (gridSize * (int(cam.x) - cam.x), gridSize * (int(cam.y) - cam.y) - (winSize[0]-winSize[1])/2, winSize[0] + gridSize, winSize[0])) #Draw frame texture to renderer

    map_texture.draw((player_character.posx * gridSize - winSize[0]/2 + (cam.x - player_character.posx) * gridSize, player_character.posy * gridSize - winSize[1]/2 + (cam.y - player_character.posy) * gridSize, winSize[0], winSize[1]), (0, 0, winSize[0], winSize[1]))

    renderer.draw_color = (155, 0, 0, 255)
    renderer.fill_rect((winSize[0]/2 - (cam.x - player_character.posx) * gridSize - (gridSize * player_character.width)/2, winSize[1]/2 - (cam.y - player_character.posy) * gridSize - (gridSize * player_character.width)/2, gridSize * player_character.width, gridSize * player_character.width))

    renderer.present()

def update():
    cam.move(player_character.posx, player_character.posy, fov+1, mapSize, dt) #Moves camera towards the player
    draw()
    if len(projectiles):
        update_projectiles(np.array(projectiles))
    win.title = str(round(clock.get_fps())) #Display FPS

map = get_map(0, 2, mapSize)
load_image_cache()
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
    if keys[pygame.K_w]:
        if keys[pygame.K_a]:
            player_character.move(-1, -1, dt, map)
        elif keys[pygame.K_d]:
            player_character.move(1, -1, dt, map)
        else:
            player_character.move(0, -1, dt, map)
    elif keys[pygame.K_s]:
        if keys[pygame.K_a]:
            player_character.move(-1, 1, dt, map)
        elif keys[pygame.K_d]:
            player_character.move(1, 1, dt, map)
        else:
            player_character.move(0, 1, dt, map)
    elif keys[pygame.K_a]:
        player_character.move(-1, 0, dt, map)
    elif keys[pygame.K_d]:
        player_character.move(1, 0, dt, map)
    #Regenerate map
    if keys[pygame.K_r]:
        map = get_map(0, 9, mapSize)
        map_surf = load_map_surf()
        map_texture = Texture.from_surface(renderer, map_surf)
    #Spawn pistol bullet
    if keys[pygame.K_g]:
        projectiles.append(bullet(player_character.posx, player_character.posy, player_character.dir, weapons["pistol"]))
    
    update()