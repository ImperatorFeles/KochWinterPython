import random
import math
import pygame
from pygame import gfxdraw

class Snowflake:

	# creates a new snowflake
	def __init__(self, start_loc, size, speed, rot_speed, dir, depth, screen_size):

		self._loc = start_loc
		self.size = size
		self._velocity = (0.0, 0.0)
		self._rot_speed = rot_speed
		self._dir = dir
		self._theta = 0
		self.depth = depth
		self._velocity = [math.sin(self._theta) * self._dir, speed]
		self.wind = [0, 0]
		self._damping = 0.001 # damping factor so wind dies down
		self.debug = False
		self._stroke_color = (0, 0, 0)
		self._screen_size = screen_size
		self._offsets = self.generate_snowflake()

		blue = random.randrange(20) # how blue the snowflakes should be
		self._fill_color = (255 - blue, 255 - blue, 255)

	# updates the snowflake's position and rotation based on the time passed
	def update(self, time):

		# update position
		self._loc[0] += (time / 1000.0) * (self._velocity[0] + self.wind[0]) * self.size / 50
		self._loc[1] += (time / 1000.0) * (self._velocity[1] + self.wind[1]) * self.size / 50

		# apply damping
		if self.wind[0] < 0.001 or self.wind[0] > 0.001:
			self.wind[0] -= self.wind[0] * self._damping

		if self.wind[1] < 0.001 or self.wind[1] > 0.001:
			self.wind[1] -= self.wind[1] * self._damping

		# bring snowflake to other side of screen outside of screen
		# in a way proportional to how far out it is
		if self._loc[0] > self._screen_size[0] + 50 or self._loc[0] < -50:
			self._loc[0] = -(self._loc[0] - self._screen_size[0])
		if self._loc[1] > self._screen_size[1] + 50 or self._loc[1] < -50:
			self._loc[1] = -(self._loc[1] - self._screen_size[1])

		# update rotation
		self._theta += (self._rot_speed + self.wind[1] / 200 + random.random()) * (time / 1000.0)
		self._velocity[0] = 100 * math.sin(self._theta) * self._dir

	# renders the snowflake to the given surface
	def render(self, surface):

		self.draw_snowflake(surface)

		if self.debug:

			self.draw_debug_info(surface)


	# draws the actual lines of the snowflake
	def draw_snowflake(self, surface):
		
		cos_theta = math.cos(self._theta)
		sin_theta = math.sin(self._theta)

		points = []

		for offset in self._offsets:

			#rotate the point
			point = (offset[0] * cos_theta - offset[1] * sin_theta, 
					offset[0] * sin_theta + offset[1] * cos_theta)

			# convert the offset ot a location
			point = (point[0] + self._loc[0], point[1] + self._loc[1])

			points.append(point)


		# draw the points
		gfxdraw.filled_polygon(surface, points, self._fill_color) # fill
		gfxdraw.aapolygon(surface, points, self._stroke_color) # border


	def draw_debug_info(self, surface):

		total_velocity = (0, 0)


	# generates the snowflake's points based on the depth and size
	def generate_snowflake(self):

		tri_size = self.size  # length of a size
		radius = math.sqrt(3) / 6 * tri_size  # radius of inscribed circle
		height = math.sqrt(3) / 2 * tri_size  # height of triangle
		height_P = height - radius  # distance from center to vertex
		start = (0, -height_P)  # starting point
		point2 = (start[0] + tri_size / 2, start[1] + height)
		point3 = (point2[0] - tri_size, point2[1])

		points = [start, point2, point3]  # start with a triangle
		new_points = []

		depth = self.depth

		while depth > 0:

			new_points = []

			# do 1 depth iteration by recursing each lkine segment in the current
			# snowflake to generate the next level
			for i in range(0, len(points)):

				koch_points = []

				if i + 1 >= len(points):
					koch_points = self.koch_recurse(points[i], points[0])
				else:
					koch_points = self.koch_recurse(points[i], points[i + 1])

				# TODO: make sure this works
				new_points = new_points + koch_points[:-1]

			points = new_points
			depth -= 1

		return points

	# returns all points of the path making up the next koch snowflake segment
	def koch_recurse(self, start, end):

		# a list of points used, to return
		points = []

		# delta from start to end
		dx = end[0] - start[0]
		dy = end[1] - start[1]

		# length of a segment of the line (1/3 length)
		segment_length = math.sqrt(dx * dx + dy * dy) / 3

		# center of the segment of the line
		segment_center = (start[0] + dx / 2, start[1] + dy / 2)

		# distance from the center of the line to the tip of the new triangle
		tip_height = math.sqrt(3) / 2 * segment_length

		# calculate location of tip
		angle = math.atan(dy / dx)

		# sign correction if we are going right, else triangle will point wrong way
		sign = -1 if dx < 0 else 1

		tip = (segment_center[0] + sign * math.sin(angle) * tip_height,
		 segment_center[1] - sign * math.cos(angle) * tip_height)

		# push the 5 vertices and return them
		points.append(start)
		points.append((start[0] + dx / 3, start[1] + dy / 3))
		points.append(tip)
		points.append((end[0] - dx / 3, end[1] - dy / 3))
		points.append(end)

		return points