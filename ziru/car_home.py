# 汽车之家图片爬虫，汽车之家的网址设置太简单了，获取起来难度不大
from __future__ import print_function
import requests
import urllib.request as rq
from lxml import etree
import os.path as osp
import random
import time

img_save_path = 'xxx'   # 用于存放爬到的图片
urls_save_path = 'xxx/urls.txt'   # 用于存放爬到的图片网址


agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

proxies = [
{'http': '162.105.87.211:8118', 'https': '162.105.87.211:8118'},
{'http': '49.65.161.18:18118', 'https': '49.65.161.18:18118'},
{'http': '121.69.13.242:53281', 'https': '121.69.13.242:53281'},
]

#headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
#proxies = {'http': '112.80.70.134:8118', 'https': '112.80.70.134:8118'}



all_car_urls = []
for i in range(6000):
    car_homepage = 'https://car.autohome.com.cn/pic/series/%d.html' % i
    print(car_homepage)

    try:
        res = requests.get(car_homepage, headers=dict(zip("User-Agent", random.choice(agents))), timeout=10)
        page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))

        urls = page.xpath('//div[@class="uibox-con carpic-list03"]')
        if len(urls) == 0:    # 有的网页没有图片
            continue
        url_subs = urls[0].xpath('//ul/li/a/img/@src')

        for url_sub in url_subs:
            if -1 == url_sub.find('spec'):    # 不爬取网页最底下的推荐图片（图片里面一般含有较多文字）
                continue

            url_sub = url_sub.replace('/t_', '/1024x0_1_q87_')    # 从缩略图到原图
            url_sub = 'https:' + url_sub
            all_car_urls.append(url_sub)
    except:
        pass

    time.sleep(random.uniform(0, 1))

with open(urls_save_path, 'w') as f:
    for url in all_car_urls:
        f.write(url + '\n')

print('Finish downloading all the image urls.')



##################################################################
# 从网址里面下载图片，与上一步分离
with open(urls_save_path, 'r') as f:
    all_car_urls = f.readlines()

all_car_urls = random.sample(all_car_urls, 10000)

for car in all_car_urls:
    index_ = car.rfind('_')
    img_name = car[index_ + 1:]
    try:
        rq.urlretrieve(car, osp.join(img_save_path, img_name))
        print('Saved %s' % img_name)
    except:
        pass
