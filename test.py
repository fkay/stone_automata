"""
Test calculating maps in advance and try find reverse path
"""
# %% libs
import numpy as np
import gc
# from scipy import signal
from copy import deepcopy
from automata import load_init_map, next_step_map_convolve


def solution_test(init_map: np.array,
                  init_lifes: int = 1,
                  start_pos_x: int = 0,
                  start_pos_y: int = 0,
                  stop_distance: int = 0,
                  special: int = 0,
                  save_maps: bool = False,
                  old_particles: list = [],
                  insert_t = 0) -> dict:
    rows, cols = init_map.shape

    # init_solution = init_solution_3(init_map, special)
    # init_moves = init_solution['moves']
    # init_map = init_solution['result_map']
    # start_pos_x = init_solution['pos_x']
    # start_pos_y = init_solution['pos_y']
    # print(f'End initial phase, stopped at: row={start_pos_y}, ' +
    #       f'col={start_pos_x}')

    # check if a old particle prevents the inti
    for p in old_particles:
        t = insert_t - p['t']
        if t < len(p['part_pos']):
            p_pos = p['part_pos'][t]
            if p_pos[0] == 0 and p_pos[1] == 0:
                return None

    # need keep maps to check where it kills lifes
    maps = [init_map]
    if init_lifes <= 1:
        next_map = init_map
    paths = [np.zeros(init_map.shape, np.int8)]

    # %% find the paths to start
    paths[0][start_pos_y, start_pos_x] = init_lifes

    stop_y = rows - 1
    stop_x = cols - 1

    i = 0
    maps_block = 100
    j = 0
    while i < 50_0000:
        if ((i + 1) % maps_block == 0):
            print(f'Created {i + 1} maps')
            # check no solution
            if np.sum(paths[i]) == 0:
                return None
        if (i % maps_block == 0):  # have 101 maps
            if False:  # save_maps:
                np.savez(f'outputs/maps{i}.npz', maps[:maps_block])
                j += maps_block
                maps = [maps[maps_block]]
                gc.collect()
        if init_lifes > 1:
            maps.append(next_step_map_convolve(maps[i - j]))
        else:
            next_map = next_step_map_convolve(next_map)
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
        if init_lifes > 1:
            paths[i] = paths[i] - maps[i - j]
        else:
            paths[i] = paths[i] - next_map
            # check particles and clear path
            for p in old_particles:
                if i + insert_t - p['t'] < len(p['part_pos']):
                    p_old_pos = p['part_pos'][i + insert_t - p['t']]
                    paths[i][p_old_pos[0], p_old_pos[1]] = 0
        paths[i][paths[i] < 0] = 0
        if paths[i][-1, -1] > 0:
            break
        if stop_distance > 0:
            # check if any cell on the diagonal with the distance is > 0
            ix = cols - 1
            iy = rows - 1 - stop_distance
            found_stop = False
            while iy < rows:
                if paths[i][iy, ix] > 0:
                    stop_x = ix
                    stop_y = iy
                    found_stop = True
                    break  # break while
                ix -= 1
                iy += 1
            if found_stop:
                break  # break for

    # find way back
    curr_y = stop_y
    curr_x = stop_x
    moves = []
    part_positions = np.zeros((len(paths), 2), dtype=np.int32)

    for i in range(len(paths) - 2, -1, -1):
        part_positions[i + 1] = curr_y, curr_x
        # if saved must reload maps butt only if checking lifes
        if init_lifes > 1:
            curr_value = (paths[i + 1][curr_y, curr_x] +
                          maps[i + 1 - j][curr_y, curr_x])
        else:
            curr_value = paths[i + 1][curr_y, curr_x]
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

    part_positions[0] = start_pos_y, start_pos_x
    moves.reverse()
    # moves = init_moves + moves

    # if with special try shorting the end
    print(f'Solution length: {len(moves)}')
    if special > 0:
        if stop_distance > 0:
            print('Complete path with special')
            final_moves = complete_solution_3(
                maps[-1],
                part_positions[-1][1],
                part_positions[-1][0],
                special
                )
            best_back = 0
            print('Complete with specials')
            final_len = (len(moves) +
                         len(final_moves['part_pos']))
            moves = moves + final_moves['moves']
        else:
            print('try solve final with special')
            final_moves = {'part_pos': np.zeros(1)}
            best_save_pos = 0
            for back_steps in range(special, (special * 10
                                              if special * 10 < len(maps)
                                              else len(maps) - 1)):
                final = complete_solution_3(
                    maps[-back_steps - 1],
                    part_positions[-back_steps - 1][1],
                    part_positions[-back_steps - 1][0],
                    special
                    )
                if (final['pos_x'] != cols - 1 or
                   final['pos_y'] != rows - 1):
                    continue
                save_pos = back_steps - final['part_pos'].shape[0]
                if save_pos > best_save_pos:
                    final_moves = deepcopy(final)     # save last conquered
                    best_back = back_steps
                    best_save_pos = save_pos

            print(f'With {best_back} final moves')

            final_len = (len(moves) - best_back - 1 +
                         len(final_moves['part_pos']))
            moves = moves[:(-best_back)] + final_moves['moves']
        print(f'Final solution length: {final_len}')

        part_positions = np.concatenate([part_positions[:(-best_back - 1)],
                                        final_moves['part_pos']],
                                        axis=0)

    return {'moves': moves, 'maps': maps, 'paths': paths,
            'stop_x': stop_x, 'stop_y': stop_y,
            'part_pos': part_positions}


# use power on end phase (problem is to define when to start)
def complete_solution_3(actual_map: np.array,
                        start_pos_x: int = 0,
                        start_pos_y: int = 0,
                        special: int = 5) -> dict:
    final_moves = []
    part_positions = np.zeros((1, 2), dtype=np.int32)
    first_r = True  # try first go to the right
    next_map = actual_map
    rows, cols = next_map.shape
    pos_x = start_pos_x
    pos_y = start_pos_y
    part_positions[0] = pos_y, pos_x
    while special > 0 and (pos_x < cols - 1 or pos_y < rows - 1):
        # check last movement
        if (cols - 1 - pos_x) + (rows - 1 - pos_y) == 1:
            if pos_x == cols - 1:
                # lest D
                final_moves.append('D')
                pos_y += 1
            elif pos_y == rows - 1:
                # last R
                final_moves.append('R')
                pos_x += 1
            next_map = next_step_map_convolve(next_map)
            part_positions = np.append(part_positions, [[pos_y, pos_x]],
                                       axis=0)
            break
        sx = pos_x - 1
        sy = pos_y - 1
        ex = pos_x + 3
        ey = pos_y + 3
        if sx < 0:
            sx = 0
        if sy < 0:
            sy = 0
        if ex > cols:
            ex = cols
        if ey > rows:
            ey = rows
        if pos_x == cols - 1:
            if first_r:
                first_r = False
                continue
            cell_r = 5
        else:
            cell_r = next_map[pos_y, pos_x + 1]
        if pos_y == rows - 1:
            if not first_r:
                first_r = True
                continue
            cell_d = 5
        else:
            cell_d = next_map[pos_y + 1, pos_x]
        if pos_y >= rows - 2:
            adjs_r = np.sum(next_map[sy:ey, pos_x:ex]) - cell_r
        else:
            adjs_r = np.sum(next_map[sy:ey - 1, pos_x:ex]) - cell_r
        if pos_x >= cols - 2:
            adjs_d = np.sum(next_map[pos_y:ey, sx:ex]) - cell_d
        else:
            adjs_d = np.sum(next_map[pos_y:ey, sx:ex - 1]) - cell_d
        if first_r:
            if ((cell_r == 0 and (adjs_r <= 1 or adjs_r >= 5)) or
               (cell_r == 1 and (adjs_r <= 3 or adjs_r >= 6))):
                final_moves.append('R')
                pos_x += 1
                first_r = False
            elif ((cell_d == 0 and (adjs_d <= 1 or adjs_d >= 5)) or
                  (cell_d == 1 and (adjs_d <= 3 or adjs_d >= 6))):
                final_moves.append('D')
                pos_y += 1
            else:
                first_r = False
                if ((cell_r == 0 and (adjs_r == 2 or adjs_r == 3)) or
                   (cell_r == 1 and adjs_r == 5)):
                    pos_x += 1
                    # change next position state
                    final_moves.append('A')
                    final_moves.append(str(pos_y))
                    final_moves.append(str(pos_x))
                    special -= 1
                    final_moves.append('R')
                    # invert the cell
                    next_map[pos_y, pos_x] = 1 - next_map[pos_y, pos_x]
                else:  # must find a 0 or 1 to change the state
                    # there is a special condition top with 4 adjs ones, and 0
                    # in the desired pos, there is no way to put another 1
                    # x 0 1
                    # 1 1 1
                    # then must change 2 cells
                    if (pos_y == (rows - 1) and cell_r == 0 and adjs_r == 4):
                        if special < 2:
                            break
                        final_moves.append('A')
                        final_moves.append(str(pos_y - 1))
                        final_moves.append(str(pos_x))
                        next_map[pos_y - 1,
                                 pos_x] = 1 - next_map[pos_y - 1, pos_x]
                        final_moves.append('A')
                        final_moves.append(str(pos_y))
                        final_moves.append(str(pos_x + 1))
                        next_map[pos_y,
                                 pos_x + 1] = 1 - next_map[pos_y,
                                                           pos_x + 1]
                        special -= 2
                    else:
                        y, x = find_adj2(cell_r, next_map[sy:pos_y + 2,
                                                          pos_x:pos_x + 3],
                                         from_left=True)
                        # change next position state
                        final_moves.append('A')
                        final_moves.append(str(sy + y))
                        final_moves.append(str(pos_x + x))
                        # invert the cell
                        next_map[sy + y,
                                 pos_x + x] = 1 - next_map[sy + y,
                                                           pos_x + x]
                        special -= 1
                    final_moves.append('R')
                    pos_x += 1
        else:  # same analysis prioritizing down movement
            if ((cell_d == 0 and (adjs_d <= 1 or adjs_d >= 5)) or
               (cell_d == 1 and (adjs_d <= 3 or adjs_d >= 6))):
                final_moves.append('D')
                pos_y += 1
                first_r = True
            elif ((cell_r == 0 and (adjs_r <= 1 or adjs_r >= 5)) or
                  (cell_r == 1 and (adjs_r <= 3 or adjs_r >= 6))):
                final_moves.append('R')
                pos_x += 1
            else:
                first_r = True
                if ((cell_d == 0 and (adjs_d == 2 or adjs_d == 3)) or
                   (cell_d == 1 and adjs_d == 5)):
                    pos_y += 1
                    # change next position state
                    final_moves.append('A')
                    final_moves.append(str(pos_y))
                    final_moves.append(str(pos_x))
                    special -= 1
                    final_moves.append('D')
                    # invert the cell
                    next_map[pos_y, pos_x] = 1 - next_map[pos_y, pos_x]
                else:  # must find a 0 or 1 to change the state
                    # there is a special condition top with 4 adjs ones, and 0
                    # in the desired pos, there is no way to put another 1
                    # x 1
                    # 0 1
                    # 1 1
                    # then must change 2 cells
                    if (pos_x == (cols - 1) and cell_d == 0 and adjs_d == 4):
                        if special < 2:
                            break
                        final_moves.append('A')
                        final_moves.append(str(pos_y))
                        final_moves.append(str(pos_x - 1))
                        next_map[pos_y,
                                 pos_x - 1] = 1 - next_map[pos_y, pos_x - 1]
                        final_moves.append('A')
                        final_moves.append(str(pos_y + 1))
                        final_moves.append(str(pos_x))
                        next_map[pos_y + 1,
                                 pos_x] = 1 - next_map[pos_y + 1,
                                                       pos_x]
                        special -= 2
                    else:
                        y, x = find_adj2(cell_d, next_map[pos_y:pos_y + 3,
                                                          sx:pos_x + 2],
                                         from_left=False)
                        # change next position state
                        final_moves.append('A')
                        final_moves.append(str(pos_y + y))
                        final_moves.append(str(sx + x))
                        # invert the cell
                        next_map[pos_y + y,
                                 sx + x] = 1 - next_map[pos_y + y,
                                                        sx + x]
                        special -= 1
                    final_moves.append('D')
                    pos_y += 1
        next_map = next_step_map_convolve(next_map)
        part_positions = np.append(part_positions, [[pos_y, pos_x]], axis=0)

    return {'moves': final_moves, 'result_map': next_map,
            'pos_x': pos_x, 'pos_y': pos_y,
            'special_left': special,
            'part_pos': part_positions}


# use power to start phase (problem if stops on a difficult spot)
def init_solution_3(init_map: np.array,
                    special: int = 5) -> dict:
    if special == 0:
        return {'moves': [], 'result_map': init_map,
                'pos_x': 0, 'pos_y': 0}
    init_moves = []
    first_r = True  # try first go to the right
    next_map = init_map
    pos_x = 0
    pos_y = 0
    while special > 0:
        sx = pos_x - 1
        sy = pos_y - 1
        if sx < 0:
            sx = 0
        if sy < 0:
            sy = 0
        cell_r = next_map[pos_y, pos_x + 1]
        cell_d = next_map[pos_y + 1, pos_x]
        adjs_r = np.sum(next_map[sy:pos_y + 2, pos_x:pos_x + 3]) - cell_r
        adjs_d = np.sum(next_map[pos_y:pos_y + 3, sx:pos_x + 2]) - cell_d
        if first_r:
            if ((cell_r == 0 and (adjs_r <= 1 or adjs_r >= 5)) or
               (cell_r == 1 and (adjs_r <= 3 or adjs_r >= 6))):
                init_moves.append('R')
                pos_x += 1
                first_r = False
            elif ((cell_d == 0 and (adjs_d <= 1 or adjs_d >= 5)) or
                  (cell_d == 1 and (adjs_d <= 3 or adjs_d >= 6))):
                init_moves.append('D')
                pos_y += 1
            else:
                first_r = False
                if ((cell_r == 0 and (adjs_r == 2 or adjs_r == 3)) or
                   (cell_r == 1 and adjs_r == 5)):
                    pos_x += 1
                    # change next position state
                    init_moves.append('A')
                    init_moves.append(str(pos_y))
                    init_moves.append(str(pos_x))
                    special -= 1
                    init_moves.append('R')
                    # invert the cell
                    next_map[pos_y, pos_x] = 1 - next_map[pos_y, pos_x]
                else:  # must find a 0 or 1 to change the state
                    # there is a special condition top with 4 adjs ones, and 0
                    # in the desired pos, there is no way to put another 1
                    # x 0 1
                    # 1 1 1
                    # then must change 2 cells
                    if (pos_y == 0 and cell_r == 0 and adjs_r == 4):
                        if special < 2:
                            break
                        init_moves.append('A')
                        init_moves.append(str(pos_y + 1))
                        init_moves.append(str(pos_x))
                        next_map[pos_y + 1,
                                 pos_x] = 1 - next_map[pos_y + 1, pos_x]
                        init_moves.append('A')
                        init_moves.append(str(pos_y))
                        init_moves.append(str(pos_x + 1))
                        next_map[pos_y,
                                 pos_x + 1] = 1 - next_map[pos_y,
                                                           pos_x + 1]
                        special -= 2
                    else:
                        y, x = find_adj(cell_r, next_map[sy:pos_y + 2,
                                                         pos_x:pos_x + 3])
                        # change next position state
                        init_moves.append('A')
                        init_moves.append(str(pos_y + y))
                        init_moves.append(str(pos_x + x))
                        # invert the cell
                        next_map[pos_y + y,
                                 pos_x + x] = 1 - next_map[pos_y + y,
                                                           pos_x + x]
                        special -= 1
                    init_moves.append('R')
                    pos_x += 1
        else:  # same analysis prioritizing down movement
            if ((cell_d == 0 and (adjs_d <= 1 or adjs_d >= 5)) or
               (cell_d == 1 and (adjs_d <= 3 or adjs_d >= 6))):
                init_moves.append('D')
                pos_y += 1
                first_r = True
            elif ((cell_r == 0 and (adjs_r <= 1 or adjs_r >= 5)) or
                  (cell_r == 1 and (adjs_r <= 3 or adjs_r >= 6))):
                init_moves.append('R')
                pos_x += 1
            else:
                first_r = True
                if ((cell_d == 0 and (adjs_d == 2 or adjs_d == 3)) or
                   (cell_d == 1 and adjs_d == 5)):
                    pos_y += 1
                    # change next position state
                    init_moves.append('A')
                    init_moves.append(str(pos_y))
                    init_moves.append(str(pos_x))
                    special -= 1
                    init_moves.append('D')
                    # invert the cell
                    next_map[pos_y, pos_x] = 1 - next_map[pos_y, pos_x]
                else:  # must find a 0 or 1 to change the state
                    # there is a special condition top with 4 adjs ones, and 0
                    # in the desired pos, there is no way to put another 1
                    # x 1
                    # 0 1
                    # 1 1
                    # then must change 2 cells
                    if (pos_x == 0 and cell_d == 0 and adjs_d == 4):
                        if special < 2:
                            break
                        init_moves.append('A')
                        init_moves.append(str(pos_y))
                        init_moves.append(str(pos_x + 1))
                        next_map[pos_y,
                                 pos_x + 1] = 1 - next_map[pos_y, pos_x + 1]
                        init_moves.append('A')
                        init_moves.append(str(pos_y + 1))
                        init_moves.append(str(pos_x))
                        next_map[pos_y + 1,
                                 pos_x] = 1 - next_map[pos_y + 1,
                                                       pos_x]
                        special -= 2
                    else:
                        y, x = find_adj(cell_d, next_map[pos_y:pos_y + 3,
                                                         sx:pos_x + 2])
                        # change next position state
                        init_moves.append('A')
                        init_moves.append(str(pos_y + y))
                        init_moves.append(str(pos_x + x))
                        # invert the cell
                        next_map[pos_y + y,
                                 pos_x + x] = 1 - next_map[pos_y + y,
                                                           pos_x + x]
                        special -= 1
                    init_moves.append('D')
                    pos_y += 1
        next_map = next_step_map_convolve(next_map)

    return {'moves': init_moves, 'result_map': next_map,
            'pos_x': pos_x, 'pos_y': pos_y}


# need fizing
def find_adj(value: int, adjs: np.array, from_lef: bool) -> tuple[int, int]:
    h, w = adjs.shape
    if h == 2:  # top cell
        for y, x in [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]:
            if adjs[y, x] == value:
                return (y, x)
    if w == 2:  # left cell
        for y, x in [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)]:
            if adjs[y, x] == value:
                return (y, x)
    for y, x in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2),
                 (2, 0), (2, 1), (2, 2)]:
        if adjs[y, x] == value:
            return (y, x)


def find_adj2(value: int, adjs: np.array, from_left: bool) -> tuple[int, int]:
    h, w = adjs.shape
    if h == 2:  # bottom cell
        for y, x in [(0, 0), (0, 1), (0, 2), (1, 2)]:
            if adjs[y, x] == value:
                return (y, x)
    if w == 2:  # right cell
        for y, x in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            if adjs[y, x] == value:
                return (y, x)
    if from_left:
        for y, x in [(0, 0), (0, 1), (0, 2), (1, 2),
                     (2, 0), (2, 1), (2, 2)]:
            if adjs[y, x] == value:
                return (y, x)
    else:
        for y, x in [(0, 0), (0, 2), (1, 0), (1, 2),
                     (2, 0), (2, 1), (2, 2)]:
            if adjs[y, x] == value:
                return (y, x)


if __name__ == '__main__':
    # %% load the initial map
    init_map = load_init_map()
    init_map = init_map[10:40, 20:50]
    init_map[0, 0] = 0  # 3
    init_map[-1, -1] = 0  # 4

    # solution = solution_test(init_map, 1, stop_distance=2)['moves']
    # solution = solution_test(init_map, 1, stop_distance=10, special=10)
    solution = solution_test(init_map, 1)
    solution_moves = solution['moves']
    solution_maps = solution['maps']
    solution_pos = solution['part_pos']
    # print(f'Solution length: {len(solution_moves)}')
    print(' '.join(solution_moves))
    print(solution_pos)

    # print('try solve final with special')
    # special = 5
    # # back_steps = special  # go back at least double the movements
    # final_moves = {'part_pos': np.zeros(1)}
    # for back_steps in range(special, len(solution_maps)):
    #     final = complete_solution_3(
    #         solution_maps[-back_steps - 1],
    #         solution_pos[-back_steps - 1][1],
    #         solution_pos[-back_steps - 1][0],
    #         special
    #         )
    #     if (final['pos_x'] != init_map.shape[1] - 1 or
    #        final['pos_y'] != init_map.shape[0] - 1):
    #         continue
    #     if final['part_pos'].shape[0] > final_moves['part_pos'].shape[0]:
    #         final_moves = deepcopy(final)     # save last conquered
    #         best_back = back_steps

    # print(' '.join(solution_moves))

    # print(f'With {best_back} final moves')
    # print(' '.join(final_moves['moves']))
    # print(f'Final pos = {final_moves["pos_x"]}, {final_moves["pos_y"]}')

    # final_solution = solution_moves[:(-best_back)] + final_moves['moves']
    # final_len = (len(solution_moves) - best_back + 1 +
    #              len(final_moves['part_pos']))
    # print(f'Final solution length: {final_len}')
    # print(' '.join(final_solution))

    # print(solution_pos)
    # print(final_moves['part_pos'])

# %%
