# import pygame
import numpy as np
from scipy import signal


# Load the map
def load_init_map(
        file_path: str = r'./inputs/input_stone_automata.txt'
        ) -> np.array:
    with open(file_path, encoding='utf-8') as file:
        rows = file.readlines()
    init_map = []
    for r in rows:
        init_map.append([int(v) for v in r.split()])
    # make start and end position always zeros
    init_map[0][0] = 0
    init_map[-1][-1] = 0
    return np.array(init_map, np.int8)


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
    # assure start and end always white (verified on maps that always on top
    # left cell and bottom right cell)
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


def next_step_map_new(old_map: np.array) -> np.array:
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
    rows, cols = old_map.shape
    new_map = np.zeros(old_map.shape)
    # assure start and end always white (verified on maps that always on top
    # left cell and bottom right cell)
    # old_map[0, 0] = 0
    old_map[rows - 1, cols - 1] = 0

    # calculate center of map
    for iy in range(1, rows-1):
        for ix in range(1, cols-1):
            adjs = (old_map[iy - 1, ix - 1] +
                    old_map[iy - 1, ix] +
                    old_map[iy - 1, ix + 1] +
                    old_map[iy, ix - 1] +
                    old_map[iy, ix + 1] +
                    old_map[iy + 1, ix - 1] +
                    old_map[iy + 1, ix] +
                    old_map[iy + 1, ix + 1])
            new_map[iy, ix] = check_living(old_map[iy, ix], adjs)

    # calculate left column
    for iy in range(1, rows-1):
        adjs = (old_map[iy - 1, 0] +
                old_map[iy - 1, 1] +
                old_map[iy, 1] +
                old_map[iy + 1, 0] +
                old_map[iy + 1, 1])
        new_map[iy, 0] = check_living(old_map[iy, 0], adjs)

    # calculate right column
    for iy in range(1, rows-1):
        adjs = (old_map[iy - 1, -2] +
                old_map[iy - 1, -1] +
                old_map[iy, -2] +
                old_map[iy + 1, -2] +
                old_map[iy + 1, -1])
        new_map[iy, -1] = check_living(old_map[iy, -1], adjs)

    # calculate top row
    for ix in range(1, cols-1):
        adjs = (old_map[0, ix - 1] +
                old_map[1, ix - 1] +
                old_map[1, ix] +
                old_map[0, ix + 1] +
                old_map[1, ix + 1])
        new_map[0, ix] = check_living(old_map[0, ix], adjs)

    # calculate bottom row
    for ix in range(1, cols-1):
        adjs = (old_map[-2, ix - 1] +
                old_map[-1, ix - 1] +
                old_map[-2, ix] +
                old_map[-2, ix + 1] +
                old_map[-1, ix + 1])
        new_map[-1, ix] = check_living(old_map[-1, ix], adjs)

    # calculate top right
    adjs = (old_map[0, -2] +
            old_map[1, -2] +
            old_map[1, -1])
    new_map[0, -1] = check_living(old_map[0, -1], adjs)

    # calculate bottom left
    adjs = (old_map[-2, 0] +
            old_map[-2, 1] +
            old_map[-1, 1])
    new_map[-1, 0] = check_living(old_map[-1, 0], adjs)

    # assure start and end colors
    old_map[0, 0] = 3
    old_map[rows - 1, cols - 1] = 4
    new_map[0, 0] = 3
    new_map[rows - 1, cols - 1] = 4
    return new_map


def next_step_map_convolve(old_map: np.array) -> np.array:
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
    rows, cols = old_map.shape
    # new_map = np.zeros(old_map.shape)
    # assure start and end always white (verified on maps that always on top
    # left cell and bottom right cell)
    # old_map[0, 0] = 0
    # old_map[rows - 1, cols - 1] = 0

    k = np.array([[1, 1, 1],
                  [1, -1.6, 1],
                  [1, 1, 1]])

    conv = signal.convolve2d(old_map, k, mode='same')
    new_map = ((conv > 1.9) & (conv < 4.1)).astype(np.int8)

    # assure start and end colors
    # old_map[0][0] = 3
    # old_map[rows - 1][cols - 1] = 4
    # new_map[0][0] = 3
    # new_map[rows - 1][cols - 1] = 4
    new_map[0][0] = 0
    new_map[rows - 1][cols - 1] = 0
    return new_map


def check_living(actual_cell: int, adjs: int) -> int:
    if actual_cell == 0:
        if (adjs > 1) & (adjs < 5):
            return 1
    else:
        if (adjs > 3) & (adjs < 6):
            return 1
    return 0


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
