import pygame
import random

from projectile import *
from AStar import *
from item import make_items

import pygame

entities = []
coins = []

class Entity ():
    def __init__(self, x, y, dir, attributes):
        self.x = x
        self.y = y
        self.dir = dir
        self.width, self.height = attributes[0][0], attributes[0][1]
        self.type = attributes[1]
        self.health = attributes[2]
        self.max_health = self.health
        self.damage = attributes[3]
        self.speed = attributes[4]
        self.color = attributes[5]
        self.drops = attributes[6]
        self.pathfind = attributes[7]
        self.hostile = attributes[8]

        self.fov = 21
        self.shake = 0

    def update(self, map, gridSize, subject, renderer, cam, dt):
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
        
        if self.pathfind:
            #print(int(self.x), int(self.y))
            node_map = make_node_map(map, self.fov, int(self.x), int(self.y))
            path = pathfind(node_map, ((self.fov - 1)/2, (self.fov - 1)/2), ((self.fov - 1)/2 + (int(subject.x) - int(self.x)), (self.fov - 1)/2 + (int(subject.y) - int(self.y))))
            
            for node in path:
                renderer.draw_color = (100, 255, 100, 255)
                print(node.x + (self.fov - 1)/2, node.y + (self.fov - 1)/2)
                renderer.fill_rect((((node.x + (self.fov - 1)/2) - cam.x) * gridSize + 1500/2, ((node.y + (self.fov - 1)/2) - cam.y) * gridSize + 1000/2, gridSize, gridSize))

            #if len(path) > 1:
                #print(path[-2].x + (self.fov - 1)/2, path[-1].y + (self.fov - 1)/2)
                #self.x -= (self.x - path[-2].x + (self.fov - 1)/2) * dt * .0005
                #self.y -= (self.y - path[-1].y + (self.fov - 1)/2) * dt * .0005



def update_entities(renderer, map, winSize, gridSize, cam, player, image_cache, dt):
    for entity in entities:
        entity.update(map, gridSize, player, renderer, cam, dt)

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
        renderer.fill_rect(((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y - (entity.height * .35)) * gridSize + winSize[1]/2, gridSize * entity.width * (entity.health / entity.max_health), gridSize * .1))
        renderer.draw_color = (0, 0, 0, 255)
        renderer.draw_rect(((entity.x - cam.x) * gridSize + winSize[0]/2 + shake_offset, (entity.y - cam.y - (entity.height * .35)) * gridSize + winSize[1]/2, gridSize * entity.width, gridSize * .1))

        if entity.health <= 0:
            for item in entity.drops:
                make_items(entity.x, entity.y, item[0], item[1][0], item[1][1])
            entities.remove(entity)

