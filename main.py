import pygame
from game.game import Game


def main():
    pygame.init()
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")   
    finally :
        pygame.quit()
    
if __name__ == "__main__":
    main()
    
