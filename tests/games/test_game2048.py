""" Test class for Game2048 class """

import unittest

from games.game2048.game2048 import Game2048, Action

class Game2048Test(unittest.TestCase):
    """ Test class for Game2048 class """

    def test_process_move(self):
        """ test the entire grid """
        original_grid = [[2, 0, 2, 0],
                         [2, 2, 4, 0],
                         [2, 2, 0, 4],
                         [2, 2, 4, 4]]
        updated_grid = [[4, 4, 2, 8],
                        [4, 2, 8, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]

        self.assertTrue(Game2048Test.process_move(original_grid, Action.UP) == updated_grid)

    def test_process_row_left(self):
        """ process row test cases (LEFT Action) """
        # LEFT
        self.assertTrue(Game2048.process_row([0, 0, 0, 2], Action.LEFT) == [2, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 0, 2, 0], Action.LEFT) == [2, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 2, 0, 0], Action.LEFT) == [2, 0, 0, 0])
        self.assertTrue(Game2048.process_row([2, 0, 0, 0], Action.LEFT) == [2, 0, 0, 0])
        self.assertTrue(Game2048.process_row([4, 2, 0, 0], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([2, 2, 0, 0], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([4, 0, 2, 0], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([2, 0, 2, 0], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([4, 0, 0, 2], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([2, 0, 0, 4], Action.LEFT) == [2, 4, 0, 0])
        self.assertTrue(Game2048.process_row([2, 0, 0, 2], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 2, 0, 2], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 4, 0, 4], Action.LEFT) == [8, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 0, 2, 2], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([0, 2, 2, 0], Action.LEFT) == [4, 0, 0, 0])
        self.assertTrue(Game2048.process_row([4, 0, 8, 2], Action.LEFT) == [4, 8, 2, 0])
        self.assertTrue(Game2048.process_row([2, 0, 2, 2], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([4, 2, 0, 8], Action.LEFT) == [4, 2, 8, 0])
        self.assertTrue(Game2048.process_row([4, 4, 0, 4], Action.LEFT) == [8, 4, 0, 0])
        self.assertTrue(Game2048.process_row([2, 2, 2, 0], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([0, 2, 2, 2], Action.LEFT) == [4, 2, 0, 0])
        self.assertTrue(Game2048.process_row([0, 2, 4, 2], Action.LEFT) == [2, 4, 2, 0])
        self.assertTrue(Game2048.process_row([0, 4, 4, 2], Action.LEFT) == [8, 2, 0, 0])
        self.assertTrue(Game2048.process_row([4, 2, 8, 2], Action.LEFT) == [4, 2, 8, 2])
        self.assertTrue(Game2048.process_row([2, 4, 4, 2], Action.LEFT) == [2, 8, 2, 0])
        self.assertTrue(Game2048.process_row([8, 8, 8, 8], Action.LEFT) == [16, 16, 0, 0])

    def test_process_row_right(self):
        """ process row test cases (RIGHT Action) """
        #RIGHT
        self.assertTrue(Game2048.process_row([0, 0, 0, 2], Action.RIGHT) == [0, 0, 0, 2])
        self.assertTrue(Game2048.process_row([0, 0, 2, 0], Action.RIGHT) == [0, 0, 0, 2])
        self.assertTrue(Game2048.process_row([0, 2, 0, 0], Action.RIGHT) == [0, 0, 0, 2])
        self.assertTrue(Game2048.process_row([2, 0, 0, 0], Action.RIGHT) == [0, 0, 0, 2])
        self.assertTrue(Game2048.process_row([4, 2, 0, 0], Action.RIGHT) == [0, 0, 4, 2])
        self.assertTrue(Game2048.process_row([2, 2, 0, 0], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([4, 0, 2, 0], Action.RIGHT) == [0, 0, 4, 2])
        self.assertTrue(Game2048.process_row([2, 0, 2, 0], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([4, 0, 0, 2], Action.RIGHT) == [0, 0, 4, 2])
        self.assertTrue(Game2048.process_row([2, 0, 0, 4], Action.RIGHT) == [0, 0, 2, 4])
        self.assertTrue(Game2048.process_row([2, 0, 0, 2], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([0, 2, 0, 2], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([0, 4, 0, 4], Action.RIGHT) == [0, 0, 0, 8])
        self.assertTrue(Game2048.process_row([0, 0, 2, 2], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([0, 2, 2, 0], Action.RIGHT) == [0, 0, 0, 4])
        self.assertTrue(Game2048.process_row([4, 0, 8, 2], Action.RIGHT) == [0, 4, 8, 2])
        self.assertTrue(Game2048.process_row([2, 0, 2, 2], Action.RIGHT) == [0, 0, 2, 4])
        self.assertTrue(Game2048.process_row([4, 2, 0, 8], Action.RIGHT) == [0, 4, 2, 8])
        self.assertTrue(Game2048.process_row([4, 4, 0, 4], Action.RIGHT) == [0, 0, 4, 8])
        self.assertTrue(Game2048.process_row([2, 2, 2, 0], Action.RIGHT) == [0, 0, 2, 4])
        self.assertTrue(Game2048.process_row([0, 2, 2, 2], Action.RIGHT) == [0, 0, 2, 4])
        self.assertTrue(Game2048.process_row([0, 2, 4, 2], Action.RIGHT) == [0, 2, 4, 2])
        self.assertTrue(Game2048.process_row([0, 4, 4, 2], Action.RIGHT) == [0, 0, 8, 2])
        self.assertTrue(Game2048.process_row([4, 2, 8, 2], Action.RIGHT) == [4, 2, 8, 2])
        self.assertTrue(Game2048.process_row([2, 4, 4, 2], Action.RIGHT) == [0, 2, 8, 2])
        self.assertTrue(Game2048.process_row([8, 8, 8, 8], Action.RIGHT) == [0, 0, 16, 16])
