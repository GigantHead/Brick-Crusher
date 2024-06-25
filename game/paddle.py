import pygame
import settings

class Paddle:
    def __init__(self):
        self.speed = 10 # speed of paddle movement 
        self.image = pygame.Surface((100,20))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect(center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 100)) # initialize the paddle at the bottom center of the screen
        
    def move(self, direction):
        # move the paddle in the indicated direction, taking into account the speed
        self.rect.x += direction * self.speed
        # prevent the paddle from moving out of the window
        self.rect.clamp_ip(pygame.Rect(0,0,settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)    