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
        self.viewer.setText(str(initial_value))

        layout = QHBoxLayout()
        layout.addWidget(self.name_placeholder)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

    def set_value(self, value: float):
        self.value = value
        self.viewer.setText(str(value))


class DelaysPlaceholder(QWidget):

    def __init__(self):
        super().__init__()

        self.name_placeholder = NamePlaceholder('Значения задержек, ps')
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.delays_placeholders = {}

        grid_layout = QGridLayout()

        for i in range(0, 8):
            current_item = DelayViewer(i + 1, 0.0)
            self.delays_placeholders[i] = current_item
            grid_layout.addWidget(current_item, i % 5 + 1, i % 2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_placeholder)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
