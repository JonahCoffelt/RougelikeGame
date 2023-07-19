import pygame
import numpy as np
import random
import math

particles = []

class Particle:
    def __init__(self, x, y, dir, color, velocity = .002, acceleration = 0, gravity = 0, turn_speed = 0):
        self.x = x
        self.y = y
        self.dir = dir
        self.color = color
        self.velocity = velocity + random.uniform(-.001, 0.001)
        self.acceleration = acceleration
        self.gravity = gravity
        self.turn_speed = turn_speed
        self.life = 0
    def update(self, dt):
        self.x += self.velocity * np.cos(self.dir) * dt
        self.y += self.velocity * np.sin(self.dir) * dt
        self.life += dt


def make_particles(x, y, dir, dir_range, quantity):
    for i in range(quantity):
        particles.append(Particle(x, y, dir + random.uniform(-dir_range, dir_range), (150, 150, 150)))

def update_particles(win_size, grid_size, x, y, dt):
    particle_surf = pygame.Surface((win_size[0], win_size[1]), pygame.SRCALPHA)
    for particle in particles:
        if particle.life > 500:
            particles.remove(particle)
        particle.update(dt)
        pygame.draw.rect(particle_surf, particle.color, (win_size[0]//2 + (particle.x - x) * grid_size, win_size[1]//2 + (particle.y - y) * grid_size, 15 * (1 - (particle.life/300)), 15 * (1 - (particle.life/300))))
    return particle_surf