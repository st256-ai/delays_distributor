from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout

BUTTON_FONT_SIZE = 10


class SimpleButton(QPushButton):
    name: str

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.setText(name)
        self.setFont(QFont('Arial', BUTTON_FONT_SIZE))


class ButtonsPlaceholder(QWidget):

    def __init__(self):
        super().__init__()

        self.calculate_button = SimpleButton('Рассчитать задержки')
        self.cancel_button = SimpleButton('Сбросить')
        self.send_button = SimpleButton('Отправить значения задержек')

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.calculate_button)
        h_layout.addWidget(self.cancel_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.send_button)
        self.setLayout(v_layout)
