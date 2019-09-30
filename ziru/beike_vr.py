# coding=utf-8
from __future__ import print_function
import requests
from lxml import etree
import random
import re
import os


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
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_file_content(src_url, use_proxy=False):
    file_path_urls = []

    header = {}
    header['Content-Type'] = 'text/html; charset=utf-8'

    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    header['Accept-Encoding'] = 'gzip, deflate, br'
    header['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    header['Connection'] = 'keep-alive'

    header['Cache-Control'] = 'max-age=0'
    header['Host'] = 'realsee.com'
    header['Referer'] = 'https://bj.ke.com/ershoufang/19050119510100253242.html?fb_expo_id=230748580808818691'

    header['Sec-Fetch-Mode'] = 'navigate'
    header['Sec-Fetch-Site'] = 'cross-site'
    header['Upgrade-Insecure-Requests'] = '1'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

    proxies = {'http': 'HTTP://127.0.0.1:8087', 'https': 'HTTP://127.0.0.1:8087'}

    if use_proxy:
        res = requests.get(src_url, headers=header, proxies=proxies, verify=False)  # 使用代理
    else:
        res = requests.get(src_url, headers=header)

    # Parse html script, return image urls
    data = res.text
    pano_index = data.find('panorama')
    new_data = data[pano_index:]
    ans = [m.start() for m in re.finditer('https://vrlab-public.ljcdn.com/release/auto3dhd', new_data)]

    for num in range(1, len(ans) - 1):
        index_jpg = new_data[ans[num]:].find('.jpg') + ans[num]
        file_path_urls.append(new_data[ans[num]: index_jpg + 4])

    return file_path_urls


def get_room_pages(root_url):
    room_urls = []
    res = requests.get(root_url, headers=dict(zip("User-Agent", random.choice(agents))), timeout=10)
    page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))

    urls = page.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[4]/ul')
    url_subs = urls[0].xpath('//li/a/@href')
    for u_ in url_subs[:-1]:
        if u_[-5:] == '.html':
            room_urls.append(u_)

    return room_urls


def get_room_detail_pages(root_url):
    room_detail_urls = []

    # open detail pages one by one
    for root_url_ in root_url:
        try:
            res = requests.get(root_url_, headers=dict(zip("User-Agent", random.choice(agents))), timeout=10)
            page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))

            urls = page.xpath('//*[@id="topImg"]/div[1]/img')
            url_subs = urls[0].xpath('//@data-vr')
            room_detail_urls.append(url_subs[0])
        except:
            print('Skip this page!')
            pass

    return room_detail_urls


def save_image_from_urls(urls, img_save_path, img_save_index):
    for url in urls:
        img_name = '%d.jpg' % img_save_index
        res = os.popen('wget -c %s -O %s' % (url, os.path.join(img_save_path, img_name))).read()
        img_save_index += 1

        if len(res) > 0:
            print('Saved %s' % img_name)          
        else:
            print('----------------------------------------')

    return img_save_index


if __name__ == '__main__':
    use_proxy = False
    image_save_path = os.path.join(os.getcwd(), 'beike_online')
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    root_url = 'https://bj.ke.com/ershoufang/tt8/'  # 二手房根目录
    room_urls = get_room_pages(root_url)            # 获取根目录下第一页所有的房子链接
    room_detail_urls = get_room_detail_pages(room_urls)     # 进入链接，获取该房子的vr页面

    img_save_index = 0
    for url in room_detail_urls:
        image_urls = get_file_content(url[:-8], False)      # 在vr页面获取所有切片图的url
        img_save_index = save_image_from_urls(image_urls, image_save_path, img_save_index)  # 每次下载一套房子的所有图片


