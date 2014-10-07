# -*- coding: utf-8 -*-

from qt import Qt, QRectF, QWidget, QPainter, QBrush, QPen, QColor

from checkers.models import Checker
from gui.dialogs import show_dialog


class BoardWidget(QWidget):
    CHECKER_SIZE_TO_FIELD = 0.6
    BORDER_SIZE_TO_FIELD = 0.5

    def __init__(self, board, controller=None, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.board = board
        self.controller = controller or CreateBoardController(board, self)

        self._selected_field = None     # (x_field, y_field) or None
        self._painter = QPainter()

        self._background_brush = QBrush(Qt.gray)
        self._white_field_brush = QBrush(Qt.white)
        self._black_field_brush = QBrush(Qt.black)
        self._white_checker_brush = QBrush(Qt.white)
        self._selected_field_brush = QBrush(Qt.green)
        self._black_checker_brush = QBrush(Qt.black)
        self._white_checker_pen = QPen(QBrush(Qt.gray), 4, j=Qt.RoundJoin)
        self._black_checker_pen = QPen(QBrush(Qt.gray), 4, j=Qt.RoundJoin)
        self._border_brush = QBrush(QColor.fromRgb(205, 127, 50))

        self._field_size = None
        self._border_size = None

    def set_selected_field(self, field):
        assert len(field) == 2 or field is None

        self._selected_field = field

    def board_rect(self):
        rect = self.rect()
        size = min([rect.width(), rect.height()]) - self._border_size * 2
        return QRectF(self._border_size, self._border_size, size, size)

    def field_rect(self, x_field, y_field):
        return QRectF(self._border_size + x_field * self._field_size,
                      self._border_size + (self.board.SIZE - 1 - y_field) * self._field_size,
                      self._field_size, self._field_size)

    def get_field_by_point(self, point):
        x_field = (point.x() - self._border_size) / self._field_size
        y_field = self.board.SIZE - (point.y() - self._border_size) / self._field_size

        if 0 <= x_field < self.board.SIZE and 0 <= y_field < self.board.SIZE:
            return int(x_field), int(y_field)

        return None

    def resizeEvent(self, event):
        rect = self.rect()
        outer_size = min([rect.width(), rect.height()])
        self._field_size = outer_size / float(self.board.SIZE + 2 * self.BORDER_SIZE_TO_FIELD)
        self._border_size = self._field_size * self.BORDER_SIZE_TO_FIELD

    def mousePressEvent(self, event):
        clicked_field = self.get_field_by_point(event.pos())
        if clicked_field:
            self.controller.field_clicked(clicked_field[0], clicked_field[1], event.button())
        return super(BoardWidget, self).mousePressEvent(event)

    def paintEvent(self, event):
        self._painter.begin(self)

        self.draw_background()
        self.draw_border()
        self.draw_fields()
        self.draw_checkers()

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
        self._painter.drawRect(inner_rect)

        labels = 'ABCDEFGHIJ'
        for i in xrange(self.board.SIZE):
            # bottom labels
            left = self._border_size + i * self._field_size
            top = outer_rect.bottom() - self._border_size
            text_rect = QRectF(left, top, self._field_size, self._border_size)
            self._painter.drawText(text_rect, Qt.AlignCenter, labels[i])

            # left labels
            top = self._border_size + (self.board.SIZE - i - 1) * self._field_size
            text_rect = QRectF(0, top, self._border_size, self._field_size)
            self._painter.drawText(text_rect, Qt.AlignCenter, str(i + 1))

    def draw_fields(self):
        for x_field in xrange(self.board.SIZE):
            for y_field in xrange(self.board.SIZE):
                if (x_field, y_field) == self._selected_field:
                    brush = self._selected_field_brush
                elif self.board.is_black_field(x_field, y_field):
                    brush = self._black_field_brush
                else:
                    brush = self._white_field_brush
                self.draw_field(x_field, y_field, brush)

    def draw_field(self, x_field, y_field, brush):
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


class BoardController(object):
    def __init__(self, board, widget):
        self.board = board
        self.widget = widget
        self._selected_field = None

    def field_clicked(self, x_field, y_field, button):
        if not self.board.is_black_field(x_field, y_field):
            # TODO: show notification
            return

        if button == Qt.LeftButton:
            # if not self._selected_field:
                self.select_field(x_field, y_field)

        self._field_clicked(x_field, y_field, button)
        self.widget.repaint()

    def _field_clicked(self, x_field, y_field, button):
        """
        Implement in subclussed if needed
        """

    def select_field(self, x_field, y_field):
        self._selected_field = (x_field, y_field)
        self.widget.set_selected_field(self._selected_field)


class CreateBoardController(BoardController):
    def _field_clicked(self, x_field, y_field, button):
        if button == Qt.RightButton and not self.board.get_checker_in_position(x_field, y_field):
            buttons = [Checker.WHITE.capitalize(), Checker.BLACK.capitalize()]
            color = show_dialog(buttons, message='Choose checker color:', title='Adding checker')
            if color:
                checker = Checker(color, x_field, y_field)
                self.board.add_checker(checker)

