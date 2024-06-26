import pygame
import settings

class Brick:
    def __init__(self, x, y):
        self.image = pygame.Surface((settings.BRICK_WIDTH,settings.BRICK_HEIGHT))
        self.image.fill(settings.colors[0])
        pygame.draw.rect(self.image, settings.BLACK, self.image.get_rect(), settings.BRICK_BORDER_WIDTH)
        self.rect = self.image.get_rect(topleft = (x,y))
        self.active_brick = True
        self.brick_toughness = 0
        self.brick_speed = 1

    
    def update(self):
        if self.active_brick:
            self.rect.y += self.brick_speed
