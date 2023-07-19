class Camera():
    def __init__(self, subject, speed):
        self.subject = subject
        self.x = subject.x
        self.y = subject.y
        self.speed = speed
        self.threshold = 0.001

    def move(self, fov, mapSize, dt):
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