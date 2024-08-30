from PySide6.QtCore import Signal
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
    calculate_delays = Signal()
    reset_system = Signal()
    send_delays = Signal()

    def __init__(self):
        super().__init__()

        self._calculate_button = SimpleButton('Рассчитать задержки')
        self._calculate_button.clicked.connect(self.__onCalculateDelays)

        self._reset_button = SimpleButton('Сбросить')
        self._reset_button.clicked.connect(self.__onSystemReset)

        self._send_button = SimpleButton('Отправить значения задержек')
        self._send_button.clicked.connect(self.__onSendDelays)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self._calculate_button)
        h_layout.addWidget(self._reset_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self._send_button)
        self.setLayout(v_layout)

    def __onCalculateDelays(self):
        self.calculate_delays.emit()

    def __onSystemReset(self):
        self.reset_system.emit()

    def __onSendDelays(self):
        self.send_delays.emit()
