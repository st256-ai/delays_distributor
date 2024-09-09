from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from buttons import ButtonsPlaceholder
from coordinate_forms import PointLocationPlaceholder, GeneratorLocationEditorPlaceholder
from delays import DelaysPlaceholder
from grid import GridPlaceholder
from initializer import InitialValuesContainer
from services import calculate_estimated_time, send_data_to_fpga, read_data_from_file, \
    send_single_slice_of_data_to_fpga


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        initials = InitialValuesContainer()
        initial_x_values = initials.get_generators_x_initials()
        initial_y_values = initials.get_generators_y_initials()

        self.grid_widget = GridPlaceholder(initial_x_values, initial_y_values)
        self.point_location_widget = PointLocationPlaceholder(QPoint(98, 98), 'Координаты точки приема')
        self.point_location_widget.location_changed.connect(self.onPointLocationChanged)
        self.buttons = ButtonsPlaceholder()
        self.buttons.calculate_delays.connect(self.onCalculateDelays)
        self.buttons.reset_system.connect(self.onSystemReset)
        self.buttons.send_delays.connect(self.onSendDelays)
        self.buttons.calibrate_signals.connect(self.onCalibrateDelays)

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

    def onCalculateDelays(self):
        generators_locations = self.generators_locations.get_generator_locations()
        point_location = self.point_location_widget.get_location()

        generators_estimated_time = {}
        for num, location in generators_locations.items():
            generators_estimated_time[num] = calculate_estimated_time(location, point_location)

        max_estimated_time = max(generators_estimated_time.values())

        delays = {}
        for num, estimated_time in generators_estimated_time.items():
            delays[num] = abs(estimated_time - max_estimated_time)

        self.delays_widget.set_delays(delays)

    def onSystemReset(self):
        self.delays_widget.reset_delays()
        self.generators_locations.reset_locations()
        self.point_location_widget.reset_location()
        self.grid_widget.reset_grid()

    def onSendDelays(self):
        # send_data_to_fpga(self, self.delays_widget.get_previous_delays(), 0)
        delays = self.delays_widget.get_delays()
        send_data_to_fpga(self, delays, 1)
        self.delays_widget.set_previous_delays(delays)

    def onCalibrateDelays(self):
        delays_data = read_data_from_file()
        for k, v in delays_data.items():
            send_single_slice_of_data_to_fpga(self, k, v[0], v[1])
