#coding=utf-8
import pandas as pd
import tushare as ts
import pymysql
import time
import random
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


year=sorted([i for i in range(1999,2017,1)],reverse=True)
quarter=[1,2,3,4]
print(year)
def dealdata():
    for r in year:
        for i in quarter:
            fund = pd.DataFrame(ts.fund_holdings(r, i))
            datatime = str(r) + "0" + str(i)
            #print(datatime)
            #print(fund)
            for index,x in fund.iterrows():
                connection("INSERT INTO test VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(x['code'],x['name'],x['date'],x['nums'],x['nlast'],x['count'],x['clast'],x['amount'],x['ratio']))
                time.sleep(random.randint(3,10))

if __name__ == '__main__':
    pool = Pool(4)
    pool.apply_async(dealdata)
    pool.close()
    pool.join()


