import pygame
from PIL import Image

images = []

def split_sheet(currentSheet, name, tile_size):

    # Get file
    filename = "Assets\SpriteSheets\{}.png".format(name)
    filepath = f"{filename}"

    for y in range(0, Image.open(filepath).size[1], tile_size):
        for x in range(0, Image.open(filepath).size[0], tile_size):

            # Creates surface with only the desired sprite/tile
            surf = pygame.Surface((tile_size, tile_size))
            surf.blit(currentSheet, (0, 0), (x, y, tile_size, tile_size))

            # Sets transparency
            surf.set_colorkey((0, 0, 0))

            images[-1].append(surf)

def process_image_sheets(sheet, name, tile_size):

    # Adds blank list for the new sheet
    images.append([])

    # Splits the given sheet into sprites/tiles
    split_sheet(sheet, name, tile_size)
    
    return images
