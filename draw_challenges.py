import pygame
import numpy as np
from datetime import datetime
from automata import load_init_map, next_step_map_convolve
from a_star import A_star

cell_color = [
        (255, 255, 255),  # 0 = white
        (0, 255, 0),  # 1 - green
        (255, 0, 0),  # 2 - curr pos - red
        (255, 255, 0),  # 3 - start - yellow
        (255, 255, 0)  # 4 - end - yellow
    ]

init_lifes = 1
life_color = 100 / init_lifes


def draw_text(screen: pygame.Surface, font: pygame.font.Font,
              color: tuple[int, int, int],
              text: str, x: int, y: int) -> None:
    img = font.render(text, True, color)
    rect = img.get_rect()
    screen.blit(img, (x - rect.width // 2,
                      y - rect.height // 2))


def draw_map(screen: pygame.Surface,
             map: np.array,
             paths: np.array,
             cell_rows: int,
             cell_cols: int,
             cell_size: tuple[int, int],
             heros: list,
             t: int,
             font,
             offset_x: int = 0,
             offset_y: int = 0,
             part_path: int = 34) -> None:
    """
    draw the map in a pygame surface

    Args:
        screen (pygame.Surface): surface to draw
        map (list[][] of int): 2d matriz with map to draw
        cell_size (tuple[int, int]): size of each cell (width, height)
        hero_pos (tuple[int, int]): (x, y) position to draw hero
    """
    for i_y in range(cell_rows):
        for i_x in range(cell_cols):
            cell = map[i_y + offset_y, i_x + offset_x]
            pygame.draw.rect(screen, (0, 0, 0),
                             (i_x * cell_size[0], i_y * cell_size[1],
                              cell_size[0], cell_size[1]))
            pygame.draw.rect(screen, cell_color[cell],
                             (i_x * cell_size[0] + 1, i_y * cell_size[1] + 1,
                              cell_size[0] - 2, cell_size[1] - 2))
            if (paths is not None and t >= part_path
               and t - part_path < len(paths)):
                cell_path = paths[t - part_path][i_y + offset_y,
                                                 i_x + offset_x]
                if cell_path > 0:
                    pygame.draw.rect(
                        screen,
                        (196 - (cell_path - 1) * life_color,
                         196 - (init_lifes - cell_path) * life_color,
                         255),
                        (i_x * cell_size[0] + 3,
                         i_y * cell_size[1] + 3,
                         cell_size[0] - 6, cell_size[1] - 6))
                    draw_text(
                        screen, font, (0, 0, 0),
                        str(cell_path),
                        i_x * cell_size[0] + cell_size[0] / 2,
                        i_y * cell_size[1] + cell_size[1] / 2)
    for h, hero in enumerate(heros):
        if t >= 0 and hero['t'] <= t:
            it = t - hero['t']
            if it > len(hero['pos']) - 1:
                it = len(hero['pos']) - 1
            hero_y = hero['pos'][it][0] - offset_y
            hero_x = hero['pos'][it][1] - offset_x
            if hero_x < 0 or hero_y < 0:
                continue
            pygame.draw.circle(screen, cell_color[2],
                               (hero_x * cell_size[0] + cell_size[0] / 2,
                                hero_y * cell_size[1] + cell_size[1] / 2),
                               cell_size[0] // 2 - 2)
            draw_text(screen, font, (255, 255, 255),
                      str(h + 1),
                      hero_x * cell_size[0] + cell_size[0] / 2,
                      hero_y * cell_size[1] + cell_size[1] / 2)


def draw_pixel_map(screen: pygame.Surface, map: np.array,
                   hero_pos: tuple[int, int],
                   offset_x: int = 0,
                   offset_y: int = 0,) -> None:
    """
    draw the map in a pygame surface

    Args:
        screen (pygame.Surface): surface to draw
        map (list[][] of int): 2d matriz with map to draw
        cell_size (tuple[int, int]): size of each cell (width, height)
        hero_pos (tuple[int, int]): (x, y) position to draw hero
    """
    width, height = screen.get_size()
    pixel_array = pygame.PixelArray(screen)
    for i_y in range(height):
        for i_x in range(width):
            cell = map[i_y + offset_y, i_x + offset_x]
            pixel_array[i_x, i_y] = cell_color[cell]
    # draw particle
    hero_pos_x = hero_pos[0] - offset_x
    hero_pos_y = hero_pos[1] - offset_y
    if (hero_pos_x >= 0 and
       hero_pos_x < width and
       hero_pos_y >= 0 and
       hero_pos_y < height):
        pixel_array[hero_pos_x, hero_pos_y] = cell_color[2]
    pixel_array.close()


solution_file_path = r'output5_20230412_1459.txt'
# solution_file_path = r'solution_20230330_1931.txt'
# missing_part = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#                 [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
#                 [1, 1, 1, 0, 0, 1, 0, 1, 0, 0],
#                 [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
#                 [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
#                 [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
#                 [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#                 [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
#                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]
# init_map = load_init_map(r'inputs/input4.txt', missing_part)
# init_map = load_init_map('inputs/test_patterns2.txt', missing_part)
init_map = load_init_map('inputs/input5.txt')
# init_map = init_map[10:30, 20:40]
# init_map[0, 0] = 3
# init_map[-1, -1] = 4

# load the path desired to track (saved with numpy savez)
paths = np.load('outputs/paths_34.npz')['paths']
# path = None

# %% Prepare pygame
# Pygame Configuration
pygame.init()
fps = 20
fpsClock = pygame.time.Clock()
(height, width) = (800, 800)  # init_map.shape
# cell_size = (8, 8)
cell_size = (40, 40)
cell_cols = width // cell_size[0]
cell_rows = height // cell_size[1]
if height > 900:
    height = 900
if width > 1700:
    width = 1780
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 40, bold=True)
font2 = pygame.font.SysFont('Arial', 20, bold=True)
font3 = pygame.font.SysFont('Arial', 10, bold=True)

# Solve the path
screen.fill((255, 255, 255))
draw_text(screen, font, (0, 0, 255), 'Solving Path',
          width // 2, height // 2 - 20)
pygame.display.flip()

heros = []
with open(solution_file_path, 'r') as solution_file:
    lines = solution_file.readlines()
    if len(lines) == 1:
        hero_moves = {'t': 0, 'moves': lines[0].split(' ')}
        heros.append(hero_moves)
        print((' ').join(hero_moves['moves']))
    else:
        for line in lines:
            chars = line.split(' ')
            hero_moves = {'t': int(chars[0]), 'moves': chars[1:]}
            heros.append(hero_moves)

heros_pos = []
max_sol_length = 0
for hero in heros:
    hero_pos = {'t': hero['t']}
    actual_pos = [0, 0]
    positions = [tuple(actual_pos)]
    for move in hero['moves']:
        if move.strip() == 'U':
            actual_pos[0] -= 1
        if move.strip() == 'D':
            actual_pos[0] += 1
        if move.strip() == 'L':
            actual_pos[1] -= 1
        if move.strip() == 'R':
            actual_pos[1] += 1
        positions.append(tuple(actual_pos))
    hero_pos['pos'] = positions
    if (hero['t'] + len(positions)) > max_sol_length:
        max_sol_length = hero['t'] + len(positions)
    heros_pos.append(hero_pos)

print('Path ready!!!')
sol_length = max_sol_length
print(f'Solution length:  {sol_length}')
draw_text(screen, font2, (255, 128, 0), 'Space - Single Step',
          width // 2, height // 2 + 30)
draw_text(screen, font2, (255, 128, 0), 'A - hold for continous move',
          width // 2, height // 2 + 60)
pygame.display.flip()

# %% Game loop
running = True
step = False
continuous = False
actual_map = init_map.copy()
maps = [init_map]
# actual_map[hero["y"]][hero['x']] = 2
reverse_step = False

offset_x = 0
offset_y = 0
offset_step = 10
offset_mult = 20

hero = {
    'x': 0,
    'y': 0,
    'step': -1,
    'map': 0
}

while running:
    if hero['step'] >= 0 and hero['step'] < len(heros_pos[0]['pos']):
        hero['x'] = heros_pos[0]['pos'][hero['step']][1]
        hero['y'] = heros_pos[0]['pos'][hero['step']][0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mous_x = pos[0] // cell_size[0]
            mous_y = pos[1] // cell_size[1]
            print(mous_x, mous_y)
            if actual_map[mous_y, mous_x] == 1:
                actual_map[mous_y, mous_x] = 0
            else:
                actual_map[mous_y, mous_x] = 1
            draw_map(screen, actual_map, paths,
                     cell_rows, cell_cols, cell_size,
                     heros_pos,
                     hero['step'],
                     font3,
                     offset_x, offset_y)
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step = True
            if event.key == pygame.K_a:
                continuous = True
            if event.key == pygame.K_s:
                continuous = True
            if event.key == pygame.K_d:
                continuous = False
            if event.key == pygame.K_z:
                reverse_step = True
            if event.key == pygame.K_UP:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    offset_y -= offset_step * offset_mult
                else:
                    offset_y -= offset_step
                if offset_y < 0:
                    offset_y = 0
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(
                    screen, actual_map, paths,
                    cell_rows, cell_cols, cell_size,
                    heros_pos,
                    hero['step'],
                    font3,
                    offset_x, offset_y)
                pygame.display.flip()
                pygame.display.set_caption(
                    f'Solving: step: {hero["step"]}/{sol_length}' +
                    f' | off_x: {offset_x} | off_y: {offset_y}' +
                    f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
            if event.key == pygame.K_DOWN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    offset_y += offset_step * offset_mult
                else:
                    offset_y += offset_step
                if offset_y > init_map.shape[0] - cell_rows:
                    offset_y = init_map.shape[0] - cell_rows
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(
                    screen, actual_map, paths,
                    cell_rows, cell_cols, cell_size,
                    heros_pos,
                    hero['step'],
                    font3,
                    offset_x, offset_y)
                pygame.display.flip()
                pygame.display.set_caption(
                    f'Solving: step: {hero["step"]}/{sol_length}' +
                    f' | off_x: {offset_x} | off_y: {offset_y}' +
                    f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
            if event.key == pygame.K_LEFT:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    offset_x -= offset_step * offset_mult
                else:
                    offset_x -= offset_step
                if offset_x < 0:
                    offset_x = 0
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(
                    screen, actual_map, paths,
                    cell_rows, cell_cols, cell_size,
                    heros_pos,
                    hero['step'],
                    font3,
                    offset_x, offset_y)
                pygame.display.flip()
                pygame.display.set_caption(
                    f'Solving: step: {hero["step"]}/{sol_length}' +
                    f' | off_x: {offset_x} | off_y: {offset_y}' +
                    f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
            if event.key == pygame.K_RIGHT:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    offset_x += offset_step * offset_mult
                else:
                    offset_x += offset_step
                if offset_x > init_map.shape[1] - cell_cols:
                    offset_x = init_map.shape[1] - cell_cols
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(
                    screen, actual_map, paths,
                    cell_rows, cell_cols, cell_size,
                    heros_pos,
                    hero['step'],
                    font3,
                    offset_x, offset_y)
                pygame.display.flip()
                pygame.display.set_caption(
                    f'Solving: step: {hero["step"]}/{sol_length}' +
                    f' | off_x: {offset_x} | off_y: {offset_y}' +
                    f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                continuous = False

    # generate next automata
    if (step or continuous):
        if hero['step'] == -1:
            hero['step'] += 1
        elif hero['step'] < sol_length:
            # generate next_map
            # actual_map = next_step_map_convolve(actual_map)  # .copy())
            if hero['map'] + 1 > len(maps) - 1:
                maps.append(next_step_map_convolve(maps[hero['map']]))
            hero['map'] += 1
            actual_map = maps[hero['map']]
            hero['step'] += 1
        if hero['step'] >= 0 and hero['step'] < len(heros_pos[0]['pos']):
            hero['x'] = heros_pos[0]['pos'][hero['step']][1]
            hero['y'] = heros_pos[0]['pos'][hero['step']][0]
        draw_map(
                screen, actual_map, paths,
                cell_rows, cell_cols, cell_size,
                heros_pos,
                hero['step'],
                font3,
                offset_x, offset_y)

        # Flip the display (render)
        pygame.display.flip()
        pygame.display.set_caption(
            f'Solving: step: {hero["step"]}/{sol_length}' +
            f' | off_x: {offset_x} | off_y: {offset_y}' +
            f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
        step = False

    if (reverse_step):
        if hero['step'] > 0:
            hero['step'] -= 1
            hero['map'] -= 1
            actual_map = maps[hero['map']]
        if hero['step'] >= 0 and hero['step'] < len(heros_pos[0]['pos']):
            hero['x'] = heros_pos[0]['pos'][hero['step']][1]
            hero['y'] = heros_pos[0]['pos'][hero['step']][0]
        draw_map(
                screen, actual_map, paths,
                cell_rows, cell_cols, cell_size,
                heros_pos,
                hero['step'],
                font3,
                offset_x, offset_y)

        # Flip the display (render)
        pygame.display.flip()
        pygame.display.set_caption(
            f'Solving: step: {hero["step"]}/{sol_length}' +
            f' | off_x: {offset_x} | off_y: {offset_y}' +
            f' | particle pos: (r:{hero["y"]}, c:{hero["x"]})')
        reverse_step = False

    # generate framerate
    fpsClock.tick(fps)

pygame.quit()
