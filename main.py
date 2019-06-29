import time
import numpy as np
import pygame

import settings as s
import objects
import scenes


def main_game(difficulty):
	'''
	This method contains the main game. You should give it one parameter; the difficulty, as a number counting from 1 up to and including 3. 

	'''
	# Create blocks
	s.total_layers = difficulty*4
	s.blockheight = s.HEIGHT/4/s.total_layers

	blocks = []
	blocktops, blockbottoms, blocklefts, blockrights = [], [], [], []
	for row in range(s.total_layers):
		for block in range(s.WIDTH//s.blockwidth):
			blocks.append(objects.Block(block*s.blockwidth, (row*s.blockheight) + s.TOP_MARGIN, s.blockwidth, s.blockheight, row, s.total_layers))
			blocktops.append(blocks[len(blocks)-1].top)
			blockbottoms.append(blocks[len(blocks)-1].bottom)
			blocklefts.append(blocks[len(blocks)-1].left)
			blockrights.append(blocks[len(blocks)-1].right)
	begin_blockscount = len(blocks)

	# Create a paddle and ball
	paddle = objects.Paddle((s.WIDTH/2)-(s.PADDLE_WIDTH/2), s.HEIGHT-50, s.PADDLE_WIDTH, 15, s.paddle_image)
	ball = objects.Ball(30, 30, s.BALL_SPEED, 10, s.ball_image, s.bounce_sound)

	start = time.time()

	# Main loop
	run = True
	while run:
		s.fpsClock.tick(60)
		s.win.fill(s.BLACK)
		score = int(begin_blockscount-len(blocks)-((time.time()-start)/(difficulty*10)))

		score_text = s.normal_font.render(str(score), True, s.WHITE)
		s.win.blit(score_text, (s.WIDTH-score_text.get_width()-10, s.HEIGHT-score_text.get_height()-10))

		# Paddle control
		if pygame.mouse.get_pos()[0] > 0+(s.PADDLE_WIDTH/2) and pygame.mouse.get_pos()[0] < s.WIDTH-(s.PADDLE_WIDTH/2):
			paddle.control() 
		elif pygame.mouse.get_pos()[0] < 0+(s.PADDLE_WIDTH/2):
			paddle.x = 0
		elif pygame.mouse.get_pos()[0] > s.WIDTH-(s.PADDLE_WIDTH/2):
			paddle.x = s.WIDTH-paddle.width
		paddle.draw()

		# Block control
		if len(blocks) == 0:
			scenes.win(score)
			return
	
		for block in blocks:
			block.draw()

		# Ball control
		if ball.rect.collidelist(blocks) != -1:
			ball.collided_block = ball.rect.collidelist(blocks)
			if blocks[ball.collided_block].layer == 0:
				ball.speed = s.BALL_SPEED+difficulty*2
			elif ball.speed != s.BALL_SPEED+difficulty:
				ball.speed = s.BALL_SPEED+difficulty + (ball.speed-s.BALL_SPEED)*0.5

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
			ball.alpha += np.random.normal()*np.pi/(difficulty*4)
			if ball.rect.colliderect(paddle.leftrect):
				ball.bounce_left()
			elif ball.rect.colliderect(paddle.rightrect):
				ball.bounce_right()

		if (ball.rect.y+(ball.radius*2)) >= s.HEIGHT:
			scenes.death(score)
			return

		ball.update()
		ball.draw()

		s.check_closed()

		pygame.display.update()


while True:
	main_game(scenes.begin())
