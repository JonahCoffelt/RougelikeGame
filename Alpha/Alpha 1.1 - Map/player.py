import numpy as np

class Player():
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.speed = .007
        self.dir = 0
        self.width = .8
    
    def move(self, x, y, dt, map):
        multiplier = 1
        if x and y:
            multiplier = np.sqrt(2) / 2
        projectedx = self.posx + x * multiplier * dt * self.speed
        projectedy = self.posy + y * multiplier * dt * self.speed

        if map[int(projectedx + self.width/2 * x)][int(self.posy)] != 1:
            self.posx = projectedx
        if map[int(self.posx)][int(projectedy + self.width/2 * y)] != 1:
            self.posy = projectedy