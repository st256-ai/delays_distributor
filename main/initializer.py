import math

from PySide6.QtCore import QPoint


class InitialValuesContainer:
    CENTER_X = 250
    CENTER_Y = 200

    def __init__(self):
        self._generators_initial_xs = []
        self._generators_initial_ys = []
        self._signal_distributor_initial_coordinates = QPoint(0, 0)
        self.initialize()

    def get_signal_distributor_initial_coordinates(self):
        return self._signal_distributor_initial_coordinates

    def get_generators_x_initials(self):
        return self._generators_initial_xs

    def get_generators_y_initials(self):
        return self._generators_initial_ys

    def initialize(self):
        sl = 2 * math.pi / 8
        radius = 40
        for i in range(0, 9):
            angle = sl * i
            x = int((self.CENTER_X + radius * math.cos(angle)))
            y = int((self.CENTER_Y + radius * math.sin(angle)))
            self._generators_initial_xs.append(x)
            self._generators_initial_ys.append(y)

        print("Initial coordinates: gener_initial_xs=" + str(self._generators_initial_xs) + ", gener_initial_ys="
              + str(self._generators_initial_ys))
