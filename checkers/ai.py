# -*- coding: utf-8 -*-

from random import choice
from copy import deepcopy

from checkers.logic import get_move, Move, get_available_moves_all_checkers

MAX_RECURSION = 3


def calculate_ai_move(board, ai_color, player_color):
    results = minimax(board, ai_color, player_color)
    result = choice(results)
    for r in results:
        print r
    return result.move_coords[0]


def minimax(board, ai_color, player_color, recursion_level=0):
    """
    return (move_coords, result_tuple)
    move_coords = (x1, y1, x2, y2)
    result_tuple = (result, ai_kicks, -player_kicks)
    """
    recursion_level += 1

    if recursion_level == MAX_RECURSION:
        return [Result(Result.TYPE.UNKNOWN)]

    color = ai_color if recursion_level % 2 else player_color

    results = [
        # (move_coords, result_tuple),
    ]

    for checker, available_fields in get_available_moves_all_checkers(board, color):
        for field in available_fields:
            board_copy = deepcopy(board)

            move_coords = (checker.x, checker.y, field[0], field[1])
            move = get_move(board_copy, checker, *field)
            board_copy.move(*move_coords)

            winner = board_copy.get_winner()
            if winner:
                result_type = Result.TYPE.WIN if color == ai_color else Result.TYPE.LOSE
                return [Result(result_type, (checker.x, checker.y, field[0], field[1]))]

            turn_results = minimax(board_copy, ai_color, player_color, recursion_level)

            turn = Result.TURN.NONE
            if move.type == Move.TYPE.KICK:
                turn = Result.TURN.AI_KICK if color == ai_color else Result.TURN.PLAYER_KICK

            for result in turn_results:
                result.add_turn(move_coords, turn)
            results.extend(turn_results)

    if not results:
        return [Result(Result.TYPE.SKIP)]

    good_results = [r for r in results if r.score_ai > r.score_player]
    if good_results:
        results = good_results

    fn = max if color == ai_color else min
    best_result = fn(results, key=lambda r: r.key())
    best_results = [result for result in results if result.key() == best_result.key()]
    return best_results


class Result(object):
    class TYPE:
        WIN = 4
        UNKNOWN = 3
        DRAW = 2
        LOSE = 1
        SKIP = 0

    class TURN:
        AI_KICK = 1
        PLAYER_KICK = -1
        NONE = 0

    def __init__(self, result_type, move_coords=None):
        self.result_type = result_type
        self.move_coords = []
        self.score_ai = 0
        self.score_player = 0

        if move_coords:
            self.add_turn(move_coords, 0, 0)

    def add_turn(self, move_coords, turn=None):
        self.move_coords.insert(0, move_coords)
        if turn == Result.TURN.AI_KICK:
            self.score_ai += 1
        elif turn == Result.TURN.PLAYER_KICK:
            self.score_player += 1

    def key(self):
        return self.result_type, self.score_ai, -self.score_player

    def __str__(self):
        return '%d:%d:%d %s' % (self.result_type, self.score_ai, self.score_player, self.move_coords)
