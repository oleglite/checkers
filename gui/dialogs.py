# -*- coding: utf-8 -*-

from qt import QDialog, QPushButton, QButtonGroup, QVBoxLayout


class Dialog(QDialog):
    def __init__(self, buttons, parent=None):
        super(Dialog, self).__init__()

        self.buttons = buttons

        self.layout = QVBoxLayout()

        self.buttons_layout = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        for i, button_name in enumerate(self.buttons, start=1):
            button = QPushButton(button_name)
            self.button_group.addButton(button, i)
            self.buttons_layout.addWidget(button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        self.button_group.buttonClicked.connect(self.button_clicked_slot)

    def button_clicked_slot(self, button):
        print self.get_button_name(button)

    def get_button_name(self, button):
        return self.buttons[self.button_group.id(button) - 1]
