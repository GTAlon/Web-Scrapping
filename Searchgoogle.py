from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#lien d'utilisation
url='https://www.google.fr/'

driver = webdriver.Chrome('C:\Program Files\webdrivers\chromedriver.exe')
driver.get(url)
driver.implicitly_wait(100)

#site a traiter
site = 'https://fr.linkedin.com/'
soup = BeautifulSoup(driver.page_source, 'html.parser')

#fonction de recherche employeur qui a pour parametre le lien du site et le nom de la personne à chercher
def find_employeur(nom,site) :
    recherche = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    recherche.send_keys(nom + ' site:' + site)
    recherche.send_keys(Keys.ENTER)
names = []

#ouverture du fichier hubTeam deja rempli et un fichier d'ecriture
with open('hubTeam.csv') as file, open('hubLink.csv', 'w',encoding='utf-8-sig',newline='') as links:
    reader = csv.reader(file, delimiter=';')
    writer = csv.writer(links,delimiter='\t')
    writer.writerow(('Nom','liens'))
    
    #recuperer le nom de chaque employeur et lance la recherche
    for line in reader:
        find_employeur(line[1],site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        #si rien n'est trouvé sur cette personne, on retourne a la page d'accueil
        if soup.find('div',attrs={'class': 'r'}) is None:
            driver.execute_script("window.history.go(-1)")
        else :
            
            #on recupere le lien hypertexte et on l'ecrit dans le fichier csv
            link = driver.find_element_by_css_selector('div.r > a').get_attribute('href')
            writer.writerow((line[1],link))
            
            #un timer de 60 secondes d'attente pour pas "reveiller" le CAPTACHA de google
            time.sleep(60)
            element = WebDriverWait(driver, 60).until(lambda x:    x.find_element_by_id('rcnt'))
            driver.execute_script("window.history.go(-1)")
        print(line[1])
        print(link)
