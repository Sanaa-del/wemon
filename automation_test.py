import sys
import subprocess
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pages = open(sys.argv[1])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver)
driver.get("https://www.google.com")
sleep(3)

for page in pages:
    print(page)
    print('line 36')
    
    driver.get(page)
    sleep(1)
    
