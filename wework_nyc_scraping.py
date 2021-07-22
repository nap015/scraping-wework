import sys
!conda install --yes --prefix {sys.prefix} selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import date
import pandas as pd
import numpy as np
import string

# set variables
today = date.today().strftime("%Y-%m-%d")
wework = 'https://www.wework.com'

driver = webdriver.Chrome('./chromedriver')
driver.get("https://www.wework.com/search?slug=new-york-city--NY&capacity=1") 
time.sleep(5)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
driver.quit()

# get urls to all buildings
building_links = []
buildings = soup.find("div",{"id":"results"}).find_all('a')
for building in buildings:
    building_links.append(wework+building['href'])

capacity_list = [num for num in range(1,21)]
capacity_extra = ['21-100','100%2B']

# get urls to all inventory space
space_links = dict()

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)
#wait = WebDriverWait(driver, 10)

for building in building_links:
    for capacity in capacity_list:
        link = building +'/reserve?capacity='+str(capacity)+'&start_date='+today
        driver.get(link) 
        #driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="uc-btn-accept-banner"]'))).click()

        req = driver.page_source
        soup4 = BeautifulSoup(req, 'html.parser')

        workspaces = soup4.find('div',{'class':'product-card'}).find_all('a',{'class':'selection-card'})
        workspaces.pop()
        for space in workspaces:
            #space_links.append(wework+space['href'])
            key = space['href']#.split('/')[-1]
            cap = space.find('div',{'class':'ray-tag ray-tag--with-icon capacity-tag'}).text
            space_links[key] = cap
            if len(cap) > 0 and int(cap) > capacity:
                capacity = int(cap)
    for capacity in capacity_extra:
        link = building +'/reserve?capacity='+capacity+'&start_date='+today
        driver.get(link) 
        #driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        #wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="uc-btn-accept-banner"]'))).click()

        req = driver.page_source
        soup4 = BeautifulSoup(req, 'html.parser')

        workspaces = soup4.find('div',{'class':'product-card'}).find_all('a',{'class':'selection-card'})
        workspaces.pop()
        for space in workspaces:
            #space_links.append(wework+space['href'])
            key = space['href']#.split('/')[-1]
            cap = space.find('div',{'class':'ray-tag ray-tag--with-icon capacity-tag'}).text
            space_links[key] = cap
        
driver.quit()

inventory = pd.DataFrame.from_dict(space_links,orient='index').reset_index().rename(columns={'index':'address', 0:'capacity'})
inventory = inventory[inventory.capacity!='']
inventory.reset_index(drop=True, inplace=True)
inventory['url'] = wework+inventory['address'].astype(str)
inventory[['building', 'space']] = inventory['address'].str.split('/reserve/', 2, expand=True)
inventory[['building', 'city', 'state']] = inventory['building'].str.split('--', 2, expand=True)
inventory['building'] = inventory['building'].str.replace('/buildings/','').str.replace('-',' ').apply(lambda x: string.capwords(x))
inventory['city'] = inventory['city'].str.replace('-',' ').str.title()
inventory['state'] = inventory['state'].astype(str).str[:2]
inventory = inventory[['state','city','building','space','capacity','url']]
inventory.to_csv('wework_nyc_inventory.csv')