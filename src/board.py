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

    def __init__(self, board: np.array = None, size: int = 4):
        if board is None:
            self.board = np.zeros((size, size))
        else:
            self.board = board
            if type(self.board) != np.array:
                self.board = np.array(board)
        self.size = len(self.board)

    def __str__(self):
        return str(self.board)
    
    def __repr__(self):
        return self.board
    
    def __eq__(self, other):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] != other.board[r, c]:
                    return False
        return True

    def utility(self) -> float:
        count = 0
        sum = 0
        for r in range(self.size):
            for c in range(self.size):
                sum += self.board[r, c]
                if self.board[r, c] != 0:
                    count += 1
        return sum / count

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
                if board[r,c] > 0:
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
        for r in range(self.size):
            for c in range(1, self.size):
                if board[r, c] == 0:
                    continue
                k = c - 1
                while k >= 0:
                    if board[r, k] == board[r, c]:
                        board[r, k] *= 2
                        board[r, c] = 0
                        break
                    elif board[r, k] > 0 and k != c - 1:
                        board[r, k + 1] = board[r, c] 
                        board[r, c]  = 0
                        break
                    k -= 1

                if k == -1 and board[r, 0] == 0:
                    board[r, 0] = board[r, c]
                    board[r, c] = 0
        return board

    def game_over(self) -> bool:
        return self.player_cannot_move_anymore()
    
    def game_won(self) -> bool:
        return self.board_contains_stone(2048)
    
    def board_contains_stone(self, x: int):
        return x in self.board

    def get_move_to_grid(self, board: 'Board') -> Direction:
        """ Returns direction in which to move in order
        to achieve the grid that is given as parameter.
        """
        b = Board(board=self.get_copy())
        if self.can_move(Direction.UP):
            b.move(Direction.UP)
            if b == board:
                return Direction.UP
            b = Board(board=self.get_copy())
        if self.can_move(Direction.DOWN):
            b.move(Direction.DOWN)
            if b == board:
                return Direction.DOWN
            b = Board(board=self.get_copy())
        if self.can_move(Direction.LEFT):
            b.move(Direction.LEFT)
            if b == board:
                return Direction.LEFT
        return Direction.RIGHT