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

User_cred = 'Username'
Pass_cred = 'Password'



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
    print(switchUrl)
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    VlanList = []
    for input in soup.find_all('option', selected=True):
    #    print(input)
        Words = input.getText() # Get the text, its very long
        print(Words)
        List = Words.split("\n") # split the new line values into list
        try:
            List[1] = List[1].strip() # Remove whitespace from second item in list
            row = [input.get('value'), List[1][2:]]
            VlanList.append(row)
        #    print(row)
        #    writer.writerow(row)
        except IndexError:
            print("Error")


    # Get The Port Description
    table = soup.find('table', class_='table table-hover table-headings w-auto')
    #print(PortTable)
    PortList = []
    Num = 0
    for row in table.tbody.find_all('tr'):

        #print("Row: " + str(Num))
        # Find all data for each column
        columns = row.find_all('td')
        # make sure the collum is not blank
        if(columns != []):

            t = 0
            for data in columns:
                # Get The Interface as raw text
                Interface = data.text.strip()
                # If this is the first colum of the row and the Interface is not a F Type interface
                if(t == 0 and Interface[0] != "F"):
                    # Add the Interface to a new list of ports
                    PortList.append(Interface)
                t = t + 1
        Num = 1 + Num

    # Combined the Lists Together
    Combined = []
    i = 0
    for Vlans in VlanList:
        # Set the list to have the Port, Vlan Number, then vlan Name
        #print(PortList[i])
        Alinged_List = [PortList[i],Vlans[0],Vlans[1]]
        Combined.append(Alinged_List)
        i = i + 1
    print(Combined)



    return Combined

def GetTable(switchUrl):
    print(switchUrl)
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Get all Tables
    tables = soup.findChildren('table')
    # Get the First Table
    PortTable = tables[1]

    print(PortTable)

    rows = my_table.findChildren(['th', 'tr'])

    for row in rows:
         cells = row.findChildren('td')
         for cell in cells:
             value = cell.string
             print("The value in this cell is %s" % value)

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
