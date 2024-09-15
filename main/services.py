import math
import time

import serial
from PySide6.QtCore import QPoint
from PySide6.QtSerialPort import QSerialPortInfo
from PySide6.QtWidgets import QMessageBox, QWidget

CALIBRATE_FILE_PATH = '../resources/calibrate.txt'
SLEEP_TIME = 0.01  # seconds
SHIFT_QUANTUM = 100  # picoseconds
BAUD_RATE = 921600

SPEED = 3 * 10 ** 8
PICO = 10 ** -12
SANTI = 10 ** -2


def calculate_length(first_point: QPoint, second_point: QPoint) -> float:
    return math.sqrt(
        abs(first_point.x() ** 2 - second_point.x() ** 2) + abs(first_point.y() ** 2 - second_point.y() ** 2))


def calculate_estimated_time(generator_location: QPoint, reception_point: QPoint) -> float:
    length = calculate_length(generator_location, reception_point)
    return (length * SANTI) / (SPEED * PICO)


def write_data_to_file(data: {int, (int, float)}) -> None:
    f = open(CALIBRATE_FILE_PATH, mode='w', encoding='utf-8')

    for k, v in data.items():
        line_to_write = str(k) + ' ' + str(v[0]) + ' ' + str(v[1]) + '\n'
        f.write(line_to_write)
    f.close()


def read_data_from_file() -> {int, (float, int)}:
    data = {}

    f = open(CALIBRATE_FILE_PATH, mode='r', encoding='utf-8')
    while True:
        line = f.readline()
        if not line:
            break

        split_line = str.split(line, ' ')
        gener_num = int(split_line[0])
        delay = float(split_line[1])
        direction = int(split_line[2])
        data[gener_num] = (delay, direction)
    f.close()

    print('Received data for calibration: ' + str(data))
    return data


def send_single_slice_of_data_to_fpga(widget: QWidget, gener_num: int, delay: float, shift_direction: int):
    send_data_to_fpga(widget, {gener_num: delay}, shift_direction)


def send_data_to_fpga(widget: QWidget, delays: {int, float}, shift_direction: int):
    data_to_send = {}
    for k, v in delays.items():
        data_to_send[k] = int(v / SHIFT_QUANTUM)

    info_list = QSerialPortInfo()
    ports = info_list.availablePorts()

    if len(ports) == 0:
        QMessageBox.critical(widget, "Error", "FPGA не подключено к порту компьютера!")
        return

    dir_string = str(shift_direction)
    ser = serial.Serial(str(ports[0].portName()), BAUD_RATE)
    for k, v in data_to_send.items():
        print('Sending gener_num...')
        ser.write(str.encode(str(k), encoding='ascii'))
        time.sleep(SLEEP_TIME)
        print('gener_num was sent!')

        print('Sending direction...')
        ser.write(str.encode(dir_string, encoding='ascii'))
        time.sleep(SLEEP_TIME)
        print('Direction was sent!')

        length = len(str(v))
        print('number=' + str(v))
        for i in range(length, 0, -1):
            num_part = int(v / 10 ** (i - 1) % 10)
            print('sending num_part=' + str(num_part) + ' of number=' + str(v) + ' for gener №' + str(k))
            ser.write(str.encode(str(num_part), encoding='ascii'))
            print('sending num_part=' + str(num_part) + ' was sent!')
            time.sleep(SLEEP_TIME)

        print('Sending STOP byte...')
        ser.write(str.encode('s', encoding='ascii'))
        print('STOP byte was sent!')
        time.sleep(SLEEP_TIME)

    QMessageBox.information(widget, "Info", "Задержки были успешно отправлены")
    return
