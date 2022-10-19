from time import sleep
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtGui

from PIL import Image
from pytesseract import pytesseract
from manga_ocr import MangaOcr

# from deepl import Translator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import cv2


# Only needed for access to command line arguments
import sys


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



tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
pytesseract_jpn_lgn = "jpn"
pytesseract_jpn_vert_lgn = "jpn_vert"
translate_destination_en = "EN-US"
deepl_site_url = "https://www.deepl.com/en/translator"
cwd = os.getcwd()
google_executable_path = cwd + "\\chromedriver_win32\\chromedriver.exe"


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

    def open_dialog(self):
        image_path = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
        )
        image_path = image_path[0]
        if self.string_not_blank(image_path):
            self.process_image(image_path)
        else:
            print("BlankOrEmpty")

    # =============== Process Image =============== #
    def process_image(self, image_path):
        self.captch_ex(image_path)

        pixmap = QPixmap(image_path)
        self.pre_translate_image_viewer.setPhoto(pixmap)

        self.scan_image_for_text(image_path)

    # =============== Scan image for text =============== #
    def scan_image_for_text(self, image_path):
        img = Image.open(image_path)

        mode_index = self.combo_box_mode.currentIndex()
            
        # Mode: Horizontal
        if mode_index == horizontal_mode_index:
            pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(img, lang = pytesseract_jpn_lgn, config = tessdata_dir_config)
        # Mode: Vertical
        elif mode_index == vertical_mode_index:
            text = pytesseract.image_to_string(img, lang = pytesseract_jpn_vert_lgn, config = tessdata_dir_config)
        # Mode: MG
        elif mode_index == mg_mode_index:
            mocr = MangaOcr()
            text = mocr(image_path)

        if self.string_not_blank(text):
            self.text_box_original.setText(text)
            self.translate_text(text)
        else:
            return

    # =============== Translate text =============== #
    def translate_text(self, untranslated_text):
        if not self.string_not_blank(untranslated_text):
            return

        if self.is_browser_alive(self.driver):
            driver = self.driver

        else:
            self.open_chrome_window()
            driver = self.driver

        untranslated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']")
        if untranslated_box_element.get_attribute('value') == untranslated_text:
            return

        previous_translation = ""
        translated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-results-heading']")
        if (translated_box_element.get_attribute('value') != ''):
            previous_translation = translated_box_element.get_attribute('value')

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).clear()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).send_keys(untranslated_text)

        if self.string_not_blank(previous_translation):
            while True:
                if (translated_box_element.get_attribute('value') != previous_translation and not translated_box_element.get_attribute('value').__contains__("[...]")):
                    sleep(1)
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
        self.handle_translated_text(text_target)

    def handle_translated_text(self, translated_text):
        self.text_box_translated.setText(translated_text)

    # =============== Check blank string =============== #
    def string_not_blank(self, checkStr):
        isNotBlankOrEmpty = True
        if not checkStr:
            isNotBlankOrEmpty = False
        if checkStr == "":
            isNotBlankOrEmpty = False
        return isNotBlankOrEmpty

    def is_browser_alive(self, driver):
        try:
            driver.current_url
            # or driver.title
            return True
        except:
            return False

    def captch_ex(self, file_name):
        img = cv2.imread(file_name)

        img_final = cv2.imread(file_name)
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
        image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
        ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY_INV)  # for black text , cv.THRESH_BINARY_INV
                                                                                # for white text , cv.THRESH_BINARY
        '''
                line  8 to 12  : Remove noisy portion 
        '''
 
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                            3))  # ORIGINAL 3,3 to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
        dilated = cv2.dilate(new_img, kernel, iterations=5)  # dilate , more the iteration more the dilation
        # dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation

        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # findContours returns 3 variables for getting contours

        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # Don't plot small false positives that aren't text
            if w < 35 and h < 35:
                continue

            # draw rectangle around contour on original image
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

            '''
            #you can crop image and send to OCR  , false detected will return no text :)
            cropped = img_final[y :y +  h , x : x + w]

            s = file_name + '/crop_' + str(index) + '.jpg' 
            cv2.imwrite(s , cropped)
            index = index + 1

            '''
        # write original image with added contours to disk
        cv2.imshow('dilate', dilated)
        cv2.imshow('captcha_result', img)
        cv2.waitKey()

    def locate_text(self, image_path):
        # Load image, grayscale, Gaussian blur, adaptive threshold
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9,9), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

        # Dilate to combine adjacent text contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
        dilate = cv2.dilate(thresh, kernel, iterations=4)

        # Find contours, highlight text areas, and extract ROIs
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        ROI_number = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 10000:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
                # ROI = image[y:y+h, x:x+w]
                # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
                # ROI_number += 1

        cv2.imshow('thresh', thresh)
        cv2.imshow('dilate', dilate)
        cv2.imshow('image', image)
        cv2.waitKey()
    # def try_online_git(self, in_file):
    #     img = cv2.imread(infile)
    #     gray = clean.grayscale(img)

    #     # binary_threshold=arg.integer_value('binary_threshold',default_value=defaults.BINARY_THRESHOLD)
    #     # if arg.boolean_value('verbose'):
    #     #     print('Binarizing with threshold value of ' + str(binary_threshold))
    #     # inv_binary = cv2.bitwise_not(clean.binarize(gray, threshold=binary_threshold))
    #     # binary = clean.binarize(gray, threshold=binary_threshold)

    #     segmented_image = seg.segment_image(gray)
    #     segmented_image = segmented_image[:,:,2]
    #     components = cc.get_connected_components(segmented_image)
    #     cc.draw_bounding_boxes(img,components,color=(255,0,0),line_size=2)

    #     imsave(outfile, img)

        
    #     cv2.imshow('segmented_image',segmented_image)
    #     cv2.waitKey()
    
    # def segment_image(img, max_scale=4.0, min_scale=0.15):
    #     (h,w)=img.shape[:2]

    #     if arg.boolean_value('verbose'):
    #         print('Segmenting ' + str(h) + 'x' + str(w) + ' image.')

    #     #create gaussian filtered and unfiltered binary images
    #     binary_threshold = arg.integer_value('binary_threshold',default_value=defaults.BINARY_THRESHOLD)
    #     if arg.boolean_value('verbose'):
    #         print('binarizing images with threshold value of ' + str(binary_threshold))
    #     binary = clean.binarize(img,threshold=binary_threshold)

    #     binary_average_size = cc.average_size(binary)
    #     if arg.boolean_value('verbose'):
    #         print('average cc size for binaryized grayscale image is ' + str(binary_average_size))
    #     '''
    #     The necessary sigma needed for Gaussian filtering (to remove screentones and other noise) seems
    #     to be a function of the resolution the manga was scanned at (or original page size, I'm not sure).
    #     Assuming 'normal' page size for a phonebook style Manga is 17.5cmx11.5cm (6.8x4.5in).
    #     A scan of 300dpi will result in an image about 1900x1350, which requires a sigma of 1.5 to 1.8.
    #     I'm encountering many smaller images that may be nonstandard scanning dpi values or just smaller
    #     magazines. Haven't found hard info on this yet. They require sigma values of about 0.5 to 0.7.
    #     I'll therefore (for now) just calculate required (nonspecified) sigma as a linear function of vertical
    #     image resolution.
    #     '''
    #     sigma = (0.8/676.0)*float(h)-0.9
    #     sigma = arg.float_value('sigma',default_value=sigma)
    #     if arg.boolean_value('verbose'):
    #         print('Applying Gaussian filter with sigma (std dev) of ' + str(sigma))
    #     gaussian_filtered = scipy.ndimage.gaussian_filter(img, sigma=sigma)

    #     gaussian_binary = clean.binarize(gaussian_filtered,threshold=binary_threshold)

    #     #Draw out statistics on average connected component size in the rescaled, binary image
    #     average_size = cc.average_size(gaussian_binary)
    #     if arg.boolean_value('verbose'):
    #         print('Binarized Gaussian filtered image average cc size: ' + str(average_size))
    #     max_size = average_size*max_scale
    #     min_size = average_size*min_scale

    #     #primary mask is connected components filtered by size
    #     mask = cc.form_mask(gaussian_binary, max_size, min_size)

    #     #secondary mask is formed from canny edges
    #     canny_mask = clean.form_canny_mask(gaussian_filtered, mask=mask)

    #     #final mask is size filtered connected components on canny mask
    #     final_mask = cc.form_mask(canny_mask, max_size, min_size)

    #     #apply mask and return images
    #     cleaned = cv2.bitwise_not(final_mask * binary)
    #     text_only = cleaned2segmented(cleaned, average_size)

    #     #if desired, suppress furigana characters (which interfere with OCR)
    #     suppress_furigana = arg.boolean_value('furigana')
    #     if suppress_furigana:
    #         if arg.boolean_value('verbose'):
    #         print('Attempting to suppress furigana characters which interfere with OCR.')
    #         furigana_mask = furigana.estimate_furigana(cleaned, text_only)
    #         furigana_mask = np.array(furigana_mask==0,'B')
    #         cleaned = cv2.bitwise_not(cleaned)*furigana_mask
    #         cleaned = cv2.bitwise_not(cleaned)
    #         text_only = cleaned2segmented(cleaned, average_size)

    #     (text_like_areas, nontext_like_areas) = filter_text_like_areas(img, segmentation=text_only, average_size=average_size)
    #     if arg.boolean_value('verbose'):
    #         print('**********there are ' + str(len(text_like_areas)) + ' text like areas total.')
    #     text_only = np.zeros(img.shape)
    #     cc.draw_bounding_boxes(text_only, text_like_areas,color=(255),line_size=-1)

    #     if arg.boolean_value('debug'):
    #         text_only = 0.5*text_only + 0.5*img
    #         #text_rows = 0.5*text_rows+0.5*gray
    #         #text_colums = 0.5*text_columns+0.5*gray

    #     #text_only = filter_text_like_areas(img, segmentation=text_only, average_size=average_size)

    #     segmented_image = np.zeros((h,w,3), np.uint8)
    #     segmented_image[:,:,0] = img
    #     segmented_image[:,:,1] = text_only
    #     segmented_image[:,:,2] = text_only
    #     return segmented_image

















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