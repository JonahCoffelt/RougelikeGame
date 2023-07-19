import pygame
from PIL import Image

tile_size = 16

images = []

#GroundSheet = pygame.image.load(r'Assets\SpriteSheets\plains.png')

def findBox(x, y, pixelMap):
    x1, y1 = x, y
    while pixelMap[x1, y1] != (0, 255, 0, 255): #find green
        x1 += 1
    while pixelMap[x1, y1] != (0, 0, 255, 255): #find blue
        y1 += 1
    return(x1, y1)

def SplitSheet(currentSheet, name):
    filename = "Assets\SpriteSheets\{}.png".format(name)
    filepath = f"{filename}"
    for y in range(0, Image.open(filepath).size[1], tile_size):
        for x in range(0, Image.open(filepath).size[0], tile_size):
            surf = pygame.Surface((tile_size, tile_size))
            surf.blit(currentSheet, (0, 0), (x, y, tile_size, tile_size))
            surf.set_colorkey((0, 0, 0))
            images[-1].append(surf)

def processImageSheets(sheet, name):
    images.append([])
    SplitSheet(sheet, name)
    return images
