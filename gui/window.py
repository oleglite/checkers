# -*- coding: utf-8 -*-

from qt import QObject, QMainWindow, QFileDialog

from checkers.serialization import load_board_from_file, save_board
from gui.board import BoardWidget
from gui.ui.mainwindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.controller = WindowController(self)

        self.board_widget = None

        self.connect_signals()

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
        self.window.set_board_widget(BoardWidget(board))

    def process_save(self):
        file_name, _ = QFileDialog.getSaveFileName(dir='boards')
        with open(file_name, 'w') as f:
            f.write(save_board(self.window.board_widget.board))
