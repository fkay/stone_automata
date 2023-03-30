import pygame

cell_color = [
        (255, 255, 255),  # 0 = white
        (0, 255, 0),  # 1 - green
        (255, 0, 0),  # 2 - curr pos - red
        (255, 255, 0),  # 3 - start - yellow
        (255, 255, 0)  # 4 - end - yellow
    ]


# Load the map
def load_init_map():
    with open(r'./inputs/input_stone_automata.txt', encoding='utf-8') as file:
        rows = file.readlines()
    init_map = []
    for i, r in enumerate(rows):
        init_map.append([int(v) for v in r.split()])
    return init_map


def draw_map(screen: pygame.Surface, map: list,
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
    for i_y, row in enumerate(map):
        for i_x, cell in enumerate(row):
            pygame.draw.rect(screen, (0, 0, 0),
                             (i_x * cell_size[0], i_y * cell_size[1],
                              cell_size[0], cell_size[1]))
            pygame.draw.rect(screen, cell_color[cell],
                             (i_x * cell_size[0] + 1, i_y * cell_size[1] + 1,
                              cell_size[0] - 2, cell_size[1] - 2))
            if i_x == hero_pos[0] and i_y == hero_pos[1]:
                pygame.draw.circle(screen, cell_color[2],
                                   (i_x * cell_size[0] + cell_size[0] / 2,
                                   i_y * cell_size[1] + cell_size[1] / 2),
                                   cell_size[0] // 2 - 2)


def next_step_map(old_map: list) -> list:
    """
    Calculates next map based on automata rules
    - White cells turn green if they have a number of adjacent green cells
      greater than 1 and less than 5. Otherwise, they remain white.
    - Green cells remain green if they have a number of green adjacent cells
      greater than 3 and less than 6. Otherwise they become white.

    Args:
        old_map (list[][] of int): map on actual situation
    Returns:
        list[][] of int: new map after iteration
    """
    # test
    rows = len(old_map)
    columns = len(old_map[0])
    new_map = []
    # assure start and end always white
    old_map[0][0] = 0
    old_map[rows - 1][columns - 1] = 0

    for iy in range(0, rows):
        new_row = []
        for ix in range(0, columns):
            # check adjacents
            adjs = 0
            if (iy != 0):
                if (ix != 0):
                    adjs += old_map[iy - 1][ix - 1]
                adjs += old_map[iy - 1][ix]
                if (ix != (columns - 1)):
                    adjs += old_map[iy - 1][ix + 1]
            if (iy != (rows - 1)):
                if (ix != 0):
                    adjs += old_map[iy + 1][ix - 1]
                adjs += old_map[iy + 1][ix]
                if (ix != (columns - 1)):
                    adjs += old_map[iy + 1][ix + 1]
            if (ix != 0):
                adjs += old_map[iy][ix - 1]
            if (ix != columns - 1):
                adjs += old_map[iy][ix + 1]
            new_cell = 0
            if old_map[iy][ix] == 0:
                if (adjs > 1) & (adjs < 5):
                    new_cell = 1
            else:
                if (adjs > 3) & (adjs < 6):
                    new_cell = 1
            new_row.append(new_cell)
        new_map.append(new_row)
    # assure start and end colors
    old_map[0][0] = 3
    old_map[rows - 1][columns - 1] = 4
    new_map[0][0] = 3
    new_map[rows - 1][columns - 1] = 4
    return new_map


def find_postion(map: list[list[int]], value: int) -> dict:
    """
    find scpecif value on the map matrix

    Args:
        map (list[list[int]]): map organized in 2d list of int
        value (int): value being searched

    Returns:
        dict: (x, y) where value found or None cause not find
    """
    for iy, y in enumerate(map):
        for ix, x in enumerate(y):
            if x == value:
                return {'x': ix, 'y': iy}
    return None
