# -*- coding: utf-8 -*-

from checkers.models import Checker, Board
from checkers.serialization import load_board_from_file


class GameError(Exception):
    """
    Something wrong while playing game
    """


class Game(object):
    def __init__(self, filename=None):
        if filename:
            self.board = load_board_from_file(filename)
        else:
            self.board = Board()

        self.white_player = Player(self, Checker.WHITE)
        self.black_player = Player(self, Checker.BLACK)

        self.current_player = self.white_player

    def turn(self):
        self.current_player.turn()

    def move(self, player, checker, x, y):
        assert player == self.current_player

        if checker.color != player.color:
            raise GameError("You can't move this checker.")

        move = get_move(self.board, checker, x, y)
        if move.type == Move.TYPE.WRONG:
            raise GameError("You can't move checker to this field.")

        if move.type == Move.TYPE.MOVE:
            self.board.move_checker(checker, x, y)
            self.check_become_king(checker)
            self.change_current_player()

        if move.type == Move.TYPE.KICK:
            self.board.move_checker(checker, x, y)
            self.board.remove_checker(move.victim)
            self.check_become_king(checker)
            available_moves = get_available_moves(self.board, checker)
            can_kick_again = any(move.type == Move.TYPE.KICK for move in available_moves)
            if not can_kick_again:
                self.change_current_player()

        return move

    def check_become_king(self, checker):
        if checker.is_king:
            return False

        if is_king_line(self.board, checker.color, checker.y):
            checker.make_king()

        return False

    def change_current_player(self):
        self.current_player = self.white_player if self.current_player == self.black_player else self.black_player


class Player(object):
    def __init__(self, game, color):
        self.game = game
        self.color = color

    def subscribe_for_turns(self, callback):
        self._subscriber = callback

    def turn(self):
        self._subscriber()

    def move(self, checker, x, y):
        self.game.move(self, checker, x, y)


class Move(object):
    class TYPE:
        WRONG = 0
        MOVE = 1
        KICK = 2

    def __init__(self, move_type, victim=None):
        self.type = move_type
        self.victim = victim


def get_move(board, checker, x, y):
    if not board.is_valid_field(x, y):
        return Move(Move.TYPE.WRONG)

    if board.get_checker_in_position(x, y) or not board.is_black_field(x, y):
        return Move(Move.TYPE.WRONG)

    dx = x - checker.x
    dy = y - checker.y
    x_direction = 1 if dx > 0 else -1
    y_direction = 1 if dy > 0 else -1

    if checker.is_king:
        if abs(dx) != abs(dy):
            return Move(Move.TYPE.WRONG)

        victims = []
        for i in xrange(1, abs(dx)):
            victim = board.get_checker_in_position(checker.x + i * x_direction, checker.y + i * y_direction)
            if victim:
                victims.append(victim)

        if len(victims) == 1:
            return Move(Move.TYPE.KICK, victims[0])

        return Move(Move.TYPE.MOVE)

    else:
        # kick
        if abs(dx) == abs(dy) == 2:
            victim = board.get_checker_in_position(checker.x + x_direction, checker.y + y_direction)
            if victim and victim.color != checker.color:
                return Move(Move.TYPE.KICK, victim)

        # check direction
        if checker.color == Checker.WHITE and dy < 0 or checker.color == Checker.BLACK and dy > 0:
            return Move(Move.TYPE.WRONG)

        # move forward
        if abs(dx) == abs(dy) == 1:
            return Move(Move.TYPE.MOVE)

        return Move(Move.TYPE.WRONG)


def get_available_moves(board, checker):
    available_moves = []
    for x in xrange(board.SIZE):
        for y in xrange(board.SIZE):
            move = get_move(board, checker, x, y)
            if move.type:
                available_moves.append((x, y))
    return available_moves


def is_king_line(board, color, y):
    if color == Checker.WHITE:
        return y == 0
    else:
        return y == board.SIZE - 1
