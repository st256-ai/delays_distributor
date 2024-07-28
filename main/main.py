import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from main_widget import MainWidget

app = QApplication(sys.argv)

main_window = QMainWindow()

main_widget = MainWidget()
main_window.setCentralWidget(main_widget)

main_window.show()

app.exec()
