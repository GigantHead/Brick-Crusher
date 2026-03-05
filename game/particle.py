import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.lifetime = 60 # frames
        self.original_color = color

    def update(self, dt):
        self.rect.center += self.velocity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        else:
             # Fade effect: decrease alpha
             alpha = int((self.lifetime / 60) * 255)
             self.image.set_alpha(alpha)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
