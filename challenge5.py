"""
Verify correct path to solve automata
"""

# %%Import libraries
from datetime import datetime
from automata import load_init_map
from a_star import A_star
from test import solution_test


# %% load the initial map
init_map = load_init_map(r'inputs/input5.txt')

# %% Try to solve it
model = A_star(init_map, heuristics_type='manhattan',
               heuristics_const=1,
               init_lifes=1)
# particle_moves = model.solve()
# %% try solving with other method
solution = solution_test(init_map,
                         init_lifes=1,
                         )

particle_moves = solution['moves']
part_pos = solution['part_pos']
old_part = [{'t': 0, 'part_pos': part_pos}]
part_moves = [{'t': 0, 'moves': particle_moves}]

print(f'First Solution length:  {len(particle_moves)}')

# try new particle every 2 t
for t in range(3, len(particle_moves), 6):
    print(f'try insert particle at {t}')
    next_sol = solution_test(init_map,
                             init_lifes=1,
                             old_particles=old_part,
                             insert_t=t)
    if next_sol is not None:
        old_part.append({'t': t, 'part_pos': next_sol['part_pos']})
        part_moves.append({'t': t, 'moves': next_sol['moves']})

# %% write the solution
moves = (' ').join(particle_moves)
print(moves)
# with open(f'output5_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
#           'w') as file:
#     file.write(moves)
# print(f'Final pos: {solution["part_pos"][-1]}')

with open(f'output5{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    for p in part_moves:
        file.write(str(p['t']) + ' ')
        file.write((' ').join(p['moves']))
        file.write('\n')

# for p in old_part:
#     print(str(p['t']))
#     print(p['part_pos'][:30])
