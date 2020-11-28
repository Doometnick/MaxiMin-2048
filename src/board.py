import numpy as np
from enum import Enum
from copy import deepcopy
from typing import Tuple, List
import logging

log = logging.getLogger(__name__)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Board:

    def __init__(self, size: int):
        self.board = np.zeros((size, size))
        self.size = size

    def get_copy(self) -> np.array:
        return deepcopy(self.board)
    
    def place(self, row: int, col: int, value: int) -> None:
        self.board[row, col] = value

    def can_move(self, direction: Direction) -> bool:
        """ Returns True if a move in a certain direction is possible,
        False otherwise.
        """
        if direction == Direction.UP:
            return self._can_move_up(self.board)
        elif direction == direction.LEFT:
            return self._can_move_up(np.rot90(self.board, 3))
        elif direction == direction.DOWN:
            return self._can_move_up(np.rot90(self.board, 2))
        elif direction == direction.RIGHT:
            return self._can_move_up(np.rot90(self.board, 1))

    def _can_move_up(self, board: np.array) -> bool:
        """ For every colum in the grid, check if there is at least one
        tile that can be moved upwards.
        """
        n = self.size
        for c in range(n):
            k = -1
            for r in range(n - 1, -1, -1):
                if board[r,c] >  0:
                    k = r
                    break
            if k > -1:
                for r in range(k, 0, -1):
                    if board[r - 1, c] == 0 or board[r, c] == board[r - 1, c]:
                        return True
        return False
