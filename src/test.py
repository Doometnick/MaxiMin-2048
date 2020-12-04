from board import Direction
import board


if __name__ == "__main__":

    b = board.Board()
    b.place(0, 2, 8)
    b.place(3, 2, 8)
    b.place(3, 1, 4)
    b.place(3, 0, 2)
    print(b.board)
    b.move(Direction.UP)
    print(b.board)
    b.move(Direction.DOWN)
    print(b.board)
