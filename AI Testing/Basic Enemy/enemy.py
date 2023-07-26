import numpy as np
from neuralNet import Network

rewards = {
    'move' : 1,
    'closer' : 50,
    'distance' : 20,
    'player' : 100
}

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.alive = True
        self.fitness = 0

        self.net = Network([6, 10, 4])
    
    def move(self, map, player_x, player_y):
        right, up, left, down = 0, 0, 0, 0
        if map[self.x + 1][self.y]: right = 1
        if map[self.x][self.y - 1]: up = 1
        if map[self.x - 1][self.y]: left = 1
        if map[self.x][self.y + 1]: down = 1

        inputs = np.array([(self.x - player_x)/15, (self.y - player_y)/15, right, up, left, down])
        outputs = self.net.feedforward(inputs)
        outputs = np.average(outputs, axis=1)
        descicion = np.argmax(outputs)
        
        distance = np.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
        max_distance = np.sqrt(30**2 + 30**2)

        if descicion == 0:
            if self.x < 29:
                self.x += 1
                self.fitness += rewards["move"] * (1 - (distance/max_distance))
        if descicion == 1:
            if self.y > 0:
                self.y -= 1
                self.fitness += rewards["move"] * (1 - (distance/max_distance))
        if descicion == 2:
            if self.x > 0:
                self.x -= 1
                self.fitness += rewards["move"] * (1 - (distance/max_distance))
        if descicion == 3:
            if self.y < 29:
                self.y += 1
                self.fitness += rewards["move"] * (1 - (distance/max_distance))
        
        if distance > np.sqrt((self.x - player_x)**2 + (self.y - player_y)**2):
            self.fitness += rewards["closer"]

        if player_x == self.x and player_y == self.y:
            self.fitness += rewards["player"]
    
    def get_fitness(self, player_x, player_y):
        distance = np.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
        max_distance = np.sqrt(30**2 + 30**2)

        self.fitness += (1 - (distance/max_distance)) * rewards["distance"]

        return self.fitness

        
