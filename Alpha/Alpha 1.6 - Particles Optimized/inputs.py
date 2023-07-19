import pygame
from projectile import *
import random
from weapons import *

def handle_inputs(keys, map, player_character, cam, dt):
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
    if keys[pygame.K_5]: player_character.equiped = 4
    if keys[pygame.K_6]: player_character.equiped = 5
    #Spawn pistol bullet
    if pygame.mouse.get_pressed()[0]:
        if player_character.fire_time >= weapons[player_character.equiped][6]:
            player_character.fire_time = 0
            cam.shake = weapons[player_character.equiped][7]
            cam.shake_magnitude = weapons[player_character.equiped][8]
            for projectile in range(weapons[player_character.equiped][4]):
                projectiles.append(bullet(player_character.x, player_character.y, player_character.dir + random.uniform(-weapons[player_character.equiped][3], weapons[player_character.equiped][3]), weapons[player_character.equiped]))
