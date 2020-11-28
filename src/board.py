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

    # TODO: np.rot90 enables to do checks/movements with less code, but is
    # not very efficient as it copies the board variable each time.
    # write own in-place method for rotation.

    def __init__(self, size: int):
        self.board = np.zeros((size, size))
        self.size = size

    def __str__(self):
        return str(self.board)
    
    def __repr__(self):
        return self.board
    
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

    def available_moves_for_player(self) -> List[Direction]:
        """ Returns directions in which the player can move.
        These are a collection of up, down, left, right directions.
        """
        ans = []
        if self.can_move(Direction.UP):
            ans.append(Direction.UP)
        if self.can_move(Direction.DOWN):
            ans.append(Direction.DOWN)
        if self.can_move(Direction.LEFT):
            ans.append(Direction.LEFT)
        if self.can_move(Direction.RIGHT):
            ans.append(Direction.RIGHT)
        return ans

    def available_moves_for_game(self) -> List[Tuple[int]]:
        """ Returns list of available moves for the game.
        The game's 'moves' are to place new stones into empty tiles.
        We assume that the game can only place stones with a value of 2 or 4.

        Returns:
            tuple(row, col, value)
        """
        ans = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] == 0:
                    ans.append((r, c, 2))
                    ans.append((r, c, 4))
        return ans

    def player_cannot_move_anymore(self) -> bool:
        if self.can_move(Direction.UP):
            return False
        if self.can_move(Direction.DOWN):
            return False
        if self.can_move(Direction.LEFT):
            return False
        if self.can_move(Direction.RIGHT):
            return False
        return True
    
    def board_is_full(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] == 0:
                    return False
        return True

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.board = self.move_left(self.board)
        elif direction == Direction.UP:
            board = self.move_left(np.rot90(self.board, 1))
            self.board = np.rot90(board, 3)
        elif direction == Direction.RIGHT:
            board = self.move_left(np.rot90(self.board, 2))
            self.board = np.rot90(board, 2)
        elif direction == Direction.DOWN:
            board = self.move_left(np.rot90(self.board, 3))
            self.board = np.rot90(board, 1)


    def move_left(self, board: np.array) -> np.array:
        """ Moves all the stones to the left.
        Stones of equal value will be merged.
        """
        for r in range(self.size):
            for c in range(1, self.size):
                k = c - 1
                while k >= 0:
                    if board[r, k] > 0 and board[r, k] == board[r, c]:
                        board[r, k] *= 2
                        board[r, c] = 0
                        break
                    elif board[r, k] > 0 and k < c:
                        board[r, k + 1] = board[r, c]
                        board[r, c] = 0
                        break
                    k -= 1
        return board