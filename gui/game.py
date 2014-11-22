# -*- coding: utf-8 -*-

from qt import QObject, QMessageBox, Signal

from checkers.ai import calculate_ai_move
from checkers.logic import Game, GameError
from checkers.models import Checker


class GameController(QObject):
    move_logged = Signal(str)
    score_updated = Signal(int, int)

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
        self.start()

    def start(self):
        pass

    def process_checker_moved(self, x1, y1, x2, y2):
        checker = self.game.board.get_checker_in_position(x1, y1)
        if not checker:
            return

        try:
            move = self.game.current_player.move(checker, x2, y2)
            self.move_logged.emit('%s: %s' % (move, checker))
        except GameError, e:
            QMessageBox.information(self.board_controller.widget, 'Wrong', str(e))

        winner = self.game.board.get_winner()
        if winner:
            QMessageBox.information(self.board_controller.widget, 'Game ended', winner.capitalize() + ' wins!')

        self._process_checker_moved(checker, x2, y2)

        self.board_controller.select_field()
        self.board_controller.set_player_color(self.game.current_player.color)

        self.score_updated.emit(self.game.white_player.score, self.game.black_player.score)

    def _process_checker_moved(self, checker, x, y):
        pass


class TwoPlayersGameController(GameController):
    def set_board_controller(self, board_controller):
        super(TwoPlayersGameController, self).set_board_controller(board_controller)
        self.board_controller.set_can_move_checkers(True)


class OnePlayerGameController(GameController):
    def __init__(self, game_file_name, player_color, parent=None):
        super(OnePlayerGameController, self).__init__(game_file_name, parent)
        self.player_color = player_color
        self.ai_color = Checker.WHITE if player_color == Checker.BLACK else Checker.BLACK

    def set_board_controller(self, board_controller):
        super(OnePlayerGameController, self).set_board_controller(board_controller)
        if self.player_color == Checker.WHITE:
            self.board_controller.set_can_move_checkers(True)
        board_controller.set_player_color(self.player_color)

    def start(self):
        if self.ai_color == Checker.WHITE:
            self._make_ai_moves()

    def _process_checker_moved(self, checker, x, y):
        self._make_ai_moves()

    def _make_ai_moves(self):
        self.board_controller.set_can_move_checkers(False)

        while self.game.current_player.color == self.ai_color:
            move_coords = calculate_ai_move(self.game.board, self.ai_color, self.player_color)
            if not move_coords:
                self.move_logged.emit('ai has skipped turn')
                break
            checker = self.game.board.get_checker_in_position(move_coords[0], move_coords[1])
            move = self.game.current_player.move(checker, move_coords[2], move_coords[3])
            self.move_logged.emit('%s: %s' % (move, checker))

        self.board_controller.set_can_move_checkers(True)


class TrainingGameController(OnePlayerGameController):
    def __init__(self, game_file_name, parent=None):
        super(TrainingGameController, self).__init__(game_file_name, Checker.WHITE, parent)


class GAME_TYPE:
    TWO_PLAYERS = 'Player vs Player'
    ONE_PLAYER = 'Players vs AI'
    TRAINING = 'Training'

    CONTROLLERS = {
        TWO_PLAYERS: TwoPlayersGameController,
        ONE_PLAYER: OnePlayerGameController,
        TRAINING: TrainingGameController,
    }
    ORDERING = [TRAINING, ONE_PLAYER, TWO_PLAYERS]
