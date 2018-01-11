#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import requests
import os
from bs4 import BeautifulSoup
import urllib2


def get_url(sku):
    url="https://www.kilimall.co.ke/item-"+sku+".html"
    return url

def get_page_content(url):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request, timeout=20)
    content = html.read()
    return content

def return_page_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    result_div = soup.find("img", class_="lazyload cloudzoom").attrs
    return result_div

read_file=open("C:/Users/Hymn/Desktop/goodsid.txt")
for r in read_file.readlines():
    print(get_url(r).replace("\n",""))
