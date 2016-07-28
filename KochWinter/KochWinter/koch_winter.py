import pygame
import time
import random
import math
import utils
from snowflake import Snowflake
from pygame.locals import *

class KochWinter:

	def __init__(self):

		self._screen_size = (1024, 720) # size of the window
		self._debug = False # flag to set debug mode
		self._snowflakes = [] # main list of snowflakes
		self._prev_mouse_pos = (0, 0) # previous mouse location to calculate wind
		self._mouse_down = False # whether or not the mouse button is pressed
		self._wind = [0.0, 0.0] # the global wind
		self._max_wind = 500.0 # maximum wind in any direction
		self._curr_fps = 0 # current frames per second
		self._snowflake_time = 0
		self._prev_time = 0


		pygame.init()

		self._screen = pygame.display.set_mode(self._screen_size)
		pygame.display.set_caption("Koch Winter")
	
		self._background = pygame.Surface(self._screen.get_size()).convert()
	

	def run(self):

		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == pygame.MOUSEBUTTONUP:
					self._mouse_down = False
					self._prev_mouse_pos = (0, 0)
					self._wind = [0, 0]
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self._mouse_down = True
				elif event.type == pygame.MOUSEMOTION:
					self._mouse_moved(pygame.mouse.get_pos())
				elif event.type == pygame.KEYUP:
					self._key_pressed(event.key)

			time.sleep(0.001)

			curr_millis = self._get_curr_millis()
			elapsed_time = curr_millis - self._prev_time
			self._snowflake_time += elapsed_time

			if elapsed_time == 0:
				continue

			self._prev_time = curr_millis
			self._curr_fps = 1 / (elapsed_time / 1000.0)

			self._draw_background()

			# try to add snowflakes every 10 milliseconds
			if self._snowflake_time > 10 and len(self._snowflakes) < 200 and random.randrange(100) < 2:

				self._snowflake_time = 0
				self._add_snowflake()


			for flake in self._snowflakes:

				flake.update(elapsed_time)
				rotated_surface = pygame.transform.rotate(flake.surface, math.degrees(flake.theta))

				diameter = flake.radius + flake.radius

				dx = (rotated_surface.get_width() - diameter) / 2
				dy = (rotated_surface.get_height() - diameter) / 2

				self._background.blit(rotated_surface, flake.loc, (dx, dy, diameter, diameter))


			if self._debug:

				self._draw_debug_info()

		
			self._screen.blit(self._background, (0, 0))
			pygame.display.flip()

			

	def _key_pressed(self, key):

		if key == pygame.K_w:

			for flake in self._snowflakes:

				flake.wind = [random.randrange(-250, 250), random.randrange(-250, 250)]


		elif key == pygame.K_d:

			self._debug = not self._debug

			for flake in self._snowflakes:

				flake.debug = self._debug


	def _mouse_moved(self, pos):

		if not self._mouse_down:

			return


		if self._prev_mouse_pos == (0, 0):

			self._prev_mouse_pos = pos

		dx = pos[0] - self._prev_mouse_pos[0]
		dy = pos[1] - self._prev_mouse_pos[1]

		self._wind[0] += dx * 2
		self._wind[1] += dy * 2

		for flake in self._snowflakes:

			flake.wind = self._wind

		self._prev_mouse_pos = pos


	def _draw_background(self):

		##TODO gradient
		#font = pygame.font.Font(None, 32)
		#text = font.render(str(math.floor(self._curr_fps)), 1, (0, 0, 0))

		self._background.fill((230, 230, 230))
		#_background.blit(text, (10, 10))

	def _draw_debug_info(self):

		#TODO everything
		return

	def _add_snowflake(self):

		# randomize snowflake properties
		location = [random.randrange(self._screen_size[0]), -50]
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
		snowflake = Snowflake(location, size, speed, rot_speed, dir, depth, self._screen_size)

		# take wind from previous snowflake if there is one
		if len(self._snowflakes) > 0:

			snowflake.wind = self._snowflakes[-1].wind
		
		# don't bother searching if there aren't any in list
		if len(self._snowflakes) == 0:

			self._snowflakes.append(snowflake)
			return

		# insert snowflake to keep order of snowflakes by snowflake size
		for i in range(0, len(self._snowflakes)):

			if self._snowflakes[i].size > snowflake.size:

				self._snowflakes.insert(i + 1, snowflake)
				return

		# biggest snowflake, put it at the end
		self._snowflakes.append(snowflake)


	def _get_curr_millis(self):

		return int(round(time.time() * 1000))