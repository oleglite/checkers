# -*- coding: utf-8 -*-

from qt import QDialog, QPushButton, QButtonGroup, QVBoxLayout, QLabel


def show_dialog(buttons, message='', title=''):
    CANCEL = 'Cancel'
    dialog = Dialog(buttons + [CANCEL], message, title)
    result_id = dialog.exec_()
    result_name = dialog.get_button_name(result_id)
    if result_name == CANCEL:
        return None
    return result_name


class Dialog(QDialog):
    def __init__(self, buttons, message='', title=''):
        super(Dialog, self).__init__()

        if title:
            self.setWindowTitle(title)

        self.buttons = buttons
        self.message_label = QLabel(message)

        self.buttons_layout = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        for i, button_name in enumerate(self.buttons, start=1):
            button = QPushButton(button_name)
            self.button_group.addButton(button, i)
            self.buttons_layout.addWidget(button)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message_label)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        self.button_group.buttonClicked.connect(self.button_clicked_slot)

    def button_clicked_slot(self, button):
        self.done(self.button_group.id(button))

    def get_button_name(self, button_id):
        return self.buttons[button_id - 1]
