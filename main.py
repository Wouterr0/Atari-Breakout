import colorsys
import sys
from random import randint
import time

import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 750, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Atari breakout!')

fpsClock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0,  0,  0)
RED = (255, 0,  0)
GREEN = (0,  255, 0)
BLUE = (0,  0,  255)

BLOCKWIDTH = 50
BLOCKHEIGHT = 20

DEEPNESS = 30


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
		self.deepness = safe_div(1, safe_div(DEEPNESS, l))
		self.color = colorsys.hsv_to_rgb(self.deepness, 1, 255)

	def draw(self):
		pygame.draw.rect(win, self.color, self.rect)


blocks = []

win.fill(RED)

for row in range(DEEPNESS):
	for block in range((WIDTH//BLOCKWIDTH)+1):
		blocks.append(Block(block*BLOCKWIDTH, (row*BLOCKHEIGHT)+50, BLOCKWIDTH, 20, row))

run = True
while run:
	fpsClock.tick(30)
	win.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

	for block in blocks:
		block.draw()

	pygame.display.update()
