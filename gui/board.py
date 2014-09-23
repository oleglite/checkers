# -*- coding: utf-8 -*-

from PySide.QtCore import Qt, QRectF
from PySide.QtGui import QWidget, QPainter, QBrush, QPen, QColor

from checkers.models import Checker


class BoardWidget(QWidget):
    CHECKER_SIZE_TO_FIELD = 0.6
    BORDER_SIZE = 20

    def __init__(self, board, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.board = board
        self._painter = QPainter()

        self._background_brush = QBrush(Qt.gray)
        self._white_field_brush = QBrush(Qt.white)
        self._black_field_brush = QBrush(Qt.black)
        self._white_checker_brush = QBrush(Qt.white)
        self._black_checker_brush = QBrush(Qt.black)
        self._white_checker_pen = QPen(QBrush(Qt.gray), 4, j=Qt.RoundJoin)
        self._black_checker_pen = QPen(QBrush(Qt.gray), 4, j=Qt.RoundJoin)
        self._border_brush = QBrush(QColor.fromRgb(205, 127, 50))

        self._field_size = None

    def board_rect(self):
        rect = self.rect()
        size = min([rect.width(), rect.height()]) - self.BORDER_SIZE * 2
        return QRectF(self.BORDER_SIZE, self.BORDER_SIZE, size, size)

    def field_rect(self, x_field, y_field):
        return QRectF(self.BORDER_SIZE + x_field * self._field_size,
                      self.BORDER_SIZE + (self.board.SIZE - 1 - y_field) * self._field_size,
                      self._field_size, self._field_size)

    def resizeEvent(self, event):
        rect = self.board_rect()
        self._field_size = min([rect.width(), rect.height()]) / float(self.board.SIZE)

    def paintEvent(self, event):
        self._painter.begin(self)

        self.draw_background()
        self.draw_border()
        self.draw_fields()
        # self.draw_checkers()

        self._painter.end()

    def draw_background(self):
        self._painter.fillRect(self.rect(), self._background_brush)

    def draw_border(self):
        rect = self.rect()
        outer_size = min([rect.width(), rect.height()])
        outer_rect = QRectF(0, 0, outer_size, outer_size)
        inner_rect = self.board_rect()
        self._painter.fillRect(outer_rect, self._border_brush)

        self._painter.setPen(QPen(QBrush(Qt.black), 3))
        self._painter.drawRect(inner_rect.adjusted(-1, -1, 0, 0))

        labels = 'ABCDEFGHIJ'
        for i in xrange(self.board.SIZE):
            x = self.BORDER_SIZE + i * self._field_size + self._field_size / 2.0 - self._field_size * 0.06
            y = outer_rect.bottom() - self._field_size * 0.1
            self._painter.drawText(x, y, labels[i])

    def draw_fields(self):
        for x_field in xrange(self.board.SIZE):
            for y_field in xrange(self.board.SIZE):
                if self.board.is_black_field(x_field, y_field):
                    brush = self._black_field_brush
                else:
                    brush = self._white_field_brush
                self._painter.fillRect(self.field_rect(x_field, y_field), brush)

    def draw_checkers(self):
        for checker in self.board.checkers:
            if checker.color == Checker.BLACK:
                brush = self._black_checker_brush
                pen = self._black_checker_pen
            else:
                brush = self._white_checker_brush
                pen = self._white_checker_pen

            self._painter.setBrush(brush)
            self._painter.setPen(pen)
            field_rect = self.field_rect(checker.x, checker.y)
            radius = self._field_size / 2.0 * self.CHECKER_SIZE_TO_FIELD
            self._painter.drawEllipse(field_rect.center(), radius, radius)
