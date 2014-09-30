# -*- coding: utf-8 -*-

from qt import QObject, QMainWindow, QFileDialog

from checkers.models import load_board, save_board
from gui.board import BoardWidget
from gui.dialogs import Dialog
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

        d = Dialog(['a', 'b', 'c'], self)
        d.exec_()

        file_name, _ = QFileDialog.getOpenFileName(dir='boards')
        with open(file_name) as f:
            board = load_board(f.read())
            self.window.set_board_widget(BoardWidget(board))

    def process_save(self):
        file_name, _ = QFileDialog.getSaveFileName(dir='boards')
        with open(file_name, 'w') as f:
            f.write(save_board(self.window.board_widget.board))




