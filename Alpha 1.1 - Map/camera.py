class Camera():
    def __init__(self, posx, posy, speed):
        self.x = posx
        self.y = posy
        self.speed = speed
        self.threshold = 0.001

    def move(self, playerx, playery, fov, mapSize, dt):
        if abs(playerx - self.x) > self.threshold:
            self.x += (playerx - self.x) * self.speed * dt
        if abs(playery - self.y) > self.threshold:
            self.y += (playery - self.y) * self.speed * dt
        if self.x - fov//2 < 0:
            self.x = fov//2
        if self.x + fov//2 > mapSize-1:
            self.x = mapSize - fov//2 - 1
        if self.y - fov//2 < 0:
            self.y = fov//2
        if self.y + fov//2 > mapSize-1:
            self.y = mapSize - fov//2 - 1