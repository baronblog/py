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

def page(readfile):
    url=[]
    for r in read_file.readline():
        result=get_url(r).replace("\n","")
        url.append(result)
    return result

url="https://d2lpfujvrf17tu.cloudfront.net/kenya/shop/store/goods/1888/2017/09/1888_05599289687817897_360.jpg"
#request = urllib2.Request(url)
#html = urllib2.urlopen(request, timeout=20)
f=open("C:/Users/Hymn/Desktop/Picture/1.jpg","wb")
result= urllib2.urlopen(url)
result_read=result.read()
f.write(result_read)
f.close()
#f.write(result)
#f.close()






