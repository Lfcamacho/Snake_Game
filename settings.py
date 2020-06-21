import pygame

SNAKE_SIZE = 12
ROWS, COLUMNS = 25, 40
WIDTH, HEIGHT = SNAKE_SIZE * COLUMNS, 440
GAME_POS_X, GAME_POS_Y = SNAKE_SIZE, 80
GAME_WIDTH, GAME_HEIGHT = WIDTH - 2 * GAME_POS_X, SNAKE_SIZE * ROWS

HS_FILE = "highscore.txt"

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (230,230,230)
GREEN = (79,205,177)
RED = (255,0,0)
PURPLE = (128,0,128)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font("fonts/ka1.ttf", 40)
SCORE_FONT = pygame.font.Font("fonts/FakeHope.ttf", 35)
GAME_FONT = pygame.font.Font("fonts/game_over.ttf", 80)
GAME_FONT_2 = pygame.font.Font("fonts/game_over.ttf", 30)
GAME_FONT_3 = pygame.font.Font("fonts/game_over.ttf", 50)