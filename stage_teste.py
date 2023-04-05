"""
Verify correct path to solve automata
Uses pygame to visualize results
"""

# %% Import libraries
import pygame
import numpy as np
from datetime import datetime
from automata import load_init_map
from test import solution_test
from a_star import A_star

cell_color = [
        (255, 255, 255),  # 0 = white
        (0, 255, 0),  # 1 - green
        (255, 0, 0),  # 2 - curr pos - red
        (255, 255, 0),  # 3 - start - yellow
        (255, 255, 0),  # 4 - end - yellow
        (255, 0, 255)  # 5 - paths opened
    ]


def draw_text(screen: pygame.Surface, font: pygame.font.Font,
              color: tuple[int, int, int],
              text: str, x: int, y: int) -> None:
    img = font.render(text, True, color)
    rect = img.get_rect()
    screen.blit(img, (x - rect.width // 2,
                      y - rect.height // 2))


def draw_map(screen: pygame.Surface, map: np.array,
             path: np.array,
             cell_size: tuple[int, int],
             hero_pos: tuple[int, int]) -> None:
    """
    draw the map in a pygame surface

    Args:
        screen (pygame.Surface): surface to draw
        map (list[][] of int): 2d matriz with map to draw
        cell_size (tuple[int, int]): size of each cell (width, height)
        hero_pos (tuple[int, int]): (x, y) position to draw hero
    """
    rows, cols = map.shape
    for i_y in range(rows):
        for i_x in range(cols):
            cell = map[i_y, i_x]
            cell_path = path[i_y, i_x]
            pygame.draw.rect(screen, (0, 0, 0),
                             (i_x * cell_size[0], i_y * cell_size[1],
                              cell_size[0], cell_size[1]))
            pygame.draw.rect(screen, cell_color[cell],
                             (i_x * cell_size[0] + 1, i_y * cell_size[1] + 1,
                              cell_size[0] - 2, cell_size[1] - 2))
            if cell_path > 0:
                pygame.draw.rect(screen, cell_color[5],
                                 (i_x * cell_size[0] + 3,
                                  i_y * cell_size[1] + 3,
                                 cell_size[0] - 6, cell_size[1] - 6))
            if i_x == hero_pos[0] and i_y == hero_pos[1]:
                pygame.draw.circle(screen, cell_color[2],
                                   (i_x * cell_size[0] + cell_size[0] / 2,
                                   i_y * cell_size[1] + cell_size[1] / 2),
                                   cell_size[0] // 2 - 2)


init_map = load_init_map()
# init_map = init_map[10:30, 20:40]
# init_map[0, 0] = 3
# init_map[-1, -1] = 4

hero = {
    'x': 0,
    'y': 0,
    'step': -1
}

# %% Prepare pygame
# Pygame Configuration
pygame.init()
fps = 10
fpsClock = pygame.time.Clock()
width, height = 850, 650
cell_size = (width // init_map.shape[1],
             height // init_map.shape[0])
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 40, bold=True)
font2 = pygame.font.SysFont('Arial', 20, bold=True)

# %% Game loop
running = True
step = False
continuous = False
actual_map = init_map.copy()
# actual_map[hero["y"]][hero['x']] = 2

# Solve the path
screen.fill((255, 255, 255))
draw_text(screen, font, (0, 0, 255), 'Solving Path',
          width // 2, height // 2 - 20)
pygame.display.flip()
solver = solution_test(init_map)
hero_moves = solver['moves']
print('Path ready!!!')
print(f'Solution length:  {len(hero_moves)}')
draw_text(screen, font2, (255, 128, 0), 'Space - Single Step',
          width // 2, height // 2 + 30)
draw_text(screen, font2, (255, 128, 0), 'A - hold for continous move',
          width // 2, height // 2 + 60)
pygame.display.flip()

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

    # generate next automata
    if (step or continuous):
        if hero['step'] == -1:
            hero['step'] += 1
        elif hero['step'] < len(hero_moves):
            # clear hero position
            # actual_map[hero["y"]][hero['x']] = 0
            # generate next_map
            actual_map = solver['maps'][hero['step'] + 1]
            # get hero new position
            if hero_moves[hero['step']] == 'U':
                hero['y'] -= 1
            if hero_moves[hero['step']] == 'D':
                hero['y'] += 1
            if hero_moves[hero['step']] == 'L':
                hero['x'] -= 1
            if hero_moves[hero['step']] == 'R':
                hero['x'] += 1
            hero['step'] += 1
            # actual_map[hero["y"]][hero['x']] = 2
            # Fill the background with white
        screen.fill((255, 255, 255))
        # draw the map
        draw_map(screen, actual_map,
                 solver['paths'][hero['step']],
                 cell_size, (hero['x'], hero['y']))

        # Flip the display (render)
        pygame.display.flip()
        step = False

    # generate framerate
    fpsClock.tick(fps)

solution = (' ').join(hero_moves)
print(solution)
write_file = False
if write_file:
    with open(f'solution_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
              'w') as file:
        file.write(solution)
pygame.quit()
