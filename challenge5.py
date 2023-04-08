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

# %% write the solution
print(f'Solution length:  {len(particle_moves)}')
moves = (' ').join(particle_moves)
print(moves)
with open(f'output5_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    file.write(moves)
print(f'Final pos: {solution["part_pos"][-1]}')
