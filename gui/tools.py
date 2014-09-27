# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager

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

