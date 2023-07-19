import random

class Camera():
    def __init__(self, subject, speed):
        self.subject = subject
        self.x = subject.x
        self.y = subject.y
        self.speed = speed
        self.threshold = 0.001
        self.shake = 0
        self.shake_magnitude = .08
        self.shake_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def move(self, fov, mapSize, dt):
        if self.shake > 0:
            shake_dir = self.shake_directions[random.randrange(0, 4)]
            self.x += shake_dir[0] * self.shake_magnitude * dt
            self.y += shake_dir[1] * self.shake_magnitude * dt
            self.shake -= dt
        if abs(self.subject.x - self.x) > self.threshold:
            self.x += (self.subject.x - self.x) * self.speed * dt
        if abs(self.subject.y - self.y) > self.threshold:
            self.y += (self.subject.y - self.y) * self.speed * dt
        if self.x - fov//2 < 0:
            self.x = fov//2
        if self.x + fov//2 > mapSize-1:
            self.x = mapSize - fov//2 - 1
        if self.y - fov//2 < 0:
            self.y = fov//2
        if self.y + fov//2 > mapSize-1:
            self.y = mapSize - fov//2 - 1
    
    def set_subject(self, subject):
        self.subject = subject