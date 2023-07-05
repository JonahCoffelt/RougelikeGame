import numpy as np

class Player():
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.speed = .01
        self.dir = 0
    
    def move(self, x, y, dt):
        multiplier = 1
        if x and y:
            multiplier = np.sqrt(2) / 2
        self.posx += x * multiplier * dt * self.speed
        self.posy += y * multiplier * dt * self.speed
