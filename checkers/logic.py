# -*- coding: utf-8 -*-

from checkers.models import Checker


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

        if checker.is_king:
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
