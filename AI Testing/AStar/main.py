import pygame
import numpy as np
from AStar import *

clock = pygame.time.Clock()

winSize = (1000, 1000)
win = pygame.display.set_mode(winSize, pygame.RESIZABLE)

run = True
pygame.init()

map_size = 30
grid_size = winSize[1]/map_size
map = np.zeros(shape=(map_size + 1, map_size + 1))
node_map = []
path = []

start_pos = (5, 5)
end_pos = (15, 15)
enemy_fov = 41

def draw():
    win.fill("black")
    for y in range(map_size):
        for x in range(map_size):
            if map[y][x] == 1:
                pygame.draw.rect(win, (255, 255, 255), (x * grid_size, y * grid_size, grid_size - 1, grid_size - 1))
        
    for path_node in path:
        pygame.draw.rect(win, (100, 255, 100), ((path_node.x + (start_pos[0] - (enemy_fov - 1)/2)) * grid_size, (path_node.y + (start_pos[1] - (enemy_fov - 1)/2)) * grid_size, grid_size - 1, grid_size - 1))

    
    pygame.draw.rect(win, (0, 255, 0), (start_pos[0] * grid_size, start_pos[1]  * grid_size, grid_size - 1, grid_size - 1))
    pygame.draw.rect(win, (255, 0, 0), (end_pos[0] * grid_size, end_pos[1]  * grid_size, grid_size - 1, grid_size - 1))
    
    pygame.display.flip()

def update():
    draw()

while run:
    dt = clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
            if event.key == pygame.K_r:
                node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
                path = pathfind(node_map, ((enemy_fov - 1)/2, (enemy_fov - 1)/2), ((enemy_fov - 1)/2 + (end_pos[0] - start_pos[0]), (enemy_fov - 1)/2 + (end_pos[1] - start_pos[1])), map_size, grid_size, enemy_fov, win, start_pos)
    
    keys = pygame.key.get_pressed()

    if pygame.mouse.get_pressed()[0]:
        mousex, mousey = pygame.mouse.get_pos()
        if (int(mousex//grid_size), int(mousey//grid_size)) == start_pos: equiped_click = 1
        elif (int(mousex//grid_size), int(mousey//grid_size)) == end_pos: equiped_click = 2
        if equiped_click == 0: 
            map[int(mousey//grid_size)][int(mousex//grid_size)] = 1
            node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
            path = pathfind(node_map, ((enemy_fov - 1)/2, (enemy_fov - 1)/2), ((enemy_fov - 1)/2 + (end_pos[0] - start_pos[0]), (enemy_fov - 1)/2 + (end_pos[1] - start_pos[1])))
        elif equiped_click == 1: 
            start_pos = (int(mousex//grid_size), int(mousey//grid_size))
            node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
            path = pathfind(node_map, ((enemy_fov - 1)/2, (enemy_fov - 1)/2), ((enemy_fov - 1)/2 + (end_pos[0] - start_pos[0]), (enemy_fov - 1)/2 + (end_pos[1] - start_pos[1])))
        elif equiped_click == 2: 
            end_pos = (int(mousex//grid_size), int(mousey//grid_size))
            start_pos = (int(mousex//grid_size), int(mousey//grid_size))
            node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
            path = pathfind(node_map, ((enemy_fov - 1)/2, (enemy_fov - 1)/2), ((enemy_fov - 1)/2 + (end_pos[0] - start_pos[0]), (enemy_fov - 1)/2 + (end_pos[1] - start_pos[1])))
    else:
        equiped_click = 0
    if pygame.mouse.get_pressed()[2]:
        mousex, mousey = pygame.mouse.get_pos()
        map[int(mousey//grid_size)][int(mousex//grid_size)] = 0
        node_map = make_node_map(map, enemy_fov, start_pos[0], start_pos[1])
        path = pathfind(node_map, ((enemy_fov - 1)/2, (enemy_fov - 1)/2), ((enemy_fov - 1)/2 + (end_pos[0] - start_pos[0]), (enemy_fov - 1)/2 + (end_pos[1] - start_pos[1])))


    update()