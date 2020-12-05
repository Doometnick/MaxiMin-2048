from typing import Tuple, List
from sys import maxsize as MAX_INT
from board import Board, Direction


def maximize(state: Board, a: int, b: int, d: int) -> Tuple[Board, int]:
    max_child, max_util = None, -1

    if d == 0 or state.player_cannot_move_anymore():
        return None, state.utility()
    
    for direction in state.available_moves_for_player():
        board = Board()
        board.board = state.get_copy()
        board.move(direction)
        _, util = minimize(board, a, b, d - 1)
        if util > max_util:
            max_child, max_util = board, util
        if max_util >= b:
            break
        if max_util > a:
            a = max_util
    
    return max_child, max_util


def minimize(state: Board, a: int, b:int, d: int) -> Tuple[Board, int]:
    min_child, min_util = None, MAX_INT

    if d == 0 or state.board_is_full():
        return None, state.utility()
    
    for row, col, value in state.available_moves_for_game():
        board = Board()
        board.board = state.get_copy()
        board.place(row, col, value)
        _, util = maximize(board, a, b, d - 1)
        if util < min_util:
            min_child, min_util = board, util
        if min_util <= a:
            break
        if min_util < b:
            b = min_util
    
    return min_child, min_util


def get_best_move(board: Board, depth: int = 5):
    child, util = maximize(Board(board.get_copy()), -1, MAX_INT, depth)
    return board.get_move_to_grid(child), util
