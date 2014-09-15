# -*- coding: utf-8 -*-

# PySide doc: http://pyside.github.io/docs/pyside/

import sys

from PySide.QtGui import QApplication

from gui.board import BoardWidget


def show_board(board):
    app = QApplication(sys.argv)

    window = BoardWidget(board)
    window.show()

    app.exec_()
    sys.exit()
