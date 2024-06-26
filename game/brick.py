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
        self.brick_speed = 0.01
        self.real_y = float(y) # record y as a float to facilitate sub-pixel movement
        self.last_update = pygame.time.get_ticks()
        

    
    def update(self):
        if self.active_brick:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.last_update
            self.last_update = current_time
            self.real_y += self.brick_speed * elapsed_time
            if int(self.real_y) != self.rect.y:
                self.rect.y = int(self.real_y)
                
            
