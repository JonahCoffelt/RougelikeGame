import numpy as np

class Player():
    def __init__(self, posx, posy):
        self.x = posx
        self.y = posy
        self.width = .75
        self.height = .75
        self.speed = .007
        self.dir = 0
        self.width = .8
        self.equiped = 0
        self.fire_time = 0
        self.pickup_range = 4
    
    def move(self, x, y, dt, map):
        multiplier = 1
        if x and y:
            multiplier = np.sqrt(2) / 2
        projectedx = self.x + x * multiplier * dt * self.speed
        projectedy = self.y + y * multiplier * dt * self.speed

        if map[int(projectedx + self.width/2 * x)][int(self.y)] != 1:
            self.x = projectedx
        if map[int(self.x)][int(projectedy + self.width/2 * y)] != 1:
            self.y = projectedy