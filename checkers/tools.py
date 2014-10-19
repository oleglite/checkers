# -*- coding: utf-8 -*-
import json
from checkers.models import Board, Checker


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


def load_board_from_file(file_name):
    with open(file_name) as f:
        board = load_board(f.read())
    return board
