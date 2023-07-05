import random
from numba import njit

directions = {
    0 : (1, 0),
    1 : (-1, 0),
    2 : (0, 1),
    3 : (0, -1)
}

#@njit
def get_map(type, rooms, size):
    map = []

    for x in range(size):
        for y in range(size):
            map.append(1)
    
    for agent in range(3):
        carving = walk(size//2, size//2, size, 200)

        for pos in carving:
            map[pos[0] + pos[1] * size] = 0
    
    return map
    
#@njit
def walk(startx, starty, size, walk_distance):
    global directions
    x, y = startx, starty
    carving = [(x, y)]
    for step in range(walk_distance):
        dir = directions[random.randrange(0, 4)]

        x += dir[0]
        y += dir[1]

        if x < 0:
            x = 0
        elif x >= size:
            x = size - 1
        if y < 0:
            y = 0
        elif y >= size:
            y = size - 1

        carving.append((x, y))
    
    return carving
        