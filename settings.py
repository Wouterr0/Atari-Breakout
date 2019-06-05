import pygame
import sys
import os
from PIL import Image, ImageEnhance

os.system("cls")

# PyGame settings
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Screen settings
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Atari breakout!')

big_font = pygame.font.SysFont('Roboto', int(WIDTH/10))
normal_font = pygame.font.SysFont('Roboto', 50)

fpsClock = pygame.time.Clock()

def check_closed():
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
def safe_div(x, y):
	'''
	This function returns the division of two numbers if one of the two is not equal to zero. Otherwise it wil return zero. It is a protection against a zero division. 
	'''
	if y == 0:
		return 0
	return x/y


def surface_to_PIL(surface):
	raw_str = pygame.image.tostring(surface, "RGBA", False)
	image = Image.frombytes("RGBA", surface.get_size(), raw_str)
	return image


def PIL_to_surface(image):
	raw_str = image.tobytes("raw", "RGBA")
	surface = pygame.image.fromstring(raw_str, image.size, "RGBA")
	return surface


def brightness(image, brightness):
	return ImageEnhance.Brightness(image).enhance(brightness)

# Path settings
path = os.path.dirname(__file__)
res_path = os.path.join(path, "resources")
img_path = os.path.join(res_path, "images")
sound_path = os.path.join(res_path, "audio")


# Resouces settings
start_button_image = pygame.image.load(os.path.join(img_path, "start.png"))
start_button_hover_image = pygame.image.load(os.path.join(img_path, "start_hover.png"))

ball_image = pygame.image.load(os.path.join(img_path, "ball.png"))
paddle_image = pygame.image.load(os.path.join(img_path, "paddle.png"))

easterEgg_image_path = os.path.join(img_path, "easter_egg.png")
easterEgg_image = pygame.image.load(easterEgg_image_path)
easterEgg_image_fliped_PIL = Image.open(easterEgg_image_path).transpose(Image.FLIP_LEFT_RIGHT)

easterEgg_image_fliped = PIL_to_surface(easterEgg_image_fliped_PIL)

bounce_sound = pygame.mixer.Sound(os.path.join(sound_path, "ball.wav"))


# Colors
WHITE = (255, 255, 255, 255)
GREY = (127, 127, 127, 255)
BLACK = (0, 0, 0, 255)
FUCHSIA = (255, 0, 255, 255)
RED = (255, 0, 0, 255)
ORANGE = (255, 127, 0, 255)
JELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
AQUA = (0, 255, 255, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
DARK_RED = (127, 0, 0, 255)
DARK_GREEN = (0, 127, 0, 255)
DARK_BLUE = (0, 0, 127, 255)
LIGHT_RED = (255, 127, 127, 255)
LIGHT_GREEN = (127, 255, 127, 255)
LIGHT_BLUE = (127, 127, 255, 255)


# Block settings
blockwidth = WIDTH # 75
blockheight = 40
total_layers = 1 #6
TOP_MARGIN = WIDTH/6


# Paddle settings
PADDLE_WIDTH = 200


# Ball settings
BALL_SPEED = 5


# Scene settings
DIFFS = {1: "Easy", 2: "Normal", 3: "Hard"}

