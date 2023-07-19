import pygame
import numpy as np
from particles import make_particles

projectiles = []

class bullet():
    def __init__(self, x, y, dir, attributes):
        self.x = x
        self.y = y
        self.dir = dir
        self.life = 0

        # Attributes listed in weapons.py
        self.damage = attributes[0]
        self.velocity = attributes[1]
        self.acceleration = attributes[2]
        self.bloom = attributes[3]
        self.quantity = attributes[4]
        self.flight_time = attributes[5]
        self.size = attributes[9]
        self.particle_info = attributes[10]
        self.trail_info = attributes[11]
        self.type = attributes[12]
        self.color = attributes[13]
    
    def update(self, dt):
        self.x += self.velocity * np.cos(self.dir) * dt
        self.y -= self.velocity * np.sin(self.dir) * dt
        self.velocity += self.acceleration * dt
        if self.velocity < 0:
            self.velocity = 0
            self.acceleration = 0
        self.life += dt
    

def update_projectiles(renderer, map, winSize, gridSize, cam, image_cache, dt):
    global projectiles
    for projectile in projectiles:
        # Moves parojectile
        projectile.update(dt)

        # Sets color and direction attributes of projectile images
        image_cache.cache[projectile.type].color = projectile.color
        image_cache.cache[projectile.type].angle = np.rad2deg(-projectile.dir) + 90
        image_cache.cache_outlines[projectile.type].color = (0, 0, 0)
        image_cache.cache_outlines[projectile.type].angle = np.rad2deg(-projectile.dir) + 90
        
        # Blits projectile image and outline
        renderer.blit(image_cache.cache[projectile.type], pygame.Rect((projectile.x - cam.x) * gridSize + winSize[0]/2, (projectile.y - cam.y) * gridSize + winSize[1]/2, gridSize * projectile.size, gridSize * projectile.size))
        renderer.blit(image_cache.cache_outlines[projectile.type], pygame.Rect((projectile.x - cam.x) * gridSize + winSize[0]/2, (projectile.y - cam.y) * gridSize + winSize[1]/2, gridSize * projectile.size, gridSize * projectile.size))

        # Creates trail particles, if any
        for particle_type in range(len(projectile.trail_info)):
            trail_info = projectile.trail_info[particle_type]
            make_particles(projectile.x, projectile.y, -projectile.dir - 3.1415, 0, trail_info[1], trail_info[2], type=trail_info[0], turn_speed=trail_info[3], lifetime=trail_info[4], size=gridSize * trail_info[5])

        # Removes projectile if lifetime is reached
        if projectile.life > projectile.flight_time:
            projectiles.remove(projectile)
        
        # Removes projectile if it hit an object
        if map[int(projectile.x)][int(projectile.y)] == 1:
            # Creates collision particles
            for particle_type in range(len(projectile.particle_info)):
                particle_info = projectile.particle_info[particle_type]
                make_particles(projectile.x, projectile.y, -projectile.dir - 3.1415, 1, particle_info[1], particle_info[2], type=particle_info[0], turn_speed=particle_info[3], lifetime=particle_info[4], size=gridSize * particle_info[5])
           
            projectiles.remove(projectile)
