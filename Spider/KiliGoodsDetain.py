  #!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import requests
import os
from bs4 import BeautifulSoup
import urllib2

'''
url='https://www.kilimall.co.ke/item-725062.html'
request = urllib2.Request(url)
html = urllib2.urlopen(request, timeout=20)
content = html.read()
soup = BeautifulSoup(content, 'html.parser')
result_div=soup.find("img",class_="lazyload cloudzoom").attrs
print(result_div)
'''

def get_page_content(url):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request, timeout=20)
    content = html.read()
    return content

def return_page_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    result_div = soup.find("img", class_="lazyload cloudzoom").attrs
    return result_div
