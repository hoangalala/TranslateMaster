# from deepl import Translator
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from classes import GlobalVariables

def open_chrome_window():
    driver = webdriver.Chrome(executable_path = GlobalVariables.google_executable_path) # , options = chrome_options

    driver.minimize_window()
    driver.get("https://www.deepl.com/translator")

    return driver