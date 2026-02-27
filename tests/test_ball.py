import pytest
import pygame
import math
from game.ball import Ball
from game.brick import Brick
import settings

class TestBall:
    @pytest.fixture
    def ball(self):
        ball = Ball()
        # Reset velocity to something predictable
        ball.speed = 5
        ball.velocity_x = 5
        ball.velocity_y = -5
        return ball

    @pytest.fixture
    def bricks(self):
        # Create a group of bricks
        bricks = pygame.sprite.Group()
        return bricks

    def test_no_collision(self, ball, bricks):
        # Place ball far away from any bricks
        ball.rect.center = (100, 100)

        # Add a brick far away
        brick = Brick(200, 200)
        bricks.add(brick)

        collided = ball.check_collision_with_bricks(bricks)

        assert collided == []
        # Velocity should remain unchanged
        assert ball.velocity_x == 5
        assert ball.velocity_y == -5

    def test_horizontal_collision(self, ball, bricks):
        # Place a brick
        brick_x, brick_y = 200, 200
        brick = Brick(brick_x, brick_y)
        bricks.add(brick)

        # Position ball to hit the left side of the brick
        # Ball center needs to be just inside the brick's left edge
        # Brick rect is at (200, 200) with size (100, 50) typically
        # Ball is 20x20

        # Position ball such that its right side overlaps with brick's left side
        # Brick left is 200. Ball width is 20.
        # If ball.rect.right is > 200, it overlaps.
        # Let's put ball.rect.right at 201. So ball.x = 201 - 20 = 181.
        # Y needs to be within brick's vertical range. Brick y is 200 to 250.
        # Ball center y at 225.

        ball.rect.right = brick.rect.left + 5 # slight overlap
        ball.rect.centery = brick.rect.centery

        # Velocity moving right
        ball.velocity_x = 5
        ball.velocity_y = 0

        collided = ball.check_collision_with_bricks(bricks)

        assert brick in collided
        assert ball.velocity_x == -5 # Should reverse x
        assert ball.velocity_y == 0  # Should not change y

    def test_vertical_collision(self, ball, bricks):
        # Place a brick
        brick_x, brick_y = 200, 200
        brick = Brick(brick_x, brick_y)
        bricks.add(brick)

        # Position ball to hit the top of the brick
        # Ball bottom overlaps with brick top
        ball.rect.centerx = brick.rect.centerx
        ball.rect.bottom = brick.rect.top + 5 # slight overlap

        # Velocity moving down
        ball.velocity_x = 0
        ball.velocity_y = 5

        collided = ball.check_collision_with_bricks(bricks)

        assert brick in collided
        assert ball.velocity_x == 0  # Should not change x
        assert ball.velocity_y == -5 # Should reverse y

    def test_multiple_brick_collision(self, ball, bricks):
        # Place two bricks side by side
        brick1 = Brick(200, 200)
        brick2 = Brick(200 + settings.BRICK_WIDTH, 200)
        bricks.add(brick1)
        bricks.add(brick2)

        # Position ball to overlap both bricks, but closer to brick1
        # Place ball between them but slightly more into brick1

        ball.rect.centerx = brick1.rect.right
        ball.rect.centery = brick1.rect.centery

        # Move ball slightly left so it's closer to brick1 center
        ball.rect.centerx -= 5

        # Ensure it overlaps brick2 as well?
        # Brick width is large (Screen width // 8 = 100).
        # If ball is at right edge of brick1, it is close to brick2 left edge.
        # Let's just test that it hits brick1 and reflects

        # Let's re-strategize "multiple collision".
        # Often happens when ball hits the "crack" between bricks.
        # Let's place ball exactly between them.

        ball.rect.centerx = brick1.rect.right
        ball.rect.centery = brick1.rect.centery

        # If the ball is exactly on the line, distance to centers might be equal?
        # Let's make it clearly closer to brick 2 for this test
        ball.rect.centerx += 2

        ball.velocity_x = -5
        ball.velocity_y = 0

        collided = ball.check_collision_with_bricks(bricks)

        # It should collide with at least one
        assert len(collided) > 0

        # Physics should reflect based on the "nearest" one.
        # If it's hitting the side, x should flip.
        assert ball.velocity_x == 5
