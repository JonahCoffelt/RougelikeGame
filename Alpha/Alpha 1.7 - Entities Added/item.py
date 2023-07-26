import pygame
import numpy as np
import random
import math

from particle import make_particles
from itemData import *

ground_item = []

class GroundItem():
    def __init__(self, x, y, attributes):
        self.x = x
        self.y = y

        self.value = attributes[0]
        self.inv_item = attributes[1]
        self.type = attributes[2]
        self.color = attributes[3]
        self.width, self.height = attributes[4][0],attributes[4][1]
        self.seek = attributes[5]
        
        self.alive = True
        self.life = 2000

        self.animation = random.randrange(-999, 999)
        self.animation_dir = 1
    
    def update(self, subject, dt):

        self.animation += dt * self.animation_dir
        if abs(self.animation) >= 1000:
            self.animation_dir *= -1
            self.animation += dt * self.animation_dir

        if not random.randrange(0, 125):
            make_particles(self.x, self.y, 0, 6.3, 3, self.color, type = 1, velocity = .000001, turn_speed = .004, lifetime = 1500, size = 5)

        if self.x >= subject.x - subject.width * .75 and self.x <= subject.x + subject.width * .75:
            if self.y >= subject.y - subject.height * .75 and self.y <= subject.y + subject.height * .75:
                make_particles(self.x, self.y, 0, 6.3, 1, self.color, type = 0, velocity = .001, turn_speed = .001, lifetime = 500, size = 10)
                make_particles(self.x, self.y, 0, 6.3, 1, (255, 255, 255), type = 1, velocity = .00001, turn_speed = .001, lifetime = 1000, size = 10)
                make_particles(self.x, self.y, 0, 6.3, 2, self.color, type = 2, velocity = .002, turn_speed = .0005, lifetime = 500, size = 15)
                self.alive = False
        if self.seek:
            if self.life > 0:
                self.life -= dt
                self.speed = 0
            else:
                if np.sqrt((self.x - subject.x)**2 + (self.y - subject.y)**2) < subject.pickup_range:
                    self.speed += .01
                    dir = -math.atan2((self.x - subject.x), (self.y - subject.y)) - 3.1415/2
                    self.x += self.speed * np.cos(dir) * dt * .02
                    self.y += self.speed * np.sin(dir) * dt * .02
                    if not random.randrange(0, 10):
                        make_particles(self.x, self.y, dir, 0, 1, (255, 255, 255), 2, velocity=.003, turn_speed=.005, size= self.speed * 25 + 5)

def make_items(x, y, item, amount, variance, radius=.5):
    for i in range(amount + random.randrange(-variance, variance + 1)):
        ground_item.append(GroundItem(x + random.uniform(-radius, radius), y + random.uniform(-radius, radius), ground_items[item]))

def update_items(renderer, cam, player, image_cache, gridSize, winSize, dt):
    for item in ground_item:
        item.update(player, dt)
        if not item.alive:
            ground_item.remove(item)
        
        image_cache.cache[1].color = (0, 0, 0, 255)
        image_cache.cache[1].alpha = 100.0
        image_cache.cache[1].angle = 0
        renderer.blit(image_cache.cache[1], pygame.Rect((item.x - cam.x) * gridSize + winSize[0]/2, (item.y - cam.y) * gridSize + winSize[1]/2 + gridSize * .35, gridSize * item.width, gridSize * item.height/3))
        image_cache.cache[1].alpha = 255.0

        image_cache.cache[item.type].color = item.color
        image_cache.cache[item.type].angle = 0
        image_cache.cache_outlines[item.type].color = (0, 0, 0, 255)
        image_cache.cache_outlines[item.type].angle = 0

        renderer.blit(image_cache.cache[item.type], pygame.Rect((item.x - cam.x) * gridSize + winSize[0]/2, (item.y - cam.y) * gridSize + winSize[1]/2 + np.sin(1.57 * (item.animation/1000)) * gridSize * .1, gridSize * item.width, gridSize * item.height))
        renderer.blit(image_cache.cache_outlines[item.type], pygame.Rect((item.x - cam.x) * gridSize + winSize[0]/2, (item.y - cam.y) * gridSize + winSize[1]/2 + np.sin(1.57 * (item.animation/1000)) * gridSize * .1, gridSize * item.width, gridSize * item.height))
