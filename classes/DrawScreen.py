from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtGui

from classes import GlobalVariables

def draw_button(window, button_title, button_rect):
    btn = QPushButton(window)
    btn.setText(button_title)
    (x, y, w, h) = button_rect
    btn.setGeometry(x ,y, w, h)
    return btn

def draw_button_bottom_left(window: QMainWindow, button_title, button_rect):
    btn = QPushButton(window)
    btn.setText(button_title)
    (x, y, w, h) = button_rect
    # print(str(window.size()))
    window_height = window.size().height()
    y = window_height - GlobalVariables.vertical_distance_to_prev - GlobalVariables.button_height
    btn.setGeometry(x, y, w, h)
    return btn