import enum

from PySide6.QtCore import QPoint, QRect, QPointF, QSize, Qt
from PySide6.QtGui import QBrush, QColor
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
    RADIUS: int = 20

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

        self.view = QGraphicsView()
        self.view.setScene(Scene())
        self.view.adjustSize()
        self.view.setFixedHeight(400)
        self.view.setFixedWidth(500)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def add_system_item(self, system_item: SystemItem):
        self.view.scene().addItem(system_item)


class Scene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(Qt.BrushStyle.Dense6Pattern)
        self.setSceneRect(QRect(0, 0, 100, 200))
