import unittest
from unittest.mock import MagicMock, patch
import settings
from game.game import Game

class TestGame(unittest.TestCase):
    @patch('game.game.pygame')
    @patch('game.game.Paddle')
    @patch('game.game.Ball')
    def test_reset_game(self, MockBall, MockPaddle, mock_pygame):
        # Setup mocks
        mock_pygame.display.set_mode.return_value = MagicMock()
        mock_pygame.time.Clock.return_value = MagicMock()
        mock_pygame.font.Font.return_value = MagicMock()
        mock_group = MagicMock()
        mock_pygame.sprite.Group.return_value = mock_group

        # Instantiate Game (calls reset_game internally)
        game = Game()

        # Verify initial call during __init__
        MockPaddle.assert_called()
        MockBall.assert_called()
        mock_pygame.sprite.Group.assert_called()

        # Modify state to verify reset behavior
        game.game_over = True
        game.active = False
        game.paddle = None
        game.ball = None
        game.bricks = None

        # Reset mocks to ensure we are capturing the new calls
        MockPaddle.reset_mock()
        MockBall.reset_mock()
        mock_pygame.sprite.Group.reset_mock()

        # Call reset_game
        game.reset_game()

        # Verify Paddle and Ball are re-initialized
        MockPaddle.assert_called_once()
        MockBall.assert_called_once()
        self.assertIsNotNone(game.paddle)
        self.assertIsNotNone(game.ball)

        # Verify Bricks group is re-initialized
        mock_pygame.sprite.Group.assert_called_once()
        self.assertEqual(game.bricks, mock_group)

        # Verify game state flags
        self.assertFalse(game.game_over)
        self.assertTrue(game.active)

        # Verify brick frequency calculation
        vertical_gap = settings.BRICK_HEIGHT * 2
        expected_frequency = (vertical_gap / settings.BRICK_SPEED) * 1000
        self.assertEqual(game.brick_frequency, expected_frequency)

if __name__ == '__main__':
    unittest.main()
