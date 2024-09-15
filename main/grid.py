import enum

from PySide6.QtCore import QPoint, QRect, QSize, Qt, QRectF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsItem


class SystemItemType(enum.Enum):
    generator = 1
    signal_distributor = 2


def determine_color(item_type):
    if item_type == SystemItemType.generator:
        return 'red'
    else:
        return 'yellow'


class SystemItem(QGraphicsEllipseItem):
    DIAMETER: int = 18

    text: str
    item_type: SystemItemType
    location: QPoint
    rect: QRect

    def __init__(self, text: str, item_type: SystemItemType, location: QPoint):
        super().__init__()

        self.text = text
        self.item_type = item_type
        self.set_location(location)

        color = determine_color(item_type)
        self.setBrush(QBrush(QColor(color), Qt.BrushStyle.SolidPattern))

        is_movable = item_type == SystemItemType.signal_distributor
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, is_movable)

    def set_location(self, location: QPoint):
        self.location = location
        radius = self.DIAMETER / 2
        modified_location = QPoint(int(location.x() - radius), int(location.y() - radius))
        self.rect: QRect = QRect(modified_location, QSize(self.DIAMETER, self.DIAMETER))
        self.setRect(self.mapRectFromScene(self.rect))

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.drawText(self.rect, Qt.AlignmentFlag.AlignCenter, self.text)


class GridPlaceholder(QWidget):

    def __init__(self, initial_x_values: list[int], initial_y_values: list[int]):
        super().__init__()

        self.initial_x_values = initial_x_values
        self.initial_y_values = initial_y_values

        self.view = QGraphicsView()

        self.scene = Scene()
        self.scene.setParent(self.view)
        self.view.setScene(self.scene)

        self.view.setMinimumSize(500, 400)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.initialize()

    def initialize(self):
        scene_base = QPoint(250, 200)
        self.scene.set_signal_distributor(QPoint(int(scene_base.x()), int(scene_base.y())))
        for i in range(0, 8):
            self.scene.add_generator(i, QPoint(self.initial_x_values[i], self.initial_y_values[i]))

    def reset_grid(self):
        self.scene.remove_all_items()
        self.initialize()

    def process_generator_location_change(self, gener_num: int, new_location: QPoint):
        self.scene.change_generator_location(gener_num, new_location)

    def process_point_location_change(self, new_location: QPoint):
        self.scene.change_point_location(new_location)


class Scene(QGraphicsScene):
    POINT_DIAMETER = 9.0

    generator_items: dict[int, SystemItem]
    signal_distributor_item: SystemItem
    point_item: QGraphicsEllipseItem

    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(Qt.BrushStyle.Dense6Pattern)
        self.setSceneRect(QRect(0, 0, 500, 400))

        self.generator_items = {}
        self.signal_distributor_item = None
        self.point_item = None

    def remove_all_items(self):
        items = self.items()
        for item in items:
            self.removeItem(item)

    def set_signal_distributor(self, location: QPoint):
        self.signal_distributor_item = SystemItem('G', SystemItemType.signal_distributor, location)
        self.addItem(self.signal_distributor_item)

    def add_generator(self, gener_num: int, location: QPoint):
        generator_item = SystemItem(str(gener_num + 1), SystemItemType.generator, location)
        self.generator_items[gener_num] = generator_item
        self.addItem(generator_item)

    def add_point(self, location: QPoint):
        rect = QRectF(location.x() - (self.POINT_DIAMETER / 2), location.y() - (self.POINT_DIAMETER / 2),
                      self.POINT_DIAMETER, self.POINT_DIAMETER)
        color = QColor('black')

        self.point_item = self.addEllipse(rect, QPen(color), QBrush(color))

    def change_generator_location(self, gener_num: int, new_location: QPoint):
        previous_item = self.generator_items[gener_num]
        if previous_item is not None:
            self.removeItem(previous_item)

        self.add_generator(gener_num, new_location)
        return True

    def change_point_location(self, new_location: QPoint):
        if self.point_item is not None:
            self.removeItem(self.point_item)
        self.add_point(new_location)
