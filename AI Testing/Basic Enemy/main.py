import pygame
import numpy as np
from enemy import Enemy
import random

clock = pygame.time.Clock()

winSize = (1000, 1000)
win = pygame.display.set_mode(winSize, pygame.RESIZABLE)

run = True
pygame.init()

map_size = 30
grid_size = winSize[1]/map_size
map = np.zeros(shape=(map_size + 1, map_size + 1))

player_x = 10
player_y = 2

parents = []

enemies = []
play = False
round = 0
generation = 0
mutation = .3

def create_enemies_generation_first(generation_size):
    for enemy in range(generation_size):
        enemies.append(Enemy(map_size//2, map_size//2))

def create_enemies_generation_children(generation_size):
    biases, weights = get_parameters()
    for enemy in range(generation_size):
        enemies.append(Enemy(map_size//2, map_size//2))
        enemies[-1].net.biases = [biases[0] + np.random.uniform(low=-mutation, high=mutation, size=biases[0].shape), biases[1] + np.random.uniform(low=-mutation, high=mutation, size=biases[1].shape)]
        enemies[-1].net.weights = [weights[0] + np.random.uniform(low=-mutation, high=mutation, size=weights[0].shape), weights[1] + np.random.uniform(low=-mutation, high=mutation, size=weights[1].shape)]

def move_enemies_generation():  
    for enemy in enemies:
        if enemy.alive:
            enemy.move(map, player_x, player_y)
        if map[enemy.y][enemy.x] == 1:
            enemy.alive = False

def get_fitest():
    parents.clear()
    fitness_values = np.array([])
    for enemy in enemies:
        fitness_values = np.append(fitness_values, enemy.get_fitness(player_x, player_y))

    for i in range(2):
        parents.append(enemies[np.argmax(fitness_values)])
        fitness_values[np.argmax(fitness_values)] = -1

def get_parameters():
    #for value in parents[0].net.biases:
    baises_1 = np.array((parents[0].net.biases[0] + parents[1].net.biases[0]) / 2)
    baises_2 = np.array((parents[0].net.biases[1] + parents[1].net.biases[1]) / 2)

    weights_1 = np.array((parents[0].net.weights[0] + parents[1].net.weights[0]) / 2)
    weights_2 = np.array((parents[0].net.weights[1] + parents[1].net.weights[1]) / 2)

    return [baises_1, baises_2], [weights_1, weights_2]

def draw():
    win.fill("black")
    for y in range(map_size):
        for x in range(map_size):
            if map[y][x] == 1:
                pygame.draw.rect(win, (255, 255, 255), (x * grid_size, y * grid_size, grid_size - 1, grid_size - 1))
    
    pygame.draw.rect(win, (0, 0, 255), (player_x * grid_size, player_y * grid_size, grid_size - 1, grid_size - 1))
    
    for enemy in enemies:
        pygame.draw.rect(win, (255, 0, 0), (enemy.x * grid_size, enemy.y * grid_size, grid_size - 1, grid_size - 1))
    
    pygame.display.flip()

def update():
    global round, generation, mutation, player_x, player_y
    if play and round > 25:
        generation += 1
        get_fitest()
        enemies.clear()
        player_x = random.randrange(0, map_size)
        player_y = random.randrange(0, map_size)
        create_enemies_generation_children(1000)
        round = 0 
        if generation % 10 == 0:
            if mutation >= .02:
                mutation -= .01
            else:
                mutation = .01
        print(mutation)
    if play:
        round += 1
        move_enemies_generation()
    draw()


while run:
    dt = clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        print("wall")
    if keys[pygame.K_e]:
        create_enemies_generation_first(1000)
        play = True

    if pygame.mouse.get_pressed()[0]:
        mousex, mousey = pygame.mouse.get_pos()
        map[int(mousey//grid_size)][int(mousex//grid_size)] = 1
    if pygame.mouse.get_pressed()[2]:
        mousex, mousey = pygame.mouse.get_pos()
        map[int(mousey//grid_size)][int(mousex//grid_size)] = 0

    update()