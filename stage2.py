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


def draw_map(screen: pygame.Surface, map: list) -> None:
    for i_y, row in enumerate(map):
        for i_x, cell in enumerate(row):
            pygame.draw.rect(screen, (0, 0, 0),
                             (i_x * cell_width, i_y * cell_heigth,
                              cell_width, cell_heigth))
            pygame.draw.rect(screen, cell_color[cell],
                             (i_x * cell_width + 1, i_y * cell_heigth + 1,
                              cell_width - 2, cell_heigth - 2))


def next_step_map(old_map: list, rows: int, columns: int) -> list:
    """
    Calculates next map based on automata rules
    - White cells turn green if they have a number of adjacent green cells
      greater than 1 and less than 5. Otherwise, they remain white.
    - Green cells remain green if they have a number of green adjacent cells
      greater than 3 and less than 6. Otherwise they become white.

    Args:
        old_map (list[][] of int): map on actual situation
        rows (int): how many rows are in the matrix
        columns (int): how many columns in the matrix
    Returns:
        list[][] of int: new map after iteration
    """
    new_map = []
    # check corners
    c00 = old_map[1][0] + old_map[1][1] + old_map[0][1]
    c01 = (old_map[1][columns - 1] +
           old_map[1][columns - 2] +
           old_map[0][columns - 2])
    c10 = (old_map[rows - 2][0] +
           old_map[rows - 2][1] +
           old_map[rows - 1][1])
    c11 = (old_map[rows - 2][columns - 1] +
           old_map[rows - 2][columns - 2] +
           old_map[rows - 1][columns - 2])

    for iy in range(1, len(old_map) - 1):
        new_row = (old_map[rows - 2][columns - 1] +
                   old_map[rows - 2][columns - 2] +
                   old_map[rows - 1][columns - 2])
        for ix in range(1, len(old_map[0]) - 1):
            # check adjacents
            pass


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

    # Flip the display (render)
    pygame.display.flip()

    # generate framerate
    fpsClock.tick(fps)

pygame.quit()
