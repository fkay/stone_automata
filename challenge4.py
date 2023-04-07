"""
Verify correct path to solve automata
"""

# %%Import libraries
from datetime import datetime
from automata import load_init_map
from a_star import A_star
from test import solution_test


# %% load the initial map
missing_part = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 1, 1, 0, 0, 1, 0, 1, 0, 0],
                [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]
init_map = load_init_map(r'inputs/input4.txt', missing_part)

# %% Try to solve it
model = A_star(init_map, heuristics_type='manhattan',
               heuristics_const=1,
               init_lifes=1)
# particle_moves = model.solve()
# %% try solving with other method
# particle_moves = solution_test(init_map, 1)['moves']

# %% write the solution
# print(f'Solution length:  {len(particle_moves)}')
# solution = (' ').join(particle_moves)
# print(solution)
# with open(f'output3_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
#           'w') as file:
#     file.write(solution)
