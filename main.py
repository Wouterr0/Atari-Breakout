import sys
import time
import numpy as np
import pygame

import settings
import objects
import scenes


def main_game(difficulty):
	# Create blocks
	settings.total_layers = difficulty*4
	settings.blockheight = settings.WIDTH/3/settings.total_layers
	

	blocks = []
	blocktops, blockbottoms, blocklefts, blockrights = [], [], [], []
	for row in range(settings.total_layers):
		for block in range(settings.WIDTH//settings.blockwidth):
			blocks.append(objects.Block(block*settings.blockwidth, (row*settings.blockheight) + settings.TOP_MARGIN, settings.blockwidth, settings.blockheight, row, settings.total_layers))
			blocktops.append(blocks[len(blocks)-1].top)
			blockbottoms.append(blocks[len(blocks)-1].bottom)
			blocklefts.append(blocks[len(blocks)-1].left)
			blockrights.append(blocks[len(blocks)-1].right)
	begin_blockscount = len(blocks)

	# Create a paddle and ball
	paddle = objects.Paddle((settings.WIDTH/2)-(settings.PADDLE_WIDTH/2), settings.HEIGHT-50, settings.PADDLE_WIDTH, 15, settings.BLUE, pygame.image.load("images/paddle.png"))
	ball = objects.Ball(settings.WIDTH//2, settings.HEIGHT-(settings.HEIGHT/2), 5, 10, pygame.image.load("images/ball.png"), pygame.mixer.Sound("sounds/ball.wav"))

	start = time.time()

	# Main loop
	run = True
	while run:
		settings.fpsClock.tick(60)
		#time.sleep(0.3)
		settings.win.fill(settings.BLACK)
		score = int(begin_blockscount-len(blocks)-((time.time()-start)/(difficulty*10)))

		score_text = settings.normal_font.render(str(score), True, settings.WHITE)
		settings.win.blit(score_text, (settings.WIDTH-score_text.get_width()-10, settings.HEIGHT-score_text.get_height()-10))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

		# Paddle control
		if pygame.mouse.get_pos()[0] > 0+(settings.PADDLE_WIDTH/2) and pygame.mouse.get_pos()[0] < settings.WIDTH-(settings.PADDLE_WIDTH/2):
			paddle.control() 
		elif pygame.mouse.get_pos()[0] < 0+(settings.PADDLE_WIDTH/2):
			paddle.x = 0
		elif pygame.mouse.get_pos()[0] > settings.WIDTH-(settings.PADDLE_WIDTH/2):
			paddle.x = settings.WIDTH-paddle.width
		paddle.draw()

		# Block control
		if len(blocks) == 0:
			scenes.win(score)
			return
		else:
			for block in blocks:
				block.draw()

			# Ball control
			if ball.rect.collidelist(blocks) != -1:
				ball.collided_block = ball.rect.collidelist(blocks)
				if blocks[ball.collided_block].layer == 0:
					ball.speed = 5+difficulty
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
				ball.bounce_top()
				ball.alpha += np.random.normal()*np.pi/8
				if ball.rect.colliderect(paddle.leftrect):
					ball.bounce_left()
				elif ball.rect.colliderect(paddle.rightrect):
					ball.bounce_right()

			ball.update()
			if (ball.rect.y+(ball.radius*2)) >= settings.HEIGHT:
				scenes.death(score)
				return

			ball.draw()

		pygame.display.update()


while True:
	main_game(scenes.begin())
