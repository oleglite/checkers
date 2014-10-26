# -*- coding: utf-8 -*-

from gui.tools import qt_application
from gui.window import Window, WindowController


def main():
    with qt_application():
        window = Window()
        controller = WindowController(window)
        window.show()


if __name__ == "__main__":
    main()
