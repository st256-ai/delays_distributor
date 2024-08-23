from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QTableWidget, \
    QTableWidgetItem


class NamePlaceholder(QLabel):
    name: str

    def __init__(self, name: str, font_size: int = 16):
        super().__init__()
        self.name = name
        self.setText(name)
        self.setFont(QFont('Arial', font_size, 81, True))


class SimpleCoordinatePlaceholder(QWidget):
    value: int
    location_changed = Signal(int)

    def __init__(self, initial_value: int, name: str = '', is_placeholder_name: bool = False):
        super().__init__()
        self.value = initial_value

        if name == '':  # TODO Need to rework this logic
            self.name_placeholder = None
        elif is_placeholder_name:
            self.name_placeholder = NamePlaceholder(name)
        else:
            self.name_placeholder = NamePlaceholder(name, 12)

        self.editor = QLineEdit()
        self.editor.editingFinished.connect(self.onValueChanged)

        layout = QHBoxLayout()
        if self.name_placeholder is not None:  # TODO
            layout.addWidget(self.name_placeholder)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def get_value(self):
        text = self.editor.text()
        # TODO need to add validations
        return int(text)

    def onValueChanged(self):
        self.location_changed.emit(self.get_value())


class PointLocationPlaceholder(QWidget):
    location: QPoint
    location_changed = Signal(QPoint)

    def __init__(self, location: QPoint, name: str = ''):
        super().__init__()
        self.location = location

        if str != '':
            self.name_placeholder = NamePlaceholder(name)
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_box = SimpleCoordinatePlaceholder(0, 'x:')
        self.x_box.location_changed.connect(self.perform_x_change)
        self.y_box = SimpleCoordinatePlaceholder(0, 'y:')
        self.y_box.location_changed.connect(self.perform_y_change)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.x_box)
        h_layout.addWidget(self.y_box)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.name_placeholder)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def perform_x_change(self, new_x_value: int):
        previous_y = self.location.y()
        new_location = QPoint(new_x_value, previous_y)
        self.set_location(new_location)
        self.location_changed.emit(new_location)

    def perform_y_change(self, new_y_value: int):
        previous_x = self.location.x()
        new_location = QPoint(previous_x, new_y_value)
        self.set_location(new_location)
        self.location_changed.emit(new_location)

    def set_location(self, location: QPoint):
        self.location = location


class GeneratorLocationEditorPlaceholder(QWidget):
    generator_location_changed = Signal(int, QPoint)
    generators_locations = {}

    def __init__(self, initial_x_values: list[int], initial_y_values: list[int]):
        super().__init__()
        self.placeholders = {}

        self.name_placeholder = NamePlaceholder('Координаты генераторов')
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(8)

        self.table.setSizeAdjustPolicy(QtWidgets.QHeaderView.SizeAdjustPolicy.AdjustToContents)

        self.table.setHorizontalHeaderLabels(["Номер", "x", "y"])
        self.table.verticalHeader().setVisible(False)

        for gener_num in range(0, 8):
            initial_point = QPoint(initial_x_values[gener_num], initial_y_values[gener_num])
            self.generators_locations[gener_num] = initial_point
            self.table.setItem(gener_num, 0, QTableWidgetItem(str(gener_num + 1)))
            self.enrich_x_table_cell(gener_num, initial_point.x())
            self.enrich_y_table_cell(gener_num, initial_point.y())

        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        self.table.adjustSize()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_placeholder)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def enrich_x_table_cell(self, gener_num: int, initial_x_value: int):
        x_widget = GeneratorCoordinatePlaceholder(gener_num, initial_x_value)
        x_widget.generator_coordinate_changed.connect(self.perform_x_change)
        self.table.setCellWidget(gener_num, 1, x_widget)

    def enrich_y_table_cell(self, gener_num: int, initial_y_value: int):
        y_widget = GeneratorCoordinatePlaceholder(gener_num, initial_y_value)
        y_widget.generator_coordinate_changed.connect(self.perform_y_change)
        self.table.setCellWidget(gener_num, 2, y_widget)

    def perform_x_change(self, gener_num: int, new_x_value: int):
        previous_y = self.generators_locations[gener_num].y()
        new_location = QPoint(new_x_value, previous_y)
        self.generators_locations[gener_num] = new_location
        self.generator_location_changed.emit(gener_num, new_location)

    def perform_y_change(self, gener_num: int, new_y_value: int):
        previous_x = self.generators_locations[gener_num].x()
        new_location = QPoint(previous_x, new_y_value)
        self.generators_locations[gener_num] = new_location
        self.generator_location_changed.emit(gener_num, new_location)


class GeneratorCoordinatePlaceholder(SimpleCoordinatePlaceholder):
    generator_id: int
    generator_coordinate_changed = Signal(int, int)

    def __init__(self, generator_id: int, initial_value: int):
        super().__init__(initial_value)
        self.generator_id = generator_id

    def onValueChanged(self):
        self.generator_coordinate_changed.emit(self.generator_id, self.get_value())
