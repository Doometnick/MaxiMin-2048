from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from board import Board, Direction


class GameDriver:

    def __init__(self):
        self.url = "https://hczhcz.github.io/2048/20ez/"
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.body = self.driver.find_element_by_tag_name("body")
        self.moves = {
            Direction.UP: Keys.ARROW_UP,
            Direction.DOWN: Keys.ARROW_DOWN,
            Direction.LEFT: Keys.ARROW_LEFT,
            Direction.RIGHT: Keys.ARROW_RIGHT
        }

    def getBoard(self) -> Board:
        board = Board()
        tiles = self.driver.find_elements_by_class_name("tile")

        for tile in tiles:
            cls = tile.get_attribute("class")
            col, row = cls.split("tile-position-")[1].split(" ")[0].split("-")
            col, row = int(col), int(row)
            num = int(cls.split("tile tile-")[1].split(" ")[0])
            row -= 1
            col -= 1
            if num > board.board[row, col]:
               board.board[row, col] = num 
            
        return board

    def move(self, direction: Direction):
        self.body.send_keys(self.moves[direction])
        time.sleep(0.2)
