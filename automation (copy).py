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

###########################
# Loop of all the pages
###########################
#TCP
def run_iperf_test(server_ip, duration=10):
    try:
        output = subprocess.check_output(['iperf', '-c', server_ip, '-t', str(duration)])
        print(output)
    except subprocess.CalledProcessError as e:
        print("Failed to run iperf test:", e.output)
        
        
#UDP        
def run_iperf_test2(server_ip, duration=10, bandwidth="10M"):  # Example: 10 Mbps bandwidth
    cmd = ['iperf3', '-c', server_ip, '-t', str(duration), '-u', '-b', bandwidth, '-R']
    try:
        output = subprocess.check_output(cmd)
        print(output.decode())  # Ensure decoding from bytes to string for printing
    except subprocess.CalledProcessError as e:
        print("Failed to run iperf test:", e.output.decode())
        

# Assuming server's IP address is 10.0.0.2 as set in myNetwork.py
server_ip = '10.0.0.2'
run_iperf_test(server_ip)
run_iperf_test2(server_ip, duration=10, bandwidth="10M")

#Loop to go over all pages
pages = open(sys.argv[1])
data=[]
chop = webdriver.ChromeOptions()
path = "./src.crx"
chop.add_extension(path)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chop)
action = ActionChains(driver)
driver.get("https://www.google.com")
sleep(3)

for page in pages:
    print(page)
    driver.get(page)
    sleep(1)
    pyautogui.moveTo(849, 120, duration=0.2)  # Move the pointer to (849, 120)
    pyautogui.click()  # Click at the current pointer position
    sleep(0.5)
    
    # Move the mouse pointer to the second position and click to run the extension
    pyautogui.moveTo(693, 279, duration=0.2)  # Move the pointer to (693, 279)
    pyautogui.click()  # Click at the current pointer position
    sleep(1)
    # Clear browser cache
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})

	# You can also clear cookies if needed
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
