import random
import math
import pygame
from pygame import gfxdraw

class Snowflake:

	# creates a new snowflake
	def __init__(self, start_loc, size, speed, rot_speed, dir, depth, screen_size):

		self.loc = start_loc
		self.size = size
		self.radius = math.sqrt(3) * self.size / 3 # the radius of the circle the snowflake is inscribed in
		self._velocity = (0.0, 0.0)
		self._rot_speed = rot_speed
		self._dir = dir
		self.theta = 0
		self.depth = depth
		self._velocity = [math.sin(self.theta) * self._dir, speed]
		self.wind = [0, 0]
		self._damping = 0.0001 # damping factor so wind dies down
		self.debug = False
		self._stroke_color = (0, 0, 0, 200)
		self._screen_size = screen_size

		blue = random.randrange(20) # how blue the snowflakes should be
		self._fill_color = (255 - blue, 255 - blue, 255, 240) 

		points = self.generate_snowflake()
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32).convert_alpha()
		gfxdraw.aapolygon(self.surface, points, self._stroke_color) # border
		gfxdraw.filled_polygon(self.surface, points, self._fill_color) # fill
		gfxdraw.polygon(self.surface, points, self._stroke_color) # fill


	# updates the snowflake's position and rotation based on the time passed
	def update(self, time):

		seconds = time / 1000.0
		
		# apply damping
		if math.fabs(self.wind[0]) > 0.001:
			self.wind[0] -= self.wind[0] * self._damping

		if math.fabs(self.wind[1]) > 0.001:
			self.wind[1] -= self.wind[1] * self._damping

		# update rotation
		self.theta += (self._rot_speed + self.wind[1] / 200 + random.random()) * seconds

		# update velocity
		self._velocity[0] = 100 * math.sin(self.theta) * self._dir

		offsets = self._get_offsets(seconds)
			
		# update center position	
		self.loc[0] += offsets[0]
		self.loc[1] += offsets[1]


	def _get_offsets(self, seconds):

		offset_x = seconds * (self._velocity[0] + self.wind[0]) * self.size / 50
		offset_y = seconds * (self._velocity[1] + self.wind[1]) * self.size / 50

		if self.loc[0] > self._screen_size[0] + 100:
			offset_x += -self._screen_size[0] - 150
		elif self.loc[0] < -100:
			offset_x += self._screen_size[0] + 150

		if self.loc[1] > self._screen_size[1] + 100:
			offset_y += -self._screen_size[1] - 150
		elif self.loc[1] < -100:
			offset_y += self._screen_size[1] + 150

		return (offset_x, offset_y)


	def draw_debug_info(self, surface):

		total_velocity = (0, 0)


	# generates the snowflake's points based on the depth and size
	def generate_snowflake(self):

		tri_size = self.size  # length of a side
		radius = math.sqrt(3) / 6 * tri_size  # radius of inscribed circle
		height = math.sqrt(3) / 2 * tri_size  # height of triangle
		height_P = height - radius  # distance from center to vertex
		start = [self.radius, self.radius - height_P]  # starting point
		point2 = [start[0] + tri_size / 2, start[1] + height]
		point3 = [point2[0] - tri_size, point2[1]]

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

		tip = [segment_center[0] + sign * math.sin(angle) * tip_height,
		 segment_center[1] - sign * math.cos(angle) * tip_height]

		# push the 5 vertices and return them
		points.append(start)
		points.append([start[0] + dx / 3, start[1] + dy / 3])
		points.append(tip)
		points.append([end[0] - dx / 3, end[1] - dy / 3])
		points.append(end)

		return points