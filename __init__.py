# -*- coding: utf-8 -*-

from checkers.models import Board, Checker

from gui import show_board


def main():
    board = Board([
        Checker(Checker.BLACK, 0, 0),
        Checker(Checker.BLACK, 0, 1),
        Checker(Checker.WHITE, 0, 2),
        Checker(Checker.WHITE, 0, 3),
    ])
    show_board(board)

if __name__ == "__main__":
    main()
