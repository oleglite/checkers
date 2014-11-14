# -*- coding: utf-8 -*-

from qt import QObject, QMainWindow, QFileDialog, QMenu, QAction, Signal, QWidget, QHBoxLayout, QPlainTextEdit

import settings
from checkers.serialization import save_board
from gui.board import create_board_widget, AVAILABLE_CONTROLLERS_ORDER
from gui.dialogs import show_dialog
from gui.game import GAME_TYPE
from gui.ui.mainwindow import Ui_MainWindow
from gui.tools import ask_checker_color


class Window(QMainWindow, Ui_MainWindow):
    new_pressed = Signal()
    open_pressed = Signal()
    save_pressed = Signal()
    change_board_controller_pressed = Signal(str)   # board_controller_id

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.board_widget = None
        self._slots = []

        if settings.EDITOR_MODE:
            self.init_editor_menu()

        self.connect_signals()

    def init_editor_menu(self):
        self.menu_editor = QMenu('Editor', self.menubar)

        self.menu_controller = QMenu('Board controller', self.menubar)
        self.controller_actions = []
        for controller_id in AVAILABLE_CONTROLLERS_ORDER:
            action = QAction(controller_id, self)
            action.triggered.connect(self.create_slot_change_board_controller(controller_id))
            self.controller_actions.append(action)
            self.menu_controller.addAction(action)
        self.menu_editor.addMenu(self.menu_controller)

        self.menubar.addMenu(self.menu_editor)

    def create_slot_change_board_controller(self, controller_id):
        def slot():
            self.change_board_controller_pressed.emit(controller_id)
        self._slots.append(slot)    # to avoid destroying slot by GC
        return slot

    def set_board_widget(self, board_widget):
        self.board_widget = board_widget
        self.log_widget = QPlainTextEdit(self)

        layout = QHBoxLayout()
        layout.addWidget(board_widget, 2)
        layout.addWidget(self.log_widget, 1)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.repaint()

    def connect_signals(self):
        self.actionNew.triggered.connect(self.new_pressed)
        self.actionOpen.triggered.connect(self.open_pressed)
        self.actionSave.triggered.connect(self.save_pressed)

    def append_to_move_log(self, msg):
        self.log_widget.appendPlainText(msg)


class WindowController(QObject):
    def __init__(self, window):
        super(WindowController, self).__init__(window)

        self.window = window

        self._board_controller_id = None

        self.create_game('boards/default.json')
        self.connect_signals()

    def connect_signals(self):
        self.window.new_pressed.connect(self.process_new)
        self.window.save_pressed.connect(self.process_save)
        self.window.open_pressed.connect(self.process_open)
        self.window.change_board_controller_pressed.connect(self.process_change_board_controller)

        self.game_controller.move_logged.connect(self.window.append_to_move_log)

    def process_new(self):
        self.create_game('boards/default.json')

    def process_open(self):
        file_name, _ = QFileDialog.getOpenFileName(dir='boards')
        if not file_name:
            return

        self.create_game(file_name)

    def process_save(self):
        file_name, _ = QFileDialog.getSaveFileName(dir='boards')
        with open(file_name, 'w') as f:
            f.write(save_board(self.window.board_widget.board))

    def process_change_board_controller(self, controller_id):
        self.create_board_widget(self.game_controller, controller_id)

    def create_game(self, file_name):
        game_type = show_dialog(GAME_TYPE.ORDERING, message='Choose game type', title='New game')
        contoller_cls = GAME_TYPE.CONTROLLERS[game_type]
        if game_type == GAME_TYPE.ONE_PLAYER:
            color = ask_checker_color('Choose your color:')
            self.game_controller = contoller_cls(file_name, color, parent=self)
        else:
            self.game_controller = contoller_cls(file_name, parent=self)

        self.create_board_widget(self.game_controller)

    def create_board_widget(self, game_controller, controller_id=None):
        if not controller_id:
            if self._board_controller_id:
                controller_id = self._board_controller_id
            elif settings.EDITOR_MODE:
                controller_id = 'editor'
            else:
                controller_id = 'game'

        self._board_controller_id = controller_id
        board_widget, board_controller = create_board_widget(game_controller.game.board, controller_id)
        game_controller.set_board_controller(board_controller)
        self.window.set_board_widget(board_widget)
