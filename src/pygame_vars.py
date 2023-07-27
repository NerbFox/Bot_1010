import pygame
from Nerb_1010 import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Initialize all the variables
size = (400, 500)
game_height = 10
game_width = 10
done = False
fps = 25
game = Nerb_1010(game_height, game_width)
counter = 0
up = False
down = False
left = False
right  = False
ctrl = False
pressing_down = False
speed = 2
Bot = False
fig_options = 3

# Initialize the game engine
pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Nerb 1010! Game")