from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QGridLayout, QVBoxLayout

from coordinate_forms import NamePlaceholder


class DelayViewer(QWidget):
    value: float

    def __init__(self, generator_number: int, initial_value: float):
        super().__init__()
        self.generator_number = generator_number
        self.value = initial_value

        name = str(generator_number) + ' генератор'
        self.name_placeholder = NamePlaceholder(name, 10)
        self.viewer = QLineEdit()
        self.viewer.setEnabled(False)
        self.viewer.setText(f'{initial_value:.2f}')

        layout = QHBoxLayout()
        layout.addWidget(self.name_placeholder)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

    def set_value(self, value: float):
        self.value = value
        self.viewer.setText(f'{value:.2f}')


class DelaysPlaceholder(QWidget):

    __INITIAL_DELAY: float = 0.0
    __delays: {int, float}

    def __init__(self):
        super().__init__()

        self.name_placeholder = NamePlaceholder('Значения задержек, ps')
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.delays_placeholders = {}

        grid_layout = QGridLayout()

        self.__delays = {}
        for i in range(0, 8):
            self.__delays[i] = self.__INITIAL_DELAY
            current_item = DelayViewer(i + 1, self.__INITIAL_DELAY)
            self.delays_placeholders[i] = current_item
            parity_flag = i % 2
            grid_layout.addWidget(current_item, i - parity_flag, parity_flag)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_placeholder)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def set_delays(self, new_delays: dict[int, float]):
        for i in range(0, 8):
            self.__delays[i] = new_delays[i]
            self.delays_placeholders[i].set_value(new_delays[i])

    def get_delays(self):
        return self.__delays

    def reset_delays(self):
        for i in range(0, 8):
            self.__delays[i] = self.__INITIAL_DELAY
            self.delays_placeholders[i].set_value(self.__INITIAL_DELAY)
