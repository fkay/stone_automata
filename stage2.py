"""
Verify correct path to solve automata
Uses pygame to visualize results
"""

# %% Import libraries
import pygame

# %% Load the map
with open(r'./inputs/input_stone_automata.txt', encoding='utf-8') as file:
    rows = file.readlines()
init_map = []
for i, r in enumerate(rows):
    init_map.append([int(v) for v in r.split()])

cell_color = [
        (255, 255, 255),  # 0 = white
        (0, 255, 0),  # 1 - green
        (255, 0, 0),  # 2 - curr pos - red
        (0, 255, 255),  # 3 - start - yellow
        (0, 255, 255)  # 4 - end - yellow
    ]

# %% Prepare pygame
# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
width, height = 850, 650
cell_width = width / 85
cell_heigth = height / 65
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 20)

circle = {'radius': 30,
          'pos_x': width / 2,
          'pos_y': height / 2,
          'speed_x': 1,
          'speed_y': 2}


def draw_map(screen, map):
    for i_y, row in enumerate(map):
        for i_x, cell in enumerate(row):
            pygame.draw.rect(screen, (0, 0, 0),
                             (i_x * cell_width, i_y * cell_heigth,
                              cell_width, cell_heigth))
            pygame.draw.rect(screen, cell_color[cell],
                             (i_x * cell_width + 1, i_y * cell_heigth + 1,
                              cell_width - 2, cell_heigth - 2))


# %% Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # draw the map
    draw_map(screen, init_map)

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (circle['pos_x'],
                                             circle['pos_y']),
                       circle['radius'])

    # Flip the display (render)
    pygame.display.flip()

    # Update position
    circle['pos_x'] += circle['speed_x']
    circle['pos_y'] += circle['speed_y']
    if ((circle['pos_x'] > (width - circle['radius'])) |
       (circle['pos_x'] < circle['radius'])):
        circle['speed_x'] *= -1
    if ((circle['pos_y'] > (height - circle['radius'])) |
       (circle['pos_y'] < circle['radius'])):
        circle['speed_y'] *= -1

    # generate framerate
    fpsClock.tick(fps)

pygame.quit()
