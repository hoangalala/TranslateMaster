import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtGui

from classes import GlobalVariables
from classes import ProcessImage
from classes import SeleniumOperations
from classes import DrawScreen

def call_auto_scan_window(previous_window):
    # app = QApplication(sys.argv)
    win = window()
    win.show()
    # sys.exit(app.exec())

class window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        # self.initUI()

        self.setWindowTitle(GlobalVariables.auto_scan_window_title)
        # =============== Open Chrome Window =============== #
        self.driver = SeleniumOperations.open_chrome_window()

        set_screen(self)

        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.driver.quit()
        return super().closeEvent(a0)

    # def __init__(self):
    #     super(window, self).__init__()
    #     self.setWindowTitle(GlobalVariables.auto_scan_window_title)
    #     # =============== Open Chrome Window =============== #
    #     self.driver = SeleniumOperations.open_chrome_window()

    #     set_screen(self)



def set_screen(auto_scan_window):
    # =============== Screen Size =============== #
    screen_width = 1000
    screen_height = GlobalVariables.pre_translate_image_viewer_loc_Y + GlobalVariables.pre_translate_image_viewer_height + GlobalVariables.vertical_distance_to_prev + GlobalVariables.text_box_original_height + GlobalVariables.vertical_distance_to_prev

    auto_scan_window.setFixedSize(screen_width, screen_height)

    # =============== Select File Button =============== #
    select_file_btn = DrawScreen.draw_button(auto_scan_window, GlobalVariables.select_file_btn_txt, GlobalVariables.select_file_btn_rect)
    select_file_btn.clicked.connect(lambda: open_dialog(auto_scan_window))

    # =============== Original Text Log Box =============== #
    text_box_original = QtWidgets.QTextEdit(auto_scan_window)
    auto_scan_window.text_box_original = text_box_original
    text_box_original.setGeometry(GlobalVariables.text_box_original_loc_X, GlobalVariables.text_box_original_loc_Y, GlobalVariables.text_box_original_width, GlobalVariables.text_box_original_height)

    # =============== Translated Text Log Box =============== #
    text_box_translated = QtWidgets.QTextEdit(auto_scan_window)
    auto_scan_window.text_box_translated = text_box_translated
    text_box_translated.setGeometry(GlobalVariables.text_box_translated_loc_X, GlobalVariables.text_box_translated_loc_Y, GlobalVariables.text_box_translated_width, GlobalVariables.text_box_translated_height)

    # =============== Scan Mode Combo Box =============== #
    combo_box_mode = QtWidgets.QComboBox(auto_scan_window)
    auto_scan_window.combo_box_mode = combo_box_mode
    auto_scan_window.combo_box_mode.addItems(GlobalVariables.ocr_mode_list)
    combo_box_mode.setGeometry(GlobalVariables.combo_box_mode_loc_X, GlobalVariables.combo_box_mode_loc_Y, GlobalVariables.combo_box_mode_width, GlobalVariables.combo_box_mode_height)

    # =============== Retranlsate Button =============== #
    retranslate_btn = DrawScreen.draw_button(auto_scan_window, GlobalVariables.retranslate_btn_txt, GlobalVariables.retranslate_btn_rect)
    retranslate_btn.clicked.connect(lambda: auto_scan_window.translate_text(auto_scan_window.text_box_original.toPlainText()))

    # =============== Pre Translate Image Viewer =============== #
    auto_scan_window.pre_translate_image_viewer = PhotoViewer(auto_scan_window)
    auto_scan_window.pre_translate_image_viewer.setGeometry(GlobalVariables.pre_translate_image_viewer_loc_X, GlobalVariables.pre_translate_image_viewer_loc_Y, GlobalVariables.pre_translate_image_viewer_width, GlobalVariables.pre_translate_image_viewer_height)

    # =============== Post Translate Image Viewer =============== #
    auto_scan_window.post_translate_image_viewer = PhotoViewer(auto_scan_window)
    auto_scan_window.post_translate_image_viewer.setGeometry(GlobalVariables.post_translate_image_viewer_loc_X, GlobalVariables.post_translate_image_viewer_loc_Y, GlobalVariables.post_translate_image_viewer_width, GlobalVariables.post_translate_image_viewer_height)

    # =============== Iteration Combo Box =============== #
    auto_scan_window.iteration_combo_box = QtWidgets.QComboBox(auto_scan_window)
    auto_scan_window.iteration_combo_box.addItems(GlobalVariables.iteration_list)
    auto_scan_window.iteration_combo_box.setGeometry(GlobalVariables.combo_box_iteration_loc_X, GlobalVariables.combo_box_iteration_loc_Y, GlobalVariables.combo_box_iteration_width, GlobalVariables.combo_box_iteration_height)
    auto_scan_window.iteration_combo_box.setCurrentIndex(4)

    # =============== Run Option Combo Box =============== #
    auto_scan_window.run_option_combo_box = QtWidgets.QComboBox(auto_scan_window)
    auto_scan_window.run_option_combo_box.addItems(GlobalVariables.run_option_list)
    auto_scan_window.run_option_combo_box.setGeometry(GlobalVariables.combo_box_run_option_loc_X, GlobalVariables.combo_box_run_option_loc_Y, GlobalVariables.combo_box_run_option_width, GlobalVariables.combo_box_run_option_height)

    # =============== Show Image Check Box =============== #
    auto_scan_window.show_image_check_box = QtWidgets.QCheckBox(auto_scan_window)
    auto_scan_window.show_image_check_box.move(GlobalVariables.check_box_show_image_loc_X, GlobalVariables.check_box_show_image_loc_Y)
    auto_scan_window.show_image_check_box.setText(GlobalVariables.check_box_show_image_text)

    # =============== Back Button =============== #
    back_btn = DrawScreen.draw_button_bottom_left(auto_scan_window, GlobalVariables.back_btn_txt, GlobalVariables.auto_scan_mode_select_btn_rect)
    back_btn.clicked.connect(lambda: back_btn_clicked(auto_scan_window))


def open_dialog(auto_scan_window):
    try:
        image_path = QFileDialog.getOpenFileName(
            auto_scan_window,
            "Open File",
            "",
            "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
        )
        image_path = image_path[0]
        # if self.check_string_not_blank(image_path):
        ProcessImage.process_image(auto_scan_window, GlobalVariables.duplicated_pic_path)
    except BaseException as e:
        print(str(e))
        return

def back_btn_clicked(auto_scan_window: window):
    auto_scan_window.close()













class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(auto_scan_window, parent):
        super(PhotoViewer, auto_scan_window).__init__(parent)
        auto_scan_window._zoom = 0
        auto_scan_window._empty = True
        auto_scan_window._scene = QtWidgets.QGraphicsScene(auto_scan_window)
        auto_scan_window._photo = QtWidgets.QGraphicsPixmapItem()
        auto_scan_window._scene.addItem(auto_scan_window._photo)
        auto_scan_window.setScene(auto_scan_window._scene)
        auto_scan_window.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        auto_scan_window.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        auto_scan_window.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        auto_scan_window.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        auto_scan_window.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        auto_scan_window.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def hasPhoto(auto_scan_window):
        return not auto_scan_window._empty

    def fitInView(auto_scan_window, scale=True):
        rect = QtCore.QRectF(auto_scan_window._photo.pixmap().rect())
        if not rect.isNull():
            auto_scan_window.setSceneRect(rect)
            if auto_scan_window.hasPhoto():
                unity = auto_scan_window.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                auto_scan_window.scale(1 / unity.width(), 1 / unity.height())
                viewrect = auto_scan_window.viewport().rect()
                scenerect = auto_scan_window.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                auto_scan_window.scale(factor, factor)
            auto_scan_window._zoom = 0

    def setPhoto(auto_scan_window, pixmap=None):
        auto_scan_window._zoom = 0
        if pixmap and not pixmap.isNull():
            auto_scan_window._empty = False
            auto_scan_window.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            auto_scan_window._photo.setPixmap(pixmap)
        else:
            auto_scan_window._empty = True
            auto_scan_window.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            auto_scan_window._photo.setPixmap(QtGui.QPixmap())
        auto_scan_window.fitInView()

    def wheelEvent(auto_scan_window, event):
        if auto_scan_window.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                auto_scan_window._zoom += 1
            else:
                factor = 0.8
                auto_scan_window._zoom -= 1
            if auto_scan_window._zoom > 0:
                auto_scan_window.scale(factor, factor)
            elif auto_scan_window._zoom == 0:
                auto_scan_window.fitInView()
            else:
                auto_scan_window._zoom = 0

    def toggleDragMode(auto_scan_window):
        if auto_scan_window.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            auto_scan_window.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif not auto_scan_window._photo.pixmap().isNull():
            auto_scan_window.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mousePressEvent(auto_scan_window, event):
        if auto_scan_window._photo.isUnderMouse():
            auto_scan_window.photoClicked.emit(auto_scan_window.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, auto_scan_window).mousePressEvent(event)