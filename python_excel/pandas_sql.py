#coding=utf-8
import pandas as pd
import tushare as ts
import pymysql
import time
import random
from sqlalchemy import create_engine
from multiprocessing import Pool


def connection(sql,*sqls):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='kilimall5224910', db='tina',use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    effect_row = cursor.execute(sql,*sqls)
    result=cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


year=[1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
quarter=[1,2,3,4]
print(year)
def fundfunction(year,quarter):
        for r in year:
            for i in quarter:
                fund = pd.DataFrame(ts.fund_holdings(r, i))
                #time.sleep(1)
                #print(fund)
                print("得到结果"+str(fund.shape)+"行数据")
                datatime = str(r) + "0" + str(i)
                #print(datatime)
                #print(fund)
                with open("C:/Users/Hymn/Desktop/fund.txt","a+") as f:
                    print("打开文件")
                    for index,x in fund.iterrows():
                        #print("开始循环")
                        result="INSERT INTO fund_holding ("+"`code`,"+"`name`,"+"date,nums,nlast,count,clast,amount,ratio) VALUES ("+str(x['code'])+","+"'"+str(x['name'])+"'"+","+"'"+str(x['date'])+"'"+","+str(x['nums'])+","+str(x['nlast'])+","+str(x['count'])+","+str(x['clast'])+","+str(x['amount'])+","+str(x['ratio'])+");"+"\n"
                        f.write(result)
                        #print("写入一个结果")

#fundfunction(year,quarter)
'''
if __name__=='__main__':
    pool=Pool(4)
    pool.apply_async(fundfunction,(year,quarter))
    pool.close()
    pool.join()
    '''



