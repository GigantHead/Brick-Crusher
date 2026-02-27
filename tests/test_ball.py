import unittest
import sys
import os
import pygame

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set dummy video driver for headless testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

from game.ball import Ball
from game.brick import Brick
import settings

class TestBall(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Create a dummy display surface
        pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.ball = Ball()

    def tearDown(self):
        pygame.quit()

    def test_brick_collision(self):
        # Create a brick at 100, 100
        brick = Brick(100, 100)
        bricks = pygame.sprite.Group()
        bricks.add(brick)

        # Position ball to collide with the bottom of the brick
        # Brick rect: x=100, y=100, w=100, h=50. Bottom is at y=150.
        # Ball rect: w=20, h=20.
        # We place ball such that its top is slightly above brick bottom.

        self.ball.rect.centerx = brick.rect.centerx
        self.ball.rect.top = brick.rect.bottom - 2

        # Set velocity to move upwards
        self.ball.velocity_x = 0
        self.ball.velocity_y = -5

        initial_vy = self.ball.velocity_y

        # Perform collision check
        collided = self.ball.check_collision_with_bricks(bricks)

        # Check if collision was detected
        self.assertTrue(len(collided) > 0, "Collision should be detected")

        # Check if velocity reversed (bounced off bottom)
        self.assertEqual(self.ball.velocity_y, -initial_vy, "Velocity Y should reverse on bottom collision")

if __name__ == '__main__':
    unittest.main()
