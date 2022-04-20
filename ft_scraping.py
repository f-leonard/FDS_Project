# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:57:13 2022

@author: 35387
"""
import requests
from bs4 import BeautifulSoup

URL = "https://www.ft.com/search?q=supply+chain"
r = requests.get(URL)

soup = BeautifulSoup(r.content,'lxml')
urls = []
for href in soup.find_all('a'):
    if 'supply chain' in href.text:
        urls.append(href.attrs['href'])
full_url = []
for url in urls:
    full_url.append('https://ft.com'+url)
text = []
for url in full_url:

    y = requests.get(url)
    soup = BeautifulSoup(y.content,'lxml')
    
    mydivs = soup.find_all("div",class_= "article__content-body n-content-body js-article__content-body")


#%%
import requests
from bs4 import BeautifulSoup
news_titles=[]

for page in range(1,6):
    url="https://www.ft.com/world?page={}".format(page)
    result=requests.get(url)
    reshult=result.content
    soup=BeautifulSoup(reshult, "lxml")
    for title in soup.findAll("a"):
        titles=title.find(text=True)
        news_titles.append(titles)

print(news_titles)        