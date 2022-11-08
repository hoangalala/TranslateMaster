from distutils.log import error
from email.mime import image
from time import sleep
import time
from collections import defaultdict
import os, shutil
import numpy as np
import textwrap

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtGui

from PIL import Image

from wand import image
from wand import drawing
from wand.font import Font

from pytesseract import pytesseract
from pytesseract import Output
from manga_ocr import MangaOcr

# from deepl import Translator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import cv2
from cv2 import dnn_DetectionModel as dnn

# Only needed for access to command line arguments
import sys

# imuils
from imutils.object_detection import non_max_suppression
import argparse

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


button_width = 100
button_height = 50

image_view_width = 400
image_view_height = 480

text_box_width = 400
text_box_height = 200

horizontal_distance_to_prev = 20
vertical_distance_to_prev = 15

select_file_btn_txt = "Select File"
select_file_btn_loc_X = 20
select_file_btn_loc_Y = 20

pre_translate_image_viewer_width = image_view_width
pre_translate_image_viewer_height = image_view_height
pre_translate_image_viewer_loc_X = select_file_btn_loc_X + button_width + horizontal_distance_to_prev
pre_translate_image_viewer_loc_Y = 20

post_translate_image_viewer_width = image_view_width
post_translate_image_viewer_height = image_view_height
post_translate_image_viewer_loc_X = pre_translate_image_viewer_loc_X + image_view_width + horizontal_distance_to_prev
post_translate_image_viewer_loc_Y = 20

text_box_original_width = text_box_width
text_box_original_height = text_box_height
text_box_original_loc_X = select_file_btn_loc_X + button_width + horizontal_distance_to_prev
text_box_original_loc_Y = pre_translate_image_viewer_loc_Y + pre_translate_image_viewer_height + vertical_distance_to_prev

text_box_translated_width = text_box_width
text_box_translated_height = text_box_height
text_box_translated_loc_X = text_box_original_loc_X + text_box_original_width + horizontal_distance_to_prev
text_box_translated_loc_Y = pre_translate_image_viewer_loc_Y + pre_translate_image_viewer_height + vertical_distance_to_prev



combo_box_mode_width = button_width
combo_box_mode_height = button_height
combo_box_mode_loc_X = select_file_btn_loc_X
combo_box_mode_loc_Y = select_file_btn_loc_Y + button_height + vertical_distance_to_prev
ocr_mode_list = ("Horizontal", "Vertical", "MG")
horizontal_mode_index = 0
vertical_mode_index = 1
mg_mode_index = 2

retranslate_btn_txt = "Retranslate"
retranslate_btn_loc_X = select_file_btn_loc_X
retranslate_btn_loc_Y = combo_box_mode_loc_Y + combo_box_mode_height + vertical_distance_to_prev

combo_box_iteration_width = button_width
combo_box_iteration_height = button_height
combo_box_iteration_loc_X = retranslate_btn_loc_X
combo_box_iteration_loc_Y = retranslate_btn_loc_Y + button_height + vertical_distance_to_prev

iteration_list = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")

combo_box_run_option_width = button_width
combo_box_run_option_height = button_height
combo_box_run_option_loc_X = retranslate_btn_loc_X
combo_box_run_option_loc_Y = combo_box_iteration_loc_Y + button_height + vertical_distance_to_prev

run_option_list = ("Finish", "Stop test")

check_box_show_image_loc_X = select_file_btn_loc_X
check_box_show_image_loc_Y = combo_box_run_option_loc_Y + button_height + vertical_distance_to_prev
check_box_show_image_text = "Show Image"



tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'  #C:\\Program Files\\Tesseract-OCR\\tessdata
pytesseract_jpn_lgn = "jpn"
pytesseract_jpn_vert_lgn = "jpn_vert"
translate_destination_en = "EN-US"
deepl_site_url = "https://www.deepl.com/en/translator"
cwd = os.getcwd()
google_executable_path = cwd + "\\chromedriver_win32\\chromedriver.exe"
process_factory_folder_path = cwd + "\\process_factory"
segmented_images_folder_path = process_factory_folder_path + "\\segmented_images"
processed_images_folder_path = process_factory_folder_path + "\\processed_images"

duplicated_pic_path = process_factory_folder_path + "\\temp.png"
translated_pic_path = process_factory_folder_path + "\\temp_translated.png"


# # Experimental
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# # End Experimental
driver = vars

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        # =============== Open Chrome Window =============== #
        self.open_chrome_window()

        self.set_screen()


    def open_chrome_window(self):
        self.driver = webdriver.Chrome(executable_path = google_executable_path) # , options = chrome_options

        self.driver.minimize_window()
        self.driver.get("https://www.deepl.com/translator")

    def set_screen(self):
        # =============== Screen Size =============== #
        screen_width = 1000
        screen_height = pre_translate_image_viewer_loc_Y + pre_translate_image_viewer_height + vertical_distance_to_prev + text_box_original_height + vertical_distance_to_prev

        self.setFixedSize(screen_width, screen_height)

        # =============== Select File Button =============== #
        select_file_btn = QPushButton(self)
        select_file_btn.setText(select_file_btn_txt)
        select_file_btn.setGeometry(select_file_btn_loc_X,select_file_btn_loc_Y,button_width,button_height)

        select_file_btn.clicked.connect(lambda: self.open_dialog())

        # =============== Original Text Log Box =============== #
        text_box_original = QtWidgets.QTextEdit(self)
        self.text_box_original = text_box_original
        text_box_original.setGeometry(text_box_original_loc_X, text_box_original_loc_Y, text_box_original_width, text_box_original_height)

        # =============== Translated Text Log Box =============== #
        text_box_translated = QtWidgets.QTextEdit(self)
        self.text_box_translated = text_box_translated
        text_box_translated.setGeometry(text_box_translated_loc_X, text_box_translated_loc_Y, text_box_translated_width, text_box_translated_height)

        # =============== Scan Mode Combo Box =============== #
        combo_box_mode = QtWidgets.QComboBox(self)
        self.combo_box_mode = combo_box_mode
        self.combo_box_mode.addItems(ocr_mode_list)
        combo_box_mode.setGeometry(combo_box_mode_loc_X, combo_box_mode_loc_Y, combo_box_mode_width, combo_box_mode_height)

        # =============== Retranlsate Button =============== #
        self.retranslate_btn = QPushButton(self)
        self.retranslate_btn.setText(retranslate_btn_txt)
        self.retranslate_btn.setGeometry(retranslate_btn_loc_X, retranslate_btn_loc_Y, button_width, button_height)
        self.retranslate_btn.clicked.connect(lambda: self.translate_text(self.text_box_original.toPlainText()))

        # =============== Pre Translate Image Viewer =============== #
        self.pre_translate_image_viewer = PhotoViewer(self)
        self.pre_translate_image_viewer.setGeometry(pre_translate_image_viewer_loc_X, pre_translate_image_viewer_loc_Y, pre_translate_image_viewer_width, pre_translate_image_viewer_height)

        # =============== Post Translate Image Viewer =============== #
        self.post_translate_image_viewer = PhotoViewer(self)
        self.post_translate_image_viewer.setGeometry(post_translate_image_viewer_loc_X, post_translate_image_viewer_loc_Y, post_translate_image_viewer_width, post_translate_image_viewer_height)

        # =============== Iteration Combo Box =============== #
        self.iteration_combo_box = QtWidgets.QComboBox(self)
        self.iteration_combo_box.addItems(iteration_list)
        self.iteration_combo_box.setGeometry(combo_box_iteration_loc_X, combo_box_iteration_loc_Y, combo_box_iteration_width, combo_box_iteration_height)
        self.iteration_combo_box.setCurrentIndex(4)

        # =============== Run Option Combo Box =============== #
        self.run_option_combo_box = QtWidgets.QComboBox(self)
        self.run_option_combo_box.addItems(run_option_list)
        self.run_option_combo_box.setGeometry(combo_box_run_option_loc_X, combo_box_run_option_loc_Y, combo_box_run_option_width, combo_box_run_option_height)

        # =============== Show Image Check Box =============== #
        self.show_image_check_box = QtWidgets.QCheckBox(self)
        self.show_image_check_box.move(check_box_show_image_loc_X, check_box_show_image_loc_Y)
        self.show_image_check_box.setText(check_box_show_image_text)

    def open_dialog(self):
        image_path = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
        )
        image_path = image_path[0]
        if self.check_string_not_blank(image_path):
            try:
                self.process_image(image_path)
            except BaseException as e:
                print(str(e))
                return
        else:
            print("BlankOrEmpty")

    # =============== Process Image =============== #
    def process_image(self, image_path):
        self.create_image_copy(image_path)

        pixmap = QPixmap(duplicated_pic_path)
        # self.pre_translate_image_viewer.setPhoto(pixmap)

        contour_list = self.detect_text_boxes()

        cropped_text_boxes = self.crop_text_boxes_from_image(contour_list)

        self.process_text_box_images(cropped_text_boxes, contour_list)

        self.scan_text_box_for_text(image_path)

        














    # =============== Create image copy =============== #
    def create_image_copy(self, image_path):
        image = Image.open(image_path)
        image_copy = image.copy()

        image_copy.save(duplicated_pic_path)
        image_copy.save(translated_pic_path)

    # =============== Detect text boxes =============== #
    def detect_text_boxes(self):
        iteration = self.iteration_combo_box.currentIndex()
        img = cv2.imread(duplicated_pic_path)

        test = self.run_option_combo_box.currentIndex()
        continue_process = (self.run_option_combo_box.currentIndex() == 0)

        # Convert to grayscale
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply threshold
        ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)

        # Apply bitwise
        image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
        ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY_INV)  # for black text , cv2.THRESH_BINARY_INV
                                                                                # for white text , cv2.THRESH_BINARY
        # ret, new_img = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY_INV)  # for black text , cv2.THRESH_BINARY_INV
        # #                                                                         # for white text , cv2.THRESH_BINARY
        '''
                line  8 to 12  : Remove noisy portion
        '''
 
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                            3))  # ORIGINAL 3,3 to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
        dilated = cv2.dilate(new_img, kernel, iterations = iteration)  # dilate , more the iteration more the dilation
        # dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation

        if self.show_image_check_box.isChecked():
            # cv2.imshow("mask", mask)
            # cv2.imshow("img2gray", img2gray)
            # cv2.imshow("new_img", new_img)
            cv2.imshow("final", dilated)
            # cv2.waitKey(0)

        if not continue_process:
            return
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # findContours returns 3 variables for getting contours

        # contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # findContours returns 3 variables for getting contours

        # self.filter_rectangular_contours(contours, img)

        # contour list
        contour_list = defaultdict(list)
        contour_list_idx_key = 0

        hierarchy = hierarchy[0]
        for component in zip(contours, hierarchy):
            current_contour = component[0]
            current_hierarchy = component[1]

            # parent_hierachy = current_hierarchy[2]
            if current_hierarchy[2] == -1:
                continue

            # get rectangle bounding contour
            
            # 

            [x, y, w, h] = cv2.boundingRect(current_contour)
            
            if self.is_as_big_as_img(current_contour, img):
                print("RID THIS CONTOUR" + str(current_contour), str(img.shape))
                continue

            if w < 10:
                print("skipped")
                continue
            # if y < 10:
            #     continue

            contour_rect = [x, y, w, h]

            for component in contour_rect:
                contour_list[contour_list_idx_key].append(component)
            contour_list_idx_key += 1

            # Don't plot small false positives that aren't text
            if w < 35 and h < 35:
                continue

            # draw rectangle around contour on original image
            cv2.rectangle(dilated, (x, y), (x + w, y + h), (255, 0, 0), 2)

            '''
            #you can crop image and send to OCR  , false detected will return no text :)
            cropped = img_final[y :y +  h , x : x + w]

            s = file_name + '/crop_' + str(index) + '.jpg' 
            cv2.imwrite(s , cropped)
            index = index + 1

            '''
        cv2.imshow("img", dilated)
        return contour_list

    def filter_rectangular_contours(self, contour_list, img):
        i = 0

        # list for storing names of shapes
        for contour in contour_list:
        
            # here we are ignoring first counter because 
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue
        
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True)
            
            # using drawContours() function
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
        
            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
        
            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
            else:
                cv2.putText(img, 'circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            # return False

    def is_as_big_as_img(self, contour, img):
        [x, y, w, h] = cv2.boundingRect(contour)
        # with_test = img.shape[1]
        # height_test = img.shape[0]
        if abs(w - img.shape[1]) < 20:
            if abs(h - img.shape[0]) < 20:
                return True
        return False


    # =============== Segment image =============== #
    def crop_text_boxes_from_image(self, contour_list):
        cropped_images_list = []
        import cv2
        image = cv2.imread(duplicated_pic_path)
        # clear segment image folder
        # folder = segmented_images_folder_path
        # for filename in os.listdir(folder):
        #     file_path = os.path.join(folder, filename)
        #     try:
        #         if os.path.isfile(file_path) or os.path.islink(file_path):
        #             os.unlink(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #     except Exception as e:
        #         print('Failed to delete %s. Reason: %s' % (file_path, e))
        self.clear_folder_contents(segmented_images_folder_path)
        self.clear_folder_contents(processed_images_folder_path)
        
        # Segment image
        for contour_list_index, contour in contour_list.items():
            x = contour[0]
            y = contour[1]
            w = contour[2]
            h = contour[3]
            crop_img = image[y:y+h, x:x+w]
            segmented_image_file_path = segmented_images_folder_path + "\\" + str(contour_list_index) + ".png"
            cv2.imwrite(segmented_image_file_path, crop_img)
            # contour_list[contour_list_index].append(crop_img)
            # cropped_image = cv2.imread(segmented_image_file_path)
            cropped_images_list.append(segmented_image_file_path)
        
        return cropped_images_list




    def process_text_box_images(self, text_box_images, text_box_contour_dict):
        # translated_tex_box_images_dict = defaultdict(image)
        for image_index, text_box_image in enumerate(text_box_images):
            text_box_text = self.scan_text_box_for_text(text_box_image)
            if not self.check_string_not_blank(text_box_text):
                continue
            translated_text = self.translate_text(text_box_text)
            translated_text_box_image = self.create_translated_text_box_with(translated_text, text_box_contour_dict[image_index], image_index)
        #     translated_tex_box_images_dict[text_box_index].append(translated_text_box_image)
        # self.overwrite_originated_text_boxes_with(translated_tex_box_images_dict, text_box_images)
            

    # =============== Scan image for text =============== #
    def scan_text_box_for_text(self, image_path):
        img = Image.open(image_path)

        mode_index = self.combo_box_mode.currentIndex()
        pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  #C:\Program Files\Tesseract-OCR\tesseract.exe

        # Mode: Horizontal
        if mode_index == horizontal_mode_index:
            # pytesseract.tesseract_cmd = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'  #C:\Program Files\Tesseract-OCR\tesseract.exe
            text = pytesseract.image_to_string(img, lang = pytesseract_jpn_lgn, config = tessdata_dir_config)
        # Mode: Vertical
        elif mode_index == vertical_mode_index:
            # pytesseract.tesseract_cmd = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'  #C:\Program Files\Tesseract-OCR\tesseract.exe
            text = pytesseract.image_to_string(img, lang = pytesseract_jpn_vert_lgn, config = tessdata_dir_config)
        # Mode: MG
        elif mode_index == mg_mode_index:
            mocr = MangaOcr()
            text = mocr(image_path)

        if self.check_string_not_blank(text):
            text = str.replace(text, "\n", "")
            return text
            # self.text_box_original.setText(text)
            # self.translate_text(text)
        else:
            return

    # =============== Translate text =============== #
    def translate_text(self, untranslated_text):
        if not self.check_string_not_blank(untranslated_text):
            return

        if self.is_browser_alive(self.driver):
            driver = self.driver

        else:
            self.open_chrome_window()
            driver = self.driver

        # untranslated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']")
        # if untranslated_box_element.get_attribute('value') == untranslated_text:
        #     return

        previous_translation = ""
        translated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-results-heading']")
        if (translated_box_element.get_attribute('value') != ''):
            previous_translation = translated_box_element.get_attribute('value')

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).clear()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).send_keys(untranslated_text)

        if self.check_string_not_blank(previous_translation):
            while True:
                if (translated_box_element.get_attribute('value') != previous_translation and not translated_box_element.get_attribute('value').__contains__("[...]")):
                    sleep(2)
                    if not translated_box_element.get_attribute('value').__contains__("[...]"):
                        text_target = translated_box_element.get_attribute('value')
                        break

        else:
            while True:
                if (translated_box_element.get_attribute('value') != ''):
                    sleep(1)
                    if not translated_box_element.get_attribute('value').__contains__("[...]"):
                        text_target = translated_box_element.get_attribute('value')
                        break
        return text_target

    def handle_translated_text(self, translated_text):
        self.text_box_translated.setText(translated_text)

    # =============== Create translated text box image =============== #
    def create_translated_text_box_with(self, text, text_box_dimensions, image_idex):
        if not text:
            return
        [x, y, w, h] = text_box_dimensions

        start = time.time()
        with image.Image(width=w, height=h, pseudo='xc:white') as canvas:
            padding = 2
            left = padding
            top = padding
            width = w - padding
            height = h - padding
            with drawing.Drawing() as context:
                context.fill_color = 'white'
                context.rectangle(left=left, top=top, width=width, height=height)
                font = Font('/System/Library/Fonts/MarkerFelt.ttc')
                context(canvas)
                canvas.caption(text, left=left, top=top, width=width, height=height, font=font, gravity='center')
            processed_image_path = processed_images_folder_path + "\\" + str(image_idex) + ".png"

            canvas.save(filename = processed_image_path)

            self.paste_on_large_image_with_image(processed_image_path, duplicated_pic_path, x, y)

            pixmap = QPixmap(translated_pic_path)
            self.post_translate_image_viewer.setPhoto(pixmap)
        end = time.time()
        print(text)
        print("Elapsed Time: " + str(end - start))

    def paste_on_large_image_with_image(self, small_image_path, large_image_path, x_offset, y_offset):
        s_img = cv2.imread(small_image_path)
        l_img = cv2.imread(translated_pic_path)
        try:
            l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

            cv2.imwrite(translated_pic_path, l_img)
        except:
            print("FAILED")

    # =============== Check blank string =============== #
    def check_string_not_blank(self, checkStr):
        isNotBlankOrEmpty = True
        if not checkStr:
            isNotBlankOrEmpty = False
        if checkStr == "":
            isNotBlankOrEmpty = False
        return isNotBlankOrEmpty

     # =============== Check if browser is open =============== #
    def is_browser_alive(self, driver):
        try:
            driver.current_url
            # or driver.title
            return True
        except:
            return False


    # =============== Show input dialog =============== #
    def show_input_dialog(self, title, label):
        text, ok = QInputDialog.getText(self, title, label)

        if ok:
            return text
    
    # =============== Clear Folder By Directory Path =============== #
    def clear_folder_contents(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)


def My_app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    My_app()