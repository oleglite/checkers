# -*- coding: utf-8 -*-

from checkers.models import Board, BoardManager, load_board_from_file
from gui import qt_application, Window, create_board_widget


def main():
    board = Board()
    # board = load_board_from_file('boards/default.json')
    board_manager = BoardManager(board)

    with qt_application():
        window = Window()
        window.set_board_widget(create_board_widget(board, board_manager))
        window.show()


if __name__ == "__main__":
    main()
