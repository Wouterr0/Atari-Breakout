import colorsys
import sys
from random import randint
import time

import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Atari breakout!')

fpsClock = pygame.time.Clock()

WHITE	= (255, 255, 255)
BLACK	= (0,  0,  0)
RED		= (255, 0,  0)
GREEN	= (0,  255, 0)
BLUE	= (0,  0,  255)
DRK_RED	= (127, 0,  0)
DARK_GREEN	= (0,  127, 0)
DARK_BLUE	= (0,  0,  127)

BLOCKWIDTH = 50
BLOCKHEIGHT = 20
BLOCK_LAYERS = 10

PADDLE_WIDTH = 150

def safe_div(x, y):
    if y == 0 or x == 0:
        return 0
    return x/y


class Block():
	def __init__(self, x, y, w, h, l):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.layer = safe_div(1, safe_div(BLOCK_LAYERS, l))
		self.color = colorsys.hsv_to_rgb(self.layer, 1, 255)

	def draw(self):
		pygame.draw.rect(win, self.color, self.rect)


class Paddle():
	def __init__(self, x, y, w, h, c):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.color = c
	
	def control(self, key=None):
		self.x = pygame.mouse.get_pos()[0]-(self.width/2)

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.width, self.height))



# Create blocks
blocks = []
for row in range(BLOCK_LAYERS):
	for block in range(WIDTH//BLOCKWIDTH):
		blocks.append(Block(block*BLOCKWIDTH, (row*BLOCKHEIGHT)+50, BLOCKWIDTH, 20, row))

# Create a paddle
paddle = Paddle((WIDTH/2)-(PADDLE_WIDTH/2), HEIGHT-50, PADDLE_WIDTH, 15, BLUE)

run = True
while run:
	fpsClock.tick(30)
	win.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

	for block in blocks:
		block.draw()
	
	if pygame.mouse.get_pos()[0] > 0+(PADDLE_WIDTH/2) and pygame.mouse.get_pos()[0] < WIDTH-(PADDLE_WIDTH/2):
		paddle.control()
	elif pygame.mouse.get_pos()[0] < 0+(PADDLE_WIDTH/2):
		paddle.x = 0
	elif pygame.mouse.get_pos()[0] > WIDTH-(PADDLE_WIDTH/2):
		paddle.x = WIDTH-paddle.width
	paddle.draw()

	pygame.display.update()
