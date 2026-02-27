import pytest
import pygame
import math
from game.ball import Ball
from game.paddle import Paddle

@pytest.fixture
def ball_paddle():
    pygame.init()
    ball = Ball()
    paddle = Paddle()
    return ball, paddle

def test_no_collision(ball_paddle):
    ball, paddle = ball_paddle
    ball.rect.center = (100, 100)
    paddle.rect.center = (300, 300)

    initial_vx = ball.velocity_x
    initial_vy = ball.velocity_y

    ball.check_collision_with_paddle(paddle)

    assert ball.velocity_x == initial_vx
    assert ball.velocity_y == initial_vy

def test_center_collision(ball_paddle):
    ball, paddle = ball_paddle
    # Place ball directly above paddle center
    paddle.rect.centerx = 400
    paddle.rect.centery = 500
    ball.rect.centerx = 400
    ball.rect.centery = 500  # Overlapping

    ball.check_collision_with_paddle(paddle)

    # Hitting center means offset is 0, angle is 0
    # sin(0) = 0, cos(0) = 1
    # vx = 0, vy = -speed
    assert math.isclose(ball.velocity_x, 0, abs_tol=1e-9)
    assert math.isclose(ball.velocity_y, -ball.speed, abs_tol=1e-9)

def test_left_side_collision(ball_paddle):
    ball, paddle = ball_paddle
    paddle.rect.centerx = 400
    paddle.rect.centery = 500

    # Hit left side (negative offset)
    ball.rect.centerx = 380
    ball.rect.centery = 500

    ball.check_collision_with_paddle(paddle)

    assert ball.velocity_x < 0
    assert ball.velocity_y < 0 # Moving up

def test_right_side_collision(ball_paddle):
    ball, paddle = ball_paddle
    paddle.rect.centerx = 400
    paddle.rect.centery = 500

    # Hit right side (positive offset)
    ball.rect.centerx = 420
    ball.rect.centery = 500

    ball.check_collision_with_paddle(paddle)

    assert ball.velocity_x > 0
    assert ball.velocity_y < 0 # Moving up

def test_velocity_magnitude(ball_paddle):
    ball, paddle = ball_paddle
    paddle.rect.centerx = 400
    paddle.rect.centery = 500

    # Test various collision points
    offsets = [-40, -20, 0, 20, 40]

    for offset in offsets:
        ball.rect.centerx = 400 + offset
        ball.rect.centery = 500

        ball.check_collision_with_paddle(paddle)

        speed = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
        assert math.isclose(speed, ball.speed, abs_tol=1e-9)
