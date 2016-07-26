import pygame
from pygame.locals import *

def main():

	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Pygame Testing")

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 0, 0))

	font = pygame.font.Font(None, 36)
	text = font.render("HELLO FRIENDO", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()

		
if __name__ == "__main__": main()