"""
Test calculating maps in advance and try find reverse path
"""

from automata import load_init_map, next_step_map_new, draw_map
from a_star import A_star


# %% function to calculate earlier map positions
def calc_positions(map_t_m1, map_t, cols, rows):
    for ix in range(rows):
        for iy in range(cols):
            pass


# %% load the initial map
init_map = load_init_map()

cols = len(init_map[0])
rows = len(init_map)

minimum_moves = cols + rows - 2

maps = [init_map]
for i in range(minimum_moves):
    maps.append(next_step_map_new(maps[i]))

step = 10
map[-1][rows-1][cols-1] = step
for calc_map in maps[-1::-1]:
    pass
