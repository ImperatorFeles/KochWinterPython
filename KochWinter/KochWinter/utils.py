import random
import math

def generate_random_normal():

	U1 = random.random()
	U2 = random.random()

	c1 = math.sqrt(-2 * math.log(U1))
	c2 = math.cos(2 * math.pi * U2)

	return c1 * c2
