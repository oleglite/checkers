# -*- coding: utf-8 -*-

from qt import QObject, QMessageBox

from checkers.logic import Game, GameError
from checkers.models import Checker


class GameController(QObject):
    def __init__(self, game_file_name, parent=None):
        super(GameController, self).__init__(parent=parent)
        self.game = Game(game_file_name)
        self.board_controller = None

    def set_board_controller(self, board_controller):
        if self.board_controller:
            self.board_controller.checker_moved.disconnect(self.process_checker_moved)
        self.board_controller = board_controller
        self.board_controller.checker_moved.connect(self.process_checker_moved)
        board_controller.set_player_color(Checker.WHITE)

    def process_checker_moved(self, x1, y1, x2, y2):
        checker = self.game.board.get_checker_in_position(x1, y1)
        if not checker:
            return

        try:
            self._process_checker_moved(checker, x2, y2)
        except GameError, e:
            QMessageBox.information(self.board_controller.widget, 'Wrong', str(e))

        self.board_controller.select_field()
        self.board_controller.set_player_color(self.game.current_player.color)

    def _process_checker_moved(self, checker, x, y):
        raise NotImplementedError()


class TwoPlayersGameController(GameController):
    def set_board_controller(self, board_controller):
        super(TwoPlayersGameController, self).set_board_controller(board_controller)
        self.board_controller.set_can_move_checkers(True)

    def _process_checker_moved(self, checker, x, y):
        print checker.color, self.game.current_player.move(checker, x, y)


class OnePlayerGameController(GameController):
    def __init__(self, game_file_name, player_color, parent=None):
        super(OnePlayerGameController, self).__init__(game_file_name, parent)
        self.player_color = player_color

    def set_board_controller(self, board_controller):
        super(OnePlayerGameController, self).set_board_controller(board_controller)
        player_make_move_first = self.player_color == Checker.WHITE
        self.board_controller.set_can_move_checkers(player_make_move_first)

    def _process_checker_moved(self, checker, x, y):
        print checker.color, self.game.current_player.move(checker, x, y)

        self.board_controller.set_can_move_checkers(checker.color != self.player_color)



class GAME_TYPE:
    TWO_PLAYERS = 'Player vs Player'
    ONE_PLAYER = 'Players vs AI'
    # TRAINING = 'Training'

    CONTROLLERS = {
        TWO_PLAYERS: TwoPlayersGameController,
        ONE_PLAYER: OnePlayerGameController,
        # TRAINING: TwoPlayersGameController,
    }
    ORDERING = [ONE_PLAYER, TWO_PLAYERS]
