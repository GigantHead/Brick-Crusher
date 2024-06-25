import pygame
import settings
from .paddle import Paddle
from .ball import Ball
from .brick import Brick

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paddle = Paddle()
        self.ball = Ball()
        self.active = False
        self.font = pygame.font.Font(None, 36)
        #self.brick = [Brick(x, y) for x in range(100, 700, 100) for y in range(50, 150, 50)]
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT    :
                    self.running = False

            # handle key presses for movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.active:
                self.paddle.move(-1)
            if keys[pygame.K_RIGHT] and self.active:
                self.paddle.move(1)
            if keys[pygame.K_SPACE]:
                self.active = True
                            
            if not self.active:
                self.draw_splash_screen("Press Space to Begin")
            else:
                self.update()
                self.draw()
                pygame.display.update()
                self.clock.tick(settings.FPS)
        pygame.quit()
    
    # draw splash screen for game start or game over    
    def draw_splash_screen(self, message):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        #overlay.set_alpha(128)  # adjust transparency: 0 is fully transparent, 255 is opaque
        overlay.fill(settings.GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # render text
        text = self.font.render(message, True, settings.WHITE)
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(settings.BLACK)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        #for brick in self.bricks:
            #brick.draw(self.screen)
            