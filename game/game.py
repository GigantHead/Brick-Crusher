import pygame
import random
import pytweening
import settings
from .paddle import Paddle
from .ball import Ball
from .brick import Brick

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Default font, size 36

        # Pre-render Game Over screen text
        self.game_over_text_surf = self.font.render("Game Over!", True, settings.WHITE)
        self.game_over_rect = self.game_over_text_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))

        self.restart_text_surf = self.font.render("Press any key to restart", True, settings.WHITE)
        self.restart_rect = self.restart_text_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3))

        self.reset_game()
        self.game_state = "SPLASH"  # Initial game state

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = pygame.sprite.Group()
        self.last_brick_time = pygame.time.get_ticks()
        vertical_gap = settings.BRICK_HEIGHT * 2
        self.brick_frequency = (vertical_gap / settings.BRICK_SPEED) * 1000
        self.game_over = False
        self.active = True

    def add_brick_row(self):
        for i in range(settings.SCREEN_WIDTH // settings.BRICK_WIDTH):
            brick = Brick(i * settings.BRICK_WIDTH, 0)
            self.bricks.add(brick)

    def update(self, dt):
        if self.game_state != "PLAYING":
            return

        self.paddle.update()
        self.ball.update()
        self.ball.check_collision_with_paddle(self.paddle)
        
        # Check collisions with bricks
        collided_bricks = self.ball.check_collision_with_bricks(self.bricks)
        for brick in collided_bricks:
            self.bricks.remove(brick)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_brick_time > self.brick_frequency:
            self.add_brick_row()
            self.last_brick_time = current_time

        self.bricks.update(dt)

        # Check for game over condition (bricks reaching paddle level)
        for brick in self.bricks:
            if brick.rect.bottom >= self.paddle.rect.top:
                self.game_state = "GAME_OVER"
                break

        # Remove bricks that have fallen off the screen
        for brick in self.bricks:
            if brick.rect.top >= settings.SCREEN_HEIGHT:
                self.bricks.remove(brick)

    def draw(self):
        if self.game_state == "SPLASH":
            self.draw_splash_screen()
        elif self.game_state == "PLAYING":
            self.screen.fill(settings.BLACK)
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            self.bricks.draw(self.screen)
            pygame.display.flip()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

    def run(self):
        while self.active:
            dt = self.clock.tick(60) / 1000.0

            self.active = self.handle_events()

            if self.game_state == "PLAYING":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.paddle.move(-1)
                if keys[pygame.K_RIGHT]:
                    self.paddle.move(1)

                self.update(dt)

            self.draw()

        pygame.quit()

    # draw splash screen for game start or game over    
    def draw_splash_screen(self):
        self.screen.fill(settings.BLACK)
        title = self.font.render("Breakout", True, settings.WHITE)
        start_text = self.font.render("Press any key to start", True, settings.WHITE)
        
        title_rect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        start_rect = start_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()

    def draw_game_over_screen(self):
        self.screen.fill(settings.BLACK)
        
        self.screen.blit(self.game_over_text_surf, self.game_over_rect)
        self.screen.blit(self.restart_text_surf, self.restart_rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_state == "SPLASH":
                    self.game_state = "PLAYING"
                elif self.game_state == "GAME_OVER":
                    self.reset_game()
                    self.game_state = "PLAYING"
        return True