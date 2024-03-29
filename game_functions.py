import sys
import pygame
import random
from ship_bullet import ShipBullet
from alien_bullet import AlienBullet
from alien import Alien
from time import sleep
import sound

def check_keydown_events(event, ai_settings, screen, ship, ship_bullets):	
	# Respond to keypress.		
	if event.key == pygame.K_RIGHT:
		# Move the ship to the right. Change flag True
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True	
	elif event.key == pygame.K_SPACE:
		# Creat a new bullet and add to the ship_bullets group.
		fire_bullet(ai_settings, screen, ship, ship_bullets)
		

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		# Don't move the ship
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, ship_bullets):
	"""Respond to the keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			file_save = open("Data/High.txt","r+")
			file_save.write(str(stats.high_score))
			file_save.close()
			sys.exit()
		elif event.type == pygame.KEYDOWN: 
			check_keydown_events(event, ai_settings, screen, ship, ship_bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, ship_bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, ship_bullets, mouse_x, mouse_y):
	"""Start new game when click Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings
		ai_settings.iniitialize_dynamic_settings()

		# Reset game statistics.
		stats.reset_stats()
		stats.game_active = True

		# Reset the scoreboard images. 
		sb.prep_score() 
		sb.prep_high_score() 
		sb.prep_level()	
		sb.prep_ships()	

		# Empty aliens, ship_bullets
		aliens.empty()
		ship_bullets.empty()

		# Create a new fleet and center ship
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		pygame.mouse.set_visible(False)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, play_button, fps_count, fps, alien_bullets):
	""" Update images on the screen and flip to the new screen."""	

	# Redraw the screen during each pass through the loop. 
	screen.fill(ai_settings.bg_color)

	# Redraw all ship_bullets behind ship and aliens.
	for ship_bullet in ship_bullets.sprites():
		ship_bullet.draw_bullet()

	for alien_bullet in alien_bullets.sprites():
		alien_bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)

	# Draw score information
	sb.show_score()

	# Draw fps
	fps_count.show_fps()
	fps_count.prep_count(fps)

	# Draw the play button if the game is inactive.
	if not stats.game_active:
		play_button.draw_button()

	# Make the most recently drawn screen visible. 
	pygame.display.flip()	

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets):
	"""Update position of ship_bullets and get rid of old ship_bullets.""" 
	# Update bullet positions.
	ship_bullets.update()
	alien_bullets.update()

	# Check bullet in edge
	for ship_bullet in ship_bullets.copy():
		if ship_bullet.rect.bottom <= 0: 
			ship_bullets.remove(ship_bullet)

	for alien_bullet in alien_bullets.copy():
		if alien_bullet.rect.top >= screen.get_rect().bottom: 
			alien_bullets.remove(alien_bullet)
	# Check for any ship_bullets that have hit aliens
	# If so, get rid of the bullet and the alien. - xoa vien dan va alien
	check_bullet_alien_collisons(ai_settings, screen, stats, sb, ship, aliens, ship_bullets)
	check_alien_bullet_ship_collisons(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets)
	
def check_bullet_alien_collisons(ai_settings, screen, stats, sb, ship, aliens, ship_bullets): 
	"""Respond to bullet alien collision"""

	collisions = pygame.sprite.groupcollide(ship_bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()	
		check_high_score(stats, sb)
		sound.alien_sound.play()	
	if len(aliens) == 0:
		# Destroy existing bullet and create new fleet
		ship_bullets.empty()
		ai_settings.increase_speed()

		# Increase level.
		stats.level += 1
		sb.prep_level()

		creat_fleet(ai_settings, screen, ship, aliens)

def check_alien_bullet_ship_collisons(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets):
	if pygame.sprite.spritecollideany(ship, alien_bullets):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets)

def fire_bullet(ai_settings, screen, ship, ship_bullets): 
	"""Fire a bullet if limit not reached yet."""
	# Create a new bullet and add it to the ship_bullets group. 
	if len(ship_bullets) < ai_settings.bullets_allowed:
		new_bullet = ShipBullet(ai_settings, screen, ship) 
		ship_bullets.add(new_bullet)
		sound.ship_bullet_sound.play()

def alien_fire_bullet(ai_settings, screen, alien, alien_bullets):
    """Create an alien bullet"""
    new_alien_bullet = AlienBullet(ai_settings, screen, alien)
    alien_bullets.add(new_alien_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row."""
	availble_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(availble_space_x / (alien_width * 2))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	availble_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
	number_rows = int(availble_space_y / (2 * alien_height))
	return number_rows

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def creat_fleet(ai_settings, screen, ship, aliens):
	"""Creat a full fleet of aliens"""
	# Creat an alien and find the number of aliens in a row
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	# Creat the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# Creat an alien and place it in row
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
	""" Respond appropriately if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets):
	"""Update the positions of all alien in the fleet"""
	# Check if the fleet is at an edge
	# and then update the positon of all aliens in fleet
	check_fleet_edges(ai_settings, aliens)
	aliens.update()	

	# Look for aliens and ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets)
	# Look for alien hitting the bottom of screen
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets)

	# Random alien fire
	randtime = random.randint(0,120)
	if randtime > 118:
		rand_id = random.randint(0, len(aliens))
		for idx, alien in enumerate(aliens.sprites()):
			if idx == rand_id:
				alien_fire_bullet(ai_settings, screen, alien, alien_bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets):
	"""Respond to ship being hit by aliens"""
	if stats.ship_left > 0:
		# Decrement ships_left
		stats.ship_left -= 1

		# Update scoreboard
		sb.prep_ships()

		# Empty the list of aliens and ship_bullets
		aliens.empty()
		ship_bullets.empty()
		alien_bullets.empty()

		# Creat a new fleet and center the ship
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# Pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets):
	"""Check if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()

	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, ship_bullets, alien_bullets)

def check_high_score(stats, sb):
	""" Check to see if have high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

