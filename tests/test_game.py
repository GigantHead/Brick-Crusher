import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adjust path to include the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import settings

class TestGame(unittest.TestCase):

    def setUp(self):
        # Create patchers for pygame and Game dependencies
        self.patchers = {
            'pygame.init': patch('game.game.pygame.init'),
            'pygame.display.set_mode': patch('game.game.pygame.display.set_mode'),
            'pygame.time.Clock': patch('game.game.pygame.time.Clock'),
            'pygame.font.Font': patch('game.game.pygame.font.Font'),
            'pygame.sprite.Group': patch('game.game.pygame.sprite.Group'),
            'Paddle': patch('game.game.Paddle'),
            'Ball': patch('game.game.Ball'),
            'Brick': patch('game.game.Brick')
        }

        # Start all patchers
        self.mocks = {}
        for name, p in self.patchers.items():
            self.mocks[name] = p.start()

        # Import Game class
        from game.game import Game
        self.GameClass = Game

    def tearDown(self):
        # Stop all patchers
        for p in self.patchers.values():
            p.stop()

    def test_add_brick_row(self):
        """Test that add_brick_row adds the correct number of bricks to the sprite group."""

        # Instantiate the Game class with mocks in place
        game = self.GameClass()

        # Access the mocked Brick class
        BrickMock = self.mocks['Brick']

        # Reset mocks to ensure a clean slate (though initialization shouldn't have called them yet ideally)
        BrickMock.reset_mock()
        game.bricks.add.reset_mock()

        # Call the method under test
        game.add_brick_row()

        # Calculate expected number of bricks
        expected_brick_count = settings.SCREEN_WIDTH // settings.BRICK_WIDTH

        # Verify that Brick constructor was called the expected number of times
        self.assertEqual(BrickMock.call_count, expected_brick_count)

        # Verify that game.bricks.add was called the expected number of times
        self.assertEqual(game.bricks.add.call_count, expected_brick_count)

if __name__ == '__main__':
    unittest.main()
