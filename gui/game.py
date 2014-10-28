# -*- coding: utf-8 -*-

from qt import QObject

from checkers.logic import Game


class GameController(QObject):
    def __init__(self, game_file_name, parent=None):
        super(GameController, self).__init__(parent=parent)
        self.game = Game(game_file_name)


class TwoPlayersGameController(GameController):
    pass


class GAME_TYPE:
    TWO_PLAYERS = 'Player vs Player'
    ONE_PLAYER = 'Players vs AI'
    TRAINING = 'Trining'

    CONTROLLERS = {
        TWO_PLAYERS: TwoPlayersGameController,
        ONE_PLAYER: TwoPlayersGameController,
        TRAINING: TwoPlayersGameController,
    }
    ORDERING = [TRAINING, ONE_PLAYER, TWO_PLAYERS]
