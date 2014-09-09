# -*- coding: utf-8 -*-

"""
https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%88%D0%BA%D0%B8
"""


class Board(object):
    def __init__(self, checkers):
        self.checkers = checkers

    def get_checker_in_position(self, x, y):
        for checker in self.checkers:
            if checker.x == x and checker.y == y:
                return checker
        return None

    def is_move_allowed(self, checker, x, y):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False

        if self.get_checker_in_position(x, y) or not self.is_black_field(x, y):
            return False

        if checker.is_king():
            pass
        else:
            if checker.color == Checker.WHITE:
                # ход вперед
                if y > checker.y:
                    return False

                # бить вперед
                # бить назад

    def is_black_field(self, x, y):
        return (x + y + 1) % 2


class BoardManager(object):
    def __init__(self, board):
        self.board = board


class Checker(object):
    BLACK = 'black'
    WHITE = 'white'

    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.is_king = False

    def move(self, x, y):
        self.x = x
        self.y = y

    def make_king(self):
        self.is_king = True
