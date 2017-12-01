from lxml import etree

import requests
import os
import re
import sys
import pymysql

db = pymysql.connect("localhost", "xxx", "xxx", "ziru")
cursor = db.cursor()



pattern_chinese = r'[\u4e00-\u9fa5]+'  #匹配中文
pattern_num = r'\d{2,4}'  #房租在三位数到四位数
pattern_url = r'([-\w]+\.)+[-\w]+([-\w\ ./?%&=#]*)?'   #匹配网址 https?://([\w-]+\.)+[\w-]+([\w-\ ./?%&=#]*)?



query = "INSERT INTO ziroom(name, location, area, floor, house_type, metro_dist, price, url)" \
      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"

def insert_into_mysql(page):
    rooms = page.xpath('//ul[@id="houseList"]/li[@class="clearfix"]')
    for room in rooms:
        utf8_name = ""
        utf8_location = ""
        utf8_area = ""
        utf8_floor = ""
        utf8_house_type = ""
        utf8_metro_dist = ""
        utf8_price = ""
        utf8_url = ""


        h3 = room.xpath('div[@class="txt"]/h3/a')
        h4 = room.xpath('div[@class="txt"]/h4/a')
        detail = room.xpath('div[@class="txt"]/div[@class="detail"]/p/span')
        area = detail[0].text
        floor = detail[1].text
        house_type = detail[2].text
        metro_dist = detail[4].text

        price1 = room.xpath('div[@class="priceDetail"]/p[@class="price"]')
        price2 = room.xpath('div[@class="priceDetail"]/p[@class="price"]/span')
        match_price1 = re.search(pattern_num, price1[0].text)
        match_price2 = re.search(pattern_chinese, price2[0].text)
        price = ""
        if match_price1 and match_price2:
            #price = match_price1.group(0) + '(' + match_price2.group(0) + ')'
            #price = match_price1.group(0)
            price = match_price1.group(0)

        room_url1 = room.xpath('div[@class="priceDetail"]/p[@class="more"]/a//@href')
        match_url = re.search(pattern_url, str(room_url1[0]))
        room_url = ""
        if match_url:
            room_url = match_url.group(0)

        #print(h3[0].text, h4[0].text, area, floor, house_type, metro_dist, price)

        #待存入数据库的参数
        if h3[0].text:
            utf8_name = h3[0].text.encode('utf-8')
        if h4[0].text:
            utf8_location = h4[0].text.encode('utf-8')
        if area:
            utf8_area = area.encode('utf-8')
        if floor:
            utf8_floor = floor.encode('utf-8')
        if house_type:
            utf8_house_type = house_type.encode('utf-8')
        if metro_dist:
            utf8_metro_dist = metro_dist.encode('utf-8')
        if price:
            utf8_price = price.encode('utf-8')
            #utf8_price = int(price)
        if room_url:
            utf8_url = room_url.encode('utf-8')


        values = (utf8_name, utf8_location, utf8_area, utf8_floor, utf8_house_type, \
                  utf8_metro_dist, utf8_price, utf8_url)
        cursor.execute(query, values)

    db.commit()


headers = {r"User-Agent":"Mozilla/4.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}
#url = r"http://www.ziroom.com/z/nl/z2.html?qwd={上地}"
url = r"http://www.ziroom.com/z/nl/z2-d23008618.html"
res = requests.get(url, headers=headers, timeout=15)
page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))

#先删掉数据库中的内容，因为可能已过期
cursor.execute("DELETE FROM ziroom")
db.commit()

#第一页数据写入数据库
insert_into_mysql(page)
print(url)

#海淀 http://www.ziroom.com/z/nl/z2-d23008618.html
#丰台 http://www.ziroom.com/z/nl/z2-d23008617.html
#昌平 http://www.ziroom.com/z/nl/z2-d23008611.html
#朝阳  http://www.ziroom.com/z/nl/z2-d23008613.html



#先找到共有多少网页
pages = page.xpath('//div[@class="pages"]/a[@class="next"]//@href')
while pages:
    match_url = re.search(pattern_url, str(pages[0]))
    if match_url:
        url = 'http://' + match_url.group(0)
    else:
        print("Can't find next page")
        break;
    res = requests.get(url, headers=headers, timeout=15)
    page = etree.HTML(res.text, parser=etree.HTMLParser(encoding='utf-8'))
    insert_into_mysql(page)


    pages = page.xpath('//div[@class="pages"]/a[@class="next"]//@href')
    print(url)
exit(0)


db.close()


