from koch_winter import KochWinter
import cProfile

def main():

	koch_winter = KochWinter()
	
	#cProfile.run('koch_winter.run()')
	koch_winter.run()


if __name__ == "__main__": main()