#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import pymysql

import os

def connection(sql):
    conn = pymysql.connect(host='kilimall.cyvvauj9gcoe.ap-northeast-1.rds.amazonaws.com', port=3306, user='kilidata', passwd='yALmLREAdPy5GEEJtMmo3APqq', db='kilimall_kenya',connect_timeout=100)
    cursor = conn.cursor()
    effect_row = cursor.execute(sql)
    result=cursor.fetchall()
    return result
    conn.commit()
    cursor.close()
    conn.close()

sql1='''SELECT
store.store_id,
store.store_name,
FROM_UNIXTIME(seller.last_login_time) AS lastlogintime,
 CASE store.store_state
WHEN 1 THEN
 'Open'
WHEN 0 THEN
 'Closed'
END AS storestate,
FROM_UNIXTIME(store.store_time) AS opentime

FROM nc_store store
LEFT JOIN nc_order o ON store.store_id=o.store_id
LEFT JOIN nc_seller seller ON store.store_id=seller.store_id
WHERE
store.is_global=1
GROUP BY store.store_id,
store.store_name,storestate
'''

select_1=connection(sql1)
select_1_list=list(select_1)
result_1=pd.DataFrame(select_1_list)
full_result_1=result_1.fillna(0)
full_result_1.columns=['storeid','storename','lastlogintime','storestate','opentime']

sql2='''
SELECT
gs.store_id,
 COUNT(DISTINCT(gs.goods_commonid)) AS live_listing
FROM
 nc_goods gs
INNER JOIN nc_store se ON gs.store_id=se.store_id
WHERE
 gs.goods_state = 1
AND gs.goods_verify = 1
AND se.is_global=1
GROUP BY gs.store_id
'''
select_2=connection(sql2)
select_2_list=list(select_2)
result_2=pd.DataFrame(select_2_list)
full_result_2=result_2.fillna(0)
full_result_2.columns=['storeid','livelisting']

sql3='''SELECT
a.store_id AS storeid,
COUNT(DISTINCT b.goods_commonid) AS activelisting,
SUM(c.order_amount) AS successgmv,
COUNT(DISTINCT c.order_id) AS paymentorder

FROM nc_order_goods a
INNER JOIN nc_goods b ON a.goods_id=b.goods_id
INNER JOIN nc_order c ON a.order_id=c.order_id
WHERE
	c.payment_time >= UNIX_TIMESTAMP('2017-09-01 00:00:00')
AND c.payment_time <= UNIX_TIMESTAMP('2017-09-30 23:59:59')
AND a.goods_num<50
GROUP BY storeid'''

select_3=connection(sql3)
select_3_list=list(select_3)
result_3=pd.DataFrame(select_3_list)
full_result_3=result_3.fillna(0)
full_result_3.columns=['storeid','activelisting','successgmv','paymentorder']

sql4='''

SELECT
a.store_id,
COUNT(DISTINCT a.goods_commonid)
FROM nc_goods_common a
WHERE
	a.goods_addtime >= UNIX_TIMESTAMP('2017-09-01 00:00:00')
AND a.goods_addtime<= UNIX_TIMESTAMP('2017-09-30 23:59:59')
GROUP BY a.store_id'''

select_4=connection(sql4)
select_4_list=list(select_4)
result_4=pd.DataFrame(select_4_list)
full_result_4=result_4.fillna(0)
full_result_4.columns=['storeid','newlisting']

finally_result_1=pd.merge(full_result_1,full_result_2,on=['storeid'],how='left')
finally_result_2=pd.merge(finally_result_1,full_result_3,on=['storeid'],how='left')
finally_result_3=pd.merge(finally_result_2,full_result_4,on=['storeid'],how='left')

finally_result_3.to_csv("C:/Users/Hymn/Desktop/louislouis.csv",index=False)