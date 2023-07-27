import pygame
import random

# Constants
GRID_SIZE = 10
BLOCK_SIZE = 30
COLORS = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
BG_COLOR = (0, 0, 0)

class Figure:
    # ... (no changes in this class)

class Tetris:
    # ... (no changes in this class)

# Initialize the game engine
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Nerb 1010! Game")

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to generate random block color
def random_color():
    return random.randint(1, len(COLORS) - 1)

# Function to draw the next three blocks
def draw_next_blocks(next_blocks):
    x = 0
    for block in next_blocks:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in block.image():
                    pygame.draw.rect(screen, COLORS[block.color],
                                     [x + BLOCK_SIZE * j + 1, size[1] - 50 + BLOCK_SIZE * i + 1,
                                      BLOCK_SIZE - 2, BLOCK_SIZE - 2])
        x += BLOCK_SIZE * 6

# ... (no changes in the other functions)

# Main game loop
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(GRID_SIZE, GRID_SIZE)
counter = 0

next_blocks = [Figure(0, 0) for _ in range(3)]

while not done:
    # ... (no changes in the event handling)

    screen.fill(BG_COLOR)

    # Draw the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, GRAY, [game.x + BLOCK_SIZE * j, game.y + BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, COLORS[game.field[i][j]],
                                 [game.x + BLOCK_SIZE * j + 1, game.y + BLOCK_SIZE * i + 1,
                                  BLOCK_SIZE - 2, BLOCK_SIZE - 2])

    # Draw the current figure
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, COLORS[game.figure.color],
                                     [game.x + BLOCK_SIZE * (j + game.figure.x) + 1,
                                      game.y + BLOCK_SIZE * (i + game.figure.y) + 1,
                                      BLOCK_SIZE - 2, BLOCK_SIZE - 2])

    # Draw the next three blocks
    draw_next_blocks(next_blocks)

    # Draw the score
    draw_text("Score: " + str(game.score), pygame.font.SysFont('Calibri', 25, True, False), WHITE, 10, 10)

    if game.state == "gameover":
        draw_text("Game Over", pygame.font.SysFont('Calibri', 65, True, False), (255, 125, 0), 20, 200)
        draw_text("Press ESC", pygame.font.SysFont('Calibri', 65, True, False), (255, 215, 0), 25, 265)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
