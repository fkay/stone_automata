"""
Test calculating maps in advance and try find reverse path
"""
# %% libs
import numpy as np
from scipy import signal
from automata import load_init_map, next_step_map_convolve


def solution_test(init_map: np.array,
                  init_lifes: int = 1) -> dict:
    rows, cols = init_map.shape

    k = np.array([[0, 1, 0],
                 [1, 0, 1],
                 [0, 1, 0]], dtype=np.int8)

    # %% inital n maps
    minimum_moves = cols + rows - 2
    maps = [init_map]
    paths = [np.zeros(init_map.shape, np.int8)]

    # %% find the paths to start
    paths[0][0, 0] = init_lifes
    i = 0
    while i < 50_0000:
        if ((i + 1) % 100 == 0):
            print(f'Created {i + 1} maps')
        maps.append(next_step_map_convolve(maps[i]))
        # paths.append((signal.convolve2d(paths[i], k, mode='same') > 0))
        new_values = np.zeros((1, paths[0].shape[1]), dtype=np.int8)
        next_path = np.concatenate((new_values, paths[i], new_values), axis=0)
        new_values = np.zeros((paths[0].shape[0], 1), dtype=np.int8)
        next_path_b = np.concatenate((new_values, paths[i], new_values),
                                     axis=1)
        next_path = np.maximum(next_path[2:], next_path[:-2])
        next_path_b = np.maximum(next_path_b[:, 2:], next_path_b[:, :-2])
        paths.append(np.maximum(next_path, next_path_b))
        i += 1
        # paths[i] = (paths[i] * (~(maps[i] == 1))) * np.int8(1)
        paths[i] = paths[i] - maps[i]
        paths[i][paths[i] < 0] = 0
        if paths[i][-1, -1] > 0:
            break
        # check no solution
        # if np.sum(paths[i]) == 0:
        #     break

    # find way back
    curr_y = rows - 1
    curr_x = cols - 1
    moves = []
    for i in range(len(paths) - 2, -1, -1):
        curr_value = paths[i + 1][curr_y, curr_x] + maps[i + 1][curr_y, curr_x]
        # check up
        if curr_y > 0 and paths[i][curr_y - 1, curr_x] >= curr_value:
            curr_y -= 1
            moves.append('D')
            continue
        # check left
        if curr_x > 0 and paths[i][curr_y, curr_x - 1] >= curr_value:
            curr_x -= 1
            moves.append('R')
            continue
        # check right
        if curr_x < cols - 2 and paths[i][curr_y, curr_x + 1] >= curr_value:
            curr_x += 1
            moves.append('L')
            continue
        # check bottom
        # if paths[i][curr_y - 1, curr_x] == curr_value:
        curr_y += 1
        moves.append('U')

    moves.reverse()
    return {'moves': moves, 'maps': maps, 'paths': paths}


if __name__ == '__main__':
    # %% load the initial map
    init_map = load_init_map()
    init_map = init_map[10:40, 20:50]
    init_map[0, 0] = 0  # 3
    init_map[-1, -1] = 0  # 4

    solution = solution_test(init_map, 5)['moves']
    print(f'Solution length: {len(solution)}')
    solution = ' '.join(solution)
    print(solution)
