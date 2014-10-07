# -*- coding: utf-8 -*-

"""
https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%88%D0%BA%D0%B8
"""

import json


class BoardError(Exception):
    """
    Something wrong with board
    """


def field_verbose(x, y):
    return "abcdefghij"[x] + str(y+1)


def save_board(board):
    checkers = [
        {
            'color': checker.color,
            'x': checker.x,
            'y': checker.y,
        }
        for checker in board.checkers
    ]
    board_data = {
        'checkers': checkers,
    }
    return json.dumps(board_data, indent=4)


def load_board(board_json):
    board = Board()
    for checker_data in json.loads(board_json)['checkers']:
        color = checker_data['color']
        x = checker_data['x']
        y = checker_data['y']

        if not Board.is_valid_field(x, y) or not color in [Checker.WHITE, Checker.BLACK]:
            raise ValueError(checker_data)

        board.add_checker(Checker(color, x, y))

    return board


class Board(object):
    SIZE = 8

    def __init__(self):
        self.checkers = []

    def add_checker(self, checker):
        if not self.is_valid_field(checker.x ,checker.y):
            raise BoardError("Invalid checker position: (%d, %d)." % (checker.x, checker.y))

        if self.get_checker_in_position(checker.x, checker.y):
            raise BoardError("Checker in %s already exists." % field_verbose(checker.x, checker.y))

        self.checkers.append(checker)

    def remove_checker(self, checker):
        if checker in self.checkers:
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


class Move(object):
    class Type:
        WRONG = 0
        MOVE = 1
        KICK = 2

    def __init__(self, move_type, victim=None):
        self.type = move_type
        self.victim = victim


class BoardManager(object):
    def __init__(self, board):
        self.board = board

    def get_move(self, checker, x, y):
        if not self.board.is_valid_field(x, y):
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

    def get_available_moves(self, checker):
        available_moves = []
        for x in xrange(self.board.SIZE):
            for y in xrange(self.board.SIZE):
                move = self.get_move(checker, x, y)
                if move.type:
                    available_moves.append((x, y))
        return available_moves


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
