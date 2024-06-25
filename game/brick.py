import pygame
import settings

class Brick:
    def __init__(self):
        self.image = pygame.SurfaceType((100,50))
        self.image.fill(settings.BLUE)
    
