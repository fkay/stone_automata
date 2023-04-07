"""
Verify correct path to solve automata
Uses pygame to visualize results
"""

# %% Import libraries
import pygame
import numpy as np
from datetime import datetime
from automata import load_init_map, next_step_map_convolve
from test import solution_test
from a_star import A_star

cell_color = [
        (255, 255, 255),  # 0 = white
        (0, 255, 0),  # 1 - green
        (255, 0, 0),  # 2 - curr pos - red
        (255, 255, 0),  # 3 - start - yellow
        (255, 255, 0),  # 4 - end - yellow
        (196, 196, 255)  # 5 - paths opened
    ]

init_lifes = 1
special = 5
start_pos_x = 0
start_pos_y = 0
life_color = 100 / init_lifes
stop_before = 0

init_map = load_init_map()
init_map = init_map[10:40, 20:50]
init_map[0, 0] = 0  # 3
init_map[-1, -1] = 0  # 4

hero = {
    'x': start_pos_x,
    'y': start_pos_y,
    'step': -1,
    'map': 0
}


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
             hero_pos: tuple[int, int],
             font) -> None:
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
                pygame.draw.rect(screen,
                                 (196 - (cell_path - 1) * life_color,
                                  196 - (init_lifes - cell_path) * life_color,
                                  255),
                                 (i_x * cell_size[0] + 3,
                                  i_y * cell_size[1] + 3,
                                  cell_size[0] - 6, cell_size[1] - 6))
                draw_text(screen, font, (0, 0, 0),
                          str(cell_path),
                          i_x * cell_size[0] + cell_size[0] / 2,
                          i_y * cell_size[1] + cell_size[1] / 2)
    pygame.draw.rect(screen, cell_color[3],
                     (0 * cell_size[0] + 1, 0 * cell_size[1] + 1,
                     cell_size[0] - 2, cell_size[1] - 2))
    pygame.draw.rect(screen, cell_color[4],
                     ((cols - 1) * cell_size[0] + 1,
                     (rows - 1) * cell_size[1] + 1,
                     cell_size[0] - 2, cell_size[1] - 2))
    pygame.draw.circle(screen, cell_color[2],
                       (hero_pos[0] * cell_size[0] + cell_size[0] / 2,
                       hero_pos[1] * cell_size[1] + cell_size[1] / 2),
                       cell_size[0] / 3 - 2,
                       1)


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
font3 = pygame.font.SysFont('Arial', 10, bold=True)

# %% Game loop
actual_map = init_map.copy()
maps = [init_map]
# actual_map[hero["y"]][hero['x']] = 2

# Solve the path
screen.fill((255, 255, 255))
draw_text(screen, font, (0, 0, 255), 'Solving Path',
          width // 2, height // 2 - 20)
pygame.display.flip()
solver = solution_test(init_map, init_lifes, start_pos_x, start_pos_y,
                       stop_before, special)
hero_moves = solver['moves']
print('Path ready!!!')
print(f'Solution length:  {len(hero_moves)}')
solution = (' ').join(hero_moves)
print(solution)
draw_text(screen, font2, (255, 128, 0), 'Space - Single Step',
          width // 2, height // 2 + 30)
draw_text(screen, font2, (255, 128, 0), 'A - hold for continous move',
          width // 2, height // 2 + 60)
pygame.display.flip()

running = True
step = False
continuous = False
reverse_step = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step = True
            if event.key == pygame.K_a:
                continuous = True
            if event.key == pygame.K_z:
                reverse_step = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                continuous = False

    # generate next automata
    if (step or continuous):
        repeat_map = False
        if hero['step'] == -1:
            hero['step'] += 1
        elif hero['step'] < len(hero_moves):
            # clear hero position
            # actual_map[hero["y"]][hero['x']] = 0
            # generate next_map
            actual_map = maps[hero['map']]
            # get hero new position
            if hero_moves[hero['step']] == 'U':
                hero['y'] -= 1
            if hero_moves[hero['step']] == 'D':
                hero['y'] += 1
            if hero_moves[hero['step']] == 'L':
                hero['x'] -= 1
            if hero_moves[hero['step']] == 'R':
                hero['x'] += 1
            if hero_moves[hero['step']] == 'A':
                repeat_map = True
                hero['step'] += 1
                change_y = int(hero_moves[hero['step']])
                hero['step'] += 1
                change_x = int(hero_moves[hero['step']])
                actual_map[change_y, change_x] = 1 - actual_map[change_y,
                                                                change_x]
                print(f'changed: row: {change_y}, col: {change_x}')
            # actual_map = solver['maps'][hero['step'] + 1]
            hero['step'] += 1
            if not repeat_map:
                if hero['map'] + 1 > len(maps) - 1:
                    maps.append(next_step_map_convolve(maps[hero['map']]))
                hero['map'] += 1
            actual_map = maps[hero['map']]
            # actual_map[hero["y"]][hero['x']] = 2
            # Fill the background with white
        screen.fill((255, 255, 255))
        # draw the map
        draw_map(screen, actual_map,
                 solver['paths'][hero['map']],
                 cell_size, (hero['x'], hero['y']),
                 font3)

        # Flip the display (render)
        pygame.display.flip()
        pygame.display.set_caption(
            f'Solving: step: {hero["step"]}' +
            f' | particle pos: ({hero["x"]}, {hero["y"]})')
        step = False

    if (reverse_step):
        if hero['step'] > 1:
            # generate previous_map
            hero['step'] -= 1
            hero['map'] -= 1
            # actual_map = solver['maps'][hero['step']]
            actual_map = maps[hero['step']]
            # get hero new position
            if hero_moves[hero['step']] == 'U':
                hero['y'] += 1
            if hero_moves[hero['step']] == 'D':
                hero['y'] -= 1
            if hero_moves[hero['step']] == 'L':
                hero['x'] += 1
            if hero_moves[hero['step']] == 'R':
                hero['x'] -= 1
            else:  # must be A command
                hero['step'] -= 2  # back another 2 positions
            # actual_map[hero["y"]][hero['x']] = 2
            # Fill the background with white
        # screen.fill((255, 255, 255))
        # draw the map
        draw_map(screen, actual_map,
                 solver['paths'][hero['step']],
                 cell_size, (hero['x'], hero['y']),
                 font3)

        # Flip the display (render)
        pygame.display.flip()
        reverse_step = False

    # generate framerate
    fpsClock.tick(fps)

write_file = False
if write_file:
    with open(f'solution_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
              'w') as file:
        file.write(solution)
pygame.quit()
