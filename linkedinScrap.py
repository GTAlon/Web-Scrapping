from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

page = 'https://www.linkedin.com/search/results/companies/?keywords=data%20science%20france&origin=GLOBAL_SEARCH_HEADER'

def g_pages(pgs,nb):
    pages = []
    strPage = 'page='
    pgs = pgs + strPage
    pages.append(pgs)
    for i in range(2,nb+1):
        page = pgs + str(i)
        pages.append(page)
    return pages

pages = g_pages(page,2)
for i in pages:
   reponse = requests.get(i)
   soup = BeautifulSoup(reponse.text,'html.parser')
   for d in soup.find_all("body"):
       print(d.text)
        
        
