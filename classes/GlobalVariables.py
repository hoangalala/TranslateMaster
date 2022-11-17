import os

button_width = 100
button_height = 50

image_view_width = 400
image_view_height = 480

text_box_width = 400
text_box_height = 200

horizontal_distance_to_prev = 20
vertical_distance_to_prev = 15

# =============== Select file button =============== #
auto_scan_mode_select_btn_text = "Auto Scan Mode"
auto_scan_mode_select_btn_width = button_width
auto_scan_mode_select_btn_height = button_height
auto_scan_mode_select_btn_loc_X = 20
auto_scan_mode_select_btn_loc_Y = 20
auto_scan_mode_select_btn_rect = (auto_scan_mode_select_btn_loc_X, auto_scan_mode_select_btn_loc_Y, auto_scan_mode_select_btn_width, auto_scan_mode_select_btn_height)

# =============== Select file button =============== #
select_file_btn_txt = "Select File"
select_file_btn_width = button_width
select_file_btn_height = button_height
select_file_btn_loc_X = 20
select_file_btn_loc_Y = 20
select_file_btn_rect = (select_file_btn_loc_X, select_file_btn_loc_Y, select_file_btn_width, select_file_btn_height)

# =============== Pre translate image viewer =============== #
pre_translate_image_viewer_width = image_view_width
pre_translate_image_viewer_height = image_view_height
pre_translate_image_viewer_loc_X = select_file_btn_loc_X + button_width + horizontal_distance_to_prev
pre_translate_image_viewer_loc_Y = 20
pre_translate_image_viewer_rect = (pre_translate_image_viewer_loc_X, pre_translate_image_viewer_loc_Y, pre_translate_image_viewer_width, pre_translate_image_viewer_height)

# =============== Post translate image viewer =============== #
post_translate_image_viewer_width = image_view_width
post_translate_image_viewer_height = image_view_height
post_translate_image_viewer_loc_X = pre_translate_image_viewer_loc_X + image_view_width + horizontal_distance_to_prev
post_translate_image_viewer_loc_Y = 20
post_translate_image_viewer_rect = (post_translate_image_viewer_loc_X, post_translate_image_viewer_loc_Y, post_translate_image_viewer_width, post_translate_image_viewer_height)

# =============== Pre translate textbox =============== #
text_box_original_width = text_box_width
text_box_original_height = text_box_height
text_box_original_loc_X = select_file_btn_loc_X + button_width + horizontal_distance_to_prev
text_box_original_loc_Y = pre_translate_image_viewer_loc_Y + pre_translate_image_viewer_height + vertical_distance_to_prev
text_box_original_rect = (text_box_original_loc_X, text_box_original_loc_Y, text_box_original_width, text_box_original_height)

# =============== Post translate textbox =============== #
text_box_translated_width = text_box_width
text_box_translated_height = text_box_height
text_box_translated_loc_X = text_box_original_loc_X + text_box_original_width + horizontal_distance_to_prev
text_box_translated_loc_Y = pre_translate_image_viewer_loc_Y + pre_translate_image_viewer_height + vertical_distance_to_prev
text_box_translated_rect = (text_box_translated_loc_X, text_box_translated_loc_Y, text_box_translated_width, text_box_translated_height)

# =============== OCR mode selection combo box =============== #
combo_box_mode_width = button_width
combo_box_mode_height = button_height
combo_box_mode_loc_X = select_file_btn_loc_X
combo_box_mode_loc_Y = select_file_btn_loc_Y + button_height + vertical_distance_to_prev
ocr_mode_list = ("Horizontal", "Vertical", "MG")
horizontal_mode_index = 0
vertical_mode_index = 1
mg_mode_index = 2
combo_box_mode_rect = (combo_box_mode_loc_X, combo_box_mode_loc_Y, combo_box_mode_width, combo_box_mode_height)

# =============== Retranslate button =============== #
retranslate_btn_txt = "Retranslate"
retranslate_btn_width = button_width
retranslate_btn_height = button_height
retranslate_btn_loc_X = select_file_btn_loc_X
retranslate_btn_loc_Y = combo_box_mode_loc_Y + combo_box_mode_height + vertical_distance_to_prev
retranslate_btn_rect = (retranslate_btn_loc_X, retranslate_btn_loc_Y, retranslate_btn_width, retranslate_btn_height)

# =============== Threshold boldness level selection combo box =============== #
combo_box_iteration_width = button_width
combo_box_iteration_height = button_height
combo_box_iteration_loc_X = retranslate_btn_loc_X
combo_box_iteration_loc_Y = retranslate_btn_loc_Y + button_height + vertical_distance_to_prev

iteration_list = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")

# =============== Run option selection combo box =============== #
combo_box_run_option_width = button_width
combo_box_run_option_height = button_height
combo_box_run_option_loc_X = retranslate_btn_loc_X
combo_box_run_option_loc_Y = combo_box_iteration_loc_Y + button_height + vertical_distance_to_prev

run_option_list = ("Finish", "Stop test")

# =============== Show image option combo box =============== #
check_box_show_image_loc_X = select_file_btn_loc_X
check_box_show_image_loc_Y = combo_box_run_option_loc_Y + button_height + vertical_distance_to_prev
check_box_show_image_text = "Show Image"

# =============== Back button =============== #


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

main_window_title = "Main interface"
auto_scan_window_title = "Auto scan interface"
