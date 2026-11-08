import sys
import types
import unittest

# The game imports OpenCV for drawing. Strategy tests do not render frames,
# so a tiny stand-in lets them run on headless machines without a GUI build.
try:
    import cv2  # noqa: F401
except ImportError:
    sys.modules["cv2"] = types.ModuleType("cv2")

from game_manager import GameManager
from pathfinding import AStarPathfinder
from strategies import AStarGhostBrain, AutoPacManBrain


class StrategyTests(unittest.TestCase):
    def setUp(self):
        self.game = GameManager(
            AutoPacManBrain(),
            [AStarGhostBrain()],
        )

    def test_astar_path_is_legal(self):
        start = (8, 8)
        goal = (1, 1)
        state = self.game._state()
        path = AStarPathfinder(state).shortest_path(start, goal)

        self.assertGreaterEqual(len(path), 2)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        for first, second in zip(path, path[1:]):
            self.assertIn((first, second), state.legal_moves)

    def test_auto_pacman_clears_the_board(self):
        for _ in range(1000):
            self.game.step()
            if self.game.status != GameManager.RUNNING:
                break

        self.assertEqual(self.game.status, GameManager.WIN)
        self.assertEqual(len(self.game.bean_list), 0)


if __name__ == "__main__":
    unittest.main()
