#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python3.5

import pymysql
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def connection(sql,dates):
    conn = pymysql.connect(host='fgshdfghsgf', port=8799, user='user_louis', passwd='g75ssaWgsdhfgdFog2vJ8b8', db='database')
    cursor = conn.cursor()
    cursor.execute('SET time_zone = "+3:00"')
    effect_row = cursor.execute(sql,dates)
    result=cursor.fetchall()
    return result
    conn.commit()
    cursor.close()
    conn.close()
	
def connections(sql):
    conn = pymysql.connect(host='sgfhdsfe.cyvvadsgfhdsgfaws.com', port=3306, user='user_louis', passwd='g7dgeyfgygfoGFog2vJ8b8', db='database')
    cursor = conn.cursor()
    effect_row = cursor.execute(sql)
    result=cursor.fetchall()
    return result
    conn.commit()
    cursor.close()
    conn.close()


sql1='''

SELECT
 ooo.goods_id,
 ooo.goods_name,
 ooo.goods_storage,
 ooo.solditem,
 ooo.store_id,
 ooo.store_name,
 ooo.timess,
 gc.gc_name,
 gc1.gc_name,
 gc2.gc_name,
 ooo.paymenttime,
ooo.leixing,
ooo.goods_price
FROM
 (
  SELECT
   og.goods_id,
   og.store_id,
   o.store_name,
   gs.gc_id_1,
   gs.gc_id_2,
   gs.gc_id_3,
   og.goods_name,
   og.goods_price,
   gs.goods_storage,
   FROM_UNIXTIME(gs.goods_addtime) AS timess,
   CASE o.payment_time
  WHEN 0 THEN
   0
  ELSE
   FROM_UNIXTIME(o.payment_time, '%%Y%%m%%d')
  END AS paymenttime,
 CASE o.logistics_type WHEN 1 THEN 'FBK'
WHEN 2 THEN 'GS'
WHEN 0 THEN 'DS'
END AS leixing,
  SUM(og.goods_num) AS solditem
 FROM
  nc_order_goods og
 INNER JOIN nc_order o ON og.order_id = o.order_id
 INNER JOIN nc_goods gs ON og.goods_id = gs.goods_id
 WHERE
FROM_UNIXTIME(o.add_time, '%%Y%%m%%d') =%s
 GROUP BY
  og.goods_id,
   og.store_id,
   o.store_name,
   gs.gc_id_1,
   gs.gc_id_2,
   gs.gc_id_3,
   og.goods_name,
   og.goods_price,
   gs.goods_storage,timess,paymenttime,leixing
 ) AS ooo
INNER JOIN nc_goods_class gc ON ooo.gc_id_1 = gc.gc_id
INNER JOIN nc_goods_class gc1 ON ooo.gc_id_2 = gc1.gc_id
INNER JOIN nc_goods_class gc2 ON ooo.gc_id_3 = gc2.gc_id
'''

sql2='''
 SELECT
  nsgs.goods_id,
	'Y'
 FROM
  nc_selected_goods nsgs
  group by nsgs.goods_id
'''

def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

today=str(getYesterday()).replace("-","")
print(today)
result_req=connection(sql1,today)
result_list=list(result_req)
result=pd.DataFrame(result_list)
result.columns=['goods_id','goods_name','stock','solditem','storeid','store_name','addtime','l1','l2','l3','paymenttime','type','goods_price']
result.to_excel("C:/Users/Hymn/Desktop/ceshi.xlsx",index=False)

result_top=connections(sql2)
result_top_list=list(result_top)
result_selection=pd.DataFrame(result_top_list)
result_selection.columns=['goods_id','Top Selection']
result_selection.to_excel("C:/Users/Hymn/Desktop/top.xlsx",index=False)
result_finally=pd.merge(result,result_selection,on="goods_id",how="left")
result_finally.to_excel("C:/Users/Hymn/Desktop/yesterday_sold_data.xlsx",index=False)
print("first file already")



username = 'your send email'
password = 'your send email passwords'
sender = username
receivers = ','.join(['your receivers email'])

# 如名字所示： Multipart就是多个部分
msg = MIMEMultipart()
msg['Subject'] = today+" Sold Item Data"
msg['From'] = sender
msg['To'] = receivers

# 下面是文字部分，也就是纯文本
puretext = MIMEText("Hi,Echo, attachment file is "+ today +"sold item data, kindly check it, thanks")
msg.attach(puretext)
print("email content already")
# 下面是附件部分 ，这里分为了好几个类型

# 首先是xlsx类型的附件，全部销售数据
xlsxpart = MIMEApplication(open("C:/Users/Hymn/Desktop/yesterday_sold_data.xlsx", 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='yesterday_sold_data.xlsx')
msg.attach(xlsxpart)
print("first attachment file already")

try:
    #print("开始连接邮件服务器了")
    client = smtplib.SMTP()
    client.connect('imap.exmail.qq.com')
    client.login(username, password)
    client.sendmail(sender, receivers, msg.as_string())
    client.quit()
    print('today data already send.')
except smtplib.SMTPRecipientsRefused:
    print('Recipient refused')
except smtplib.SMTPAuthenticationError:
    print('Auth error')
except smtplib.SMTPSenderRefused:
    print('Sender refused')
except Exception as  e:
    print(e)
