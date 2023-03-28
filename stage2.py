"""
Verify correct path to solve automata
Uses pygame to visualize results
"""

# %% Import libraries
import pygame
from automata import load_init_map, next_step_map, draw_map
from astar import solve_Astar

init_map = load_init_map()

hero = {
    'x': 0,
    'y': 0
}

hero_moves = []

# %% Prepare pygame
# Pygame Configuration
pygame.init()
fps = 10
fpsClock = pygame.time.Clock()
width, height = 850, 650
cell_size = (width / len(init_map[0]),
             height / len(init_map))
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 20)

# %% Game loop
running = True
step = False
continuous = False
actual_map = init_map.copy()
actual_map[hero["y"]][hero['x']] = 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step = True
            if event.key == pygame.K_a:
                continuous = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                continuous = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # draw the map
    draw_map(screen, actual_map, cell_size)

    # Flip the display (render)
    pygame.display.flip()

    # generate next automata
    if step | continuous:
        # clear hero position
        actual_map[hero["y"]][hero['x']] = 0
        actual_map = next_step_map(actual_map.copy())
        if ((hero['x'] < len(actual_map[0])) &
           (actual_map[hero["y"]][hero['x'] + 1] != 1)):
            hero['x'] += 1
            hero_moves.append('R')
        elif ((hero['y'] < len(actual_map)) &
              (actual_map[hero["y"] + 1][hero['x']] != 1)):
            hero['y'] += 1
            hero_moves.append('D')
        elif ((hero['x'] > 0) &
              (actual_map[hero["y"]][hero['x'] - 1] != 1)):
            hero['x'] -= 1
            hero_moves.append('L')
        elif ((hero['y'] > 0) &
              (actual_map[hero["y"] - 1][hero['x']] != 1)):
            hero['y'] -= 1
            hero_moves.append('U')
        else:
            hero_moves.append('X')
        actual_map[hero["y"]][hero['x']] = 2
        step = False

    # generate framerate
    fpsClock.tick(fps)
print((' ').join(hero_moves))
pygame.quit()
