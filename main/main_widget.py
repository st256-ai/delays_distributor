from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from buttons import ButtonsPlaceholder
from coordinate_forms import PointLocationPlaceholder, GeneratorLocationEditorPlaceholder
from delays import DelaysPlaceholder
from grid import GridPlaceholder, SystemItem, SystemItemType


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.grid_widget = GridPlaceholder()
        self.point_location_widget = PointLocationPlaceholder(QPoint(0, 0), 'Координаты точки приема')
        self.point_location_widget.location_changed.connect(self.onPointLocationChanged)
        self.buttons = ButtonsPlaceholder()

        initial_x_values = [0, 0, 0, 0, 0, 0, 0, 0]
        initial_y_values = [0, 0, 0, 0, 0, 0, 0, 0]

        self.delays_widget = DelaysPlaceholder()
        self.generators_locations = GeneratorLocationEditorPlaceholder(initial_x_values, initial_y_values)
        self.generators_locations.generator_location_changed.connect(self.onGeneratorLocationChanged)

        left_layout.addWidget(self.grid_widget)
        left_layout.addWidget(self.point_location_widget)
        left_layout.addWidget(self.buttons)

        right_layout.addWidget(self.delays_widget)
        right_layout.addWidget(self.generators_locations)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def onGeneratorLocationChanged(self, gener_num: int, new_location: QPoint):
        self.grid_widget.process_generator_location_change(gener_num, new_location)

    def onPointLocationChanged(self, new_location: QPoint):
        self.grid_widget.process_point_location_change(new_location)
