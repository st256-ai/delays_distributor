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
    RADIUS: int = 18

    text: str
    item_type: SystemItemType
    location: QPoint

    def __init__(self, text: str, item_type: SystemItemType, location: QPoint):
        super().__init__()

        self.text = text
        self.item_type = item_type
        self.set_location(location)

        color = determine_color(item_type)
        self.setBrush(QBrush(QColor(color), Qt.BrushStyle.SolidPattern))

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
                     False)  # Do not change this value to True, it will crash the whole system!

    def set_location(self, location: QPoint):
        self.location = location

        modified_location = QPoint(location.x() - self.RADIUS, location.y() - self.RADIUS)
        rect: QRect = QRect(modified_location, QSize(self.RADIUS, self.RADIUS))
        self.setRect(rect)

    # def paintEvent(self):


class GridPlaceholder(QWidget):

    def __init__(self):
        super().__init__()

        self.scene = Scene()

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.adjustSize()
        self.view.setFixedHeight(400)
        self.view.setFixedWidth(500)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.initialize()

    def initialize(self):
        self.scene.set_signal_distributor(QPoint(0, 0))
        for i in range(0, 8):
            self.scene.add_generator(i, QPoint(i * 10 + 40, i * 10 + 40))

    def process_generator_location_change(self, gener_num: int, new_location: QPoint):
        self.scene.change_generator_location(gener_num, new_location)

    def process_point_location_change(self, new_location: QPoint):
        self.scene.change_point_location(new_location)


class Scene(QGraphicsScene):
    POINT_RADIOS = 12.0

    generator_items: dict[int, SystemItem]
    signal_distributor_item: SystemItem
    point_item: QGraphicsEllipseItem

    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(Qt.BrushStyle.Dense6Pattern)
        self.setSceneRect(QRect(0, 0, 100, 200))

        self.generator_items = {}
        self.signal_distributor_item = None
        self.point_item = None

    def set_signal_distributor(self, location: QPoint):
        self.signal_distributor_item = SystemItem('G', SystemItemType.signal_distributor, location)
        self.addItem(self.signal_distributor_item)

    def add_generator(self, gener_num: int, location: QPoint):
        generator_item = SystemItem(str(gener_num + 1), SystemItemType.generator, location)
        self.generator_items[gener_num] = generator_item
        self.addItem(generator_item)

    def add_point(self, location: QPoint):
        rect = QRectF(location.x(), location.y(), self.POINT_RADIOS, self.POINT_RADIOS)
        color = QColor('black')

        self.point_item = self.addEllipse(rect, QPen(color), QBrush(color))

    def change_generator_location(self, gener_num: int, new_location: QPoint):
        previous_item = self.generator_items[gener_num]
        if previous_item is not None:
            self.removeItem(previous_item)

        self.add_generator(gener_num, new_location)

    def change_point_location(self, new_location: QPoint):
        if self.point_item is not None:
            self.removeItem(self.point_item)
        self.add_point(new_location)

