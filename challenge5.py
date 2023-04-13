"""
Verify correct path to solve automata
"""

# %%Import libraries
import numpy as np
from datetime import datetime
from automata import load_init_map
from a_star import A_star
from test import solution_test


# %% load the initial map
init_map = load_init_map(r'inputs/input5.txt')

# %% Try to solve it
model = A_star(init_map, heuristics_type='manhattan',
               heuristics_const=3,
               init_lifes=1)
solution = model.solve()
# try solving with other method
# with test method always gets the shortest path, but the particles tend
# to stall at the beginning preventing new particles to enter
# perhaps A* will be better
# top result with test: 159
# with A star takes half day and found 295 particles with constant heuristics 3
# solution = solution_test(init_map,
#                          init_lifes=1,
#                          )

particle_moves = solution['moves']
part_pos = solution['part_pos']
old_part = [{'t': 0, 'part_pos': part_pos}]
part_moves = [{'t': 0, 'moves': particle_moves}]

print(f'First Solution length:  {len(particle_moves)}')
max_len_permitted = len(particle_moves)

# try new particle every t
for t in range(1, max_len_permitted):
    # other particle could reache the end first
    if t >= max_len_permitted:
        break
    print(f'try insert particle at {t}')
    # next_sol = solution_test(init_map,
    #                          init_lifes=1,
    #                          old_particles=old_part,
    #                          insert_t=t)
    model.heuristics_const = 3 + t / 100    # as time pass, search faster
    next_sol = model.solve(insert_t=t, old_part=old_part)
    if next_sol is not None:
        if t + len(next_sol['moves']) < max_len_permitted:
            max_len_permitted = t + len(next_sol['moves'])
        old_part.append({'t': t, 'part_pos': next_sol['part_pos']})
        part_moves.append({'t': t, 'moves': next_sol['moves']})
        # if t == 34:
        #     np.savez(f'outputs/paths_{t}.npz', paths=next_sol['paths'])

# %% write the solution
moves = (' ').join(particle_moves)
print(moves)
# with open(f'output5_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
#           'w') as file:
#     file.write(moves)
# print(f'Final pos: {solution["part_pos"][-1]}')

with open(f'output5_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    for p in part_moves:
        file.write(str(p['t']) + ' ')
        file.write((' ').join(p['moves']))
        file.write('\n')

# for p in old_part:
#     print(str(p['t']))
#     print(p['part_pos'][:30])
