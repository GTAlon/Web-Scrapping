from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#site a traiter
url_page= "https://orangefabfrance.fr/fr/les_start_up/"

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

#nombre d'élément à traiter
num_links = len(driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[6]/div/div/div'))
#//*[@id="root"]/div/div/div[2]/div/div/div[6]/div

#emplacement des differents boutonà cliquer pour changer de page
elements = []
elements.append('//*[@id="main"]/div[4]/nav/ul/li[4]/a')
elements.append('//*[@id="main"]/div[4]/nav/ul/li[5]/a')
elements.append('//*[@id="main"]/div[4]/nav/ul/li[5]/a')
elements.append('/html/body/a/span[2]')

#ouverture du fichier d'écriture
with open('orange.csv', 'w',encoding='utf-8-sig',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter='|')
        writer.writerow(('Nom Entreprise','Descriptif','Facebook','Twitter','Linkedin','Youtube'))
        
        #une boucle pour cliquer sur chaque bouton pour ouvrir une autre page
        for j in range(2,6):
            #soup = BeautifulSoup(driver.page_source, 'html.parser')
            #code_soup = soup.find('ol', attrs={'class': 'list-unstyled row'})
            #souup = code_soup.find_all('li',recursive=False)
            liens = driver.find_elements_by_css_selector(' h2 > a')
            print(len(liens))
            #traitement de chaque élément
            for lien in liens :
                driver.execute_script("window.open(arguments[0])", lien.get_attribute("href"))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if soup.find('h1') is None :
                    name =''
                else :
                    name = soup.find('h1').text
                if soup.find('div',attrs={'class':'elementor-text-editor elementor-clearfix'}) is None :
                    descri =''
                else :
                    descri = soup.find('div',attrs={'class':'elementor-text-editor elementor-clearfix'}).text
                reseaux = driver.find_elements_by_css_selector('div.elementor-social-icons-wrapper > a')
                fb = ''
                tw =''
                linkedin =''
                youtube = ''
                for reseau in reseaux :
                    if "facebook" in reseau.get_attribute("href") :
                       fb = reseau.get_attribute("href")
                    if "twitter" in reseau.get_attribute("href") :
                        tw = reseau.get_attribute("href")
                    if "linkedin" in reseau.get_attribute("href") :
                        linkedin = reseau.get_attribute("href")
                    if "youtube" in reseau.get_attribute("href") :
                        youtube = reseau.get_attribute("href") 
                print(name,descri,fb,tw,linkedin,youtube)
                writer.writerow((name,descri,fb,tw,linkedin,youtube))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            driver.get("https://orangefabfrance.fr/fr/les_start_up/?fwp_paged=" + str(j))
            

    

