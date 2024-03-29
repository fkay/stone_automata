"""
Verify correct path to solve automata
"""

# %%Import libraries
from datetime import datetime
from automata import load_init_map
from test import solution_test
from a_star import A_star


# %% load the initial map
init_map = load_init_map(r'inputs/input1.txt')

# %% Try to solve it
model = A_star(init_map,
               3.0)
# particle_moves = model.solve()

# %% try solving with other method
particle_moves = solution_test(init_map)['moves']

# %% write the solution
print(f'Solution length:  {len(particle_moves)}')
solution = (' ').join(particle_moves)
print(solution)
with open(f'output1_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    file.write(solution)
