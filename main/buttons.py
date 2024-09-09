from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout

BUTTON_FONT_SIZE = 10

CALCULATE_BUTTON_TEXT = 'Рассчитать задержки'
RESET_BUTTON_TEXT = 'Сбросить'
SEND_BUTTON_TEXT = 'Отправить значения задержек'
CALIBRATE_BUTTON_TEXT = 'Калибровка'


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
    calibrate_signals = Signal()

    def __init__(self):
        super().__init__()

        self._calculate_button = SimpleButton(CALCULATE_BUTTON_TEXT)
        self._calculate_button.clicked.connect(self.__onCalculateDelays)

        self._reset_button = SimpleButton(RESET_BUTTON_TEXT)
        self._reset_button.clicked.connect(self.__onSystemReset)

        self._send_button = SimpleButton(SEND_BUTTON_TEXT)
        self._send_button.clicked.connect(self.__onSendDelays)

        self._calibrate_button = SimpleButton(CALIBRATE_BUTTON_TEXT)
        self._calibrate_button.clicked.connect(self.__onCalibrateDelays)

        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(self._calculate_button)
        h_layout_1.addWidget(self._reset_button)

        h_layout_2 = QHBoxLayout()
        h_layout_2.addWidget(self._send_button)
        h_layout_2.addWidget(self._calibrate_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        self.setLayout(v_layout)

    def __onCalculateDelays(self):
        self.calculate_delays.emit()

    def __onSystemReset(self):
        self.reset_system.emit()

    def __onSendDelays(self):
        self.send_delays.emit()

    def __onCalibrateDelays(self):
        self.calibrate_signals.emit()
