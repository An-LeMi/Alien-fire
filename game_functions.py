import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):	
	# Respond to keypress.		
	if event.key == pygame.K_RIGHT:
		# Move the ship to the right. Change flag True
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True	
	elif event.key == pygame.K_SPACE:
		# Creat a new bullet and add to the bullets group.
		fire_bullet(ai_settings, screen, ship, bullets)
		

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		# Don't move the ship
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
	"""Respond to the keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN: 
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)	

def update_screen(ai_settings, screen, ship, aliens, bullets):
	""" Update images on the screen and flip to the new screen."""	

	# Redraw the screen during each pass through the loop. 
	screen.fill(ai_settings.bg_color)

	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)

	# Make the most recently drawn screen visible. 
	pygame.display.flip()	

def update_bullets(bullets):
	"""Update position of bullets and get rid of old bullets.""" 
	# Update bullet positions.
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0: 
			bullets.remove(bullet)

def fire_bullet(ai_settings, screen, ship, bullets): 
	"""Fire a bullet if limit not reached yet."""
	# Create a new bullet and add it to the bullets group. 
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship) 
		bullets.add(new_bullet)

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
	
def update_aliens(ai_settings, aliens):
	"""Update the positions of all alien in the fleet"""
	# Check if the fleet is at an edge
	# and then update the positon of all aliens in fleet
	check_fleet_edges(ai_settings, aliens)
	aliens.update()				





