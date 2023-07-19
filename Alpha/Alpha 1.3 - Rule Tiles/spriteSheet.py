import pygame
from PIL import Image

#tile_size = 16
images = []

def split_sheet(currentSheet, name, tile_size):
    filename = "Assets\SpriteSheets\{}.png".format(name)
    filepath = f"{filename}"
    for y in range(0, Image.open(filepath).size[1], tile_size):
        for x in range(0, Image.open(filepath).size[0], tile_size):
            surf = pygame.Surface((tile_size, tile_size))
            surf.blit(currentSheet, (0, 0), (x, y, tile_size, tile_size))
            surf.set_colorkey((0, 0, 0))
            images[-1].append(surf)

def process_image_sheets(sheet, name, tile_size):
    images.append([])
    split_sheet(sheet, name, tile_size)
    return images
