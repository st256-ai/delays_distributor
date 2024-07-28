from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from buttons import ButtonsPlaceholder
from coordinate_forms import LocationPlaceholder, GeneratorLocationEditorPlaceholder
from delays import DelaysPlaceholder
from grid import GridPlaceholder, SystemItem, SystemItemType


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.grid_widget = GridPlaceholder()
        self.point_location_widget = LocationPlaceholder(QPoint(0, 0), 'Координаты точки приема')
        self.initialize_grid_placeholder()
        self.buttons = ButtonsPlaceholder()

        self.delays_widget = DelaysPlaceholder()
        self.generators_locations = GeneratorLocationEditorPlaceholder()

        left_layout.addWidget(self.grid_widget)
        left_layout.addWidget(self.point_location_widget)
        left_layout.addWidget(self.buttons)

        right_layout.addWidget(self.delays_widget)
        right_layout.addWidget(self.generators_locations)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def initialize_grid_placeholder(self):
        signal_distributor = SystemItem('G', SystemItemType.signal_distributor, QPoint(0, 0))
        self.grid_widget.add_system_item(signal_distributor)
        for i in range(1, 9):
            new_item = SystemItem(str(i), SystemItemType.generator, QPoint(i * 10 + 40, i * 10 + 40))
            self.grid_widget.add_system_item(new_item)
