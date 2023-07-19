import pygame
from spriteSheet import images

def get_tile_state2(x, y, map, tile_type):
    b1, b2, b3, b4 = 0, 0, 0, 0
    if map[x - 1][y + 1] == tile_type:
        b1 = 1
    if map[x + 1][y + 1] == tile_type:
        b2 = 1
    if map[x + 1][y - 1] == tile_type:
        b3 = 1
    if map[x - 1][y - 1] == tile_type:
        b4 = 1
    
    state = b1 + (b2 * 2) + (b3 * 4) + (b4 * 8)

    return state

def get_tile_state3(x, y, map, tile_type):
    b1, b2, b3, b4 = 0, 0, 0, 0
    if map[x - 1][y - 1] == tile_type or map[x - 1][y] == tile_type or map[x][y - 1] == tile_type:
        b1 = 1
    if map[x + 1][y - 1] == tile_type or map[x + 1][y] == tile_type or map[x][y - 1] == tile_type:
        b2 = 1
    if map[x + 1][y + 1] == tile_type or map[x + 1][y] == tile_type or map[x][y + 1] == tile_type:
        b3 = 1
    if map[x - 1][y + 1] == tile_type or map[x - 1][y] == tile_type or map[x][y + 1] == tile_type:
        b4 = 1
    
    state = b1 + (b2 * 2) + (b3 * 4) + (b4 * 8)

    return state

def get_tile_state(x, y, map, tile_type):
    tile = pygame.Surface((16, 16))
    b1, b2, b3 = 0, 0, 0
    if map[x - 1][y] != tile_type: b1 = 1
    if map[x - 1][y - 1] != tile_type: b2 = 1
    if map[x][y - 1] != tile_type: b3 = 1
    tile.blit(images[0][(b1 + b2 * 2 + b3 * 4)], (0, 0))

    b1, b2, b3 = 0, 0, 0
    if map[x + 1][y] != tile_type: b1 = 1
    if map[x + 1][y - 1] != tile_type: b2 = 1
    if map[x][y - 1] != tile_type: b3 = 1
    tile.blit(images[0][(b1 + b2 * 2 + b3 * 4) + 8], (8, 0))

    b1, b2, b3 = 0, 0, 0
    if map[x + 1][y] != tile_type: b1 = 1
    if map[x + 1][y + 1] != tile_type: b2 = 1
    if map[x][y + 1] != tile_type: b3 = 1
    tile.blit(images[0][(b1 + b2 * 2 + b3 * 4) + 16], (8, 8))

    b1, b2, b3 = 0, 0, 0
    if map[x - 1][y] != tile_type: b1 = 1
    if map[x - 1][y + 1] != tile_type: b2 = 1
    if map[x][y + 1] != tile_type: b3 = 1
    tile.blit(images[0][(b1 + b2 * 2 + b3 * 4) + 24], (0, 8))

    return tile