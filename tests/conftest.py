import os
import pygame
import pytest

@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    yield
    pygame.quit()
