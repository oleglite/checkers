# -*- coding: utf-8 -*-

from qt import QObject, QMainWindow, QFileDialog, QMenu, QAction

import settings
from checkers.serialization import load_board_from_file, save_board
from gui.board import create_board_widget, AVAILABLE_CONTROLLERS_ORDER
from gui.ui.mainwindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.controller = WindowController(self)

        self.board_widget = None

        if settings.EDITOR_MODE:
            self.init_editor_menu()

        self.connect_signals()

    def init_editor_menu(self):
        self.menu_editor = QMenu('Editor', self.menubar)

        self.menu_controller = QMenu('Controller', self.menubar)
        self.controller_actions = []
        for controller in AVAILABLE_CONTROLLERS_ORDER:
            action = QAction(controller, self)
            self.controller_actions.append(action)
            self.menu_controller.addAction(action)
        self.menu_editor.addMenu(self.menu_controller)

        self.menubar.addMenu(self.menu_editor)

    def set_board_widget(self, board_widget):
        self.board_widget = board_widget
        self.setCentralWidget(board_widget)
        self.repaint()

    def connect_signals(self):
        self.actionOpen.triggered.connect(self.controller.process_open)
        self.actionSave.triggered.connect(self.controller.process_save)


class WindowController(QObject):
    def __init__(self, window):
        super(WindowController, self).__init__(window)

        self.window = window

    def process_open(self):
        file_name, _ = QFileDialog.getOpenFileName(dir='boards')
        if not file_name:
            return

        board = load_board_from_file(file_name)
        self.window.set_board_widget(create_board_widget(board))

    def process_save(self):
        file_name, _ = QFileDialog.getSaveFileName(dir='boards')
        with open(file_name, 'w') as f:
            f.write(save_board(self.window.board_widget.board))
