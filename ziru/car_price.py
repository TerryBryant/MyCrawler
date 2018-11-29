# coding=utf-8
from __future__ import print_function
from lxml import etree
import requests
import smtplib
from email.mime.text import MIMEText
import sched
import time

g_price = 0.0


# send email
def send_email(curr_price, prev_price):
    msg_from = 'xx@xx.com'
    pwd = 'xxx'   # 国内部分邮箱使用的是什么授权码，所以这里根据需要要么填授权码要么填邮箱密码
    msg_to = 'xx@xx.com'

    email_subject = '降价通知！！！'
    email_content = '当前价格为：%.2f万，上次价格为：%.2f万' % (curr_price, prev_price)
    msg = MIMEText(email_content)
    msg['Subject'] = email_subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    try:
        s = smtplib.SMTP("smtp.xx.com")
        s.login(msg_from, pwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('发送成功')
    except Exception as e:
        print('发送失败')
    finally:
        s.quit()


# get information from website
def get_price_info():
    headers = {r"User-Agent":"Mozilla/4.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}

    url = r"http://car.bitauto.com/bentian2xw/m122666/jiangjia/c12/"
    res = requests.get(url, headers=headers, timeout=15)
    page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))

    prices = page.xpath('//div[@class="main-inner-section sales-agent-list"]')  # '//' is very important
    all_prices = prices[0].xpath('div[@class="row reduce-list"]/div[@class="col-xs-6"]/div[@class="row"]'
                                 '/div[@class="col-xs-7 middle"]/p[@class="price"]/span[@class="now-price"]')

    lowest_price = float(all_prices[0].text[:-1])

    global g_price
    if lowest_price < g_price:
        send_email(lowest_price, g_price)
        g_price = lowest_price

    return lowest_price


# Program begins
g_price = get_price_info()
print('查价格程序开始运行了...')

# Set up a schedule task
schedule = sched.scheduler(time.time, time.sleep)


def execute_command(cmd, inc):
    get_price_info()
    schedule.enter(inc, 0, execute_command, (cmd, inc))


def main(cmd, inc=60):
    schedule.enter(inc, 0, execute_command, (cmd, inc))
    schedule.run()


# Start the schedule
main('', 14400)     # check every 4 hours

