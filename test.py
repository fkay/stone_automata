"""
Test calculating maps in advance and try find reverse path
"""
# %% libs
import numpy as np
from scipy import signal
from automata import load_init_map, next_step_map_convolve


# %% load the initial map
init_map = load_init_map()
init_map = init_map[10:30, 20:40]
init_map[0, 0] = 3
init_map[-1, -1] = 4


def solution_test(init_map: np.array) -> list:
    rows, cols = init_map.shape

    k = np.array([[0, 1, 0],
                 [1, 0, 1],
                 [0, 1, 0]], dtype=np.int8)

    # %% inital n maps
    minimum_moves = cols + rows - 2
    maps = [init_map]
    paths = [np.zeros(init_map.shape)]

    # %% find the paths to start
    paths[0][0, 0] = 1
    i = 0
    while i < 50_0000:
        maps.append(next_step_map_convolve(maps[i]))
        paths.append(signal.convolve2d(paths[i], k, mode='same'))
        i += 1
        paths[i] = (paths[i] > 0) * (i + 1) * (~(maps[i] == 1))
        if paths[i][-1, -1] > 0:
            break

    # find way back
    curr_y = rows - 1
    curr_x = cols - 1
    curr_value = paths[-1][curr_y, curr_x]
    moves = []
    for i in range(len(paths) - 2, -1, -1):
        curr_value -= 1
        # check up
        if curr_y > 0 and paths[i][curr_y - 1, curr_x] == curr_value:
            curr_y -= 1
            moves.append('D')
            continue
        # check left
        if curr_x > 0 and paths[i][curr_y, curr_x - 1] == curr_value:
            curr_x -= 1
            moves.append('R')
            continue
        # check right
        if curr_x < cols - 2 and paths[i][curr_y, curr_x + 1] == curr_value:
            curr_x += 1
            moves.append('L')
            continue
        # check bottom
        # if paths[i][curr_y - 1, curr_x] == curr_value:
        curr_y += 1
        moves.append('U')

    moves.reverse()
    return {'moves': moves, 'maps': maps, 'paths': paths}


solution = solution_test(init_map)['moves']
solution = ' '.join(solution)
print(solution)
