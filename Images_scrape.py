import os.path
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from numpy import loadtxt
from pathlib import Path
import urllib.request
from time import sleep
import xlsxwriter



workbook = xlsxwriter.Workbook('noimageplants.xlsx')
worksheet = workbook.add_worksheet()

# TO DO - run script multiple times until not a robot sign

"""f""ile = open('ScientificNames.csv', 'rb')
current_folder = Path.cwd()
save_path = os.path.join(current_folder, "/Images")
print("Saving path is")
print(save_path)"""
file = open('ScientificNames.csv', 'rb')
save_path = "Images/"
if not os.path.exists(save_path):
    print(f'Making directory: {str(save_path)}')
    os.makedirs(save_path)
#save_path = os.path.join(os.path.abspath(__file__), '..', "/Images")

if not os.path.exists(save_path):
    print(f'Making directory: {str(save_path)}')
    os.makedirs(save_path)

# Load csv with plant names
data = loadtxt(file, dtype=str, delimiter=";", usecols=range(1))


# Setup chrome
chrome_options = Options()

chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# Visit website
driver.get('https://images.google.com/')

# Click accept all button
driver.find_element('xpath', "/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]").click()

# Finding the search box

search_box = driver.find_element("xpath", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")))

# Run for the first one
search_box.send_keys(data[0])

# Click search button

driver.find_element("xpath", "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button").click()

#Click first image Path /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]



#img_first = driver.find_element("xpath", '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img')
img_first = driver.find_element("xpath", '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]')
img_first.screenshot(save_path + data[0] + ".png")


# Loop through all names and download
for i in range(len(data)):
    # try:
    # Find again search box

    search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/c-wiz/c-wiz/div/div[3]/div[2]/div/div[1]/form/div[1]/div[2]/div/div[2]/input")))
    search_box.clear()
    # Type the search query in the search box
    search_box.send_keys(data[i])
    rnd = (random.randint(1, 1000)/1000)
    sleep(rnd)

    # Click search button
    driver.find_element("xpath", "/html/body/c-wiz/c-wiz/div/div[3]/div[2]/div/div[1]/form/div[1]/div[2]/button").click()

                                        #"/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]"
                                         #"/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img"
                                        #"/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]"
    #Click first image
    try:
        rnd = (random.randint(1, 10) / 100)
        sleep(rnd)
        driver.find_element("xpath", "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]").click()
        #Get image
        img_first = driver.find_element("xpath", "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img")
    except:

        print("Image " + data[i] + " not downloaded")
        worksheet.write('A1', data[i])

    if(img_first != None):

        # Find the source image
        src=img_first.get_attribute("src")

        #Waiting for the image to load
        rnd = (random.randint(1, 2000)/1000)
        sleep(rnd)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img")))

        #Save as image
        urllib.request.urlretrieve(src, save_path + data[i] + ".png")

        img_first = None
    #img_first.screenshot(save_path + data[i] + ".png")

    # except:
    #     try:
    #         img_first = driver.find_element("xpath",
    #                                         "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a")
    #         img_first.screenshot(save_path + data[i] + ".png")
    #     except:
    #         try:
    #             img_first = driver.find_element("xpath",
    #                                             "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]")
    #             img_first.screenshot(save_path + data[i] + ".png")
    #         except:
    #             print("Image " + data[i] + " not downloaded")

#driver.close()
workbook.close()