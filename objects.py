import colorsys
import numpy as np
import pygame

import settings as s


class Block():
	def __init__(self, xpos, ypos, width, height, current_layer, total_layers):
		'''
		Block(xpos, ypos, width, current_layer, total_layers) -> None

		This class contains a block at a position with a matching color.

		'''
		self.x = xpos
		self.y = ypos
		self.width = width
		self.height = height
		self.top = pygame.Rect(self.x, self.y, self.width, 0)
		self.bottom = pygame.Rect(self.x, self.y+self.height, self.width, 0)
		self.left = pygame.Rect(self.x, self.y, 0, self.height)
		self.right = pygame.Rect(self.x+self.width, self.y, 0, self.height)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.layer = current_layer
		self.color = colorsys.hsv_to_rgb(s.safe_div(1, s.safe_div(total_layers, self.layer)), 1, 255) # This makes the color rainbow.

	def draw(self):
		# Draw block
		pygame.draw.rect(s.win, self.color, self.rect)


class Paddle(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, width, height, *appearance):
		'''
		Paddle(xpos, ypos, width, height, color)

		'''
		self.x = xpos
		self.y = ypos
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height)
		self.rightrect = pygame.Rect(self.x+self.width/2, self.y, self.width/2, self.height)
		if type(appearance[0]) == pygame.Color or type(appearance[0]) == tuple:
			self.color = appearance[0]
		elif type(appearance[0]) == pygame.Surface:
			self.image = appearance[0]
		else:
			raise AttributeError("No or wrong appearance attribute is given. Please give a tuple for a colored Paddle or a pygame.Surface and image is displayed.")

	def control(self):
		# Paddle to mouse x
		self.x = pygame.mouse.get_pos()[0]-(self.width/2)

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.leftrect = pygame.Rect(self.x, self.y, self.width/2, self.height)
		self.rightrect = pygame.Rect(self.x+self.width/2, self.y, self.width/2, self.height)

		if hasattr(self, "color"):
			print(self.color)
			pygame.draw.rect(s.win, self.color, self.rect)
		elif hasattr(self, "image"):
			s.win.blit(self.image, (self.x, self.y))


class Ball(pygame.sprite.Sprite):
	def __init__(self, xpos, ypos, speed, radius, image, sound):
		pygame.sprite.Sprite.__init__(self)
		self.x = xpos
		self.y = ypos
		self.radius = radius
		self.image = image
		self.rect = pygame.Rect(int(self.x-self.radius), int(self.y-self.radius), int(self.x+self.radius), int(self.y+self.radius))
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.alpha = np.pi*0.5 + np.random.normal()*np.pi/8 # The angle the Ball is facing towards in radians.
		self.speed = speed
		self.color = s.WHITE
		self.sound = sound
		self.collided_block = None

	def update(self):
		'''
		Updates the state of the Ball one frame further.
		'''
		self.collide_wall()
		self.x += np.cos(self.alpha) * self.speed
		self.y += np.sin(self.alpha) * self.speed
		self.rect = pygame.Rect(int(self.x-self.radius), int(self.y-self.radius), self.radius*2, self.radius*2)

	# Draw ball object
	def draw(self):
		s.win.blit(self.image, (self.x-self.radius, self.y-self.radius))
		# pygame.draw.rect(s.win, s.LIGHT_BLUE, self.rect) # For debug purposes

	def collide_wall(self):
		'''
		Checks if it hits the wall. If so then it bounces in the right direction.
		'''
		# Collide top
		if self.y-self.radius <= 0:
			self.bounce_bottom()
		# Collide left
		if self.x-self.radius <= 0:
			self.bounce_right()
		# Collide right
		if self.x+self.radius >= s.WIDTH:
			self.bounce_left()

	def bounce_top(self):
		'''Let the Ball bounce from the bottom up to the top'''
		pygame.mixer.Sound.play(self.sound)
		if np.sin(self.alpha) > 0:
			self.alpha = np.pi*2 - self.alpha

	def bounce_bottom(self):
		'''Let the Ball bounce from the top down to the bottom.'''
		pygame.mixer.Sound.play(self.sound)
		if np.sin(self.alpha) < 0:
			self.alpha = np.pi*2 - self.alpha

	def bounce_left(self):
		'''Let the Ball bounce from the right to the left'''
		pygame.mixer.Sound.play(self.sound)
		if np.cos(self.alpha) > 0:
			self.alpha = np.pi - self.alpha

	def bounce_right(self):
		'''Let the Ball bounce from the left to the right.'''
		pygame.mixer.Sound.play(self.sound)
		if np.cos(self.alpha) < 0:
			self.alpha = np.pi - self.alpha
