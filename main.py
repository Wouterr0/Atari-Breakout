import colorsys
import os
import sys
import time
from random import randint

import pygame
from pygame import gfxdraw
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
big_font = pygame.font.SysFont('Roboto', int(WIDTH/10))
normal_font = pygame.font.SysFont('Roboto', 50)
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

BLOCKWIDTH = 75
BLOCKHEIGHT = 30
block_layers = 9

PADDLE_WIDTH = 200


def safe_div(x, y):
	if y == 0 or x == 0:
		return 0
	return x/y


def translate(num, start1, stop1, start2, stop2):
	return start2 + (stop2 - start2) * ((num - start1) / (stop1 - start1))


def begin_menu_scene():
	button = pygame.Rect(WIDTH/2-WIDTH/4, HEIGHT/2+WIDTH/16, WIDTH/2, HEIGHT/4)
	start_button_image = pygame.image.load("start.png")
	while not(pygame.mouse.get_pressed()[0] and pygame.Rect(100, 100, start_button_image.get_rect()[2], start_button_image.get_rect()[3]).collidepoint(pygame.mouse.get_pos())):
		print(pygame.Rect(100, 100, start_button_image.get_rect()
                    [2], start_button_image.get_rect()[3]))
		win.fill(DARK_GREEN)
		pygame.draw.rect(win, FUCHSIA, button)
		win.blit(start_button_image, ((WIDTH-start_button_image.get_width()) /
                                2, (HEIGHT-start_button_image.get_height())/2-100))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pygame.display.update()


def winning_scene(score):
	winning_title = big_font.render(
		"You won! Your score is " + str(score), True, WHITE)
	winning_text = normal_font.render(
		"Press space to return to home.", True, WHITE)
	while not pygame.key.get_pressed()[pygame.K_SPACE]:
		win.fill(BLACK)
		pygame.draw.rect(win, ORANGE, (WIDTH/14, HEIGHT /
                                 5, (WIDTH/14)*12, (HEIGHT/5)*3))
		win.blit(winning_title, ((WIDTH-winning_title.get_width()) /
                           2, (HEIGHT-winning_title.get_height())/2))
		win.blit(winning_text, ((WIDTH-winning_text.get_width()) /
                          2, ((HEIGHT-winning_text.get_height())/2)+100))

		if pygame.key.get_pressed()[pygame.K_KP_ENTER] or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			easter_egg_image = pygame.image.load("easter_egg.png")
			win.blit(easter_egg_image, ((WIDTH-easter_egg_image.get_width()) /
                               2, (HEIGHT-easter_egg_image.get_height())/2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pygame.display.update()


class Block():
	def __init__(self, x, y, w, h, layer):
		'''
		This object is a block and shit
		'''
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.top = pygame.Rect(self.x, self.y, self.width, 0)
		self.bottom = pygame.Rect(self.x, self.y+self.height, self.width, 0)
		self.left = pygame.Rect(self.x, self.y, 0, self.height)
		self.right = pygame.Rect(self.x+self.width, self.y, 0, self.height)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.layer = layer
		self.color = colorsys.hsv_to_rgb(
			safe_div(1, safe_div(block_layers, self.layer)), 1, 255)

	def draw(self):
		# Draw block
		pygame.draw.rect(win, self.color, self.rect)


class Paddle(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, width, height, color, image):
		self.x = xpos
		self.y = ypos
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height/2)
		self.rightrect = pygame.Rect(
			self.x+(self.width/2), self.y+(self.height/2), self.width/2, self.height/2)
		self.image = image
		self.color = color

	def control(self, key=None):
		# Paddle to mouse x
		self.x = pygame.mouse.get_pos()[0]-(self.width/2)

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height/2)
		self.rightrect = pygame.Rect(
			self.x+(self.width/2), self.y+(self.height/2), self.width/2, self.height/2)
		# pygame.draw.rect(win, (255, 255, 255), self.rect)
		win.blit(self.image, (self.x, self.y))


class Ball(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, xdir, ydir, speed, radius, image, sound):
		pygame.sprite.Sprite.__init__(self)
		self.x = xpos
		self.y = ypos
		self.radius = radius
		self.image = image
		self.rect = self.image.get_rect()
		self.xdir = xdir
		self.ydir = ydir
		self.speed = speed
		self.color = WHITE
		self.sound = sound
		self.collided_block = None

	def update(self):
		# Update position of Ball
		self.collide_wall()
		self.x += int(self.xdir * self.speed)
		self.y += int(self.ydir * self.speed)
		self.rect = pygame.Rect(self.x-self.radius, self.y -
		                        self.radius, self.radius*2, self.radius*2)

	def draw(self):
		# Draw ball object
		# pygame.gfxdraw.filled_circle(win, self.x, self.y, self.radius, self.color)
		# pygame.gfxdraw.aacircle(win, self.x, self.y, self.radius, self.color)
		win.blit(self.image, (self.x-self.radius, self.y-self.radius))

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
		pygame.mixer.Sound.play(self.sound)
		self.ydir = -1

	def bounce_bottom(self):
		pygame.mixer.Sound.play(self.sound)
		self.ydir = 1

	def bounce_left(self):
		pygame.mixer.Sound.play(self.sound)
		self.xdir = -1

	def bounce_right(self):
		pygame.mixer.Sound.play(self.sound)
		self.xdir = 1


def main_game(difficulty):
	# Create blocks
	blocks = []
	blocktops, blockbottoms, blocklefts, blockrights = [], [], [], []
	for row in range(block_layers):
		for block in range(WIDTH//BLOCKWIDTH):
			blocks.append(Block(block*BLOCKWIDTH, (row*BLOCKHEIGHT) +
                            (HEIGHT/8), BLOCKWIDTH, BLOCKHEIGHT, row))
			blocktops.append(blocks[len(blocks)-1].top)
			blockbottoms.append(blocks[len(blocks)-1].bottom)
			blocklefts.append(blocks[len(blocks)-1].left)
			blockrights.append(blocks[len(blocks)-1].right)
	begin_blockscount = len(blocks)

	# Create a paddle and ball
	paddle = Paddle((WIDTH/2)-(PADDLE_WIDTH/2), HEIGHT-50,
	                PADDLE_WIDTH, 15, BLUE, pygame.image.load("paddle.png"))
	ball = Ball(WIDTH//2, HEIGHT-(HEIGHT/8), 0, 1, 5, 10,
	            pygame.image.load("ball.png"), pygame.mixer.Sound("ball.wav"))

	start = time.time()

	# Main loop
	run = True
	while run:
		fpsClock.tick(60)
		#time.sleep(0.3)
		win.fill(BLACK)
		score = int(begin_blockscount-len(blocks))
		if not int(time.time()-start) % 10:
			score -= 1
		score_text = normal_font.render(str(score), True, WHITE)
		win.blit(score_text, (WIDTH-100, HEIGHT-20))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

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
			winning_scene(score)
			return
		else:
			for block in blocks:
				block.draw()

			# Ball control
			if ball.rect.collidelist(blocks) != -1:
				ball.collided_block = ball.rect.collidelist(blocks)
				if blocks[ball.collided_block].layer == 0:
					ball.speed = 7.5
				elif ball.speed != 5:
					ball.speed = 5 + (ball.speed-5)*0.5

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

			if pygame.sprite.collide_rect(ball, paddle):
				if ball.rect.colliderect(paddle.leftrect):
					ball.bounce_top()
					ball.bounce_left()
				elif ball.rect.colliderect(paddle.rightrect):
					ball.bounce_top()
					ball.bounce_right()

			ball.update()
			ball.draw()

		pygame.display.update()


begin_menu_scene()
main_game(0)

# os.system("cls")
sys.exit(0)
