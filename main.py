import colorsys
import sys
import os
import time
from random import randint

import pygame
from pygame import gfxdraw
from pygame.locals import *

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Roboto', 200)
pygame.display.set_caption('Atari breakout!')

fpsClock = pygame.time.Clock()

# Colours
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

BLOCKWIDTH = 100
BLOCKHEIGHT = 30
TOP_MARGIN = 100
BLOCK_LAYERS = 6

PADDLE_WIDTH = 200


def safe_div(x, y):
	if y == 0 or x == 0:
		return 0
	return x/y


def winning_scene():
	winning_text = font.render('You won!!!', True, WHITE)
	pygame.draw.rect(win, ORANGE, (WIDTH/7, HEIGHT/5, (WIDTH/7)*5, (HEIGHT/5)*3))
	win.blit(winning_text, ((WIDTH-winning_text.get_width()) /
                         2, (HEIGHT-winning_text.get_height())/2))


class Block():
	def __init__(self, x, y, w, h, l):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.top = pygame.Rect(self.x, self.y, self.width, 0)
		self.bottom = pygame.Rect(self.x, self.y+self.height, self.width, 0)
		self.left = pygame.Rect(self.x, self.y, 0, self.height)
		self.right = pygame.Rect(self.x+self.width, self.y, 0, self.height)
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
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height/2)
		self.rightrect = pygame.Rect(
			self.x+(self.width/2), self.y+(self.height/2), self.width/2, self.height/2)
		self.color = c

	def control(self, key=None):
		self.x = pygame.mouse.get_pos()[0]-(self.width/2)

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height/2)
		self.rightrect = pygame.Rect(
			self.x+(self.width/2), self.y+(self.height/2), self.width/2, self.height/2)
		pygame.draw.rect(win, (255, 255, 255), self.rect)


class Ball():
	def __init__(self, x, y, xd, yd, s, r):
		self.x = x
		self.y = y
		self.radius = r
		self.rect = pygame.Rect(self.x-self.radius, self.y -
		                        self.radius, self.radius*2, self.radius*2)
		self.xdir = xd
		self.ydir = yd
		self.speed = s
		self.color = WHITE
		self.collided_block = None

	def update(self):
		self.collide_wall()
		self.x += int(self.xdir * self.speed)
		self.y += int(self.ydir * self.speed)
		self.rect = pygame.Rect(self.x-self.radius, self.y -
		                        self.radius, self.radius*2, self.radius*2)

	def collide_wall(self):
		# Collide top
		if self.rect.y <= 0:
			self.bounce_bottom()
		# Collide bottom
		if (self.rect.y+(self.radius*2)) >= HEIGHT:
			self.bounce_top()
		# Collide left
		if self.rect.x <= 0:
			self.bounce_right()
		# Collide right
		if (self.rect.x+(self.radius*2)) >= WIDTH:
			self.bounce_left()

	def bounce_top(self):
		self.ydir = -1

	def bounce_bottom(self):
		self.ydir = 1

	def bounce_left(self):
		self.xdir = -1

	def bounce_right(self):
		self.xdir = 1

	# def collide_sides(self, blocktops, blockbottoms, blocklefts, blockrights):
	# 	self.collided_top = self.rect.collidelist(blocktops)
	# 	self.collided_bottom = self.rect.collidelist(blockbottoms)
	# 	self.collided_left = self.rect.collidelist(blocklefts)
	# 	self.collided_right = self.rect.collidelist(blockrights)

	def draw(self):
		pygame.gfxdraw.filled_circle(win, self.x, self.y, self.radius, self.color)
		pygame.gfxdraw.aacircle(win, self.x, self.y, self.radius, self.color)


# Create blocks
blocks = []
blocktops, blockbottoms, blocklefts, blockrights = [], [], [], []
for row in range(BLOCK_LAYERS):
	for block in range(WIDTH//BLOCKWIDTH):
		blocks.append(Block(block*BLOCKWIDTH, (row*BLOCKHEIGHT) +
                      TOP_MARGIN, BLOCKWIDTH, BLOCKHEIGHT, row))
		blocktops.append(blocks[len(blocks)-1].top)
		blockbottoms.append(blocks[len(blocks)-1].bottom)
		blocklefts.append(blocks[len(blocks)-1].left)
		blockrights.append(blocks[len(blocks)-1].right)

# Create a paddle and ball
paddle = Paddle((WIDTH/2)-(PADDLE_WIDTH/2), HEIGHT-50, PADDLE_WIDTH, 15, BLUE)
ball = Ball(WIDTH//2, HEIGHT-350, -1, -1, 5, 10)

# Main loop
run = True
while run:
	fpsClock.tick(60)
	#time.sleep(0.3)
	win.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# Paddle control
	if pygame.mouse.get_pos()[0] > 0+(PADDLE_WIDTH/2) and pygame.mouse.get_pos()[0] < WIDTH-(PADDLE_WIDTH/2):
		paddle.control()
	elif pygame.mouse.get_pos()[0] < 0+(PADDLE_WIDTH/2):
		paddle.x = 0
	elif pygame.mouse.get_pos()[0] > WIDTH-(PADDLE_WIDTH/2):
		paddle.x = WIDTH-paddle.width
	paddle.draw()

	# Block control
	if len(blocks) == 0:
		winning_scene()
	for block in blocks:
		block.draw()

	# Ball control
	if ball.rect.collidelist(blocks) != -1:
		ball.collided_block = ball.rect.collidelist(blocks)
		if blocktops[ball.collided_block].colliderect(ball.rect):
			ball.bounce_top()
		elif blockbottoms[ball.collided_block].colliderect(ball.rect):
			ball.bounce_bottom()
		elif blocklefts[ball.collided_block].colliderect(ball.rect):
			ball.bounce_left()
		elif blockrights[ball.collided_block].colliderect(ball.rect):
			ball.bounce_right()
		del blocks[ball.collided_block]
		del blocktops[ball.collided_block]
		del blockbottoms[ball.collided_block]
		del blocklefts[ball.collided_block]
		del blockrights[ball.collided_block]

	if ball.rect.colliderect(paddle.leftrect):
		ball.bounce_top()
		ball.bounce_left()
	elif ball.rect.colliderect(paddle.rightrect):
		ball.bounce_top()
		ball.bounce_right()
	if ball.rect.colliderect(paddle.rightrect) and ball.rect.colliderect(paddle.leftrect):
		print("There is no easter egg...")
	ball.update()
	ball.draw()

	pygame.display.update()
# os.system("cls")
sys.exit(0)
