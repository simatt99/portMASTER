from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from dotenv import load_dotenv
load_dotenv()
import os

# Run Headlessly
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

#f = open('VlansOut.csv', 'w')
#writer = csv.writer(f)
# If you want to open Chrome
driver = webdriver.Chrome()
#options = webdriver.ChromeOptions();
#options.add_argument('headless');

User_cred = os.environ.get('USERNAME')
Pass_cred = os.environ.get('PASSWORD')

print(User_cred)



# If you want to open Firefox
#driver = webdriver.Firefox()
switchUrl = "https://switches.net.oregonstate.edu/switches/27/391/"
def login():
    driver.get("https://switches.net.oregonstate.edu/accounts/login/")
    print("Got Login Page")
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    username.send_keys(User_cred)
    password.send_keys(Pass_cred)
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    print("Logged In")

def getVlan(switchUrl): #Get the vlans and write them to a file
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    VlanList = []
    for input in soup.find_all('option', selected=True):
    #    print(input)
        Words = input.getText() # Get the text, its very long
        List = Words.split("\n") # split the new line values into list
        try:
            List[1] = List[1].strip() # Remove whitespace from second item in list
            row = [input.get('value'), List[1][2:]]
            VlanList.append(row)
        #    print(row)
        #    writer.writerow(row)
        except IndexError:
            print("Error")

    return VlanList


def GetSwitchURLFromName(Name):
    driver.get("https://switches.net.oregonstate.edu/switches/")
    Search = driver.find_element(By.NAME,'switchname')
    Search.send_keys(Name)
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if link.getText() == Name.lower():
            link = str("https://switches.net.oregonstate.edu" + link.get('href'))
            print(link)
            return link

    return 0

def Quit():
    #f.close()
    #driver.close()
    return driver.quit()
