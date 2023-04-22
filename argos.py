import selenium 
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

counties = ['Antrim','Armagh','Fermanagh', 'Londonderry, County Londonderry']
#counties = ['Antrim']
format = {
    'Postcode':'',
    'Store': '',
    'Store Name': '',
    'Address': ''
    
    }



new = pd.DataFrame.from_dict([format])


PATH = '/Users/syedislam/Desktop/Chromedriver/chromedriver'

base_url = 'https://www.argos.co.uk/stores/?clickOrigin=header:home:stores'

driver = webdriver.Chrome(PATH)

driver.get(base_url)

time.sleep(3)

driver.find_element(By.XPATH,'//*[@id="consent_prompt_submit"]').click()

time.sleep(5)

for county in counties:

    driver.find_element(By.XPATH,'//*[@id="searchbox"]').send_keys(county)

    time.sleep(3)

    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/form/button').click()


    time.sleep(3)

    driver.find_element(By.XPATH,'//*[@id="searchbox"]').clear()

    time.sleep(2)

    
    results_length = driver.find_elements(By.XPATH,'//*[contains(@id,"sc-store-")]')

    counter = len(results_length)
    count = 0
    while count<counter:
        count = count+1
        time.sleep(3)
        g = driver.find_element(By.XPATH,f'/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/ol/li[{count}]/div/p[3]/span')
        time.sleep(2)
        fe = driver.find_element(By.XPATH,f'/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/ol/li[{count}]/div/p[1]')

        #print(g.get_attribute('//*[@id="sc-store-4420"]/div/p[1]'))
        address_with_pcode = str(g.get_attribute('textContent'))
        split = address_with_pcode.split(',')
        split_no_pcode = split.pop()
        address = ','.join(split_no_pcode)
        store_name = str(fe.get_attribute('textContent'))
        format['Address'] = split[-1]
        format['Store Name'] = store_name
        format['Store'] = 'Argos'
        format['Postcode'] = split_no_pcode
        new = new.append(format, ignore_index = True)
    
    time.sleep(3)

clean_list = new.dropna()

clean_list = clean_list.drop_duplicates(subset=['Store Name'])

clean_list.to_csv('Argos.csv', index=False)




