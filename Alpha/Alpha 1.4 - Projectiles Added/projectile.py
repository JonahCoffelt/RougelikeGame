import math

class bullet():
    def __init__(self, x, y, dir, attributes):
        self.x = x
        self.y = y
        self.dir = dir
        self.life = 0
        self.damage = attributes[0]
        self.velocity = attributes[1]
        self.acceleration = attributes[2]
        self.bloom = attributes[3]
        self.quantity = attributes[4]
        self.flight_time = attributes[5]
    
    def update(self, dt):
        self.x += self.velocity * math.cos(self.dir) * dt
        self.y -= self.velocity * math.sin(self.dir) * dt
        self.velocity += self.acceleration
        if self.velocity < 0:
            self.velocity = 0
            self.acceleration = 0
        self.life += dt
    

def update_projectiles(projectilesArray):
    for projectile in projectilesArray:
        projectile.x += 1
