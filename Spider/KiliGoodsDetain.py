#!/usr/bin/python
# -*- coding: UTF-8 -*-

#函数内部调用其他函数

import re
import requests
import os
from bs4 import BeautifulSoup
import urllib2


def get_url(sku):
    url="https://www.kilimall.co.ke/item-"+sku+".html"
    return url

def get_page_content(url):
    try:
        request = urllib2.Request(url)
        html = urllib2.urlopen(request, timeout=20)
        content = html.read()
        return content
    except:
        print(url)
        return 0

def get_img_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    result_div = soup.find("img", class_="lazyload cloudzoom").attrs
    return result_div

def sku_id(readfile):
    url=[]
    for r in read_file.readlines():
        result=get_url(r).replace("\n","")
        url.append(result)
    return url

def getimg(imgdata):
    try:
        f = open("C:/Users/Hymn/Desktop/Picture/"+"Kilimall Kenya "+imgdata['alt']+".png", "wb")
        result=urllib2.urlopen(imgdata['src'])
        result_read=result.read()
        f.write(result_read)
        f.close()
        return 1
    except:
        print(imgdata['src'])
        return 0

read_file=open("C:/Users/Hymn/Desktop/goodsid.txt")
link=sku_id(read_file)
for r in link:
    link_content=get_page_content(r)
    img_content=get_img_content(link_content)
    getimg(img_content)








