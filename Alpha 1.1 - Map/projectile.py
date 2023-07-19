from numba import njit
from numba import int32, float32, int8, types, typed
from numba.experimental import jitclass

#Specifications of jit class
spec = [
    ('x', float32),
    ('y', float32),
    ('dir', float32),
    ('velocity', float32),
    ('acceleration', float32),
    ('flight_time', float32),
    ('bloom', float32),
    ('quantity', float32),
]

@jitclass(spec)
class bullet2():
    def __init__(self, x, y, dir, velocity, acceleration, flight_time, bloom, quantity):
        self.x = x
        self.y = y
        self.dir = dir
        self.velocity = velocity
        self.acceleration = acceleration
        self.flight_time = flight_time
        self.bloom = bloom
        self.quantity = quantity

class bullet():
    def __init__(self, x, y, dir, attributes):
        self.x = x
        self.y = y
        self.dir = dir
        self.velocity = attributes[0]
        self.acceleration = attributes[1]
        self.flight_time = attributes[2]
        self.bloom = attributes[3]
        self.quantity = attributes[4]
    
    def update(self):
        self.x += 1
    

def update_projectiles(projectilesArray):
    for projectile in projectilesArray:
        projectile.x += 1
