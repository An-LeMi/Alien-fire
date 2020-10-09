import sys  

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
# from alien import Alien -  Don't need because don't use ailen in here


def run_game():
	# Initialize game and create screen object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	# Make the Play button.
	play_button = Button(ai_settings, screen, "Play")

	# Creat an instance to store game statistics and create a scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	# Set background color
	bg_color = (ai_settings.bg_color)

	# Make a ship
	ship = Ship(ai_settings,screen)
	
	# Make a bullet
	bullets = Group()

	# Make ailen
	aliens = Group()

	# Creat the fleet of ailens
	gf.creat_fleet(ai_settings, screen, ship, aliens)

	# Start the main loop for game.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()		 
