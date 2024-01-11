from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import re
import os
import time

current_directory = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(current_directory, 'geckodriver.exe')

service = Service(executable_path=driver_path)
options = webdriver.FirefoxOptions()
#options.add_argument("--start-maximized")
options.headless = False



driver = webdriver.Firefox(service=service, options=options)
#driver.maximize_window()
driver.implicitly_wait(10)

# Provide your login details
username = "testone123@gmail.com"
password = "testone123"

def login_user(username, password, driver):
    url = "https://essays-writing-service.org/login"
    driver.get(url)

    time.sleep(5)
    # Locate the username and password fields and input the credentials
    username_field = driver.find_element("xpath", "/html/body/div[3]/div/div[2]/section/div/div/div/div/form/input[2]")
    password_field = driver.find_element("xpath", "/html/body/div[3]/div/div[2]/section/div/div/div/div/form/input[3]")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the form
    submit_button = driver.find_element("xpath", "/html/body/div[3]/div/div[2]/section/div/div/div/div/form/button")
    submit_button.click()

login_user(username, password, driver)
