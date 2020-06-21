from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#page à traiter
url_page= "http://www.alloweb.org/annuaire-startups/base-de-donnees-startups/annuaire-frenchtech/"
def g_pages(pgs,nb):
    pages = []
    strPage = '?page='
    pgs = pgs + strPage
    pages.append(pgs)
    for i in range(2,nb+1):
        page = pgs + str(i)
        pages.append(page)
    return pages


driver = webdriver.Chrome('C:\Program Files\webdrivers\chromedriver.exe')
driver.get(url_page)
driver.implicitly_wait(100)
num_links = len(driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[6]/div/div/div'))
#//*[@id="primary"]/nav/div/a[4]
#//*[@id="primary"]/nav/div/a[6]
#//*[@id="primary"]/nav/div/a[7]
#//*[@id="primary"]/nav/div/a[8]
#//*[@id="primary"]/nav/div/a[8]
elements = []
#les différents emplacement des bouton sur lequel on devra cliquer pour afficher toutes les pages
elements.append('//*[@id="primary"]/nav/div/a[4]')
elements.append('//*[@id="primary"]/nav/div/a[6]')
elements.append('//*[@id="primary"]/nav/div/a[7]')
elements.append('//*[@id="primary"]/nav/div/a[8]')
#ouverture du fichier décriture
with open('Frenchtech.csv', 'w',encoding='utf-8-sig',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter='|')
        writer.writerow(('Nom Entreprise','Descriptif','Nom et Prénom','Email','Site Internet','Téléphone','Adresse'))
        #cliquer 16 fois sur "page suivante"
        for j in range(16) :
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            liens = driver.find_elements_by_css_selector('a.listing-row-image-link')
            print(len(liens))
            for lien in liens :
                  #recupere le nom de l'entreprise
                #href = i.find('h2',attrs={'class': 'listing-row-title'})
                
                #a = href.a.text
                #descri = i.find('div',attrs={'class': 'listing-row-content'}).text
                driver.execute_script("window.open(arguments[0])", lien.get_attribute("href"))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if soup.find('li',attrs={'class':'email'}) is None :
                    email = ''
                else :
                    email = soup.find('li',attrs={'class':'email'}).text.replace('Adresse email','')
                if soup.find('li',attrs={'class':'website'}) is None :
                    website = ''
                else :
                    website = soup.find('li',attrs={'class':'website'}).text.replace('Site Internet','')
                if soup.find('li',attrs={'class':'person'}) is None :
                    person =''
                else:
                    person = soup.find('li',attrs={'class':'person'}).text.replace('Nom & Prénom','')
                if soup.find('li',attrs={'class':'address'}) is None :
                    address = ''
                else :
                    address = soup.find('li',attrs={'class':'address'}).text.replace('Adresse','')
                if soup.find('li',attrs={'class':'phone'}) is None :
                    phone = ''
                else :
                    phone = soup.find('li',attrs={'class':'phone'}).text.replace('Téléphone','')
                name = soup.find('h1').text.replace('Revendication','')
                descrip = soup.find('div',attrs={'class':'listing-detail-description-wrapper'}).text
                #recupere la petite description fourni
                #print(a)
                #print(descri)
                print(name,descrip,person,email,website,phone,address)
                writer.writerow((name,descrip,person,email,website,phone,address))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            if j == 15 :
                element = driver.find_element_by_xpath('//*[@id="filter-2"]/div/form/div[17]/div/div[2]/ul/li[1]')
            else :
                element = driver.find_element_by_css_selector('a.next.page-numbers')
            driver.execute_script("arguments[0].click();", element)
            #code_soup = soup.find('div', attrs={'class': 'listings-row'})
            #souup = code_soup.find_all('div',recursive=False)

    

 

