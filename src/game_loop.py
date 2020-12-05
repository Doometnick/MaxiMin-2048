from board import Board, Direction
from game_driver import GameDriver
from minimax import get_best_move

MAX_DEPTH = 5

game_driver = GameDriver()
moves = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
moves_count = 1


if __name__ == "__main__":

    while True:
        board = game_driver.getBoard()
        if board.game_over():
            print("Game Over.")
            break
        if board.game_won():
            print("You won!")
            break
        move, util = get_best_move(board, MAX_DEPTH)
        print(f"Move {moves_count}: {move} - utility {round(util, 2)}")
        game_driver.move(move)
        moves_count += 1
