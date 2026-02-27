import pytest
import pygame
import math
from game.ball import Ball
from game.brick import Brick
import settings

# Initialize pygame for headless testing
pygame.display.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)

@pytest.fixture
def ball():
    return Ball()

@pytest.fixture
def brick():
    return Brick(100, 100)

def test_collision_top(ball, brick):
    # Ball is above the brick, moving down
    ball.rect.center = (100 + settings.BRICK_WIDTH // 2, 90)
    ball.velocity_x = 0
    ball.velocity_y = 5

    collision_point = ball.get_collision_point(brick)

    # Expected intersection is roughly at the top edge of the brick
    expected_y = brick.rect.top
    assert math.isclose(collision_point.y, expected_y, abs_tol=1.0)
    assert settings.BRICK_WIDTH // 2 <= collision_point.x - 100 <= settings.BRICK_WIDTH // 2 + 1 # Close to center x

def test_collision_bottom(ball, brick):
    # Ball is below the brick, moving up
    ball.rect.center = (100 + settings.BRICK_WIDTH // 2, 100 + settings.BRICK_HEIGHT + 10)
    ball.velocity_x = 0
    ball.velocity_y = -5

    collision_point = ball.get_collision_point(brick)

    # Expected intersection is roughly at the bottom edge of the brick
    expected_y = brick.rect.bottom
    assert math.isclose(collision_point.y, expected_y, abs_tol=1.0)

def test_collision_left(ball, brick):
    # Ball is to the left, moving right
    ball.rect.center = (90, 100 + settings.BRICK_HEIGHT // 2)
    ball.velocity_x = 5
    ball.velocity_y = 0

    collision_point = ball.get_collision_point(brick)

    # Expected intersection is roughly at the left edge of the brick
    expected_x = brick.rect.left
    assert math.isclose(collision_point.x, expected_x, abs_tol=1.0)

def test_collision_right(ball, brick):
    # Ball is to the right, moving left
    ball.rect.center = (100 + settings.BRICK_WIDTH + 10, 100 + settings.BRICK_HEIGHT // 2)
    ball.velocity_x = -5
    ball.velocity_y = 0

    collision_point = ball.get_collision_point(brick)

    # Expected intersection is roughly at the right edge of the brick
    expected_x = brick.rect.right
    assert math.isclose(collision_point.x, expected_x, abs_tol=1.0)

def test_no_intersection(ball, brick):
    # Ball is far away and moving away
    ball.rect.center = (0, 0)
    ball.velocity_x = -5
    ball.velocity_y = -5

    collision_point = ball.get_collision_point(brick)

    # Should return center if no intersection found (based on current implementation)
    assert collision_point == pygame.math.Vector2(ball.rect.center)
