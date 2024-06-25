import pygame
import settings

class Ball:
    def __init__(self):
        self.image = pygame.Surface((20,20))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect(center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 120)) # initialize the ball right above the paddle

    def move(self):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        