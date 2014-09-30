# -*- coding: utf-8 -*-

from checkers.models import Board
from gui import qt_application, Window, BoardWidget


def main():
    board = Board()

    with qt_application():
        window = Window()
        window.set_board_widget(BoardWidget(board))
        window.show()


if __name__ == "__main__":
    main()
