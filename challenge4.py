"""
Verify correct path to solve automata
"""

# %%Import libraries
from datetime import datetime
from automata import load_init_map
from a_star import A_star
from test import solution_test


# %% load the initial map
# the missing part was resolved manually following the rule
# with more time, try like an algorithm like wave function collapse to reolve
# and checking the rules with simple compare and depth search for coninous
# blocks
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
# init_map = load_init_map('inputs/test_patterns2.txt', missing_part)

# %% Try to solve it
model = A_star(init_map, heuristics_type='manhattan',
               heuristics_const=1,
               init_lifes=1)
# particle_moves = model.solve()
# %% try solving with other method
# with init lifes = 1 dont store the pass maps
particle_moves = solution_test(init_map, 1)['moves']

# %% write the solution
print(f'Solution length:  {len(particle_moves)}')
solution = (' ').join(particle_moves)
print(solution)
with open(f'output4_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    file.write(solution)
