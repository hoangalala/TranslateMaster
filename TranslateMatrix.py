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

    # =============== Auto Mode Select Button =============== #
    exit_btn = DrawScreen.draw_button_bottom_left(main_window, GlobalVariables.exit_btn_txt, GlobalVariables.exit_btn_rect)
    exit_btn.clicked.connect(lambda: exit_btn_clicked(main_window))

def auto_mode_select_btn_clicked(main_window: window, auto_mode_select_btn):
    QPushButton.setEnabled(auto_mode_select_btn, False)
    main_window.hide()
    main_window.auto_scan_window = AutoScanWindow.window()
    main_window.auto_scan_window.exec()
    main_window.show()
    QPushButton.setEnabled(auto_mode_select_btn, True)

def exit_btn_clicked(main_window: window):
    main_window.close()

def My_app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    My_app()