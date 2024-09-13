import sys
import subprocess
import random  # Import the random module
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


        
# Check if the correct number of arguments is provided
if len(sys.argv) != 7:
    print("Usage: python script.py <url_file_path> <line_number>")
    sys.exit(1)

# Get the URL file path and line number from command-line arguments


fixed_urls_file = sys.argv[1]
cluster1_urls_file = sys.argv[2]
cluster2_urls_file = sys.argv[3]
cluster3_urls_file = sys.argv[4]
cluster4_urls_file = sys.argv[5]
line_number = sys.argv[6]   

#Loop to go over all pages
pages = open(fixed_urls_file)
data=[]
chop = webdriver.ChromeOptions()
path = "./src.crx"
chop.add_extension(path)

chop.add_argument('--ignore-certificate-errors')
chop.add_argument('--disable-popup-blocking')
chop.add_argument('--disable-notifications')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chop)
driver.set_page_load_timeout(300)
action = ActionChains(driver)
driver.get("https://www.google.com")
sleep(3)

#add a sampler to get a part of pages and not all pages  
#pass it on browser ?

for page in pages:
    print(page)
    page=page+'?scenario=F'+str(line_number)
    print(page)
    driver.get(page)
        

    #driver.get(page)
    sleep(1)
    pyautogui.moveTo(849, 120, duration=0.2)  # Move the pointer to (849, 120)
    pyautogui.click()  # Click at the current pointer position
    sleep(0.5)
    
    # Move the mouse pointer to the second position and click to run the extension
    pyautogui.moveTo(693, 279, duration=0.2)  # Move the pointer to (693, 279)
    pyautogui.click()  # Click at the current pointer position
    sleep(10)
    # Clear browser cache
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

	# You can also clear cookies if needed
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    
# Function to get all URLs from a file
def get_all_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]  # Strip to remove any leading/trailing whitespace


pages1 = get_all_urls_from_file(cluster1_urls_file)
pages2 = get_all_urls_from_file(cluster2_urls_file)
pages4 = get_all_urls_from_file(cluster4_urls_file)
pages3 = get_all_urls_from_file(cluster3_urls_file)
    

cluster1_url = random.choice(pages1) + '?scenario=' + str(line_number)
print(random.choice(pages1))
print(cluster1_url)
cluster2_url = random.choice(pages2)  + '?scenario=' + str(line_number)
cluster3_url = random.choice(pages3)  + '?scenario=' + str(line_number)
cluster4_url = random.choice(pages4)  + '?scenario=' + str(line_number)
  
    
 
 
for page in [cluster1_url, cluster2_url, cluster3_url, cluster4_url]:
    driver.get(page)
        

    #driver.get(page)
    sleep(1)
    pyautogui.moveTo(849, 120, duration=0.2)  # Move the pointer to (849, 120)
    pyautogui.click()  # Click at the current pointer position
    sleep(0.5)
    
    # Move the mouse pointer to the second position and click to run the extension
    pyautogui.moveTo(693, 279, duration=0.2)  # Move the pointer to (693, 279)
    pyautogui.click()  # Click at the current pointer position
    sleep(10)
    # Clear browser cache
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

	# You can also clear cookies if needed
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    
       
    
    
    
    
    
    
    
    
    
    
