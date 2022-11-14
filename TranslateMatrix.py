from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

# Import Classes
from classes import ProcessImage
from classes import GlobalVariables
from classes import SeleniumOperations
from classes import AutoScanWindow
driver = vars

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle(GlobalVariables.main_window_title)

        AutoScanWindow.call_auto_scan_window(self)

def set_screen(main_window):
    # =============== Screen Size =============== #
    screen_width = 400
    screen_height = 600
    main_window.setFixedSize(screen_width, screen_height)

    

def My_app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    My_app()