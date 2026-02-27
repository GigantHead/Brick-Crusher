import pytest
import pygame
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.brick import Brick
import settings

# Dummy video driver for headless environments
os.environ["SDL_VIDEODRIVER"] = "dummy"

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    try:
        pygame.init()
        yield
    finally:
        pygame.quit()

def test_brick_initialization():
    x, y = 100, 200
    brick = Brick(x, y)

    assert brick.rect.x == x
    assert brick.rect.y == y
    assert brick.real_y == float(y)
    assert brick.image.get_width() == settings.BRICK_WIDTH
    assert brick.image.get_height() == settings.BRICK_HEIGHT

def test_brick_update(mocker):
    """Test standard update behavior"""
    x, y = 100, 100
    brick = Brick(x, y)

    # Mock settings.BRICK_SPEED to be consistent for testing
    mocker.patch('settings.BRICK_SPEED', 10)

    dt = 0.5 # 0.5 seconds
    brick.update(dt)

    # Expected movement: 10 pixels/sec * 0.5 sec = 5 pixels
    assert brick.real_y == 105.0
    assert brick.rect.y == 105

def test_brick_update_accumulation(mocker):
    """Test that small updates accumulate correctly in real_y"""
    x, y = 100, 100
    brick = Brick(x, y)

    # Mock settings.BRICK_SPEED
    mocker.patch('settings.BRICK_SPEED', 10)

    # Small dt that results in < 1 pixel movement
    dt = 0.05 # 0.5 pixels
    brick.update(dt)

    assert brick.real_y == 100.5
    assert brick.rect.y == 100 # int(100.5) is 100

    # Another update
    brick.update(dt)

    assert brick.real_y == 101.0
    assert brick.rect.y == 101 # int(101.0) is 101
