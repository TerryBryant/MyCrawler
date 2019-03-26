# coding=utf-8
from __future__ import print_function
import requests
import json
import os.path as osp



# 爬下来的文件保存路径
file_saving_root = '/home/terry/workspace/me'

# 网络文件路径的前缀，后面接具体的hdf文件名
file_download_path = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MCD19A2/2017/293'


# 这些参数和文件位置有关系，nasa页面里面的文件分四段进行加载，加载在四个坐标区域内
area_of_interest = ['x121.20y31.80,x121.87y31.49'
                    , 'x120.05y25.28,x122.00y21.92'
                    , 'x108.62y20.13,x111.02y18.19'
                    , 'x73.62y53.54,x134.76y20.23']

source_page_urls = []
for area in area_of_interest:
    source_page_urls.append('https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product=MCD19A2&collection=6&dateRanges='
                       '2017-10-20..2017-10-20&areaOfInterest=%s&dayCoverage=true&dnboundCoverage=true' % area)

def get_file_content(use_proxy=False):
    url_file_path = []
    #url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MCD19A2/2017/293/MCD19A2.A2017293.h29v06.006.2018119160954.hdf'

    url = 'https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product=MCD19A2&collection=6&dateRanges=' \
          '2017-10-20..2017-10-20&areaOfInterest=x121.20y31.80,x121.87y31.49&dayCoverage=true&dnboundCoverage=true'


    header = {}
    # header['Access-Control-Allow-Credentials'] = 'true'
    #header['Content-Encoding'] = 'gzip'
    # header['Content-Length'] = '1879'
    header['Content-Type'] = 'application/json'

    header['Accept'] = '*/*'
    header['Accept-Encoding'] = 'gzip, deflate, br'
    header['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    header['Connection'] = 'keep-alive'
    header['Host'] = 'ladsweb.modaps.eosdis.nasa.gov'
    header['Referer'] = 'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MCD19A2--6/2017-10-20..2017-10-20/DB/Country:CHN'
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    header['X-Requested-With'] = 'XMLHttpRequest'

    proxies = {'http': 'HTTP://127.0.0.1:8087', 'https': 'HTTP://127.0.0.1:8087'}

    for url in source_page_urls:
        if use_proxy:
            res = requests.get(url, headers=header, proxies=proxies, verify=False)  # 使用代理
        else:
            res = requests.get(url, headers=header)

        data_dict = json.loads(res.text)    # 解析出来的文件保存在dict里面

        for key, value in data_dict.items():
            file_name = value['name']
            url_file_path.append(osp.join(file_download_path, file_name))

            # with open(osp.join(file_saving_root, file_name), 'wb') as f:
            #     f.write(requests.get(url_file_path, headers=fake_headers).content)

    return url_file_path


def save_hdf_files(file_path_urls_, use_proxy=False):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    proxies = {'http': 'HTTP://127.0.0.1:8087', 'https': 'HTTP://127.0.0.1:8087'}

    for url in file_path_urls_:
        print('正在下载文件： %s' % url)
        if use_proxy:
            res = requests.get(url, headers=header, proxies=proxies, verify=False)  # 使用代理
        else:
            res = requests.get(url, headers=header)

        index = url.rfind('/')
        file = url[index+1:]

        with open(osp.join(file_saving_root, file), 'wb') as f:
            f.write(res.content)


if __name__ == '__main__':
    file_path_urls = get_file_content(use_proxy=False)
    save_hdf_files(file_path_urls, use_proxy=False)


