import pygame
import random
import settings
from .paddle import Paddle
from .ball import Ball
from .brick import Brick

class Game:
    def __init__(self):
        pygame.init()
        # display variables
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # gameplay variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.paddle = Paddle()
        self.ball = Ball()
        self.last_brick_time = pygame.time.get_ticks()
        self.bricks = []
        self.brick_frequency = 4000
        self.brick_spawn_probability = settings.INITIAL_BRICK_SPAWN_PROBABILITY
        
        # variables for start and end of game splash screen
        self.active = False
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.reset_game()
                        else:
                            self.active = True
            
            # clear the screen at the start of each frame
            self.screen.fill(settings.BLACK)
                    
            # splash screen before game start and after game over
            if not self.active and not self.game_over:
                self.draw_splash_screen("Press Space to Begin")
            elif self.game_over:
                self.draw_splash_screen("Game Over! Press Space to Retry")
                
            else:
                self.handle_keys()
                self.update()
                self.draw()

            pygame.display.update()
            self.clock.tick(settings.FPS)
        pygame.quit()
    
    # draw splash screen for game start or game over    
    def draw_splash_screen(self, message):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(settings.SPLASH_SCREEN_TRANSPARENCY)  # adjust transparency: 0 is fully transparent, 255 is opaque
        overlay.fill(settings.GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # render text
        text = self.font.render(message, True, settings.WHITE)
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_brick_time > self.brick_frequency:
            self.add_brick_row()
            if self.brick_spawn_probability <= 1 - settings.BRICK_PROBABILITY_INCREMENT:
                self.brick_spawn_probability += settings.BRICK_PROBABILITY_INCREMENT
            else: self.brick_spawn_probability = 1
            self.last_brick_time = current_time

        
        for brick in self.bricks:
            brick.update()
            if brick.rect.bottom >= self.paddle.rect.top:
                self.game_over = True
                self.active = False 
    
    def add_brick_row(self):
        row = []
        min_bricks = 1 # ensure minimum of one brick per row
        for i in range(settings.SCREEN_WIDTH // settings.BRICK_WIDTH):
            if random.random() < self.brick_spawn_probability or min_bricks > 0:
                brick = Brick(i * settings.BRICK_WIDTH, 0)
                row.append(brick)
                min_bricks -= 1
        self.bricks.extend(row)

    def reset_game(self):
        self.active = True
        self.game_over = False
        self.bricks = []
        self.paddle = Paddle()
        self.ball = Ball()
        self.last_brick_time = pygame.time.get_ticks()
        self.brick_frequency = 3000
        self.brick_spawn_probability = settings.INITIAL_BRICK_SPAWN_PROBABILITY

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            if brick.active_brick:
                self.screen.blit(brick.image, brick.rect)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move(-1)
        if keys[pygame.K_RIGHT]:
            self.paddle.move(1)        