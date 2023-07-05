from numba import njit

class bullet():
    def __init__(self, attributes):
        self.posx = attributes[0]
        self.posy = attributes[1]
        self.dir = attributes[2]
        self.velocity = attributes[3]
        self.acceleration = attributes[4]
        self.flight_time = attributes[5]
        self.bloom = attributes[6]
        self.quantity = attributes[7]