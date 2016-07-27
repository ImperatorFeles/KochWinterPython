import pygame
import time
import random
import math
import cProfile
import utils
from snowflake import Snowflake
from pygame.locals import *

_screen_size = (1024, 720) # size of the window
_debug = False # flag to set debug mode
_snowflakes = [] # main list of snowflakes
_prev_mouse_pos = (0, 0) # previous mouse location to calculate wind
_mouse_down = False # whether or not the mouse button is pressed
_wind = [0.0, 0.0] # the global wind
_max_wind = 500.0 # maximum wind in any direction
_prev_time = 0 # previous fram start time
_curr_fps = 0 # current frames per second
_background = None
_screen = None

def main():

	global _screen_size
	global _background
	global _prev_time
	global _screen


	pygame.init()
	_screen = pygame.display.set_mode(_screen_size)
	pygame.display.set_caption("Pygame Testing")
	
	_background = pygame.Surface(_screen.get_size())
	_background = _background.convert()

	_prev_time = get_curr_millis()

	_screen.blit(_background, (0, 0))
	pygame.display.flip()
	
	cProfile.run('loop()')
	loop()


def key_pressed(key):

	global _snowflakes
	global _debug

	if key == pygame.K_w:

		for flake in _snowflakes:

			flake.wind = [random.randrange(-250, 250), random.randrange(-250, 250)]


	elif key == pygame.K_d:

		_debug = not _debug

		for flake in _snowflakes:

			flake.debug = _debug


def mouse_moved(pos):

	global _mouse_down
	global _prev_mouse_pos
	global _wind
	global _snowflakes

	if not _mouse_down:

		return


	if _prev_mouse_pos == (0, 0):

		_prev_mouse_pos = pos

	dx = pos[0] - _prev_mouse_pos[0]
	dy = pos[1] - _prev_mouse_pos[1]

	_wind[0] += dx * 2
	_wind[1] += dy * 2

	for flake in _snowflakes:

		flake.wind = _wind

	_prev_mouse_pos = pos
	

def loop():

	global _prev_time
	global _curr_fps
	global _background
	global _snowflakes
	global _debug
	global _screen
	global _mouse_down
	global _prev_mouse_pos
	global _wind

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONUP:
				_mouse_down = False
				_prev_mouse_pos = (0, 0)
				_wind = [0, 0]
			elif event.type == pygame.MOUSEBUTTONDOWN:
				_mouse_down = True
			elif event.type == pygame.MOUSEMOTION:
				mouse_moved(pygame.mouse.get_pos())
			elif event.type == pygame.KEYUP:
				key_pressed(event.key)

		updated_flakes = 0

		if (updated_flakes > len(_snowflakes)):
			updated_flakes = 0

		curr_millis = get_curr_millis()
		elapsed_time = curr_millis - _prev_time

		if elapsed_time == 0:
			continue

		_prev_time = curr_millis
		_curr_fps = 1 / (elapsed_time / 1000.0)

		draw_background()

		# try to add snowflakes every 10 milliseconds
		for i in range(0, elapsed_time % 10 + 1):

			# add a new snowflake if we don't have enough and rng says we should
			if len(_snowflakes) < 200 and random.randrange(100) < 2:

				add_snowflake()

		# update the snowflakes
		for i in range(updated_flakes, min(updated_flakes + 1, len(_snowflakes))):
			_snowflakes[i].update(elapsed_time)

		updated_flakes += 1

		for flake in _snowflakes:

			flake.update(elapsed_time)

		# draw the snowflakes
		for flake in _snowflakes:

			_background.blit(flake.get_surface(), flake.loc)

		if _debug:

			draw_debug_info()

		
		_screen.blit(_background, (0, 0))
		pygame.display.flip()


def draw_background():

	#TODO gradient
	_background.fill((200, 200, 200))


def draw_debug_info():

	#TODO everything
	return

def add_snowflake():

	global _screen_size
	global _snowflakes

	# randomize snowflake properties
	location = [random.randrange(_screen_size[0]), -50]
	size = random.randrange(40) + 10
	speed = random.randrange(70) + 50
	rot_speed = random.randrange(3) + 1
	dir = random.randrange(2) - 1
	depth = math.floor(utils.generate_random_normal() + 1.85)

	# make sure depth was generated correctly
	while size < 40 and depth > 1 or depth < 0 or depth > 3:

		depth = math.floor(utils.generate_random_normal() + 1.85)

	# make flakes besides 1 and 2 more rare
	if depth != 0 and depth != 1 and random.randrange(100) < 40:

		depth = 1

	# create the snowflake
	snowflake = Snowflake(location, size, speed, rot_speed, dir, depth, _screen_size)

	# take wind from previous snowflake if there is one
	if len(_snowflakes) > 0:

		snowflake.wind = _snowflakes[-1].wind
		
	# don't bother searching if there aren't any in list
	if len(_snowflakes) == 0:

		_snowflakes.append(snowflake)
		return

	# insert snowflake to keep order of snowflakes by snowflake size
	for i in range(0, len(_snowflakes)):

		if _snowflakes[i].size > snowflake.size:

			_snowflakes.insert(i + 1, snowflake)
			return

	# biggest snowflake, put it at the end
	_snowflakes.append(snowflake)


def get_curr_millis():

	return int(round(time.time() * 1000))

if __name__ == "__main__": main()