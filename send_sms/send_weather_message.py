# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
import urllib2
import json

"""
短信业务调用接口示例，版本号：v20180320

Created on 2018-03-20

"""

reload(sys)
sys.setdefaultencoding('utf8')

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "your key id"
ACCESS_KEY_SECRET = "your secret key"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name);

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # 查询的手机号码
    queryRequest.set_PhoneNumber(phone_number)
    # 可选 - 流水号
    queryRequest.set_BizId(biz_id)
    # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # 必填-当前页码从1开始计数
    queryRequest.set_CurrentPage(current_page)
    # 必填-页大小
    queryRequest.set_PageSize(page_size)

    # 调用短信记录查询接口，返回json
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    # TODO 业务处理

    return queryResponse


def get_weather_content(url):
    '''
    获取api页面展示内容
    '''
    try:
        request = urllib2.Request(url)
        html = urllib2.urlopen(request, timeout=50)
        content = html.read()
        return content
    except:
        print(url)
        return 0


def query_url(city):
    '''
    拼接api请求链接
    '''
    url = "https://api.seniverse.com/v3/weather/daily.json?key=vxm8iidadqccffhe&location=" + beijing + "&language=zh-Hans&unit=c&start=0&days=5"
    return url


def parsing(jsons):
    '''
    根据api返回结果导入json
    '''
    parsings = json.loads(jsons)
    weather_result = parsings.get('results')[0].get('daily')[0]
    return weather_result


url = "https://api.seniverse.com/v3/weather/daily.json?key=vxm8iidadqccffhe&location=hengyang&language=zh-Hans&unit=c&start=0&days=5"
result = json.loads(get_weather_content(url))
a = result.get('results')[0].get('daily')[0]
today_low_temperature = a.get("low")
today_high_temperature = a.get("high")
today_weather = a.get("text_day")

__name__ = 'send'
if __name__ == 'send':
    __business_id = uuid.uuid1()
    print __business_id
    params = "{\"low\":\"20\",\"high\":\"30\",\"weather\":\"yintian\"}"
    params_low_temperature = params.replace("20", today_low_temperature)
    params_high_temperature = params_low_temperature.replace("30", today_high_temperature)
    params_today_weather = params_high_temperature.replace("yintian", today_weather)
print send_sms(__business_id, "18711041019", "最可爱的小马", "SMS_127168313", params_today_weather)

if __name__ == 'query':
    print query_send_detail("1234567^8901234", "18711041019", 10, 1, "20180320")

