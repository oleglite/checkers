# -*- coding: utf-8 -*-

from random import choice
from copy import deepcopy

from checkers.logic import get_available_move_fields, get_move, Move

MAX_RECURSION = 3


class RESULT:
    WIN = 4
    UNKNOWN = 3
    DRAW = 2
    LOSE = 1


def minimax(board, ai_color, player_color, recursion_level=0):
    """
    return (move_coords, result_tuple)
    move_coords = (x1, y1, x2, y2)
    result_tuple = (result, ai_kicks, -player_kicks)
    """
    recursion_level += 1

    color = ai_color if recursion_level % 2 else player_color

    results = [
        # (move_coords, result_tuple),
    ]

    for checker in board.get_checkers(color):
        for field in get_available_move_fields(board, checker):
            board_copy = deepcopy(board)

            move_coords = (checker.x, checker.y, field[0], field[1])
            move = get_move(board_copy, checker, *field)
            board_copy.move(*move_coords)

            winner = board_copy.get_winner()
            if winner:
                if color == ai_color:
                    return checker.x, checker.y, field[0], field[1], (RESULT.WIN, 0, 0)
                else:
                    return checker.x, checker.y, field[0], field[1], (RESULT.LOSE, 0, 0)

            if recursion_level == MAX_RECURSION:
                result = RESULT.UNKNOWN
                ai_kicks = player_kicks = 0
            else:
                result, ai_kicks, player_kicks = minimax(board_copy, ai_color, player_color, recursion_level)[1]

            if move.type == Move.TYPE.KICK:
                if color == ai_color:
                    ai_kicks += 1
                else:
                    player_kicks -= 1

            results.append((move_coords, (result, ai_kicks, player_kicks)))

    if not results:
        return (), (RESULT.UNKNOWN, 0, 0)

    fn = max if color == ai_color else min
    best_result = fn(results, key=lambda i: i[1])
    best_results = [result for result in results if result[1] == best_result[1]]
    ai_choice = choice(best_results)
    return ai_choice

