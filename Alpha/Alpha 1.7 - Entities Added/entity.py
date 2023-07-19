import pygame
import numpy as np
import random

from projectile import *

entities = []

class Entity ():
    def __init__(self, x, y, dir, width, height, type, color, health, hostile=False, damage=0, pathfind=False):
        self.x = x
        self.y = y
        self.dir = dir
        self.width, self.height = width, height
        self.type = type
        self.color = color
        self.health = health
        self.max_health = health

        self.hostile = hostile
        self.damage = damage
        self.pathfind = pathfind
    
        self.shake = 0

    def update(self, gridSize, dt):
        if self.shake < 0:
            self.shake = 0
        if self.shake:
            self.shake -= dt
        for projectile in projectiles:
            if projectile.x > self.x and projectile.x < self.x + self.width:
                if projectile.y > self.y and projectile.y < self.y + self.height:
                    self.health -= projectile.damage
                    self.shake = 100
                    destroy_projectile(projectile, gridSize)

def update_entities(renderer, map, winSize, gridSize, cam, image_cache, dt):
    for entity in entities:
        entity.update(gridSize, dt)

        image_cache.cache[entity.type].color = entity.color
        image_cache.cache[entity.type].angle = 0
        image_cache.cache_outlines[entity.type].color = (0, 0, 0, 255)
        image_cache.cache_outlines[entity.type].angle = 0

        shake_offset = 0
        if entity.shake:
            shake_offset = gridSize * random.uniform(-0.1, 0.1)
            image_cache.cache[entity.type].angle = random.uniform(-15, 15)
            image_cache.cache_outlines[entity.type].angle = image_cache.cache[entity.type].angle

        renderer.blit(image_cache.cache[entity.type], pygame.Rect((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y) * gridSize + winSize[1]/2, gridSize * entity.width, gridSize * entity.height))
        renderer.blit(image_cache.cache_outlines[entity.type], pygame.Rect((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y) * gridSize + winSize[1]/2, gridSize * entity.width, gridSize * entity.height))

        if entity.shake:
            image_cache.cache[entity.type].color = (255, 0, 0, 255)
            image_cache.cache[entity.type].alpha = 150.0
            renderer.blit(image_cache.cache[entity.type], pygame.Rect((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y) * gridSize + winSize[1]/2, gridSize * entity.width, gridSize * entity.height))
            image_cache.cache[entity.type].alpha = 255.0

        renderer.draw_color = (255, 0, 0, 255)
        renderer.fill_rect(((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y - (entity.height * .35)) * gridSize + winSize[1]/2, gridSize * entity.width * (entity.health / entity.max_health), gridSize * .2))
        renderer.draw_color = (0, 0, 0, 255)
        renderer.draw_rect(((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y - (entity.height * .35)) * gridSize + winSize[1]/2, gridSize * entity.width, gridSize * .2))

        if entity.health <= 0:
            entities.remove(entity)

