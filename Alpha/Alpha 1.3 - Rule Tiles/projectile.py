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
