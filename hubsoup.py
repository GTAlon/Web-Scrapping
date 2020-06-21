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

url_page= "https://lehub.web.bpifrance.fr/search"
time = 3

driver = webdriver.Chrome('C:\Program Files\webdrivers\chromedriver.exe')
driver.get(url_page)
driver.implicitly_wait(100)
#Cliquer sur le bouton "Charger Plus"  29 fois pour afficher toutes les entitées
element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[6]/div/button')
for i in range(29):
    driver.execute_script("arguments[0].click();", element)
#recupere le nombre d'élément
num_start = len(driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[6]/div/div/div'))
print(num_start)
elems = driver.find_elements_by_css_selector('a.sc-jbKcbu.JjNx')
#Ouvre les fichiers 
with open('hub.csv', 'w',encoding='utf-8-sig',newline='') as ID,open('hubClients.csv', 'w',encoding='utf-8-sig',newline='') as cl,open('hubTeam.csv', 'w',encoding='utf-8-sig',newline='') as t,open('hubInvest.csv', 'w',encoding='utf-8-sig',newline='') as inv:
    writerID = csv.writer(ID,delimiter='|')
    writerCl = csv.writer(cl,delimiter='|')
    writerT = csv.writer(t,delimiter='|')
    writerInv = csv.writer(inv,delimiter='\t')
    writerID.writerow(('SIREN','Nom Entreprise','Adresse'))
    writerCl.writerow(('SIREN','Nom Entreprise'))
    writerT.writerow(('SIREN','Nom','Poste Occupe'))
    writerInv.writerow(('SIREN','Date','Montant','Tour','Investisseur'))
#début du traitement de la page
    for elem in elems :
        #selectionne un lien et clique dessus
        driver.execute_script("window.open(arguments[0])", elem.get_attribute("href"))
        driver.switch_to.window(driver.window_handles[1])
        element = WebDriverWait(driver, 5).until(lambda x:    x.find_element_by_id('root'))
        #if driver.find_element_by_css_selector('div.sc-hEsumM.klDYNU') is None:   
        #Recherche de client si il trouve pas envoie un message
        try:
            btn_client = driver.find_element_by_css_selector('div.sc-hEsumM.klDYNU')
            driver.execute_script("arguments[0].click();", btn_client)
        except:
            print("Pas de clients")
               #btn_client = driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/a')
            #driver.execute_script("arguments[0].click();", btn_client)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        names_clients = []
        noms_team = []
        lesPostes = []
        investisseur = []
        if soup.find('div',attrs={'class': 'startup__identity'}) is None :
            div = ''
        else :
            div = soup.find('div',attrs={'class': 'startup__identity'})
            #Recupere les chiffes du numero SIren
            if div.find('div',attrs={'class': 'sc-kjoXOD iqvuns'}) is None:
                siren = ''
            else :
                siren = div.find('div',attrs={'class': 'sc-kjoXOD iqvuns'}).text.split('N° SIREN :')
                Siren =''
                for s in range(10) :
                    Siren = Siren + siren[1][s]
        #recupere l'adresse
            if div.find('span') is None :
                adr = ''
            else :
                adr = div.find('span')
                adresse = adr.get_text(separator=" ").strip()
        if soup.find('div',attrs={'class': 'startup__presentation'}):
            data =''
        else :
            data = soup.find('div',attrs={'class': 'startup__presentation'})
        #recupere le nom de l'entreprise et ses clients
        if soup.find('h1') is None:
            titre = ''
        else :
            titre = soup.find('h1').text
        if soup.find('div',attrs={'class':'startup__clients'}) is None :
            clients=''
        else :
            clients = soup.find('div',attrs={'class':'startup__clients'})
            aCli = clients.find_all('a',attrs={'class': 'sc-feJyhm iDPzNP'})
            #sc-hEsumM klDYNU
            for client in aCli :
                nam = client.find_next('div')
                name = nam.find_next('div')
                names_clients.append(name.text)
                writerCl.writerow((Siren,name.text))
        #recupere les noms, le poste de l'equipe 
        if soup.find('div',attrs={'class':'startup__team'}) is None :
            team=''
        else :
            team = soup.find('div',attrs={'class':'startup__team'})
            nom_team = team.find_all('div',attrs={'class' : 'sc-iQKALj OpDsF'})
            poste = team.find_all('div',attrs={'class' : 'sc-bwCtUz zoEuq'})
            for nom, p in zip(nom_team, poste) :
                name_team = nom.text
                noms_team.append(name_team)
                postes = p.text
                lesPostes.append(postes)
                writerT.writerow((Siren,name_team,postes))
            #sc-iQKALj OpDsF
            #sc-bwCtUz zoEuq
        #recupere les investisseurs
        if soup.find('div',attrs={'class':'startup__investments'}) is None :
            invest=''
        else :
            invest = soup.find('div',attrs={'class':'startup__investments'})
            line = invest.find_all('tr',attrs={'class' : 'ant-table-row ant-table-row-level-0'})
            for inves in line :
                inv = inves
                investisseur.append(inves.text)
                writerInv.writerow((Siren,inves.find_all('td')[0].get_text(),inves.find_all('td')[1].get_text(),inves.find_all('td')[2].get_text(),inves.find_all('td')[3].get_text()))
                
        print(titre)
        print(Siren)
        print(adresse)
        print(names_clients)
        print(noms_team)
        print(lesPostes)
        print(investisseur)
        writerID.writerow((Siren,titre,adresse))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(elem.get_attribute("href"))
