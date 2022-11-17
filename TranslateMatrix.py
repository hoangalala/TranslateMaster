from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

# Import Classes
from classes import ProcessImage
from classes import GlobalVariables
from classes import SeleniumOperations
from classes import AutoScanWindow
from classes import DrawScreen
driver = vars
# auto_mode_select_btn = QPushButton

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle(GlobalVariables.main_window_title)
        set_screen(self)

        # AutoScanWindow.call_auto_scan_window(self)

def set_screen(main_window):
    # =============== Screen Size =============== #
    screen_width = 400
    screen_height = 500
    main_window.setFixedSize(screen_width, screen_height)

    # =============== Auto Mode Select Button =============== #
    auto_mode_select_btn = DrawScreen.draw_button(main_window, GlobalVariables.auto_scan_mode_select_btn_text, GlobalVariables.auto_scan_mode_select_btn_rect)
    auto_mode_select_btn.clicked.connect(lambda: auto_mode_select_btn_clicked(main_window, auto_mode_select_btn))

def auto_mode_select_btn_clicked(main_window, auto_mode_select_btn):
    QPushButton.setEnabled(auto_mode_select_btn, False)
    AutoScanWindow.call_auto_scan_window(main_window)
    # QPushButton.setDisabled(auto_mode_select_btn, True)

def My_app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    My_app()