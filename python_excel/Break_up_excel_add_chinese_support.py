#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import xlrd

#read_temple=pd.read_excel("C:/Users/Hymn/Desktop/read_temple.xlsx")
#read_temple.to_excel("C:/Users/Hymn/Desktop/ceshi.xlsx")

read_temple=pd.ExcelFile("C:/Users/Hymn/Desktop/Uganda.xlsx")
read_temple_sheet1=read_temple.parse("总账单".decode("utf-8"))
read_temple_sheet2=read_temple.parse("账单明细".decode("utf-8"))
read_temple_sheet3=read_temple.parse("运费明细".decode("utf-8"))
read_temple_sheet4=read_temple.parse("罚款明细".decode("utf-8"))

company=[]
for r in read_temple_sheet1['公司名'.decode("utf-8")]:
    company.append(r)



company_unique=list(set(company))




for company_name in  company_unique:
    read_temple_sheet1_filter1=read_temple_sheet1[read_temple_sheet1[u'公司名']==company_name]
    read_temple_sheet2_filter2 = read_temple_sheet2[read_temple_sheet2['公司名'.decode("utf-8")] == company_name]
    read_temple_sheet3_filter3 = read_temple_sheet3[read_temple_sheet3['公司名'.decode("utf-8")] == company_name]
    read_temple_sheet4_filter4 = read_temple_sheet4[read_temple_sheet4['公司名'.decode("utf-8")] == company_name]
    writer = pd.ExcelWriter("C:/Users/Hymn/Desktop/UG/"+company_name+".xlsx")
    read_temple_sheet1_filter1.to_excel(writer,"总账单".decode("utf-8"),index=False)
    read_temple_sheet2_filter2.to_excel(writer, "账单明细".decode("utf-8"),index=False)
    read_temple_sheet3_filter3.to_excel(writer, "运费明细".decode("utf-8"),index=False)
    read_temple_sheet4_filter4.to_excel(writer, "罚款明细".decode("utf-8"), index=False)
    writer.save()

