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