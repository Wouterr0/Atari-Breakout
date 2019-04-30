import pygame


pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Atari breakout!')

big_font = pygame.font.SysFont('Roboto', int(WIDTH/10))
normal_font = pygame.font.SysFont('Roboto', 50)

fpsClock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
JELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
DARK_RED = (127, 0, 0)
DARK_GREEN = (0, 127, 0)
DARK_BLUE = (0, 0, 127)

blockwidth = WIDTH#75
blockheight = 40
total_layers = 6
TOP_MARGIN = WIDTH/8

PADDLE_WIDTH = 200

DIFFS = {1: "Easy", 2: "Normal", 3: "Hard"}
