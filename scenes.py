import pygame
import numpy as np
import sys

import settings


def begin():
	diff_button = pygame.Rect(settings.WIDTH/2-settings.WIDTH/4, settings.HEIGHT/2+settings.WIDTH/16, settings.WIDTH/2, settings.HEIGHT/4)
	start_button_image = pygame.image.load("images/start.png")
	diff_state = 1
	settings.win.fill(settings.DARK_GREEN)
	while not(pygame.mouse.get_pressed()[0] and pygame.Rect((settings.WIDTH-start_button_image.get_width())/2, (settings.HEIGHT-start_button_image.get_height())/2-100, start_button_image.get_rect()[2], start_button_image.get_rect()[3]).collidepoint(pygame.mouse.get_pos())):
		
		if diff_button.collidepoint(pygame.mouse.get_pos()):
			if pygame.key.get_pressed()[pygame.K_1]:
				diff_state = 1
			if pygame.key.get_pressed()[pygame.K_2]:
				diff_state = 2
			if pygame.key.get_pressed()[pygame.K_3]:
				diff_state = 3
	
		settings.win.blit(start_button_image, ((settings.WIDTH-start_button_image.get_width())/2, (settings.HEIGHT-start_button_image.get_height())/2-100))
		pygame.draw.rect(settings.win, settings.FUCHSIA, diff_button)
		diff_state_text = settings.normal_font.render(settings.DIFFS[diff_state], True, settings.BLACK)
		settings.win.blit(diff_state_text, tuple(np.subtract(diff_button.center, (diff_state_text.get_width()/2, diff_state_text.get_height()/2))))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pygame.display.update()
	
	return diff_state


def death(score):
	death_text = settings.big_font.render("You lost! Your score was " + str(score), True, settings.WHITE)
	return_text = settings.normal_font.render("Press space to return to home.", True, settings.WHITE)
	while not pygame.key.get_pressed()[pygame.K_SPACE]:
		settings.win.fill(settings.BLACK)
		pygame.draw.rect(settings.win, settings.RED, (settings.WIDTH/20, settings.HEIGHT / 5, (settings.WIDTH/20)*18, (settings.HEIGHT/5)*3))
		settings.win.blit(death_text, ((settings.WIDTH-death_text.get_width()) / 2, (settings.HEIGHT-death_text.get_height())/2))
		settings.win.blit(return_text, ((settings.WIDTH-return_text.get_width()) / 2, ((settings.HEIGHT-return_text.get_height())/2)+100))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pygame.display.update()


def win(score):
	winning_title = settings.big_font.render("You won! Your score was " + str(score), True, settings.WHITE)
	return_text = settings.normal_font.render("Press space to return to home.", True, settings.WHITE)
	while not pygame.key.get_pressed()[pygame.K_SPACE]:
		settings.win.fill(settings.BLACK)
		pygame.draw.rect(settings.win, settings.ORANGE, (settings.WIDTH/14, settings.HEIGHT / 5, (settings.WIDTH/14)*12, (settings.HEIGHT/5)*3))
		settings.win.blit(winning_title, ((settings.WIDTH-winning_title.get_width()) / 2, (settings.HEIGHT-winning_title.get_height())/2))
		settings.win.blit(return_text, ((settings.WIDTH-return_text.get_width()) / 2, ((settings.HEIGHT-return_text.get_height())/2)+100))

		if pygame.key.get_pressed()[pygame.K_KP_ENTER] or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			easter_egg_image = pygame.image.load("images/easter_egg.png")
			settings.win.blit(easter_egg_image, ((settings.WIDTH-easter_egg_image.get_width())/2, (settings.HEIGHT-easter_egg_image.get_height())/2))
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		pygame.display.update()
