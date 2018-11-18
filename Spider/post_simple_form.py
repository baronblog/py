
#此代码仅用于展示简单表单页面登录，登录参数仅限于简单crsf，账号和密码等简单参数

import requests
from lxml import etree

sessions = requests.session()

headers={
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Referrer": "https://www.kilimall.co.ke"
}
requests_url = "https://www.kilimall.co.ke/index.php?act=login&ref_url=%2Findex.php%3Fact%3Dmember_order%26state_type%3Dstate_new"
request_html = sessions.get(requests_url, headers=headers).text
#print(request_html)
html = etree.HTML(request_html)
#print(html)
html_value = html.xpath('//input[@name="formhash"]/@value')
print(html_value)
post_login="https://www.kilimall.co.ke/index.php?act=login&op=login"
post_data = {
    "formhash": html_value,
    "form_submit": "ok",
    "user_name": youraccpunt,
    "password": yourpassword,
    "client": "pc",
    "ref_url": "/index.php?act=member_order&state_type=state_new"
}

result=sessions.post(post_login,data=post_data,headers=headers)
print(result)



