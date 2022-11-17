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

# Only needed for access to command line arguments
import sys
from classes import SeleniumOperations
from classes import GlobalVariables

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
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

# =============== Process Image =============== #
def process_image(auto_scan_window, image_path):
    create_image_copy(image_path)

    pixmap = QPixmap(duplicated_pic_path)
    # auto_scan_window.pre_translate_image_viewer.setPhoto(pixmap)

    contour_list = detect_text_boxes(auto_scan_window)

    cropped_text_boxes = crop_text_boxes_from_image(contour_list)

    process_text_box_images(auto_scan_window, cropped_text_boxes, contour_list)

    scan_text_box_for_text(auto_scan_window, image_path)

    














# =============== Create image copy =============== #
def create_image_copy(image_path):
    image = Image.open(image_path)
    image_copy = image.copy()

    image_copy.save(duplicated_pic_path)
    image_copy.save(translated_pic_path)

# =============== Detect text boxes =============== #
def detect_text_boxes(auto_scan_window):
    iteration = auto_scan_window.iteration_combo_box.currentIndex()
    img = cv2.imread(duplicated_pic_path)

    continue_process = (auto_scan_window.run_option_combo_box.currentIndex() == 0)

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

    if auto_scan_window.show_image_check_box.isChecked():
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
        
        if is_as_big_as_img(current_contour, img):
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

def filter_rectangular_contours(contour_list, img):
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

def is_as_big_as_img(contour, img):
    [x, y, w, h] = cv2.boundingRect(contour)
    if abs(w - img.shape[1]) < 20:
        if abs(h - img.shape[0]) < 20:
            return True
    return False


# =============== Segment image =============== #
def crop_text_boxes_from_image(contour_list):
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
    clear_folder_contents(segmented_images_folder_path)
    clear_folder_contents(processed_images_folder_path)
    
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




def process_text_box_images(auto_scan_window, text_box_images, text_box_contour_dict):
    # translated_tex_box_images_dict = defaultdict(image)
    for image_index, text_box_image in enumerate(text_box_images):
        text_box_text = scan_text_box_for_text(auto_scan_window, text_box_image)
        if not check_string_not_blank(text_box_text):
            continue
        translated_text = translate_text(auto_scan_window, text_box_text)
        translated_text_box_image = create_translated_text_box_with(translated_text, text_box_contour_dict[image_index], image_index)
    #     translated_tex_box_images_dict[text_box_index].append(translated_text_box_image)
    # self.overwrite_originated_text_boxes_with(translated_tex_box_images_dict, text_box_images)
        

# =============== Scan image for text =============== #
def scan_text_box_for_text(auto_scan_window, image_path):
    img = Image.open(image_path)

    mode_index = auto_scan_window.combo_box_mode.currentIndex()
    pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  #C:\Program Files\Tesseract-OCR\tesseract.exe

    # Mode: Horizontal
    if mode_index == GlobalVariables.horizontal_mode_index:
        # pytesseract.tesseract_cmd = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'  #C:\Program Files\Tesseract-OCR\tesseract.exe
        text = pytesseract.image_to_string(img, lang = pytesseract_jpn_lgn, config = tessdata_dir_config)
    # Mode: Vertical
    elif mode_index == GlobalVariables.vertical_mode_index:
        # pytesseract.tesseract_cmd = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'  #C:\Program Files\Tesseract-OCR\tesseract.exe
        text = pytesseract.image_to_string(img, lang = pytesseract_jpn_vert_lgn, config = tessdata_dir_config)
    # Mode: MG
    elif mode_index == GlobalVariables.mg_mode_index:
        mocr = MangaOcr()
        text = mocr(image_path)

    if check_string_not_blank(text):
        text = str.replace(text, "\n", "")
        return text
    else:
        return

# =============== Translate text =============== #
def translate_text(auto_scan_window, untranslated_text):
    if not check_string_not_blank(untranslated_text):
        return

    if is_browser_alive(auto_scan_window.driver):
        driver = auto_scan_window.driver

    else:
        driver = SeleniumOperations.open_chrome_window()

    # untranslated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']")
    # if untranslated_box_element.get_attribute('value') == untranslated_text:
    #     return

    previous_translation = ""
    translated_box_element = driver.find_element(By.XPATH, "//textarea[@aria-labelledby='translation-results-heading']")
    if (translated_box_element.get_attribute('value') != ''):
        previous_translation = translated_box_element.get_attribute('value')

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).clear()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-labelledby='translation-source-heading']"))).send_keys(untranslated_text)

    if check_string_not_blank(previous_translation):
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

def handle_translated_text(auto_scan_window, translated_text):
    auto_scan_window.text_box_translated.setText(translated_text)

# =============== Create translated text box image =============== #
def create_translated_text_box_with(auto_scan_window, text, text_box_dimensions, image_idex):
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

        paste_on_large_image_with_image(processed_image_path, duplicated_pic_path, x, y)

        pixmap = QPixmap(translated_pic_path)
        auto_scan_window.post_translate_image_viewer.setPhoto(pixmap)
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
def check_string_not_blank(checkStr):
    isNotBlankOrEmpty = True
    if not checkStr:
        isNotBlankOrEmpty = False
    if checkStr == "":
        isNotBlankOrEmpty = False
    return isNotBlankOrEmpty

    # =============== Check if browser is open =============== #
def is_browser_alive(driver):
    try:
        driver.current_url
        # or driver.title
        return True
    except:
        return False


# =============== Show input dialog =============== #
def show_input_dialog(auto_scan_window, title, label):
    text, ok = QInputDialog.getText(auto_scan_window, title, label)

    if ok:
        return text

# =============== Clear Folder By Directory Path =============== #
def clear_folder_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))