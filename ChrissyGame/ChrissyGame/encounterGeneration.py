import random
from numba import njit

#directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

@njit
def get_map(type, rooms, size):
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    map = []

    for x in range(size):
        for y in range(size):
            map.append(1)
    
    startx, starty = 20, 20
    for room in range(rooms):
        #create room carving
        for agent in range(5):
            carving = walk(startx, starty, size, 250, directions, map)

            for pos in carving:
                map[pos[0] + pos[1] * size] = room + 2
        
        #find edge
        dir = random.randrange(1, 3)
        if dir == 1:
            curpos = map[starty * size]
            startx = size - 1
        else:
            curpos = map[startx]
            starty = size - 1
        dir = directions[dir]
        while curpos == 1:
            startx += dir[0]
            starty += dir[1]
            if startx < 0:
                startx = 0
            elif startx >= size:
                startx = size - 1
            if starty < 0:
                starty = 0
            elif starty >= size:
                starty = size - 1
            curpos = map[startx + starty * size]
        if room < rooms-1:
            for i in range(random.randrange(6, 12)):
                map[startx + starty * size] = 0
                startx -= dir[0]
                starty -= dir[1]
                if startx < 0:
                    startx = 0
                elif startx >= size:
                    startx = size - 1
                if starty < 0:
                    starty = 0
                elif starty >= size:
                    starty = size - 1
    
    return map

@njit
def walk(startx, starty, size, walk_distance, directions, map):
    x, y = startx, starty
    carving = [(x, y)]
    for step in range(walk_distance):
        dir = directions[random.randrange(0, 4)]

        color = map[x + y * size]

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

        if not check_surroundings(color, x, y, map, size):
            x -= dir[0]
            y -= dir[1]

        carving.append((x, y))
    
    return carving

@njit
def check_surroundings(color, posx, posy, map, size):
    alone = True
    #print(posx, posy)
    if posx > 0:
        if map[(posx - 1) + (posy) * size] != color and map[(posx - 1) + (posy) * size] != 1:
            alone = False
    if posx < size - 1:
        if map[(posx + 1) + (posy) * size] != color and map[(posx + 1) + (posy) * size] != 1:
            alone = False
    if posy < size - 1:
        if map[(posx) + (posy + 1) * size] != color and map[(posx) + (posy + 1) * size] != 1:
            alone = False
    if posy > 0:
        if map[(posx) + (posy - 1) * size] != color and map[(posx) + (posy - 1) * size] != 1:
            alone = False
    if posx < size - 1:
        if posy < size - 1:
            if map[(posx + 1) + (posy + 1) * size] != color and map [(posx + 1) + (posy + 1) * size] != 1:
                alone = False
        if posy > 0:
            if map[(posx + 1) + (posy - 1) * size] != color and map[(posx + 1) + (posy - 1) * size] != 1:
                alone = False
    if posx > 0:
        if posy < size - 1:
            if map[(posx - 1) + (posy + 1) * size] != color and map[(posx - 1) + (posy + 1) * size] != 1:
                alone = False
        if posy > 0:
            if map[(posx - 1) + (posy - 1) * size] != color and map[(posx - 1) + (posy - 1) * size] != 1:
                alone = False
    return alone
