from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, Qt
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

        layout = QHBoxLayout()
        if self.name_placeholder is not None:  # TODO
            layout.addWidget(self.name_placeholder)
        layout.addWidget(self.editor)
        self.setLayout(layout)


class LocationPlaceholder(QWidget):
    location: QPoint

    def __init__(self, location: QPoint, name: str = ''):
        super().__init__()
        self.location = location

        if str != '':
            self.name_placeholder = NamePlaceholder(name)
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_box = SimpleCoordinatePlaceholder(0, 'x:')
        self.y_box = SimpleCoordinatePlaceholder(0, 'y:')

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.x_box)
        h_layout.addWidget(self.y_box)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.name_placeholder)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def set_location(self, location: QPoint):
        self.location = location


class GeneratorLocationEditorPlaceholder(QWidget):

    def __init__(self):
        super().__init__()
        self.placeholders = {}

        self.name_placeholder = NamePlaceholder('Координаты генераторов')
        self.name_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget()  # Create a table
        self.table.setColumnCount(3)
        self.table.setRowCount(8)

        self.table.setSizeAdjustPolicy(QtWidgets.QHeaderView.SizeAdjustPolicy.AdjustToContents)

        self.table.setHorizontalHeaderLabels(["Номер", "x", "y"])
        self.table.verticalHeader().setVisible(False)

        # TODO this can be done in much shorter way
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(1, 0, QTableWidgetItem("2"))
        self.table.setItem(2, 0, QTableWidgetItem("3"))
        self.table.setItem(3, 0, QTableWidgetItem("4"))
        self.table.setItem(4, 0, QTableWidgetItem("5"))
        self.table.setItem(5, 0, QTableWidgetItem("6"))
        self.table.setItem(6, 0, QTableWidgetItem("7"))
        self.table.setItem(7, 0, QTableWidgetItem("8"))

        self.table.setCellWidget(0, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(1, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(2, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(3, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(4, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(5, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(6, 1, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(7, 1, SimpleCoordinatePlaceholder(0))

        self.table.setCellWidget(0, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(1, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(2, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(3, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(4, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(5, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(6, 2, SimpleCoordinatePlaceholder(0))
        self.table.setCellWidget(7, 2, SimpleCoordinatePlaceholder(0))

        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        self.table.adjustSize()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_placeholder)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)


class GeneratorLocationPlaceholder(QWidget):

    def __init__(self, location: QPoint):
        super().__init__()
        self.placeholder = LocationPlaceholder(location)

    def set_location(self, location: QPoint):
        self.placeholder.set_location(location)
