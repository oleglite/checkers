# -*- coding: utf-8 -*-

from collections import defaultdict
from copy import deepcopy

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

        if (x, y) not in get_available_fields_for_checker(self.board, checker):
            raise GameError("You must kick.")

        if move.type == Move.TYPE.MOVE:
            self.board.move_checker(checker, x, y)
            became_king = self._check_become_king(checker)
            if not became_king or not self._can_kick_again(checker):
                self._change_current_player()

        if move.type == Move.TYPE.KICK:
            self.board.move_checker(checker, x, y)
            self.board.remove_checker(move.victim)
            self._check_become_king(checker)
            if not self._can_kick_again(checker):
                self._change_current_player()

        return move

    def _check_become_king(self, checker):
        if not checker.is_king and is_king_line(self.board, checker.color, checker.y):
            checker.make_king()
            return True
        return False

    def _change_current_player(self):
        self.current_player = self.white_player if self.current_player == self.black_player else self.black_player

    def _can_kick_again(self, checker):
        available_move_fields = get_available_fields_for_checker(self.board, checker)
        can_kick_again = any(get_move(self.board, checker, new_x, new_y).type == Move.TYPE.KICK
                             for new_x, new_y in available_move_fields)
        return can_kick_again


class Player(object):
    def __init__(self, game, color):
        self.game = game
        self.color = color

    def subscribe_for_turns(self, callback):
        self._subscriber = callback

    def turn(self):
        self._subscriber()

    def move(self, checker, x, y):
        return self.game.move(self, checker, x, y)


class Move(object):
    class TYPE:
        WRONG = 0
        MOVE = 1
        KICK = 2

    NAMES = {
        TYPE.WRONG: 'Wrong',
        TYPE.MOVE: 'Move',
        TYPE.KICK: 'Kick'
    }

    def __init__(self, move_type, victim=None):
        self.type = move_type
        self.victim = victim

    def __str__(self):
        result = 'Move: %s' % self.NAMES[self.type].upper()
        if self.victim:
            result += ', Victim: %s' % self.victim
        return result


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
            if victims[0].color == checker.color:
                return Move(Move.TYPE.WRONG)
            else:
                return Move(Move.TYPE.KICK, victims[0])

        if len(victims) > 1:
            return Move(Move.TYPE.WRONG)

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


def _get_available_moves(board, checker):
    available_moves = defaultdict(list)
    for x in xrange(board.SIZE):
        for y in xrange(board.SIZE):
            move = get_move(board, checker, x, y)
            if move.type:
                available_moves[move.type].append((x, y))
    return available_moves


def _get_available_move_fields(board, checker):
    available_moves = _get_available_moves(board, checker)

    kick_moves = available_moves[Move.TYPE.KICK]
    if kick_moves:
        kick_moves_2 = []
        for move_field in kick_moves:
            board_copy = deepcopy(board)
            checker_copy = board_copy.get_checker_in_position(checker.x, checker.y)
            board_copy.move_checker(checker_copy, *move_field)
            available_moves_2 = _get_available_moves(board_copy, checker_copy)
            if available_moves_2[Move.TYPE.KICK]:
                kick_moves_2.append(move_field)

        return kick_moves_2 or kick_moves, Move.TYPE.KICK

    return available_moves[Move.TYPE.MOVE], Move.TYPE.MOVE


def get_available_moves_all_checkers(board, color):
    move_fields = {}
    for checker in board.get_checkers(color):
        available_fields, move_type = _get_available_move_fields(board, checker)
        move_fields.setdefault(move_type, []).append((checker, available_fields))

    return move_fields.get(Move.TYPE.KICK) or move_fields.get(Move.TYPE.MOVE, [])


def get_available_fields_for_checker(board, checker):
    available_moves = get_available_moves_all_checkers(board, checker.color)
    for moves_for_checker, available_fields in available_moves:
        if moves_for_checker == checker:
            return available_fields
    return []


def is_king_line(board, color, y):
    if color == Checker.WHITE:
        return y == board.SIZE - 1
    else:
        return y == 0
