import pygame
from pygame._sdl2.video import Texture, Image

class ImageCache():
    def __init__(self, renderer):
        self.renderer = renderer
        self.set_cache()

    def set_cache(self):

        # Creates template square image
        self.square_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.square_surf.fill((255, 255, 255))
        self.square_text = Texture.from_surface(self.renderer, self.square_surf)
        self.square_image = Image(self.square_text)

        # Cirlce
        self.circle_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.circle_surf, (255, 255, 255), (5, 5), 5)
        self.circle_text = Texture.from_surface(self.renderer, self.circle_surf)
        self.circle_image = Image(self.circle_text)

        # Polygon (diamond with long tail)
        self.polygon_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.polygon_surf, (255, 255, 255), ((10, 0), (5, 5), (10, 19), (15, 5)))
        self.polygon_text = Texture.from_surface(self.renderer, self.polygon_surf)
        self.polygon_image = Image(self.polygon_text)

        self.cache = [self.square_image, self.circle_image, self.polygon_image]

        # Square outline
        self.square_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.square_surf, (255, 255, 255), (0, 0, 10, 10), 2)
        self.square_text = Texture.from_surface(self.renderer, self.square_surf)
        self.square_image = Image(self.square_text)

        # Circle outline
        self.circle_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.circle_surf, (255, 255, 255), (5, 5), 5, 2)
        self.circle_text = Texture.from_surface(self.renderer, self.circle_surf)
        self.circle_image = Image(self.circle_text)

        # Polygon outline
        self.polygon_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.polygon_surf, (255, 255, 255), ((10, 0), (5, 5), (10, 19), (15, 5)), 2)
        self.polygon_text = Texture.from_surface(self.renderer, self.polygon_surf)
        self.polygon_image = Image(self.polygon_text)

        self.cache_outlines = [self.square_image, self.circle_image, self.polygon_image]

def set_image_cache(renderer):
    return ImageCache(renderer)