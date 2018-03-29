#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python3.6

import pymysql
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def connection(sql,dates):
    conn = pymysql.connect(host='jumia-slave.cdhsfguj9gcoe.ap-fghsdft-1.rds.amazonaws.com', port=7866, user='user_lyang', passwd='dgsdfgssaWyXid7P1oGFog2vJ8b8', db='kilimall_kenya')
    cursor = conn.cursor()
    effect_row = cursor.execute(sql,dates)
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
  CASE o.logistics_type
 WHEN 1 THEN
  'FBK'
 WHEN 2 THEN
  'GS'
 WHEN 0 THEN
  'DS'
 END AS leixing,
 SUM(og.goods_num) AS solditem
FROM
 nc_order_goods og
INNER JOIN nc_order o ON og.order_id = o.order_id
INNER JOIN nc_goods gs ON og.goods_id = gs.goods_id
INNER JOIN nc_goods_common common ON gs.goods_commonid = common.goods_commonid
WHERE
 FROM_UNIXTIME(o.add_time, '%%Y%%m%%d') =%s
AND common.goods_commonid IN (
 SELECT
  gs.goods_commonid
 FROM
  nc_selected_goods nsgs
INNER JOIN nc_goods gs ON nsgs.goods_id=gs.goods_id
)
GROUP BY
 og.goods_id,
 gs.gc_id_1,
 gs.gc_id_2,
 gs.gc_id_3,
 og.goods_name,
 og.store_id,
 og.goods_price,
 o.store_name,
 gs.goods_storage,
 paymenttime,
 leixing
 ) AS ooo
INNER JOIN nc_goods_class gc ON ooo.gc_id_1 = gc.gc_id
INNER JOIN nc_goods_class gc1 ON ooo.gc_id_2 = gc1.gc_id
INNER JOIN nc_goods_class gc2 ON ooo.gc_id_3 = gc2.gc_id
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
a=result.to_excel("C:/Users/Hymn/Desktop/sheet.xlsx")

username = 'your email'
password = 'your passwords'
sender = username
receivers = ','.join(['receiver email'])

# 如名字所示： Multipart就是多个部分
msg = MIMEMultipart()
msg['Subject'] = 'Python mail Test'
msg['From'] = sender
msg['To'] = receivers

# 下面是文字部分，也就是纯文本
puretext = MIMEText('我是纯文本部分，')
msg.attach(puretext)

# 下面是附件部分 ，这里分为了好几个类型

# 首先是xlsx类型的附件
xlsxpart = MIMEApplication(open('sheet.xlsx', 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='sheet.xlsx')
msg.attach(xlsxpart)
#如果需要多个附件，需要多个msg.attach

try:
    client = smtplib.SMTP()
    client.connect('imap.exmail.qq.com')
    client.login(username, password)
    client.sendmail(sender, receivers, msg.as_string())
    client.quit()
    print('带有各种附件的邮件发送成功！')
except smtplib.SMTPRecipientsRefused:
    print('Recipient refused')
except smtplib.SMTPAuthenticationError:
    print('Auth error')
except smtplib.SMTPSenderRefused:
    print('Sender refused')
