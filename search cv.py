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
mot = 'Site déposer cv'
soup = BeautifulSoup(driver.page_source, 'html.parser')

#fonction de recherche employeur qui a pour parametre le lien du site et le nom de la personne à chercher
def find_(mot_clef) :
    recherche = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    recherche.send_keys(mot_clef)
    recherche.send_keys(Keys.ENTER)
names = []

#ouverture du fichier hubTeam deja rempli et un fichier d'ecriture
with open('Google CV.csv', 'w',encoding='utf-8-sig',newline='') as links:
    writer = csv.writer(links,delimiter='|')
    writer.writerow(('Nom','Description','Liens'))
    find_(mot)
    
            #on recupere le lien hypertexte et on l'ecrit dans le fichier csv
    for i in range(0,23) :
        links = driver.find_elements_by_css_selector('div.r > a')
        print(len(links))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in links :
            lien = link.get_attribute("href")
            nom = lien.split('.')[1]
            
        for i in soup.find_all('span',attrs={'class':'st'}) :
            descri = i.text
            print(nom)
            print(descri)
            print(lien)
            writer.writerow((nom,descri,lien))
        #un timer de 60 secondes d'attente pour pas "reveiller" le CAPTACHA de google
        time.sleep(45)
        element = WebDriverWait(driver, 60).until(lambda x:    x.find_element_by_id('rcnt'))
        element = driver.find_element_by_css_selector('a#pnnext.pn')
        driver.execute_script("arguments[0].click();", element)   
    driver.execute_script("window.history.go(-1)")
