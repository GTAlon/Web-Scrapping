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

url= "https://www.linkedin.com/"

driver = webdriver.Chrome('C:\Program Files\webdrivers\chromedriver.exe')
driver.get(url)
driver.implicitly_wait(100)
#fonction de connexion à linkedin avec les id et mdp
def connect():
    element = driver.find_element_by_xpath('/html/body/nav/a[3]')
    driver.execute_script("arguments[0].click();", element)
    inputMail = driver.find_element_by_id('username')
    inputMail.send_keys('stagiareopi@outlook.fr')
    time.sleep(5)
    inputMdp = driver.find_element_by_id('password')
    inputMdp.send_keys('opinaka')
    time.sleep(20)
    inputMdp.send_keys(Keys.ENTER)
connect()
#//*[@id="join-form"]/p[3]/a
pages_Linkedin = []
#nombre d'entites copier
count = 0
#ouverture des differents fichiers
with open('hubLink.csv',encoding='utf-8-sig') as recup,open('profilesLinkedin.csv', 'w',encoding='utf-8-sig',newline='') as linkedin:
    reader =csv.reader(recup,delimiter=';')
    writer = csv.writer(linkedin,delimiter=';')
    writer.writerow(('Nom','Poste Actuel','Lieu','Experience','Formation','Licence/Certification'))
    #recuperation des liens linkedin
    for l in reader:   
        pages_Linkedin.append(l[1])
        print(l[1])
    for links in pages_Linkedin :
        count = count + 1
        #if soup.find_element_by_xpath('#//*[@id="join-form"]/p[3]/a') is None:
        #//*[@id="layout-main"]/div/div div class flip-card
        if pages_Linkedin[0] == links or pages_Linkedin[1] == links :
            time.sleep(3)
        else :
            time.sleep(2)
            driver.execute_script("window.open(arguments[0])", links)
            driver.switch_to.window(driver.window_handles[1])
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if soup.find('div',attrs={'class':'flip-card'}) is None :
                time.sleep(3)
                driver.refresh()
                    #if driver.find_element_by_css_selector('#ember361 > button') is None :
                     #   element=''
                    #else :
                     #   element = driver.find_element_by_css_selector('#ember361 > button')
                      #  driver.execute_script("arguments[0].click();", element)
                name=''
                poste=''
                pos=''
                exp = []
                form = []
                licen= []
                if soup.find('div',attrs={'class':'flex-1 mr5'}) is None :
                    info=""
                else :
                    info=soup.find('div',attrs={'class':'flex-1 mr5'})
                    name = info.find('li',attrs={'class':'inline t-24 t-black t-normal break-words'}).text.replace('\n','')
                    poste = info.find('h2').text.replace('\n','')
                    pos = info.find('li',attrs={'class':'t-16 t-black t-normal inline-block'}).text.replace('\n','')
                    if soup.find('div',attrs={'id':'oc-background-section'}) is None :
                        sec=''
                    else :
                        #element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('section.pv-profile-section.pv-profile-section--reorder-enabled.background-section.artdeco-container-card.ember-view'))
                        time.sleep(5)
                        sec = soup.find('div',attrs={'id':'oc-background-section'})
                        if soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'}) is None :
                            sec1=soup.find('div',attrs={'class':'pv-profile-section__section-pager ember-view'})
                        else :
                            sec1 = soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'})
                            #if sec1.find('div',attrs={'class':'pv-profile-section-pager ember-view'}) is not None :
                        #divs = sec1.find('div',attrs={'class':'pv-profile-section-pager ember-view'})
                            #print(divs)
                            #nbDivs = len(divs)
                            #print(nbDivs)
                            for ex in sec1.find_all('h3',attrs={'class':'t-16 t-black t-bold'}) :
                                exp.append(ex.text)
                            for forma in sec1.find_all('h3',attrs={'class':'pv-entity__school-name t-16 t-black t-bold'}) :
                                form.append(forma.text)
                            for lic in sec1.find_all('h3',attrs={'class':'t-16 t-bold'}) :
                                licen.append(lic.text)
                    profile = [name,poste,pos,exp,form,licen]
                writer.writerow(profile)
                print(profile)
                print(count)
                print(name)
                print(poste)
                print(pos)
                print(exp,form,licen)
                #time pour eviter l'anti robot
                time.sleep(60)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                driver.refresh()
            #js guest
            else :
                #si selenium se deconnecte de linkedin et après reconnexion sur
                #le navigateur par défaut, selenium se reconnectera automatiquement
                element = driver.find_element_by_css_selector('a.form-toggle')
                driver.execute_script("arguments[0].click();", element)
                inputMail = driver.find_element_by_id('login-email')
                inputMail.send_keys('stagiareopi@outlook.fr')
                time.sleep(5)
                inputMdp = driver.find_element_by_id('login-password')
                inputMdp.send_keys('opinaka')
                time.sleep(20)
                inputMdp.send_keys(Keys.ENTER)
                time.sleep(3)
                driver.refresh()
                    #if driver.find_element_by_css_selector('#ember361 > button') is None :
                     #   element=''
                    #else :
                     #   element = driver.find_element_by_css_selector('#ember361 > button')
                      #  driver.execute_script("arguments[0].click();", element)
                name=''
                poste=''
                pos=''
                exp = []
                form = []
                licen= []
                if soup.find('div',attrs={'class':'flex-1 mr5'}) is None :
                    info=""
                else :
                    info=soup.find('div',attrs={'class':'flex-1 mr5'})
                    name = info.find('li',attrs={'class':'inline t-24 t-black t-normal break-words'}).text.replace('\n','')
                    poste = info.find('h2').text.replace('\n','')
                    pos = info.find('li',attrs={'class':'t-16 t-black t-normal inline-block'}).text.replace('\n','')
                    if soup.find('div',attrs={'id':'oc-background-section'}) is None :
                        sec=''
                    else :
                            #element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('section.pv-profile-section.pv-profile-section--reorder-enabled.background-section.artdeco-container-card.ember-view'))
                        time.sleep(5)
                        sec = soup.find('div',attrs={'id':'oc-background-section'})
                        if soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'}) is None :
                            sec1=soup.find('div',attrs={'class':'pv-profile-section__section-pager ember-view'})
                        else :
                            sec1 = soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'})
                            #if sec1.find('div',attrs={'class':'pv-profile-section-pager ember-view'}) is not None :
                            #divs = sec1.find('div',attrs={'class':'pv-profile-section-pager ember-view'})
                                #print(divs)
                                #nbDivs = len(divs)
                                #print(nbDivs)
                            for ex in sec1.find_all('h3',attrs={'class':'t-16 t-black t-bold'}) :
                                exp.append(ex.text)
                            for forma in sec1.find_all('h3',attrs={'class':'pv-entity__school-name t-16 t-black t-bold'}) :
                                form.append(forma.text)
                            for lic in sec1.find_all('h3',attrs={'class':'t-16 t-bold'}) :
                                licen.append(lic.text)
                            profile = [name,poste,pos,exp,form,licen]
                    writer.writerow(profile)
                print(profile)
                print(count)
                print(name)
                print(poste)
                print(pos)
                print(exp,form,licen)
                time.sleep(60)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                driver.refresh()
                

            #info = div.find_all('p',attrs={'class':'pv-entity__secondary-title t-14 t-black t-normal'})
            #print(titre.text,info.text)
    #if soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'}) is None:
     #   time.sleep(1)
    #else :
     #   profile = soup.find('section',attrs={'class':'pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card ember-view'})
      #  divs = profile.find_all('div',attrs={'class':'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})
       # for div in divs :
        #    d = div.find('ul',attrs={'class':'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})
         #   print(d)
            #for liste in exp.find_all('li'):
                #titre = liste.h3.text
                #taff = liste.find('p',attrs={'class':'pv-entity__secondary-title t-14 t-black t-normal'})
                #print(titre,taff)
    
    
