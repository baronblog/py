import pandas as pd


fileobj=pd.read_excel("C:/Users/Hymn/Desktop/offsite/onsitesearch.xlsx")

for index,value in fileobj.iterrows():
    qty = value['click']
    keywords = value['keywords']
    with open("C:/Users/Hymn/Desktop/offsite/onsitesearch.txt","a+") as f:
        for r in range(1, qty+1):
            f.write(str(keywords)+"\n")
