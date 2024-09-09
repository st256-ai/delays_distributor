import enum

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QHeaderView, QMessageBox

MIN_X = 10
MAX_X = 240

MIN_Y = 10
MAX_Y = 190


class Coordinate(enum.Enum):
    x = 1
    y = 2


class NamePlaceholder(QLabel):
    name: str

    def __init__(self, name: str, font_size: int = 16):
        super().__init__()
        self.name = name
        self.setText(name)
        self.setFont(QFont('Arial', font_size, 81, True))


class SimpleCoordinatePlaceholder(QWidget):
    __value: int
    location_changed = Signal(int)

    def __init__(self, initial_value: int, coordinate: Coordinate):
        super().__init__()
        self.__value = initial_value
        self.coordinate = coordinate

        self.__editor = QLineEdit(str(self.__value))
        self.__editor.editingFinished.connect(self._onValueChanged)

        layout = QHBoxLayout()
        layout.addWidget(self.__editor)
        self.setLayout(layout)

    def set_value(self, new_value: int):
        self.__validate_input(new_value)
        self.__value = new_value
        self.__editor.setText(str(new_value))

    def __validate_input(self, new_value) -> bool:
        if isinstance(new_value, str):
            try:
                int(new_value)
            except ValueError:
                QMessageBox.critical(self, "Error", 'Координата должна быть числом!')
                return False

        int_value = int(new_value)
        if self.coordinate == Coordinate.x:
            if MIN_X <= int_value <= MAX_X:
                return True
            else:
                QMessageBox.critical(self, "Error", 'Координата x должна лежать в диапозоне от ' + str(MIN_X) +
                                     ' до ' + str(MAX_X) + '!')
                return False
        else:
            if MIN_Y <= int_value <= MAX_Y:
                return True
            else:
                QMessageBox.critical(self, "Error", 'Координата y должна лежать в диапозоне от ' + str(MIN_Y) +
                                     ' до ' + str(MAX_Y) + '!')
                return False

    def get_value(self):
        return self.__value

    def _onValueChanged(self):
        input_text = self.__editor.text()
        result = self.__validate_input(input_text)

        if result:
            self.__value = int(input_text)
            self.location_changed.emit(self.__value)
        else:
            self.__editor.setText(str(self.__value))


class NamedCoordinatePlaceholder(SimpleCoordinatePlaceholder):
    location_changed = Signal(int)

    def __init__(self, initial_value: int, coordinate: Coordinate, name: str = ''):
        super().__init__(initial_value, coordinate)

        self.name_placeholder = NamePlaceholder(name)
        layout = QHBoxLayout()
        layout.addWidget(self.name_placeholder)
        self.setLayout(layout)

    def _onValueChanged(self):
        self.location_changed.emit(self.get_value())


class PointLocationPlaceholder(QWidget):
    location: QPoint
    location_changed = Signal(QPoint)

    def __init__(self, initial_location: QPoint, name: str = ''):
        super().__init__()
        self.initial_location = initial_location
        self.location = initial_location

        self.name_placeholder = NamePlaceholder(name)
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_box = NamedCoordinatePlaceholder(initial_location.x(), Coordinate.x, 'x:')
        self.x_box.location_changed.connect(self._perform_x_change)
        self.y_box = NamedCoordinatePlaceholder(initial_location.y(), Coordinate.y,  'y:')
        self.y_box.location_changed.connect(self._perform_y_change)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.x_box)
        h_layout.addWidget(self.y_box)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.name_placeholder)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def reset_location(self):
        self.set_location(self.initial_location)
        self.x_box.set_value(self.initial_location.x())
        self.y_box.set_value(self.initial_location.y())

    def set_location(self, location: QPoint):
        self.location = location

    def get_location(self) -> QPoint:
        return self.location

    def _perform_x_change(self, new_x_value: int):
        previous_y = self.location.y()
        new_location = QPoint(new_x_value, previous_y)
        self.set_location(new_location)
        self.location_changed.emit(new_location)

    def _perform_y_change(self, new_y_value: int):
        previous_x = self.location.x()
        new_location = QPoint(previous_x, new_y_value)
        self.set_location(new_location)
        self.location_changed.emit(new_location)


class GeneratorLocationEditorPlaceholder(QWidget):
    generator_location_changed = Signal(int, QPoint)
    _generators_locations: {int, QPoint} = {}

    def __init__(self, initial_x_values: list[int], initial_y_values: list[int]):
        super().__init__()
        self.placeholders = {}

        self.initial_x_values = initial_x_values
        self.initial_y_values = initial_y_values

        self.name_placeholder = NamePlaceholder('Координаты генераторов')
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(8)

        # self.table.setContentsMargins(QtWidgets.QHeaderView.SizeAdjustPolicy.AdjustIgnored)

        self.table.setHorizontalHeaderLabels(["Номер", "x", "y"])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.verticalHeader().setVisible(False)

        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        self.table.adjustSize()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for gener_num in range(0, 8):
            initial_point = QPoint(initial_x_values[gener_num], initial_y_values[gener_num])
            self._generators_locations[gener_num] = initial_point
            widget_item = QTableWidgetItem(str(gener_num + 1))
            widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(gener_num, 0, widget_item)
            self.__enrich_x_table_cell(gener_num, initial_point.x())
            self.__enrich_y_table_cell(gener_num, initial_point.y())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_placeholder)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def reset_locations(self):
        for gener_num in range(0, 8):
            initial_point = QPoint(self.initial_x_values[gener_num], self.initial_y_values[gener_num])
            self._generators_locations[gener_num] = initial_point
            self.__enrich_x_table_cell(gener_num, initial_point.x())
            self.__enrich_y_table_cell(gener_num, initial_point.y())

    def get_generator_locations(self) -> {int, QPoint}:
        return self._generators_locations

    def __enrich_x_table_cell(self, gener_num: int, initial_x_value: int):
        x_widget = GeneratorCoordinatePlaceholder(gener_num, initial_x_value, Coordinate.x)
        x_widget.generator_coordinate_changed.connect(self.__perform_x_change)
        self.table.setCellWidget(gener_num, 1, x_widget)

    def __enrich_y_table_cell(self, gener_num: int, initial_y_value: int):
        y_widget = GeneratorCoordinatePlaceholder(gener_num, initial_y_value, Coordinate.y)
        y_widget.generator_coordinate_changed.connect(self.__perform_y_change)
        self.table.setCellWidget(gener_num, 2, y_widget)

    def __perform_x_change(self, gener_num: int, new_x_value: int):
        previous_y = self._generators_locations[gener_num].y()
        new_location = QPoint(new_x_value, previous_y)
        self._generators_locations[gener_num] = new_location
        self.generator_location_changed.emit(gener_num, new_location)

    def __perform_y_change(self, gener_num: int, new_y_value: int):
        previous_x = self._generators_locations[gener_num].x()
        new_location = QPoint(previous_x, new_y_value)
        self._generators_locations[gener_num] = new_location
        self.generator_location_changed.emit(gener_num, new_location)


class GeneratorCoordinatePlaceholder(SimpleCoordinatePlaceholder):
    generator_id: int
    generator_coordinate_changed = Signal(int, int)

    def __init__(self, generator_id: int, initial_value: int, coordinate: Coordinate):
        super().__init__(initial_value, coordinate)
        self.generator_id = generator_id

    def onValueChanged(self):
        self.generator_coordinate_changed.emit(self.generator_id, self.get_value())
