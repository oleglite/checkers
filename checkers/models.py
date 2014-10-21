# -*- coding: utf-8 -*-
"""
https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%88%D0%BA%D0%B8
"""


class BoardError(Exception):
    """
    Something wrong with board
    """


def field_verbose(x, y):
    return "abcdefghij"[x] + str(y + 1)


class Board(object):
    SIZE = 8

    def __init__(self):
        self.checkers = []

    def add_checker(self, checker):
        self._check_free_field(checker.x, checker.y)
        self.checkers.append(checker)

    def move_checker(self, checker, x, y):
        self._check_free_field(x, y)
        if checker not in self.checkers:
            raise BoardError("This checker not on board, can't move it: %s." % checker)

        checker.move(x, y)

    def _check_free_field(self, x, y):
        if not self.is_valid_field(x, y):
            raise BoardError("Invalid checker position: (%d, %d)." % (x, y))

        if self.get_checker_in_position(x, y):
            raise BoardError("Checker in %s already exists." % field_verbose(x, y))

    def remove_checker(self, checker):
        if checker not in self.checkers:
            raise BoardError("This checker not on board, can't remove it: %s." % checker)
        self.checkers.remove(checker)

    def get_checker_in_position(self, x, y):
        for checker in self.checkers:
            if checker.x == x and checker.y == y:
                return checker
        return None

    @staticmethod
    def is_black_field(x, y):
        return (x + y + 1) % 2

    @classmethod
    def is_valid_field(cls, x, y):
        return cls.is_black_field(x, y) and 0 <= x < cls.SIZE and 0 <= y < cls.SIZE


class Checker(object):
    BLACK = 'black'
    WHITE = 'white'

    def __init__(self, color, x, y):
        assert color == self.BLACK or color == self.WHITE

        self.x = x
        self.y = y
        self.color = color
        self.is_king = False

    def move(self, x, y):
        self.x = x
        self.y = y

    def make_king(self):
        self.is_king = True

    def __str__(self):
        return "%s checker in %s".capitalize() % (self.color, field_verbose(self.x, self.y))
