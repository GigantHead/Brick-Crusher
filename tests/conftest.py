import os
import sys
import pytest
import pygame

# Set SDL_VIDEODRIVER to dummy to avoid "No available video device" error
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    pygame.init()
    # Create a dummy display to support Surface creation if needed
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()
