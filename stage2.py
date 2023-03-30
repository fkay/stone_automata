"""
Verify correct path to solve automata
Uses pygame to visualize results
"""

# %% Import libraries
import pygame
from datetime import datetime
from automata import load_init_map, next_step_map, draw_map
from a_star import A_star


def draw_text(screen: pygame.Surface, font: pygame.font.Font,
              color: tuple[int, int, int],
              text: str, x: int, y: int) -> None:
    img = font.render(text, True, color)
    rect = img.get_rect()
    screen.blit(img, (x - rect.width // 2,
                      y - rect.height // 2))


init_map = load_init_map()

hero = {
    'x': 0,
    'y': 0,
    'step': -1
}

# %% Prepare pygame
# Pygame Configuration
pygame.init()
fps = 10
fpsClock = pygame.time.Clock()
width, height = 850, 650
cell_size = (width // len(init_map[0]),
             height // len(init_map))
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 40, bold=True)
font2 = pygame.font.SysFont('Arial', 20, bold=True)

# %% Game loop
running = True
step = False
continuous = False
actual_map = init_map.copy()
# actual_map[hero["y"]][hero['x']] = 2

# Solve the path
screen.fill((255, 255, 255))
draw_text(screen, font, (0, 0, 255), 'Solving Path',
          width // 2, height // 2 - 20)
pygame.display.flip()
solver = A_star(init_map)
hero_moves = solver.solve()
print('Path ready!!!')
print(f'Solution length:  {len(hero_moves)}')
draw_text(screen, font2, (255, 128, 0), 'Space - Single Step',
          width // 2, height // 2 + 30)
draw_text(screen, font2, (255, 128, 0), 'A - hold for continous move',
          width // 2, height // 2 + 60)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step = True
            if event.key == pygame.K_a:
                continuous = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                continuous = False

    # generate next automata
    if (step or continuous):
        if hero['step'] == -1:
            hero['step'] += 1
        elif hero['step'] < len(hero_moves):
            # clear hero position
            # actual_map[hero["y"]][hero['x']] = 0
            # generate next_map
            actual_map = next_step_map(actual_map.copy())
            # get hero new position
            if hero_moves[hero['step']] == 'U':
                hero['y'] -= 1
            if hero_moves[hero['step']] == 'D':
                hero['y'] += 1
            if hero_moves[hero['step']] == 'L':
                hero['x'] -= 1
            if hero_moves[hero['step']] == 'R':
                hero['x'] += 1
            hero['step'] += 1
            # actual_map[hero["y"]][hero['x']] = 2
            # Fill the background with white
        screen.fill((255, 255, 255))
        # draw the map
        draw_map(screen, actual_map, cell_size, (hero['x'], hero['y']))

        # Flip the display (render)
        pygame.display.flip()
        step = False

    # generate framerate
    fpsClock.tick(fps)

solution = (' ').join(hero_moves)
print(solution)
with open(f'solution_{datetime.now().strftime(r"%Y%m%d_%H%M")}.txt',
          'w') as file:
    file.write(solution)
pygame.quit()
