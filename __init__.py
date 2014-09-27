# -*- coding: utf-8 -*-

from checkers.models import Board, load_board
from gui import qt_application, Window, BoardWidget


def main():
    with open('./boards/default.json') as f:
        board = load_board(f.read())

    with qt_application():
        window = Window()
        window.set_board_widget(BoardWidget(board))
        window.show()


if __name__ == "__main__":
    main()
