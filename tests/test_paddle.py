import os
# Ensure pygame doesn't try to open a window
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from game.paddle import Paddle
import settings

@pytest.fixture
def paddle():
    pygame.init()
    yield Paddle()
    pygame.quit()

def test_initial_position(paddle):
    # Paddle initializes at center of screen width, 100 pixels from bottom
    assert paddle.rect.centerx == settings.SCREEN_WIDTH // 2
    assert paddle.rect.centery == settings.SCREEN_HEIGHT - 100

def test_move_right(paddle):
    initial_x = paddle.rect.x
    paddle.move(1)
    assert paddle.rect.x == initial_x + paddle.speed

def test_move_left(paddle):
    initial_x = paddle.rect.x
    paddle.move(-1)
    assert paddle.rect.x == initial_x - paddle.speed

def test_left_boundary(paddle):
    # Move paddle to the far left
    paddle.rect.x = -100
    paddle.move(-1) # Try to move further left
    assert paddle.rect.x == 0 # Should be clamped to 0

def test_right_boundary(paddle):
    # Move paddle to the far right
    paddle.rect.x = settings.SCREEN_WIDTH + 100
    paddle.move(1) # Try to move further right
    assert paddle.rect.right == settings.SCREEN_WIDTH # Should be clamped to screen width
