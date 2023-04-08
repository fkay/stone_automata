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


def draw_text(screen: pygame.Surface, font: pygame.font.Font,
              color: tuple[int, int, int],
              text: str, x: int, y: int) -> None:
    img = font.render(text, True, color)
    rect = img.get_rect()
    screen.blit(img, (x - rect.width // 2,
                      y - rect.height // 2))


def draw_map(screen: pygame.Surface,
             map: np.array,
             cell_rows: int,
             cell_cols: int,
             cell_size: tuple[int, int],
             hero_pos: tuple[int, int],
             offset_x: int = 0,
             offset_y: int = 0) -> None:
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
            if (i_x + offset_x == hero_pos[0] and
               i_y + offset_y == hero_pos[1]):
                pygame.draw.circle(screen, cell_color[2],
                                   (i_x * cell_size[0] + cell_size[0] / 2,
                                   i_y * cell_size[1] + cell_size[1] / 2),
                                   cell_size[0] // 2 - 2)


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


solution_file_path = r'output5_20230407_2033.txt'
# solution_file_path = r'solution_20230330_1931.txt'
# init_map = load_init_map('inputs/test_patterns.txt')
init_map = load_init_map('inputs/input5.txt')
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

with open(solution_file_path, 'r') as solution_file:
    hero_moves = solution_file.readline().split(' ')

print((' ').join(hero_moves))

print('Path ready!!!')
sol_length = len(hero_moves)
print(f'Solution length:  {sol_length}')
draw_text(screen, font2, (255, 128, 0), 'Space - Single Step',
          width // 2, height // 2 + 30)
draw_text(screen, font2, (255, 128, 0), 'A - hold for continous move',
          width // 2, height // 2 + 60)
pygame.display.flip()

offset_x = 0
offset_y = 0
offset_step = 5

while running:
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
            draw_map(screen, actual_map,
                     cell_rows, cell_cols, cell_size,
                     (hero['x'], hero['y']),
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
            if event.key == pygame.K_UP:
                offset_y -= offset_step
                if offset_y < 0:
                    offset_y = 0
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(screen, actual_map,
                         cell_rows, cell_cols, cell_size,
                         (hero['x'], hero['y']),
                         offset_x, offset_y)
                pygame.display.flip()
            if event.key == pygame.K_DOWN:
                offset_y += offset_step
                if offset_y > init_map.shape[0] - cell_rows:
                    offset_y = init_map.shape[0] - cell_rows
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(screen, actual_map,
                         cell_rows, cell_cols, cell_size,
                         (hero['x'], hero['y']),
                         offset_x, offset_y)
                pygame.display.flip()
            if event.key == pygame.K_LEFT:
                offset_x -= offset_step
                if offset_x < 0:
                    offset_x = 0
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(screen, actual_map,
                         cell_rows, cell_cols, cell_size,
                         (hero['x'], hero['y']),
                         offset_x, offset_y)
                pygame.display.flip()
            if event.key == pygame.K_RIGHT:
                offset_x += offset_step
                if offset_x > init_map.shape[1] - cell_cols:
                    offset_x = init_map.shape[1] - cell_cols
                # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
                #                offset_x, offset_y)
                draw_map(screen, actual_map,
                         cell_rows, cell_cols, cell_size,
                         (hero['x'], hero['y']),
                         offset_x, offset_y)
                pygame.display.flip()
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
            actual_map = next_step_map_convolve(actual_map)  # .copy())
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
        # screen.fill((255, 255, 255))
        # draw the map
        # draw_pixel_map(screen, actual_map, (hero['x'], hero['y']),
        #                offset_x, offset_y)
        draw_map(screen, actual_map,
                 cell_rows, cell_cols, cell_size,
                 (hero['x'], hero['y']),
                 offset_x, offset_y)

        # Flip the display (render)
        pygame.display.flip()
        pygame.display.set_caption(
            f'Solving: step: {hero["step"]}/{sol_length}' +
            f' | off_x: {offset_x} | off_y: {offset_y}' +
            f' | particle pos: ({hero["x"]}, {hero["y"]})')
        step = False

    # generate framerate
    fpsClock.tick(fps)

pygame.quit()
