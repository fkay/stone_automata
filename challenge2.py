"""
Verify correct path to solve automata
"""

# %%Import libraries
from datetime import datetime
from automata import load_init_map, next_step_map_convolve
from a_star import A_star


# %% load the initial map
init_map = load_init_map(r'inputs/input1.txt')

# %% Try to solve it
model = A_star(init_map,
               3.0)
particle_moves = model.solve()

# %% write the solution
print(f'Solution length:  {len(particle_moves)}')
solution = (' ').join(particle_moves)
print(solution)
with open(f'output1_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    file.write(solution)
