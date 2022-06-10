from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv

f = open('VlansOut.csv', 'w')
writer = csv.writer(f)
# If you want to open Chrome
driver = webdriver.Chrome()
Name = "als-1011a-vfsw"
# If you want to open Firefox
#driver = webdriver.Firefox()
switchUrl = "https://switches.net.oregonstate.edu/switches/27/391/"
def login():
    driver.get("https://switches.net.oregonstate.edu/accounts/login/")
    print("Got Login Page")
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    username.send_keys("username")
    password.send_keys("password")
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    print("Logged In")

def getVlan(switchUrl): #Get the vlans and write them to a file
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for input in soup.find_all('option', selected=True):
    #    print(input)
        Words = input.getText() # Get the text, its very long
        List = Words.split("\n") # split the new line values into list
        List[1] = List[1].strip() # Remove whitespace from second item in list

        row = [input.get('value'), List[1][2:]]
        print(row)
        writer.writerow(row)
    f.close()


def GetSwitchURLFromName(Name):
    driver.get("https://switches.net.oregonstate.edu/switches/")
    Search = driver.find_element(By.NAME,'switchname')
    Search.send_keys(Name)
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if link.getText() == Name.lower():
            return "https://switches.net.oregonstate.edu" + link.get('href')

    return 0

login()
switchUrl = GetSwitchURLFromName(Name)

getVlan(switchUrl)


#Todo
#  Rebuild the Search feature based off names
#Export Vlans as List of Name and Number
# in main check if vlans exist from report
# if not get from the Scraper
# Start by matching ports with the Gi ports
# Download AKIPS reports
#
