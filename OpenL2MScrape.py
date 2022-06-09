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
# If you want to open Firefox
#driver = webdriver.Firefox()
switchUrl = "https://switches.net.oregonstate.edu/switches/27/391/"
def login():
    driver.get("https://switches.net.oregonstate.edu/accounts/login/")
    print("Got Login Page")
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    username.send_keys("username")
    password.send_keys("Password")
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

login()
getVlan(switchUrl)
