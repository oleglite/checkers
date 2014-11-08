# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager
from checkers.models import Checker
from gui.dialogs import show_dialog

from qt import QApplication


@contextmanager
def qt_application():
    app = QApplication(sys.argv)

    yield

    app.exec_()
    sys.exit()


def place_between(number, minimum, maximum):
    """
    >>> place_between(3, 1, 4)
    3
    >>> place_between(0, 1, 4)
    1
    >>> place_between(7, 1, 4)
    4
    """
    if number < minimum:
        return minimum
    elif number > maximum:
        return maximum
    else:
        return number


def ask_checker_color(message='Choose checker color:'):
    button_values = [Checker.WHITE, Checker.BLACK]
    button_names = [name.capitalize() for name in button_values]
    color = show_dialog(button_names, button_values, message=message, title='Select checker color')
    return color
