import colorsys
import numpy as np
import pygame

import settings


def safe_div(x, y):
	'''
	This function returns the division of two numbers if one of the two is not equal to zero. Otherwise it wil return zero. It is a protection against division with zero. 
	'''
	if y == 0 or x == 0:
		return 0
	return x/y

class Block():
	def __init__(self, x, y, w, h, current_layer, total_layers):
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
		self.layer = current_layer
		self.color = colorsys.hsv_to_rgb(safe_div(1, safe_div(total_layers, self.layer)), 1, 255)

	def draw(self):
		# Draw block
		pygame.draw.rect(settings.win, self.color, self.rect)


class Paddle(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, width, height, color, image):
		self.x = xpos
		self.y = ypos
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height)
		self.rightrect = pygame.Rect(self.x+self.width/2, self.y, self.width/2, self.height)
		self.image = image
		self.color = color

	def control(self):
		# Paddle to mouse x
		self.x = pygame.mouse.get_pos()[0]-(self.width/2)

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height)
		self.rightrect = pygame.Rect(self.x+self.width/2, self.y, self.width/2, self.height)
		settings.win.blit(self.image, (self.x, self.y))


class Ball(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, speed, radius, image, sound):
		pygame.sprite.Sprite.__init__(self)
		self.x = xpos
		self.y = ypos
		self.radius = radius
		self.image = image
		self.rect = self.image.get_rect()
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.alpha = np.pi*0.5 + np.random.normal()*np.pi/8
		self.speed = speed
		self.color = settings.WHITE
		self.sound = sound
		self.collided_block = None

	def update(self):
		# Update position of Ball
		self.collide_wall()
		self.x += np.cos(self.alpha) * self.speed
		self.y += np.sin(self.alpha) * self.speed
		self.rect = pygame.Rect(int(self.x-self.radius), int(self.y-self.radius), self.radius*2, self.radius*2)

	def draw(self):
		# Draw ball object
		settings.win.blit(self.image, (self.x, self.y))

	def collide_wall(self):
		# Collide top
		if self.y <= 0:
			self.bounce_bottom()
		# Collide left
		if self.x <= 0:
			self.bounce_right()
		# Collide right
		if (self.x+(self.radius*2)) >= settings.WIDTH:
			self.bounce_left()

	def bounce_top(self):
		pygame.mixer.Sound.play(self.sound)
		if np.sin(self.alpha) > 0:
			self.alpha = np.pi*2 - self.alpha

	def bounce_bottom(self):
		pygame.mixer.Sound.play(self.sound)
		if np.sin(self.alpha) < 0:
			self.alpha = np.pi*2 - self.alpha

	def bounce_left(self):
		pygame.mixer.Sound.play(self.sound)
		if np.cos(self.alpha) > 0:
			self.alpha = np.pi - self.alpha

	def bounce_right(self):
		pygame.mixer.Sound.play(self.sound)
		if np.cos(self.alpha) < 0:
			self.alpha = np.pi - self.alpha
