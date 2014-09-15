# -*- coding: utf-8 -*-

"""
https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%88%D0%BA%D0%B8
"""


class Board(object):
    SIZE = 8

    def __init__(self, checkers):
        self.checkers = checkers

    def get_checker_in_position(self, x, y):
        for checker in self.checkers:
            if checker.x == x and checker.y == y:
                return checker
        return None

    def is_black_field(self, x, y):
        return (x + y + 1) % 2


class Move(object):
    class Type:
        WRONG = 0
        MOVE = 1
        KICK = 2

    def __init__(self, move_type, victim=None):
        self.move_type = move_type
        self.victim = victim


class BoardManager(object):
    def __init__(self, board):
        self.board = board

    def get_move(self, checker, x, y):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return Move(Move.Type.WRONG)

        if self.board.get_checker_in_position(x, y) or not self.board.is_black_field(x, y):
            return Move(Move.Type.WRONG)

        dx = x - checker.x
        dy = y - checker.y
        x_direction = 1 if dx > 0 else -1
        y_direction = 1 if dy > 0 else -1

        if checker.is_king():
            if abs(dx) != abs(dy):
                return Move(Move.Type.WRONG)

            victims = []
            for i in xrange(1, abs(dx)):
                victim = self.board.get_checker_in_position(checker.x + i * x_direction, checker.y + i * y_direction)
                if victim:
                    victims.append(victim)

            if len(victims) == 1:
                return Move(Move.Type.KICK, victims[0])

            return Move(Move.Type.MOVE)

        else:
            # kick
            if abs(dx) == abs(dy) == 2:
                victim = self.board.get_checker_in_position(checker.x + x_direction, checker.y + y_direction)
                if victim and victim.color != checker.color:
                    return Move(Move.Type.KICK, victim)

            # check direction
            if checker.color == Checker.WHITE and dy < 0 or checker.color == Checker.BLACK and dy > 0:
                return Move(Move.Type.WRONG)

            # move forward
            if abs(dx) == abs(dy) == 1:
                return Move(Move.Type.MOVE)

            return Move(Move.Type.WRONG)


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
