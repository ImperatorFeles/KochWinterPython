import random
import math
import pygame
from pygame import gfxdraw

class Snowflake:

	# creates a new snowflake
	def __init__(self, start_loc, size, speed, rot_speed, dir, depth, screen_size):

		self.loc = start_loc
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
		self._points = self.generate_snowflake()
		self._surface = pygame.Surface((int(math.sqrt(3) / 3 * self.size), int(math.sqrt(3) / 3 * self.size)))

		blue = random.randrange(20) # how blue the snowflakes should be
		self._fill_color = (255 - blue, 255 - blue, 255)

	# updates the snowflake's position and rotation based on the time passed
	def update(self, time):

		seconds = time / 1000.0

		prev_theta = self._theta

		self._apply_damping()
		self._update_rotation(seconds)
		self._update_velocity()
		offsets = self._get_offsets(seconds)
			
		# update center position	
		self.loc[0] += offsets[0]
		self.loc[1] += offsets[1]
		
		# only offset position by change in theta
		dtheta = self._theta - prev_theta
		cos_theta = math.cos(dtheta)
		sin_theta = math.sin(dtheta)

		# update all the points
		for point in self._points:
			
			self._update_point(point, offsets, cos_theta, sin_theta)


	def _apply_damping(self):
		
		# apply damping
		if math.fabs(self.wind[0]) > 0.001:
			self.wind[0] -= self.wind[0] * self._damping

		if math.fabs(self.wind[1]) > 0.001:
			self.wind[1] -= self.wind[1] * self._damping


	def _update_rotation(self, seconds):
		
		self._theta += (self._rot_speed + self.wind[1] / 200 + random.random()) * seconds


	def _update_velocity(self):

		self._velocity[0] = 100 * math.sin(self._theta) * self._dir


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


	def _update_point(self, point, offsets, cos_theta, sin_theta):
		
		# update position
		point[0] += offsets[0]
		point[1] += offsets[1]

		# update rotation
		point[0] -= self.loc[0]
		point[1] -= self.loc[1]

		new_x = point[0] * cos_theta - point[1] * sin_theta
		new_y = point[0] * sin_theta + point[1] * cos_theta

		point[0] = new_x + self.loc[0]
		point[1] = new_y + self.loc[1]


		
	# renders the snowflake to the given surface
	def get_surface(self):

		self.draw_snowflake()

		return self._surface

		#if self.debug:

		#	self.draw_debug_info(surface)


	# draws the actual lines of the snowflake
	def draw_snowflake(self):
		
		# draw the points
		self._surface.fill((0, 0, 0, 0))
		gfxdraw.filled_polygon(self._surface, self._points, self._fill_color) # fill
		gfxdraw.aapolygon(self._surface, self._points, self._stroke_color) # border


	def draw_debug_info(self, surface):

		total_velocity = (0, 0)


	# generates the snowflake's points based on the depth and size
	def generate_snowflake(self):

		tri_size = self.size  # length of a side
		radius = math.sqrt(3) / 6 * tri_size  # radius of inscribed circle
		height = math.sqrt(3) / 2 * tri_size  # height of triangle
		height_P = height - radius  # distance from center to vertex
		start = [self.loc[0], self.loc[1] - height_P]  # starting point
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