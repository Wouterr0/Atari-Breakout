import pygame
import numpy as np
import sys

import settings as s


def begin():
	diff_button = pygame.Rect(s.WIDTH/2-s.WIDTH/4, s.HEIGHT/2+s.WIDTH/16, s.WIDTH/2, s.HEIGHT/4)

	start_button_rect = pygame.Rect((s.WIDTH-s.start_button_image.get_width())/2, (s.HEIGHT-s.start_button_image.get_height())/2-100, s.start_button_image.get_rect()[2], s.start_button_image.get_rect()[3])
	diff_state = 1
	s.win.fill(s.DARK_GREEN)
	
	while not(pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos())):

		if diff_button.collidepoint(pygame.mouse.get_pos()):
			if pygame.key.get_pressed()[pygame.K_1]:
				diff_state = 1
			if pygame.key.get_pressed()[pygame.K_2]:
				diff_state = 2
			if pygame.key.get_pressed()[pygame.K_3]:
				diff_state = 3

		if start_button_rect.collidepoint(pygame.mouse.get_pos()):
			s.win.blit(s.start_button_hover_image, ((s.WIDTH-s.start_button_image.get_width())/2, (s.HEIGHT-s.start_button_image.get_height())/2-100))
		else:
			s.win.blit(s.start_button_image, ((s.WIDTH-s.start_button_image.get_width())/2, (s.HEIGHT-s.start_button_image.get_height())/2-100))

		pygame.draw.rect(s.win, s.FUCHSIA, diff_button)
		diff_state_text = s.normal_font.render(s.DIFFS[diff_state], True, s.BLACK)
		s.win.blit(diff_state_text, tuple(np.subtract(diff_button.center, (diff_state_text.get_width()/2, diff_state_text.get_height()/2))))

		s.check_closed()
		pygame.display.update()
	
	return diff_state


def death(score):
	death_text = s.big_font.render("You lost! Your score was " + str(score), True, s.WHITE)
	return_text = s.normal_font.render("Press space to return to home.", True, s.WHITE)
	while not pygame.key.get_pressed()[pygame.K_SPACE]:
		s.win.fill(s.BLACK)
		pygame.draw.rect(s.win, s.RED, (s.WIDTH/20, s.HEIGHT / 5, (s.WIDTH/20)*18, (s.HEIGHT/5)*3))
		s.win.blit(death_text, ((s.WIDTH-death_text.get_width()) / 2, (s.HEIGHT-death_text.get_height())/2))
		s.win.blit(return_text, ((s.WIDTH-return_text.get_width()) / 2, ((s.HEIGHT-return_text.get_height())/2)+100))

		s.check_closed()
		pygame.display.update()


def win(score):
	winning_title = s.big_font.render("You won! Your score was " + str(score), True, s.WHITE)
	return_text = s.normal_font.render("Press space to return to home.", True, s.WHITE)
	while not pygame.key.get_pressed()[pygame.K_SPACE]:
		s.win.fill(s.BLACK)
		pygame.draw.rect(s.win, s.ORANGE, (s.WIDTH/14, s.HEIGHT / 5, (s.WIDTH/14)*12, (s.HEIGHT/5)*3))
		s.win.blit(winning_title, ((s.WIDTH-winning_title.get_width()) / 2, (s.HEIGHT-winning_title.get_height())/2))
		s.win.blit(return_text, ((s.WIDTH-return_text.get_width()) / 2, ((s.HEIGHT-return_text.get_height())/2)+100))

		# Easteregg
		if pygame.key.get_pressed()[pygame.K_KP_ENTER] or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			if pygame.key.get_pressed()[pygame.K_KP_ENTER] and pygame.key.get_pressed()[pygame.K_ESCAPE]:
				s.win.blit(s.easterEgg_image_fliped, ((s.WIDTH-s.easterEgg_image_fliped.get_width())/2, (s.HEIGHT-s.easterEgg_image_fliped.get_height())/2))
			else:
				s.win.blit(s.easterEgg_image, ((s.WIDTH-s.easterEgg_image.get_width())/2, (s.HEIGHT-s.easterEgg_image.get_height())/2))
	
		s.check_closed()
		pygame.display.update()


def pause(background):
	background = s.PIL_to_surface(s.brightness(s.surface_to_PIL(background), 0.3))
	while True:
		s.win.blit(background, (0, 0))

		s.check_closed()
		pygame.display.update()
