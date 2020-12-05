import unittest
from board import Direction, Board
import tests.testdata as testdata

class TestMoving(unittest.TestCase):

    def test_moving(self):
        for board_in, action, board_expected in testdata.moving_tests:
            board = Board(board_in)
            board.move(action)
            try:
                self.assertTrue(board == Board(board_expected))
            except AssertionError:
                print(f"Input board \n{Board(board_in).board}")
                print(f"Move {action}")
                print(f"Output: \n{board.board}")
                print(f"Expected output: \n{Board(board_expected).board}")
                raise
