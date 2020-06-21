from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#page a traiter
url_page= "https://jobs.stationf.co/startups"

page = urllib.request.urlopen(url_page)

def g_pages(pgs,nb):
    pages = []
    strPage = '?page='
    pgs = pgs + strPage
    pages.append(pgs)
    for i in range(2,nb+1):
        page = pgs + str(i)
        pages.append(page)
    return pages

soup = BeautifulSoup(page, 'html.parser')

driver = webdriver.Chrome('C:\Program Files\webdrivers\chromedriver.exe')
driver.get(url_page)
driver.implicitly_wait(100)
num_links = len(driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[6]/div/div/div'))
#//*[@id="root"]/div/div/div[2]/div/div/div[6]/div
#Ouverture du fichier d'écriture
with open('jobstation.csv', 'w',encoding='utf-8-sig',newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter='|')
    writer.writerow(('Nom Entreprise','Description'))
    liens = driver.find_elements_by_css_selector('a.organization-link')
    print(len(liens))
        #recupere toutes la liste des entreprise
    for lien in liens :
        driver.execute_script("window.open(arguments[0])", lien.get_attribute("href"))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if soup.find('h1',attrs={'class':'page-header-title'}) is None :
            name = ''
        else :
            name = soup.find('h1',attrs={'class':'page-header-title'}).text.replace('\n','')
        if soup.find('div',attrs={'class':'block-content block-content-text text-formated'}) is None :
            descri =''
        else :
            descri = soup.find('div',attrs={'class':'block-content block-content-text text-formated'}).text.replace('\n','')
        print(name,descri)
        writer.writerow((name,descri))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    

    # go back to initial page

