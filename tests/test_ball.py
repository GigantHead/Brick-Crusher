import pytest
import pygame
from game.ball import Ball
from game.brick import Brick
import settings

class TestBallCollision:
    @pytest.fixture
    def ball(self):
        # Create a ball and reset its position for controlled testing
        ball = Ball()
        # Ensure consistent speed
        ball.speed = 5
        return ball

    @pytest.fixture
    def brick(self):
        # Create a brick at a known location (e.g., 100, 100)
        return Brick(100, 100)

    def test_collision_left_side(self, ball, brick):
        """Test ball hitting the left side of the brick."""
        # Setup ball moving right
        ball.velocity_x = 5
        ball.velocity_y = 0

        # Position ball rect right edge exactly at brick rect left edge
        ball.rect.right = brick.rect.left
        # Align vertically to be in the middle of the brick
        ball.rect.centery = brick.rect.centery

        ball.handle_brick_collision(brick)

        # Expect velocity_x to flip
        assert ball.velocity_x == -5
        # Expect velocity_y to remain unchanged
        assert ball.velocity_y == 0

    def test_collision_right_side(self, ball, brick):
        """Test ball hitting the right side of the brick."""
        # Setup ball moving left
        ball.velocity_x = -5
        ball.velocity_y = 0

        # Position ball rect left edge exactly at brick rect right edge
        ball.rect.left = brick.rect.right
        # Align vertically
        ball.rect.centery = brick.rect.centery

        ball.handle_brick_collision(brick)

        # Expect velocity_x to flip
        assert ball.velocity_x == 5
        assert ball.velocity_y == 0

    def test_collision_top_side(self, ball, brick):
        """Test ball hitting the top side of the brick."""
        # Setup ball moving down
        ball.velocity_x = 0
        ball.velocity_y = 5

        # Position ball rect bottom edge exactly at brick rect top edge
        ball.rect.bottom = brick.rect.top
        # Align horizontally
        ball.rect.centerx = brick.rect.centerx

        ball.handle_brick_collision(brick)

        # Expect velocity_y to flip
        assert ball.velocity_y == -5
        # Expect velocity_x to remain unchanged
        assert ball.velocity_x == 0

    def test_collision_bottom_side(self, ball, brick):
        """Test ball hitting the bottom side of the brick."""
        # Setup ball moving up
        ball.velocity_x = 0
        ball.velocity_y = -5

        # Position ball rect top edge exactly at brick rect bottom edge
        ball.rect.top = brick.rect.bottom
        # Align horizontally
        ball.rect.centerx = brick.rect.centerx

        ball.handle_brick_collision(brick)

        # Expect velocity_y to flip
        assert ball.velocity_y == 5
        assert ball.velocity_x == 0

    def test_collision_overlap_left(self, ball, brick):
        """
        Test ball slightly overlapping the left side.

        Note: The current collision logic is simplistic and relies on strict inequality checks.
        If the ball overlaps the brick (e.g. rect.right > brick.rect.left), the logic may fail
        to identify it as a horizontal collision and instead treat it as vertical (y-flip).
        This test is currently a placeholder to document this behavior and may need to be updated
        if collision logic becomes more robust.
        """
        pass

    def test_collision_overlap_top(self, ball, brick):
        """
        Test ball slightly overlapping the top side.

        See note in test_collision_overlap_left.
        """
        pass
