import pygame
import numpy as np
import random

particles = []

class Particle:
    def __init__(self, x, y, dir, color, type = 0, velocity = .002, turn_speed = 0, lifetime = 500, size = 15):
        self.x = x
        self.y = y
        self.dir = dir
        self.color = color
        self.type = type
        self.velocity = velocity + random.uniform(-.001, 0.001)
        self.turn_speed = random.uniform(-turn_speed, turn_speed)
        self.lifetime = lifetime
        self.life = 0
        self.size = size
        
    def update(self, dt):
        self.x += self.velocity * np.cos(self.dir) * dt
        self.y += self.velocity * np.sin(self.dir) * dt
        self.dir += self.turn_speed * dt
        self.life += dt


def make_particles(x, y, dir, dir_range, quantity, clr, type = 0, velocity = .002, turn_speed = 0, lifetime = 500, size = 15):
    for i in range(quantity):

        # Creates particle with randomly offset color value
        color_mult = random.uniform(0.5, 1.0)
        color = (int(clr[0] * color_mult), int(clr[1] * color_mult), int(clr[2] * color_mult), random.randrange(20, 255))
        particles.append(Particle(x, y, dir + random.uniform(-dir_range, dir_range), color, type, velocity, turn_speed, lifetime, size))

def update_particles(renderer, image_cache, win_size, grid_size, x, y, dt):
    for particle in particles:
        # Removes dead particles
        if particle.life > particle.lifetime:
            particles.remove(particle)
        
        # Updates particle postion and roatation
        particle.update(dt)
        
        # Sets image color and direction attributes
        image_cache.cache[particle.type].color = particle.color
        image_cache.cache[particle.type].angle = np.rad2deg(particle.dir) + 90

        # Blits particle image
        renderer.blit(image_cache.cache[particle.type], pygame.Rect((win_size[0]//2 + (particle.x - x) * grid_size, win_size[1]//2 + (particle.y - y) * grid_size, particle.size * (1 - (particle.life/particle.lifetime)), particle.size * (1 - (particle.life/particle.lifetime)))))