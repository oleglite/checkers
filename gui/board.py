# -*- coding: utf-8 -*-

from qt import Qt, QRectF, QWidget, QPainter, QBrush, QPen, QColor, Signal, QObject, QSize

from checkers.logic import get_available_fields_for_checker
from checkers.models import Checker
from gui.dialogs import show_dialog
from gui.tools import ask_checker_color


def create_board_widget(board, controller_id):
    widget = BoardWidget(board)
    controller = AVAILABLE_CONTROLLERS[controller_id](board, widget)
    return widget, controller


class BoardWidget(QWidget):
    CHECKER_SIZE_TO_FIELD = 0.6
    BORDER_SIZE_TO_FIELD = 0.5

    field_clicked = Signal(int, int, int)   # button, x, y

    def __init__(self, board, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.board = board

        self._selected_field = None     # (x_field, y_field) or None
        self._available_moves = []      # [(x_field, y_field), ...] or None
        self._painter = QPainter()

        self._background_brush = QBrush(Qt.gray)
        self._white_field_brush = QBrush(Qt.white)
        self._black_field_brush = QBrush(Qt.black)
        self._white_checker_brush = QBrush(Qt.white)
        self._white_king_checker_brush = QBrush(Qt.white)
        self._selected_field_brush = QBrush(Qt.blue)
        self._available_move_field_brush = QBrush(Qt.green)
        self._black_checker_brush = QBrush(Qt.black)
        self._black_king_checker_brush = QBrush(Qt.black)
        self._white_checker_pen = QPen(QBrush(Qt.gray), 5, j=Qt.RoundJoin)
        self._black_checker_pen = QPen(QBrush(Qt.gray), 5, j=Qt.RoundJoin)
        self._white_king_checker_pen = QPen(QBrush(Qt.red), 5, j=Qt.RoundJoin)
        self._black_king_checker_pen = QPen(QBrush(Qt.red), 5, j=Qt.RoundJoin)
        self._border_brush = QBrush(QColor.fromRgb(205, 127, 50))

        self._field_size = None
        self._border_size = None

    def set_selected_field(self, field):
        assert field is None or len(field) == 2

        self._selected_field = field

    def set_available_moves(self, fields):
        assert all(len(field) == 2 for field in fields) or fields is None

        if not fields:
            self._available_moves = []

        self._available_moves = fields

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
            self.field_clicked.emit(int(event.button()), clicked_field[0], clicked_field[1])
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
                elif (x_field, y_field) in self._available_moves:
                    brush = self._available_move_field_brush
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
                if checker.is_king:
                    brush = self._black_king_checker_brush
                    pen = self._black_king_checker_pen
                else:
                    brush = self._black_checker_brush
                    pen = self._black_checker_pen
            else:
                if checker.is_king:
                    brush = self._white_king_checker_brush
                    pen = self._white_king_checker_pen
                else:
                    brush = self._white_checker_brush
                    pen = self._white_checker_pen

            self._painter.setBrush(brush)
            self._painter.setPen(pen)
            field_rect = self.field_rect(checker.x, checker.y)
            radius = self._field_size / 2.0 * self.CHECKER_SIZE_TO_FIELD
            self._painter.drawEllipse(field_rect.center(), radius, radius)


class BoardController(QObject):
    checker_moved = Signal(int, int, int, int)  # from_x, from_y, to_x, to_y

    def __init__(self, board, widget):
        super(BoardController, self).__init__(parent=widget)
        self.board = board
        self.widget = widget
        self._player_color = None
        self._selected_field = None
        self._can_move_checkers = False
        self._can_select = True

        self.connect_signals()

    def connect_signals(self):
        self.widget.field_clicked.connect(self.process_field_clicked)

    def set_player_color(self, player_color):
        self._player_color = player_color

    def set_can_move_checkers(self, value):
        self._can_move_checkers = value
        self._can_select = value

    def process_field_clicked(self, button, x_field, y_field):
        self._field_clicked(button, (x_field, y_field))
        self.widget.repaint()

    def _field_clicked(self, button, clicked_field):
        if button == Qt.LeftButton:
            checker = self.board.get_checker_in_position(*clicked_field)
            if checker and checker.color == self._player_color:
                self.select_field(clicked_field)
            elif self._selected_field and self._can_move_checkers:
                self.checker_moved.emit(self._selected_field[0], self._selected_field[1], *clicked_field)

    def select_field(self, new_selected_field=None):
        if not self._can_select:
            new_selected_field = None

        self._selected_field = new_selected_field
        self.widget.set_selected_field(self._selected_field)
        self.update_available_moves()

    def clear_selection(self):
        self._selected_field = None
        self.widget.set_available_moves(())

    def update_available_moves(self):
        if not self._selected_field:
            self.widget.set_available_moves(())
            return

        selected_checker = self.board.get_checker_in_position(*self._selected_field)
        if selected_checker:
            available_moves = get_available_fields_for_checker(self.board, selected_checker)
        else:
            available_moves = ()

        self.widget.set_available_moves(available_moves)


class BoardEditorController(BoardController):
    MAKE_KING = 'Make king'
    MAKE_NOT_KING = 'Make not king'
    REMOVE = 'Remove'

    def _field_clicked(self, button, clicked_field):
        if button == Qt.LeftButton:
            self.select_field(clicked_field)
        elif button == Qt.RightButton:
            checker = self.board.get_checker_in_position(*clicked_field)
            if checker:
                make_king = self.MAKE_NOT_KING if checker.is_king else self.MAKE_KING
                answer = show_dialog([make_king, self.REMOVE], message='Chose action:', title='Editing checker')
                if answer == self.MAKE_KING:
                    checker.make_king()
                elif answer == self.MAKE_NOT_KING:
                    checker.is_king = False
                elif answer == self.REMOVE:
                    self.board.remove_checker(checker)
            else:
                color = ask_checker_color('Change color to:')
                if color:
                    checker = Checker(color, *clicked_field)
                    self.board.add_checker(checker)

            self.update_available_moves()



AVAILABLE_CONTROLLERS = {
    'game': BoardController,
    'editor': BoardEditorController,
}
AVAILABLE_CONTROLLERS_ORDER = ['game', 'editor']

assert set(AVAILABLE_CONTROLLERS) == set(AVAILABLE_CONTROLLERS_ORDER)
