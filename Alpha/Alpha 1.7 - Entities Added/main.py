import pygame
import math
from pygame._sdl2.video import Window, Renderer, Texture

from weapons import *
from projectile import update_projectiles, projectiles
from encounterGeneration import get_map
from player import Player
from camera import Camera
from spriteSheet import process_image_sheets, images
from tileRules import *
from particle import *
from imageCache import *
from entity import *
from item import *
from inputs import handle_inputs

clock = pygame.time.Clock()

winSize = (1280, 720)
win = Window(title="pygame", size=winSize, resizable=True)
renderer = Renderer(win)

mapSize = 150 #Width/Height of map array
fov = 60 #Number of tiles displayed on screen
gridSize = winSize[0]//fov #Pixel lenght/width of tiles

player_character = Player(20, 20) #Initialize player
cam = Camera(player_character, .004) #Initialize camera

process_image_sheets(pygame.image.load(r'Assets\SpriteSheets\cornerTileTest.png'), 'cornerTileTest', 8)
process_image_sheets(pygame.image.load(r'Assets\SpriteSheets\SampleTileSheet.png'), 'SampleTileSheet', 16)

image_cache = set_image_cache(renderer)

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

def update():
    cam.move(fov+1, mapSize, dt) # Moves camera towards the player
    player_character.dir = -math.atan2((mousey - (winSize[1]/2 + (player_character.y - cam.y) * gridSize)), (mousex - (winSize[0]/2 + (player_character.x - cam.x) * gridSize)))
    if player_character.fire_time < weapons[player_character.equiped][6]:
        player_character.fire_time += dt
    
    draw() # Draws map and player to renderer
    
    update_particles(renderer, image_cache, winSize, gridSize, cam.x, cam.y, dt) # Updates particle position and draws to renderer
    update_entities(renderer, map, winSize, gridSize, cam, player_character, image_cache, dt) # Updates entity position and draws to renderer
    update_projectiles(renderer, map, winSize, gridSize, cam, image_cache, dt) # Updates projectile position and draws to renderer
    update_items(renderer, cam, player_character, image_cache, gridSize, winSize, dt)

    renderer.present()
    
    win.title = "FPS : " + str(round(clock.get_fps())) + "   Projectiles : " + str(len(projectiles)) + "   Particles : " + str(len(particles))

map = get_map(0, 2, mapSize)
map_surf = load_map_surf()
map_texture = Texture.from_surface(renderer, map_surf)

while run:
    dt = clock.tick(60) #Delta time (time from last fram to current frame)
    
    mousex, mousey = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win.destroy()
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    handle_inputs(keys, map, player_character, cam, dt)
    
    # Regenerate map (I kept this here because it will change in the future)
    if keys[pygame.K_r]:
        map = get_map(0, 9, mapSize)
        map_surf = load_map_surf()
        map_texture = Texture.from_surface(renderer, map_surf)

    update()