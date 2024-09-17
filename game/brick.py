import pygame
import settings

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((settings.BRICK_WIDTH, settings.BRICK_HEIGHT))
        self.image.fill(settings.colors[0])
        pygame.draw.rect(self.image, settings.BLACK, self.image.get_rect(), settings.BRICK_BORDER_WIDTH)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.real_y = float(y)

    def update(self, dt):
        self.real_y += settings.BRICK_SPEED * dt
        self.rect.y = int(self.real_y)

    def draw(self, screen):
        if self.active_brick:
            screen.blit(self.image, self.rect)

