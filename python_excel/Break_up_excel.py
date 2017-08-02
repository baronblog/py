#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import xlrd

#read_temple=pd.read_excel("C:/Users/Hymn/Desktop/read_temple.xlsx")
#read_temple.to_excel("C:/Users/Hymn/Desktop/ceshi.xlsx")

read_temple=pd.ExcelFile("C:/Users/Hymn/Desktop/read_temple.xlsx")
read_temple_sheet1=read_temple.parse("Total_Bill")
read_temple_sheet2=read_temple.parse("Bill_Detail")
read_temple_sheet3=read_temple.parse("Shipped_Detail")

company=[]
for r in read_temple_sheet1['company']:
    company.append(r)

company_unique=list(set(company))
for company_name in  company_unique:
    read_temple_sheet1_filter1=read_temple_sheet1[read_temple_sheet1.company==company_name]
    read_temple_sheet2_filter2 = read_temple_sheet2[read_temple_sheet2.company == company_name]
    read_temple_sheet3_filter3 = read_temple_sheet3[read_temple_sheet3.company == company_name]
    writer = pd.ExcelWriter("C:/Users/Hymn/Desktop/template/"+company_name+".xlsx")
    read_temple_sheet1_filter1.to_excel(writer,"Total_Bill",index=False)
    read_temple_sheet2_filter2.to_excel(writer, "Bill_Detail",index=False)
    read_temple_sheet3_filter3.to_excel(writer, "Shipped_Detail",index=False)
    writer.save()

