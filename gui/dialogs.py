# -*- coding: utf-8 -*-

from qt import QDialog, QPushButton, QButtonGroup, QVBoxLayout, QLabel


def show_dialog(names, values=None, message='', title=''):
    assert values is None or len(names) == len(values)
    if not values:
        values = names

    CANCEL = 'Cancel'
    dialog = Dialog(names + [CANCEL], values + [CANCEL], message, title)
    result_id = dialog.exec_()
    result_value = dialog.get_button_value(result_id)
    if result_value == CANCEL:
        return None
    return result_value


class Dialog(QDialog):
    def __init__(self, names, values, message='', title=''):
        assert len(names) == len(values)

        super(Dialog, self).__init__()

        if title:
            self.setWindowTitle(title)

        self.names = names
        self.values = values
        self.message_label = QLabel(message)

        self.buttons_layout = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        for i, button_name in enumerate(self.names, start=1):
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
        return self.names[button_id - 1]

    def get_button_value(self, button_id):
        return self.values[button_id - 1]
