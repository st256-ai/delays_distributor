import math
import time

import serial
from PySide6.QtCore import QPoint
from PySide6.QtSerialPort import QSerialPortInfo

FILE_PATH = './resources/test.txt'
SLEEP_TIME = 0.001
SHIFT_QUANTUM = 100

SPEED = 3 * 10 ** 8
PICO = 10**12
SANTI = 10**-2


def calculate_length(first_point: QPoint, second_point: QPoint) -> float:
    return math.sqrt(
        abs(first_point.x() ** 2 - second_point.x() ** 2) + abs(first_point.y() ** 2 - second_point.y() ** 2))


def calculate_estimated_time(generator_location: QPoint, reception_point: QPoint) -> float:
    length = calculate_length(generator_location, reception_point)
    return length * SANTI * PICO / SPEED


def read_data_from_file():
    pass


def send_data_to_fpga(delays: {int, float}):
    data_to_send = {}
    for k, v in delays.items():
        data_to_send[k] = v / SHIFT_QUANTUM

    info_list = QSerialPortInfo()
    ports = info_list.availablePorts()

    if len(ports) == 0:
        return

    ser = serial.Serial(str(ports[0]), 9600)
    for k, v in data_to_send.items():
        ser.write(str.encode(k))
        time.sleep(SLEEP_TIME)
        ser.write(str.encode(v))
        time.sleep(SLEEP_TIME)

