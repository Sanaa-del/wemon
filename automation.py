import sys
import subprocess
import random  # Import the random module
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import urllib.parse
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

chop.add_argument('--disable-gpu')
chop.add_argument('--disable-software-rasterizer')
chop.add_argument('--disable-search-engine-choice-screen')
chop.add_argument('--ignore-certificate-errors')
chop.add_argument('--disable-popup-blocking')
chop.add_argument('--disable-notifications')


#chromedriver_path = '/home/sghandi/.wdm/drivers/chromedriver/linux64/128.0.6613.137/chromedriver-linux64/chromedriver'  # Update this with your actual path

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chop)
#driver = webdriver.Chrome(service=Service(chromedriver_path), options = chop)

driver.set_page_load_timeout(100)
action = ActionChains(driver)
driver.get("https://www.google.com")
#print(driver.capabilities)

sleep(3)
timeouts=0



# Function to get all URLs from a file
def get_all_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]  # Strip to remove any leading/trailing whitespace

def encode_url(url):
    base_part = 'http://10.0.0.2/'
    # Split the base and the rest of the URL
    if url.startswith(base_part):
        rest_of_url = url[len(base_part):]
        # Encode the rest of the URL
        encoded_url = urllib.parse.quote(rest_of_url, safe=':/')
        return base_part + encoded_url
    return url

pages1 = get_all_urls_from_file(cluster1_urls_file)
pages2 = get_all_urls_from_file(cluster2_urls_file)
pages4 = get_all_urls_from_file(cluster4_urls_file)
pages3 = get_all_urls_from_file(cluster3_urls_file)
    

cluster1_url = encode_url(random.choice(pages1)) + '?scenario=' + str(line_number)
#print(random.choice(pages1))
#print(cluster1_url)
cluster2_url = encode_url(random.choice(pages2))  + '?scenario=' + str(line_number)
cluster3_url = encode_url(random.choice(pages3))  + '?scenario=' + str(line_number)
cluster4_url = encode_url(random.choice(pages4))  + '?scenario=' + str(line_number)
  
    
for url in pages:
    print(url)
    #page=encode_url(page)
    #print('encdoded page:   ', url)
    clean_url = url.strip()
    page=encode_url(clean_url) +'?scenario=F'+str(line_number)
    print(page)
    try:
	    driver.get(page)
	    sleep(1)
	    pyautogui.moveTo(849, 120, duration=0.2)  # Move the pointer to (849, 120)
	    pyautogui.click()  # Click at the current pointer position
	    sleep(0.5)
	   
	    pyautogui.moveTo(693, 279, duration=0.2)  # Move the pointer to (693, 279)
	    pyautogui.click()  # Click at the current pointer position
    except:
    	print('TIMEOUT')
    	timeouts=timeouts+1	    
    sleep(3)
    # Clear browser cache
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

	# You can also clear cookies if needed
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    


#urls1 = get_all_urls_from_file('/home/sghandi/Téléchargements/funny.txt')

# Encode all URLs
#encoded_urls = [encode_url(url) for url in urls1]

#cluster1_url, cluster2_url, cluster3_url, cluster4_url
for page in [cluster1_url, cluster2_url, cluster3_url, cluster4_url]:
    try:
    	driver.get(page)
    	
    	sleep(1)
    	pyautogui.moveTo(849, 120, duration=0.2)  # Move the pointer to (849, 120)
    	pyautogui.click()  # Click at the current pointer position
    	sleep(0.5)
    
    	# Move the mouse pointer to the second position and click to run the extension
    	pyautogui.moveTo(693, 279, duration=0.2)  # Move the pointer to (693, 279)
    	pyautogui.click()
    except:
    	print('TIMEOUT')
    	timeouts=timeouts+1
    	
    	

    #driver.get(page)
      # Click at the current pointer position
    sleep(3)
    # Clear browser cache
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

	# You can also clear cookies if needed
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    
if timeouts>=3:    	
	flag_file = '/tmp/timeouts.flag'
	print('flag done')
	with open(flag_file, 'w') as f:
    		f.write(str(line_number))     
    
    
    
    
    
    
    
    
    
    
