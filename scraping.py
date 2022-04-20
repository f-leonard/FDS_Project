# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 11:02:08 2022

@author: 35387
"""

import requests
from bs4 import BeautifulSoup
import urllib.request

url = "https://www.ft.com/content/e347aae3-8098-4f82-a97a-28d17769fa3e"
# opening the url for reading
html = urllib.request.urlopen(url)
  
# parsing the html file
soup = BeautifulSoup(html, 'html.parser')
body = soup.find_all('div')
print(soup.div.p.text)
		