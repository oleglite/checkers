# -*- coding: utf-8 -*-

from checkers.logic import Game
from checkers.models import Board
from checkers.serialization import load_board_from_file
from gui import qt_application, Window, create_board_widget


def main():
    # board = Board()
    # board = load_board_from_file('boards/default.json')

    game = Game('boards/default.json')

    with qt_application():
        window = Window()
        window.set_board_widget(create_board_widget(game.board, game.white_player))
        window.show()


if __name__ == "__main__":
    main()
