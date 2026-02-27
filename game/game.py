import pygame
import random
import pytweening
import settings
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .particle import Particle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Default font, size 36
        self.reset_game()
        self.game_state = "SPLASH"  # Initial game state

        # Screen shake
        self.shake_duration = 0
        self.shake_magnitude = 0
        self.canvas = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.last_brick_time = pygame.time.get_ticks()
        vertical_gap = settings.BRICK_HEIGHT * 2
        self.brick_frequency = (vertical_gap / settings.BRICK_SPEED) * 1000
        self.game_over = False
        self.active = True
        self.score = 0

    def trigger_shake(self, magnitude, duration):
        self.shake_magnitude = magnitude
        self.shake_duration = duration

    def add_brick_row(self):
        for i in range(settings.SCREEN_WIDTH // settings.BRICK_WIDTH):
            color = random.choice(settings.colors)
            brick = Brick(i * settings.BRICK_WIDTH, 0, color)
            self.bricks.add(brick)

    def spawn_particles(self, pos, color):
        for _ in range(10):
            particle = Particle(pos, color)
            self.particles.add(particle)

    def update(self, dt):
        if self.game_state != "PLAYING":
            return

        self.paddle.update()
        self.ball.update()

        # Check collision with paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.check_collision_with_paddle(self.paddle)
            self.trigger_shake(5, 10)
        
        # Check collisions with bricks
        collided_bricks = self.ball.check_collision_with_bricks(self.bricks)
        for brick in collided_bricks:
            self.bricks.remove(brick)
            self.spawn_particles(brick.rect.center, brick.color)
            self.trigger_shake(3, 5)
            self.score += 10

        current_time = pygame.time.get_ticks()
        if current_time - self.last_brick_time > self.brick_frequency:
            self.add_brick_row()
            self.last_brick_time = current_time

        self.bricks.update(dt)
        self.particles.update(dt)

        # Check for game over condition (bricks reaching paddle level)
        for brick in self.bricks:
            if brick.rect.bottom >= self.paddle.rect.top:
                self.game_state = "GAME_OVER"
                break

        # Remove bricks that have fallen off the screen
        for brick in self.bricks:
            if brick.rect.top >= settings.SCREEN_HEIGHT:
                self.bricks.remove(brick)

        # Screen shake update
        if self.shake_duration > 0:
            self.shake_duration -= 1
        else:
             self.shake_magnitude = 0

    def draw(self):
        if self.game_state == "SPLASH":
            self.draw_splash_screen()
        elif self.game_state == "PLAYING":
            self.canvas.fill(settings.BLACK)
            self.paddle.draw(self.canvas)
            self.ball.draw(self.canvas)
            self.bricks.draw(self.canvas)
            self.particles.draw(self.canvas)

            # Score
            score_text = self.font.render(f"Score: {self.score}", True, settings.WHITE)
            self.canvas.blit(score_text, (10, 10))

            # Apply Shake
            offset_x = 0
            offset_y = 0
            if self.shake_duration > 0:
                offset_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
                offset_y = random.randint(-self.shake_magnitude, self.shake_magnitude)

            self.screen.fill(settings.BLACK) # Clear screen before blitting canvas
            self.screen.blit(self.canvas, (offset_x, offset_y))
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
        title = self.font.render("Breakout", True, settings.NEON_BLUE)
        start_text = self.font.render("Press any key to start", True, settings.WHITE)
        
        title_rect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        start_rect = start_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()

    def draw_game_over_screen(self):
        self.screen.fill(settings.BLACK)
        game_over_text = self.font.render("Game Over!", True, settings.NEON_PINK)
        score_text = self.font.render(f"Final Score: {self.score}", True, settings.WHITE)
        restart_text = self.font.render("Press any key to restart", True, settings.WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        score_rect = score_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
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
