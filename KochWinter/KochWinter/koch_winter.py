import pygame
from snowflake import Snowflake
from pygame.locals import *

def main():

	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Pygame Testing")


	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((200, 200, 200))

	for i in range(0, 10):

		Snowflake(((i + 1) * 55, (i + 1) * 55), i * 5 + 30, 0, 0, 0, i / 2, (800, 600)).draw_snowflake(background)

	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()

		
if __name__ == "__main__": main()